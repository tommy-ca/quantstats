# Design Document: Markdown Output Implementation

## Document Information

**Project**: QuantStats Markdown Output Support  
**Version**: 1.0.0  
**Date**: 2025-12-30  
**Status**: Design Complete  
**Author**: QuantStats Development Team  

## Executive Summary

This design document outlines the detailed implementation approach for adding markdown output support to QuantStats. The design leverages existing infrastructure while introducing minimal new components, ensuring consistency with the current codebase architecture and maintaining backward compatibility.

## Design Principles

### 1. Consistency with Existing Patterns
- Mirror the `html()` function structure and parameter naming
- Use the same template-based approach with placeholder replacement
- Leverage existing metrics calculation and plot generation functions
- Follow established error handling patterns
- **Extend existing infrastructure instead of duplicating functionality**

### 2. Minimal Disruption
- No changes to existing HTML functionality
- No additional external dependencies
- Reuse existing backend abstraction layer
- Maintain current file organization
- **Shared helper functions for cross-format consistency**

### 3. Extensibility
- Template system supports customization
- Figure embedding strategy configurable
- Backend-agnostic design for future plotting backends
- Output format abstraction for potential future formats

### 4. Performance Consideration
- Efficient memory usage for large datasets
- Stream processing for figure generation
- Lazy evaluation where possible
- Minimal overhead compared to HTML generation

## Architecture Design

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    quantstats.markdown()                     │
│                        (Entry Point)                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Data Processing Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Input Validation│  │ Data Preparation │  │ Metrics Calc │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Content Generation Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Plot Generation  │  │ Table Formatting│  │ Template     │ │
│  │   (Backends)    │  │   (Markdown)   │  │ Processing   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Output Handling Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Figure Embedding │  │ Content Assembly │  │ File/Display │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Design

```
Input Parameters
    ↓
[Validation Layer]
    ↓
[Data Preparation]
    ├── Returns cleaning
    ├── Benchmark alignment
    └── Trading periods calculation
    ↓
[Content Generation]
    ├── Metrics calculation (reuse existing)
    ├── Plot generation (reuse existing backends)
    └── Table formatting (new markdown-specific)
    ↓
[Template Processing]
    ├── Load markdown template
    ├── Replace placeholders
    └── Handle conditional sections
    ↓
[Output Processing]
    ├── Figure embedding (base64 or files)
    ├── Content assembly
    └── Output delivery (string/file/notebook)
```

## Detailed Component Design

### 1. Core Function Design

#### Function Signature
```python
def markdown(
    returns,                    # Core data input
    benchmark=None,             # Optional benchmark
    rf=0.0,                     # Risk-free rate
    title="Strategy Tearsheet", # Report title
    output=None,                # Output destination
    compounded=True,            # Compounding flag
    periods_per_year=252,       # Trading periods
    figfmt="png",              # Figure format
    template_path=None,         # Custom template
    match_dates=True,           # Date alignment
    embed_images=True,          # Embedding strategy
    **kwargs,                   # Additional parameters
) -> Optional[str]:
```

#### Parameter Design Rationale

| Parameter | Design Decision | Rationale |
|-----------|-----------------|-----------|
| `figfmt="png"` | Default to PNG | Better markdown compatibility than SVG |
| `embed_images=True` | Default to base64 | Self-contained documents |
| No `grayscale` parameter | Omitted | Not applicable to markdown |
| No `bokeh_resources` parameter | Omitted | Interactive resources not markdown-compatible |
| `template_path=None` | Optional customization | Follows HTML pattern |

#### Internal Structure Design
```python
def markdown(...):
    # Phase 1: Input Validation
    _validate_markdown_inputs(returns, benchmark, template_path)
    
    # Phase 2: Data Preparation (reuse existing)
    returns, benchmark = _prepare_data(returns, benchmark, match_dates, rf)
    
    # Phase 3: Content Generation
    metrics = _generate_metrics(returns, benchmark, **kwargs)
    figures = _generate_figures(returns, benchmark, figfmt, **kwargs)
    
    # Phase 4: Template Processing
    template = _load_markdown_template(template_path)
    content = _process_template(template, metrics, figures, **kwargs)
    
    # Phase 5: Output Handling
    return _handle_output(content, output)
```

