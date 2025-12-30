# Plan: Unit tests and E2E tests for hvPlot migrations

## Phase 1: Test Infrastructure [checkpoint: db36668]

- [x] Task: Install test dependencies (`beautifulsoup4` for DOM parsing) 7e09295
- [x] Task: Conductor - User Manual Verification 'Test Infrastructure' (Protocol in workflow.md) db36668

## Phase 2: Unit Tests for hvPlot Integration

- [ ] Task: Create unit tests for core plots returning hvPlot objects
  - [ ] Write Tests (Red Phase)
  - [ ] Verify implementation (Green Phase)
- [ ] Task: Ensure tests handle live `yfinance` data fetching
  - [ ] Write Tests
  - [ ] Implement robust data loading for tests
- [ ] Task: Conductor - User Manual Verification 'Unit Tests for hvPlot Integration' (Protocol in workflow.md)

## Phase 3: E2E Tests for HTML Reports

- [ ] Task: Create E2E test for `qs.reports.html()` with hvPlot
  - [ ] Write Tests (Red Phase) - Verify DOM presence of Bokeh markers
  - [ ] Verify implementation (Green Phase)
- [ ] Task: Verify inclusion of Bokeh/HoloViews runtime scripts in output
  - [ ] Write Tests
  - [ ] Verify template contains necessary tags
- [ ] Task: Conductor - User Manual Verification 'E2E Tests for HTML Reports' (Protocol in workflow.md)
