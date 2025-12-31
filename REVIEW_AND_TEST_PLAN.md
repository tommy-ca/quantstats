# Plan: Review hvPlot Migration & Run Tests with uv

## Overview
This plan outlines the process for comprehensively reviewing the hvPlot migration implementation and running the full test suite using `uv run --with pytest` to ensure isolated, reproducible test execution.

## Current Status

### Implementation Progress
- **Backend Architecture**: ✅ Complete - Sophisticated backend selection with hvPlot as default
- **Plot Coverage**: ✅ Complete - All 18 core plotting functions have hvPlot equivalents
- **Report Integration**: ✅ Complete - Full HTML report generation with interactive Bokeh charts
- **Test Suite**: ✅ Good - 14 passing tests covering unit and integration scenarios
- **Production Ready**: ✅ Yes - Code generates working interactive reports

### Known Issues
- Matplotlib import conflict when running markdown tests in multi-test runs
- Test isolation needs improvement when switching backends within same Python process

## Phase 1: Environment Setup

### 1.1 Create uv Environment
```bash
# Create isolated Python environment with uv
uv venv --python 3.11 .venv

# Activate environment
source .venv/bin/activate

# Install project in development mode with test dependencies
uv pip install -e ".[test,mpl,hvplot]"
```

### 1.2 Verify Installation
```bash
# Verify all dependencies are installed
uv pip list | grep -E "(pytest|pytest-cov|beautifulsoup4)"

# Verify backend availability
python -c "import hvplot; print('hvPlot available')" || echo "hvPlot missing"
python -c "import matplotlib; print('matplotlib available')" || echo "matplotlib missing"
python -c "import seaborn; print('seaborn available')" || echo "seaborn missing"
```

## Phase 2: Code Review

### 2.1 Architecture Review
- [ ] Backend selection logic (`quantstats/_plotting/backend.py`)
- [ ] Backend switching in wrappers (`quantstats/_plotting/wrappers.py`)
- [ ] hvPlot implementations (`quantstats/_plotting/hvplot_backend.py`)
- [ ] Report integration (`quantstats/reports.py`)

### 2.2 Implementation Quality Review
- [ ] Error handling consistency across backends
- [ ] Parameter validation and defaults
- [ ] Memory management and resource cleanup
- [ ] Documentation completeness

### 2.3 Performance Review
- [ ] Performance characteristics vs matplotlib
- [ ] Memory usage patterns
- [ ] Large dataset handling
- [ ] Optimization opportunities

### 2.4 Integration Testing Review
- [ ] Test coverage analysis
- [ ] Test scenario completeness
- [ ] Edge case handling
- [ ] Real-world data scenarios

## Phase 3: Test Execution

### 3.1 Unit Tests (hvPlot Backend Only)
```bash
# Run hvPlot-specific tests with isolated backend
QS_PLOT_BACKEND=hvplot uv run --with pytest tests/test_hvplot_backend.py -v

# Test individual plot object types
QS_PLOT_BACKEND=hvplot uv run --with pytest tests/test_hvplot_objects.py -v
```

### 3.2 Integration Tests
```bash
# Run E2E report generation tests
uv run --with pytest tests/test_e2e_report.py -v

# Test full report generation with hvPlot backend
uv run --with pytest tests/test_hvplot_report.py -v
```

### 3.3 Performance Tests
```bash
# Run performance benchmarks
uv run --with pytest tests/test_performance.py -v -s

# This will benchmark:
# - hvPlot vs matplotlib generation times
# - Multi-column performance (10 strategies)
# - High-frequency data (minute-level)
# - Full HTML report generation
```

### 3.4 Cross-Backend Tests
```bash
# Test matplotlib backend for regression testing
QS_PLOT_BACKEND=matplotlib uv run --with pytest tests/test_comprehensive.py -v

# Test edge cases across backends
uv run --with pytest tests/test_edge_cases.py -v
```

### 3.5 Regression Tests
```bash
# Run issue-specific regression tests
uv run --with pytest tests/test_issue_467.py -v
uv run --with pytest tests/test_issue_468.py -v
```

### 3.6 Full Test Suite
```bash
# Run complete test suite with coverage
uv run --with pytest tests/ -v --cov=quantstats --cov-report=html --cov-report=term

# This will run all 14+ tests and generate coverage report
```