### 2. Template System Design

#### Template Structure Design
```markdown
# Header Section
# {{title}}
{{date_range}}
{{benchmark_title}} Generated by [QuantStats](http://quantstats.io) (v. {{v}})

---

## Performance Summary
{{metrics}}

## Analysis Sections
### Returns Analysis
{{returns}}
{{log_returns}}
{{vol_returns}}

### Risk Metrics  
{{rolling_beta}}
{{rolling_vol}}
{{rolling_sharpe}}
{{rolling_sortino}}

### Drawdown Analysis
{{dd_periods}}
{{dd_plot}}

### Visualizations
{{monthly_heatmap}}
{{returns_dist}}
{{eoy_returns}}
{{monthly_dist}}
{{daily_returns}}
```

#### Placeholder Design Strategy

| Placeholder Type | Content | Generation Function |
|------------------|---------|---------------------|
| Metadata | `{{title}}`, `{{date_range}}`, `{{v}}` | Direct string replacement |
| Tables | `{{metrics}}` | `_markdown_table()` |
| Figures | All `{{*_plot}}`, `{{*_returns}}` | `_embed_markdown_figure()` |
| Conditional | `{{benchmark_title}}` | Conditional inclusion |

#### Template Loading Design
```python
def _load_markdown_template(template_path=None):
    """
    Load markdown template with fallback to default.
    
    Design: Secure path handling with validation
    """
    if template_path is None:
        # Default template path
        template_path = Path(__file__).parent / 'report.md'
    else:
        # Custom template with security validation
        template_path = Path(template_path).resolve()
        _validate_template_path(template_path)
    
    # Read with UTF-8 encoding and error handling
    try:
        return template_path.read_text(encoding='utf-8')
    except Exception as e:
        raise FileNotFoundError(f"Failed to read template: {e}")
```

### 3. Figure Embedding Design

#### Embedding Strategy Design

**Unified Approach**:
Figures are processed through a shared pipeline that supports both HTML and Markdown embedding, ensuring consistent behavior across report formats.

**Strategy 1: Base64 Embedding (Default)**
- **Pros**: Self-contained documents, no external files
- **Cons**: Larger file size (~33% increase)
- **Use Case**: Documentation, README files

**Strategy 2: File Reference**
- **Pros**: Smaller markdown file, separate figure management
- **Cons**: Requires file system management
- **Use Case**: Large reports, web deployment

#### Implementation Design
```python
def _embed_figure(
    figfiles,           # Figure data (StringIO or list)
    figfmt,            # Format (png/svg/jpg)
    format_type="html", # Target format (html/markdown)
    embed_images=True,  # Strategy selector
    base_path=None,     # Base path for file references
    caption=None        # Optional caption
) -> str:
    """
    Design: Strategy pattern for embedding approaches, shared between HTML and Markdown
    """
    if format_type == "markdown":
        return _embed_markdown_figure(figfiles, figfmt, embed_images, base_path, caption)
    return _embed_html_figure(figfiles, figfmt) # Existing logic
```

#### Backend Integration Design

**Matplotlib Backend:**
```python
def _generate_matplotlib_figure(plot_func, *args, figfmt="png", **kwargs):
    """
    Design: Direct matplotlib integration
    """
    # Generate plot using existing function
    fig = plot_func(*args, **kwargs)
    
    # Convert to in-memory file
    img_data = StringIO()
    fig.savefig(img_data, format=figfmt, bbox_inches='tight', dpi=100)
    
    # Clean up matplotlib resources
    plt.close(fig)
    
    return img_data
```

**hvPlot Backend:**
```python
def _generate_hvplot_figure(plot_func, *args, figfmt="png", **kwargs):
    """
    Design: Static export for interactive charts
    """
    # Generate interactive plot
    plot = plot_func(*args, backend='hvplot', **kwargs)
    
    # Export static version
    if hasattr(plot, 'save'):
        # Use hvPlot save functionality
        img_data = StringIO()
        plot.save(img_data, format=figfmt)
        return img_data
    else:
        # Fallback to matplotlib if hvPlot export fails
        return _generate_matplotlib_figure(
            lambda *a, **k: plot.opts(backend='matplotlib').plot(*a, **k),
            *args, figfmt=figfmt, **kwargs
        )
```

