# Requirements Document: Markdown Output Support

## Project Overview

**Project Name**: Markdown Output Support for QuantStats  
**Version**: 1.0.0  
**Date**: 2025-12-30  
**Author**: QuantStats Development Team  

### Purpose

Add markdown output format support to QuantStats library as an alternative to the existing HTML tearsheet reports, enabling users to generate portfolio performance analysis reports in markdown format for documentation, README files, and text-based workflows.

## Business Requirements

### BR-001: Market Demand
Users need markdown output for:
- Documentation generation
- README files in GitHub repositories
- Static site generators
- Text-based reporting workflows
- Integration with markdown-based tools

### BR-002: Competitive Advantage
Provide markdown output to match/compete with other financial analysis tools that support multiple output formats.

### BR-003: User Experience
Enable seamless transition from HTML to markdown output with minimal learning curve.

## Functional Requirements

### FR-001: Core Markdown Generation
**Priority**: High  
**Description**: Generate comprehensive tearsheet reports in markdown format equivalent to existing HTML reports.

**Acceptance Criteria**:
- Function `quantstats.markdown()` generates complete tearsheet
- Output includes all sections: metrics, returns analysis, plots, tables
- Markdown is valid and renderable by standard markdown parsers

### FR-002: Template System
**Priority**: High  
**Description**: Template-based markdown generation similar to HTML template system.

**Acceptance Criteria**:
- Default markdown template (`report.md`) provided
- Custom template path supported
- Template placeholders replaced with actual data
- Template structure mirrors HTML template organization

### FR-003: Figure Embedding
**Priority**: High  
**Description**: Support embedding charts and visualizations in markdown format.

**Acceptance Criteria**:
- Matplotlib figures embedded as base64 or file references
- hvPlot charts converted to static PNG for markdown compatibility
- Multiple figure formats supported (PNG, SVG, JPG)
- Configurable embedding strategy (base64 vs file links)

### FR-004: Table Formatting
**Priority**: High  
**Description**: Convert performance metrics and data tables to markdown table format.

**Acceptance Criteria**:
- All HTML tables converted to markdown pipe format
- Proper alignment and formatting maintained
- Multi-column DataFrame support
- Index display configurable

### FR-005: Output Options
**Priority**: Medium  
**Description**: Multiple output modes for flexibility.

**Acceptance Criteria**:
- Return markdown string
- Save to `.md` file
- Auto-display in Jupyter notebooks
- Download trigger in browser environments

### FR-006: Backend Compatibility
**Priority**: High  
**Description**: Work with existing plotting backends.

**Acceptance Criteria**:
- Matplotlib backend full support
- hvPlot backend support with static fallback
- Backend detection and appropriate handling
- No breaking changes to existing backend system

## Non-Functional Requirements

### NFR-001: Performance
- Markdown generation performance comparable to HTML generation
- Memory usage optimized for large datasets
- Figure embedding efficiency (base64 vs file trade-offs)

### NFR-002: Compatibility
- Python 3.8+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Compatible with existing QuantStats API design patterns
- No breaking changes to existing functionality

### NFR-003: Maintainability
- Code follows existing QuantStats conventions
- Reuses existing infrastructure where possible
- Clear separation of concerns
- Comprehensive test coverage

### NFR-004: Usability
- API consistency with existing `html()` function
- Clear documentation and examples
- Intuitive parameter naming
- Graceful error handling

## Technical Requirements

### TR-001: Dependencies
- No additional external dependencies required
- Use existing libraries: pandas, numpy, tabulate, base64
- Leverage existing plotting backend infrastructure

### TR-002: File Structure
```
quantstats/
├── reports.py          # Add markdown() function
├── report.md          # New markdown template
└── __init__.py        # Export markdown function
```

### TR-003: API Design
```python
def markdown(
    returns,
    benchmark=None,
    rf=0.0,
    title="Strategy Tearsheet",
    output=None,
    compounded=True,
    periods_per_year=252,
    figfmt="png",
    template_path=None,
    match_dates=True,
    embed_images=True,
    **kwargs,
):
```

## Constraints and Assumptions

### Constraints
- Must maintain backward compatibility
- Cannot modify existing HTML functionality
- Limited to existing dependency set
- Must follow existing code style patterns

### Assumptions
- Users have basic familiarity with markdown format
- Standard markdown parser capabilities (GitHub, CommonMark)
- File system write permissions for output options
- Network access for benchmark data (if used)

## Success Metrics

### Quantitative Metrics
- Adoption rate: % of users utilizing markdown output
- Performance: Generation time within 10% of HTML generation
- Code coverage: >90% test coverage for new functionality
- Bug rate: <1% critical bugs in first 3 months

### Qualitative Metrics
- User satisfaction with markdown output quality
- Ease of use compared to HTML output
- Integration success with markdown-based workflows
- Community feedback and feature requests

## Risk Assessment

### High Risk
- hvPlot interactive chart compatibility with markdown format
- Base64 embedding size limitations
- Cross-platform rendering differences

### Medium Risk
- Template customization complexity
- Performance with large datasets
- User expectation management

### Low Risk
- Basic table formatting
- API design consistency
- Backward compatibility maintenance

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Core `markdown()` function structure
- Basic template system
- Simple table formatting

### Phase 2: Figures & Visualizations (Week 3-4)
- Figure embedding implementation
- Backend compatibility
- Multiple format support

### Phase 3: Advanced Features (Week 5-6)
- Custom template support
- File output options
- Error handling and edge cases

### Phase 4: Testing & Documentation (Week 7-8)
- Comprehensive test suite
- Documentation updates
- Performance optimization

## Approval

**Stakeholder**: QuantStats Development Team  
**Approval Date**: 2025-12-30  
**Review Status**: Pending Implementation  

---

*This requirements document serves as the foundation for the technical specification and design phases of the markdown output feature.*