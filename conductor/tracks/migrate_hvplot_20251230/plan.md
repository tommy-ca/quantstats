# Plan: Migrate visualizations from Matplotlib/Seaborn to hvPlot

## Phase 1: Preparation

- [ ] Task: Update `requirements.txt` and `setup.py` to include `hvplot`
- [ ] Task: Conductor - User Manual Verification 'Preparation' (Protocol in workflow.md)

## Phase 2: Core Plotting Infrastructure

- [ ] Task: Refactor `quantstats/_plotting/core.py` to support hvPlot backend
  - [ ] Write Tests
  - [ ] Implement hvPlot base components in `core.py`
- [ ] Task: Conductor - User Manual Verification 'Core Plotting Infrastructure' (Protocol in workflow.md)

## Phase 3: Core Plot Migration

- [ ] Task: Migrate `cumulative_returns` plot to hvPlot
  - [ ] Write Tests
  - [ ] Implement `cumulative_returns` using hvPlot
- [ ] Task: Migrate `daily_returns` plot to hvPlot
  - [ ] Write Tests
  - [ ] Implement `daily_returns` using hvPlot
- [ ] Task: Migrate `drawdown` plot to hvPlot
  - [ ] Write Tests
  - [ ] Implement `drawdown` using hvPlot
- [ ] Task: Conductor - User Manual Verification 'Core Plot Migration' (Protocol in workflow.md)

## Phase 4: Report Integration

- [ ] Task: Update `quantstats/reports.py` to handle hvPlot objects
  - [ ] Write Tests
  - [ ] Implement hvPlot support in report generation
- [ ] Task: Update `quantstats/report.html` template for interactive charts
  - [ ] Write Tests
  - [ ] Implement template updates
- [ ] Task: Conductor - User Manual Verification 'Report Integration' (Protocol in workflow.md)