## Phase 4: Results Analysis

### 4.1 Performance Analysis
```python
# Extract performance metrics from test results
# - Compare hvPlot vs matplotlib times
# - Identify performance bottlenecks
# - Validate against <110% threshold
# - Memory usage analysis
```

### 4.2 Issue Documentation
- [ ] Document all test failures with root cause analysis
- [ ] Identify performance regressions
- [ ] Categorize issues by severity
- [ ] Create fix recommendations

### 4.3 Coverage Analysis
```bash
# Analyze test coverage
uv run --with pytest --cov=quantstats --cov-report=json

# Use coverage data to identify:
# - hvPlot-specific code paths
# - Backend switching logic
# - Error handling branches
# - Edge case coverage
```

## Phase 5: Issue Resolution

### 5.1 Critical Issues (P0)
- [ ] Fix matplotlib import conflicts in multi-backend tests
- [ ] Resolve test isolation issues
- [ ] Address any performance regressions

### 5.2 High Priority Issues (P1)
- [ ] Improve error messages for missing backends
- [ ] Enhance backend validation
- [ ] Optimize memory usage for large datasets

### 5.3 Medium Priority Issues (P2)
- [ ] Improve documentation for interactive features
- [ ] Add warnings for performance degradation
- [ ] Enhance test coverage gaps

## Phase 6: Validation & Sign-off

### 6.1 Final Test Suite
```bash
# Run final comprehensive test suite
uv run --with pytest tests/ -v --tb=short --cov=quantstats

# Verify all tests pass with uv environment
```

### 6.2 Production Readiness Checklist
- [ ] All tests pass in isolated uv environment
- [ ] No regressions in matplotlib backend
- [ ] Performance within acceptable thresholds
- [ ] Coverage >80% for hvPlot code paths
- [ ] Documentation updated
- [ ] Code review findings addressed

### 6.3 Release Decision
- [ ] Review test results with stakeholder
- [ ] Approve hvPlot migration for production
- [ ] Plan release timeline
- [ ] Update version and CHANGELOG

## Success Criteria

### Technical Requirements
- [ ] All tests pass with 100% success rate in uv environment
- [ ] hvPlot generation time <110% of matplotlib
- [ ] Memory usage within acceptable limits for 100K+ data points
- [ ] No regressions in matplotlib backend functionality
- [ ] Coverage >80% for new hvPlot code paths

### Quality Requirements
- [ ] Code review findings documented and addressed
- [ ] Performance characteristics well-understood
- [ ] Edge cases handled gracefully
- [ ] Error messages are user-friendly
- [ ] Documentation reflects interactive features

### Production Readiness
- [ ] Cross-platform compatibility verified
- [ ] Real-world data scenarios tested
- [ ] Performance benchmarks established
- [ ] Migration guide created for users
- [ ] Release notes prepared

## Risk Mitigation

### Known Risks
1. **Matplotlib Import Conflicts**: Tests may fail when switching backends
   - Mitigation: Run tests with isolated Python processes per backend
   - Alternative: Improve test isolation in code

2. **Performance Regression**: hvPlot may be slower than expected
   - Mitigation: Establish performance baselines before optimization
   - Alternative: Accept reasonable performance for v1.0

3. **Coverage Gaps**: Some hvPlot paths may have insufficient testing
   - Mitigation: Add targeted tests for identified gaps
   - Alternative: Accept documented gaps for v1.0 with plan to address

## Timeline Estimate

- **Phase 1**: 15 minutes (Environment setup)
- **Phase 2**: 2 hours (Code review)
- **Phase 3**: 1 hour (Test execution)
- **Phase 4**: 1 hour (Results analysis)
- **Phase 5**: 2 hours (Issue resolution)
- **Phase 6**: 30 minutes (Validation)

**Total Estimated Time**: 6.5 hours

## Next Steps

1. Execute Phase 1: Environment Setup
2. Proceed to Phase 2: Code Review  
3. Run Phase 3: Test Execution
4. Complete Phase 4: Results Analysis
5. Address Phase 5: Issue Resolution
6. Finish Phase 6: Validation & Sign-off