### 4. Table Formatting Design

#### Markdown Table Design
```python
def _markdown_table(obj, showindex="default"):
    """
    Design: Leverage tabulate with pipe format
    
    Input: pandas DataFrame
    Output: GitHub-flavored markdown table
    """
    # Use tabulate for consistent formatting
    table_str = _tabulate(
        obj,
        headers="keys",
        tablefmt="pipe",      # Markdown pipe format
        floatfmt=".2f",       # Consistent decimal places
        showindex=showindex   # Index display control
    )
    
    # Post-processing for alignment
    return _align_markdown_table(table_str)

def _align_markdown_table(table_str):
    """
    Design: Ensure proper column alignment
    """
    lines = table_str.split('\n')
    if len(lines) >= 2:
        # Ensure separator line has proper colons for alignment
        separator = lines[1]
        # Default to left alignment for text, right for numbers
        lines[1] = separator.replace('-', ':-')
    
    return '\n'.join(lines)
```

#### Table Content Design

**Metrics Table Structure:**
```markdown
| Metric                | Strategy    | Benchmark   |
|-----------------------|-------------|-------------|
| CAGR %                | 15.23       | 12.45       |
| Sharpe Ratio          | 1.23        | 0.98        |
| Max Drawdown %        | -12.34      | -15.67      |
| Volatility (Ann) %    | 18.45       | 16.78       |
```

**Multi-Column Handling:**
```python
def _handle_multicolumn_table(obj, strategy_titles):
    """
    Design: Support for multiple strategies
    """
    if isinstance(obj, _pd.DataFrame) and len(obj.columns) > 1:
        # Add strategy name context
        obj.columns = [f"{strategy_titles[i]}" if i < len(strategy_titles) else f"Strategy {i+1}" 
                      for i in range(len(obj.columns))]
    
    return _markdown_table(obj)
```

### 5. Error Handling Design

#### Validation Layer Design
```python
def _validate_markdown_inputs(returns, benchmark, template_path):
    """
    Design: Comprehensive input validation
    """
    # Returns data validation
    if returns is None:
        raise ValueError("Returns data cannot be None")
    
    if not isinstance(returns, (_pd.Series, _pd.DataFrame)):
        raise TypeError("Returns must be pandas Series or DataFrame")
    
    if len(returns) == 0:
        raise ValueError("Returns data cannot be empty")
    
    # Benchmark validation
    if benchmark is not None:
        if not isinstance(benchmark, (_pd.Series, str, _pd.DataFrame)):
            raise TypeError("Benchmark must be Series, string ticker, or DataFrame")
    
    # Template validation
    if template_path is not None:
        template_path = Path(template_path)
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        if not template_path.is_file():
            raise ValueError(f"Template path is not a file: {template_path}")

def _validate_output_path(output_path):
    """
    Design: Secure output path validation
    """
    if output_path is not None:
        output_path = Path(output_path)
        
        # Check parent directory exists and is writable
        if not output_path.parent.exists():
            raise FileNotFoundError(f"Output directory does not exist: {output_path.parent}")
        
        if not os.access(output_path.parent, os.W_OK):
            raise PermissionError(f"Output directory is not writable: {output_path.parent}")
```

#### Graceful Degradation Design
```python
def _handle_backend_fallback(function_name, *args, **kwargs):
    """
    Design: Graceful handling of backend issues
    """
    try:
        # Try primary backend
        if _plotting_backend.is_matplotlib():
            return getattr(_plots, function_name)(*args, **kwargs)
        elif _plotting_backend.is_hvplot():
            return getattr(_plots, function_name)(*args, backend='hvplot', **kwargs)
    except Exception as e:
        # Fallback strategy
        if _plotting_backend.is_hvplot():
            # Try matplotlib fallback
            try:
                return getattr(_plots, function_name)(*args, backend='matplotlib', **kwargs)
            except Exception:
                pass
        
        # Final fallback: return placeholder
        return f"*Unable to generate {function_name} plot: {str(e)}*"
```

