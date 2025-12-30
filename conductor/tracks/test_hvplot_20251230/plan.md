# Plan: Unit tests and E2E tests for hvPlot migrations

## Phase 1: Test Infrastructure ✅ COMPLETE [checkpoint: db36668]

- [x] Task: Install test dependencies (`beautifulsoup4` for DOM parsing) 7e09295
- [x] Task: Conductor - User Manual Verification 'Test Infrastructure' (Protocol in workflow.md) db36668

## Phase 2: Unit Tests for hvPlot Integration ✅ COMPLETE

- [x] Task: Create unit tests for core plots returning hvPlot objects
  - [x] Write Tests (Red Phase) c23d500
  - [x] Verify implementation (Green Phase)
- [x] Task: Ensure tests handle live `yfinance` data fetching c23d500
  - [x] Write Tests c23d500
  - [x] Implement robust data loading for tests c23d500
- [ ] Task: Conductor - User Manual Verification 'Unit Tests for hvPlot Integration' (Protocol in workflow.md)

## Phase 3: E2E Tests for HTML Reports ✅ COMPLETE

- [x] Task: Create E2E test for `qs.reports.html()` with hvPlot
  - [x] Write Tests (Red Phase) - Verify DOM presence of Bokeh markers 6c14420
  - [x] Verify implementation (Green Phase)
- [x] Task: Verify inclusion of Bokeh/HoloViews runtime scripts in output 6c14420
  - [x] Write Tests 6c14420
  - [x] Verify template contains necessary tags 6c14420
- [ ] Task: Conductor - User Manual Verification 'E2E Tests for HTML Reports' (Protocol in workflow.md)

## Phase 4: Performance & Stress Testing ⏳ IN PROGRESS

- [ ] Task: Create performance benchmarking suite
  - [ ] Write `tests/test_performance.py`
  - [ ] Benchmark hvPlot vs matplotlib generation times
  - [ ] Profile memory usage for large datasets
  - [ ] Test with 10M+ data points
  - [ ] Test high-frequency data (minute-level returns)
  - [ ] Test multiple strategy columns (10+)

- [ ] Task: Validate performance thresholds
  - [ ] Ensure hvPlot generation <110% of matplotlib time
  - [ ] Document memory usage characteristics
  - [ ] Identify optimization opportunities

## Phase 5: Edge Case & Error Handling ⏳ PLANNED

- [ ] Task: Create edge case test suite
  - [ ] Write `tests/test_edge_cases.py`
  - [ ] Test empty/None input data
  - [ ] Test mixed timezone scenarios
  - [ ] Test non-numeric data handling
  - [ ] Test corrupted yfinance data
  - [ ] Test backend switching mid-session

- [ ] Task: Verify error handling
  - [ ] Test user-friendly error messages
  - [ ] Validate graceful degradation
  - [ ] Test recovery from error states

## Phase 6: Cross-Backend Compatibility ⏳ PLANNED

- [ ] Task: Create backend consistency tests
  - [ ] Write `tests/test_backend_consistency.py`
  - [ ] Verify consistent outputs between backends
  - [ ] Test backend availability handling
  - [ ] Verify parameter inheritance
  - [ ] Test feature parity matrix

- [ ] Task: Document backend differences
  - [ ] Create feature parity reference
  - [ ] Document hvPlot-specific features
  - [ ] Document matplotlib-only features
  - [ ] Create migration guide

## Phase 7: Real-World Data Integration ⏳ PLANNED

- [ ] Task: Create live data test suite
  - [ ] Write `tests/test_real_world.py`
  - [ ] Test different market sectors
  - [ ] Test various timeframes
  - [ ] Test international markets
  - [ ] Test high volatility periods

- [ ] Task: Validate yfinance integration
  - [ ] Test network resilience
  - [ ] Test invalid ticker handling
  - [ ] Test partial data scenarios
  - [ ] Test rate limiting

## Phase 8: Production Environment Testing ⏳ PLANNED

- [ ] Task: Cross-platform validation
  - [ ] Test on Python 3.8-3.12
  - [ ] Test on Linux, macOS, Windows
  - [ ] Test memory-constrained environments
  - [ ] Test offline scenarios (CDN failures)
  - [ ] Test proxy configurations

- [ ] Task: Final validation
  - [ ] All tests pass on target environments
  - [ ] No regressions in matplotlib backend
  - [ ] Performance within thresholds
  - [ ] Documentation completeness verified