### 6. Performance Optimization Design

#### Memory Management Design
```python
def _optimize_figure_generation(figures, embed_images=True):
    """
    Design: Memory-efficient figure handling
    """
    if embed_images and len(figures) > 5:
        # For many figures, consider file-based approach
        warnings.warn("Many figures detected. Consider using embed_images=False for better memory usage.")
    
    # Clean up figure objects after embedding
    for fig in figures:
        if hasattr(fig, 'close'):
            fig.close()
    
    return figures

def _stream_large_dataset(returns, chunk_size=1000):
    """
    Design: Stream processing for large datasets
    """
    if len(returns) > chunk_size * 10:  # Very large dataset
        # Process in chunks for memory efficiency
        chunks = [returns[i:i+chunk_size] for i in range(0, len(returns), chunk_size)]
        return _process_chunks(chunks)
    else:
        return returns
```

#### Caching Design
```python
def _cache_template(template_path):
    """
    Design: Template caching for repeated calls
    """
    cache_key = str(template_path)
    
    if cache_key not in _template_cache:
        _template_cache[cache_key] = template_path.read_text(encoding='utf-8')
    
    return _template_cache[cache_key]

# Global cache for templates
_template_cache = {}
```

## Integration Design

### 1. Module Integration Design

#### `reports.py` Modifications
```python
# New imports (if needed)
from pathlib import Path
import warnings

# New function placement (after html() function)
def markdown(...):
    """Implementation as designed above"""

# Helper functions placement (after existing helpers)
def _markdown_table(...):
    """Table formatting implementation"""

def _embed_markdown_figure(...):
    """Figure embedding implementation"""

# Template validation functions
def _validate_template_path(...):
    """Security validation implementation"""
```

#### `__init__.py` Updates
```python
# Add to existing exports
from .reports import markdown as tearsheet_markdown

# Or add to main namespace
from .reports import markdown

# Update __all__ list
__all__ = [
    'stats', 'plots', 'reports', 'utils', 'html', 'markdown',  # Add markdown
    # ... existing exports
]
```

### 2. File System Integration Design

#### New Files Structure
```
quantstats/
├── reports.py              # Enhanced with markdown functionality
├── report.html             # Existing (unchanged)
├── report.md               # New markdown template
├── __init__.py             # Updated exports
└── _plotting/
    ├── backend.py          # Existing (unchanged)
    └── [no new files]      # Leverage existing backend system
```

#### Template File Design
```markdown
<!-- report.md - Default markdown template -->
# {{title}}
{{date_range}}

{{benchmark_title}} Generated by [QuantStats](http://quantstats.io) (v. {{v}})

---

## Performance Summary

{{metrics}}

## Returns Analysis

### Cumulative Returns
{{returns}}

### Log Returns  
{{log_returns}}

### Volatility Analysis
{{vol_returns}}

### End-of-Year Returns
{{eoy_returns}}

### Monthly Distribution
{{monthly_dist}}

### Daily Returns Analysis
{{daily_returns}}

---

## Risk Metrics

### Rolling Beta
{{rolling_beta}}

### Rolling Volatility
{{rolling_vol}}

### Rolling Sharpe Ratio
{{rolling_sharpe}}

### Rolling Sortino Ratio
{{rolling_sortino}}

---

## Drawdown Analysis

### Drawdown Periods
{{dd_periods}}

### Drawdown Chart
{{dd_plot}}

---

## Monthly Heatmap
{{monthly_heatmap}}

---

## Returns Distribution
{{returns_dist}}
```

## Testing Strategy Design

### 1. Unit Test Design

#### Core Function Tests
```python
class TestMarkdownFunction:
    def test_basic_generation(self):
        """Test basic markdown generation with minimal parameters"""
        returns = _generate_test_returns()
        result = qs.markdown(returns)
        
        assert isinstance(result, str)
        assert '# Strategy Tearsheet' in result
        assert '## Performance Summary' in result
        
    def test_with_benchmark(self):
        """Test benchmark inclusion in markdown"""
        returns = _generate_test_returns()
        benchmark = _generate_test_benchmark()
        result = qs.markdown(returns, benchmark=benchmark)
        
        assert 'Benchmark' in result
        assert '| CAGR %' in result
        
    def test_custom_template(self):
        """Test custom template functionality"""
        returns = _generate_test_returns()
        custom_template = self._create_custom_template()
        result = qs.markdown(returns, template_path=custom_template)
        
        assert 'Custom Title' in result
        
    def test_file_output(self):
        """Test file saving functionality"""
        returns = _generate_test_returns()
        output_file = Path('test_output.md')
        
        qs.markdown(returns, output=str(output_file))
        
        assert output_file.exists()
        output_file.unlink()  # Cleanup
```

#### Helper Function Tests
```python
class TestMarkdownHelpers:
    def test_table_formatting(self):
        """Test _markdown_table function"""
        df = _pd.DataFrame({
            'Metric': ['CAGR', 'Sharpe'],
            'Value': [15.23, 1.23]
        })
        
        result = _markdown_table(df)
        
        assert '| Metric | Value |' in result
        assert '| CAGR | 15.23 |' in result
        
    def test_figure_embedding(self):
        """Test _embed_markdown_figure function"""
        fig_data = self._create_test_figure()
        
        result = _embed_markdown_figure(fig_data, 'png', embed_images=True)
        
        assert result.startswith('![')
        assert 'data:image/png;base64,' in result
```

### 2. Integration Test Design

#### Backend Integration Tests
```python
class TestBackendIntegration:
    def test_matplotlib_backend(self):
        """Test matplotlib figure generation"""
        # Force matplotlib backend
        _plotting_backend.set_backend('matplotlib')
        
        returns = _generate_test_returns()
        result = qs.markdown(returns)
        
        assert 'data:image/' in result  # Figure embedded
        
    def test_hvplot_backend(self):
        """Test hvPlot static export"""
        # Force hvPlot backend
        _plotting_backend.set_backend('hvplot')
        
        returns = _generate_test_returns()
        result = qs.markdown(returns)
        
        assert 'data:image/' in result  # Static figure embedded
```

### 3. Performance Test Design

#### Benchmark Tests
```python
class TestPerformance:
    def test_generation_time_comparison(self):
        """Compare markdown vs HTML generation time"""
        returns = _generate_large_test_returns()
        
        # Time HTML generation
        start = time.time()
        qs.html(returns, output='test.html')
        html_time = time.time() - start
        
        # Time markdown generation
        start = time.time()
        qs.markdown(returns, output='test.md')
        md_time = time.time() - start
        
        # Markdown should be within 110% of HTML time
        assert md_time < html_time * 1.1
        
    def test_memory_usage(self):
        """Test memory usage with large datasets"""
        returns = _generate_large_test_returns()
        
        # Monitor memory during generation
        initial_memory = self._get_memory_usage()
        result = qs.markdown(returns)
        final_memory = self._get_memory_usage()
        
        # Memory increase should be reasonable
        memory_increase = final_memory - initial_memory
        assert memory_increase < len(returns) * 0.5  # Less than 50% of data size
```

## Deployment and Release Design

### 1. Version Management Design

#### Semantic Versioning
```
Current: 0.0.1
Target: 0.1.0 (minor version - new feature)

Breaking Changes: None
New Features: Markdown output support
Bug Fixes: N/A
```

#### Release Checklist
- [ ] All tests passing (>90% coverage)
- [ ] Documentation updated
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Backward compatibility verified

### 2. Documentation Design

#### API Documentation
```python
def markdown(...):
    """
    Generate markdown tearsheet report for portfolio performance analysis.
    
    This function creates a comprehensive markdown report containing performance
    metrics, visualizations, and analysis of investment returns. The report
    includes comparisons with benchmarks, drawdown analysis, and various
    performance charts in markdown format suitable for documentation and
    text-based workflows.
    
    Parameters
    ----------
    returns : pd.Series or pd.DataFrame
        Daily returns data for the strategy/portfolio
    benchmark : pd.Series, str, or None, default None
        Benchmark returns for comparison. Can be a Series of returns,
        a ticker symbol string, or None for no benchmark
    rf : float, default 0.0
        Risk-free rate for calculations (as decimal, e.g., 0.02 for 2%)
    title : str, default "Strategy Tearsheet"
        Title to display at the top of the markdown report
    output : str or None, default None
        File path to save the markdown report. If None, returns string
    compounded : bool, default True
        Whether to compound returns for calculations
    periods_per_year : int, default 252
        Number of trading periods per year for annualization
    figfmt : str, default "png"
        Format for embedded charts ('png', 'svg', 'jpg')
    template_path : str or None, default None
        Path to custom markdown template file. Uses default if None
    match_dates : bool, default True
        Whether to align returns and benchmark start dates
    embed_images : bool, default True
        Whether to embed images as base64 (True) or use file references (False)
    **kwargs
        Additional keyword arguments for customization:
        - strategy_title: Custom name for the strategy
        - benchmark_title: Custom name for the benchmark
        - active_returns: Whether to show active returns vs benchmark
    
    Returns
    -------
    str or None
        Markdown content string when output=None, None when saved to file
    
    Examples
    --------
    >>> import quantstats as qs
    >>> 
    >>> # Generate markdown content
    >>> md_content = qs.markdown(returns, benchmark='^GSPC')
    >>> print(md_content)
    >>> 
    >>> # Save to file
    >>> qs.markdown(returns, output='strategy_report.md', title='My Strategy')
    >>> 
    >>> # Custom template
    >>> qs.markdown(returns, template_path='custom.md')
    >>> 
    >>> # File-based figures for smaller file size
    >>> qs.markdown(returns, embed_images=False, output='report.md')
    
    See Also
    --------
    quantstats.html : Generate HTML tearsheet report
    quantstats.metrics : Calculate performance metrics
    quantstats.plots : Generate performance visualizations
    
    Notes
    -----
    - For hvPlot backend, interactive charts are exported as static images
    - Base64 embedding increases file size by ~33% but creates self-contained documents
    - File references require the figures to be saved separately
    - Template customization follows the same pattern as HTML templates
    
    References
    ----------
    .. [1] QuantStats Documentation: https://quantstats.readthedocs.io/
    .. [2] Markdown Guide: https://www.markdownguide.org/
    """
```

#### User Guide Structure
```markdown
# Markdown Output Guide

## Quick Start
```python
import quantstats as qs

# Basic markdown generation
md_report = qs.markdown(returns)

# Save to file
qs.markdown(returns, output='report.md')
```

## Advanced Usage
### Custom Templates
### Figure Embedding Options
### Backend Considerations
### Performance Tips

## Examples
### Basic Strategy Report
### Benchmark Comparison
### Multi-Strategy Analysis
```

## Future Considerations

### 1. Extensibility Design

#### Output Format Abstraction
```python
# Future design for multiple output formats
class ReportGenerator:
    def __init__(self, format_type):
        self.format_type = format_type
    
    def generate(self, returns, **kwargs):
        if self.format_type == 'html':
            return self._generate_html(returns, **kwargs)
        elif self.format_type == 'markdown':
            return self._generate_markdown(returns, **kwargs)
        elif self.format_type == 'pdf':  # Future
            return self._generate_pdf(returns, **kwargs)
```

#### Plugin Architecture
```python
# Future design for backend plugins
class FigureBackend:
    def generate_figure(self, plot_func, *args, **kwargs):
        raise NotImplementedError
    
    def embed_in_format(self, figure_data, format_type):
        raise NotImplementedError

class MatplotlibMarkdownBackend(FigureBackend):
    def generate_figure(self, plot_func, *args, **kwargs):
        # Matplotlib-specific implementation
        pass
    
    def embed_in_format(self, figure_data, format_type):
        if format_type == 'markdown':
            return self._embed_markdown(figure_data)
        # ... other formats
```

### 2. Performance Optimization Roadmap

#### Phase 1: Current Implementation
- Basic markdown generation
- Base64 figure embedding
- Template-based approach

#### Phase 2: Performance Enhancements
- Lazy figure generation
- Improved memory management
- Template caching

#### Phase 3: Advanced Features
- Parallel figure generation
- Streaming output for large datasets
- Compression for embedded figures

---

*This design document provides the complete implementation blueprint for the markdown output feature, ensuring consistency with existing patterns while maintaining extensibility for future enhancements.*