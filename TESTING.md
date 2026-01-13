# Testing Guide

This guide covers testing the RCM Process Mining Demo application.

## Quick Validation Checklist

Use this checklist to verify the application is working correctly:

### Data Layer
- [ ] Delta table exists: `rcm_demo.process_mining.rcm_events`
- [ ] Table has data: `SELECT COUNT(*) FROM rcm_demo.process_mining.rcm_events`
- [ ] All 50+ activities present: `SELECT COUNT(DISTINCT activity_code) FROM ...`
- [ ] Date range is correct (2023-2024)
- [ ] No NULL values in critical columns

### Application Startup
- [ ] App starts without errors
- [ ] Configuration validation passes
- [ ] Secret scope credentials load successfully
- [ ] Database connection established
- [ ] Port 8080 is accessible

### Main Page
- [ ] Page loads within 5 seconds
- [ ] Header displays correctly
- [ ] Navigation links work
- [ ] Statistics panel shows data
- [ ] Graph container renders
- [ ] Filters are interactive

### Graph Visualization
- [ ] Nodes appear on graph
- [ ] Edges connect nodes
- [ ] Colors are correct (green/blue/red)
- [ ] Node labels are readable
- [ ] Edge thickness varies
- [ ] Graph is interactive (pan/zoom)

### Filters
- [ ] Granularity slider works (1-5)
- [ ] Date picker opens and accepts dates
- [ ] Department dropdown populates
- [ ] Outcome dropdown populates
- [ ] "Apply Filters" button responds
- [ ] Graph updates after filtering

### Interactivity
- [ ] Click node shows details
- [ ] Hover over edge shows tooltip
- [ ] Node selection highlights
- [ ] Statistics update with filters
- [ ] Legend displays correctly

### Glossary Page
- [ ] Navigate to /glossary works
- [ ] All phases display
- [ ] All 50+ activities listed
- [ ] Descriptions are readable
- [ ] Formatting is correct
- [ ] Back to main page works

### Responsive Design
- [ ] Desktop view (1920x1080)
- [ ] Tablet view (768x1024)
- [ ] Mobile view (375x667)
- [ ] Sidebar collapses on mobile
- [ ] Graph is scrollable

## Manual Testing Scenarios

### Scenario 1: Happy Path Analysis

**Goal**: Identify the most common successful path

**Steps**:
1. Set granularity to 2 (Average)
2. Filter outcome: "Success - Full Payment"
3. Click "Apply Filters"
4. Observe green edges (happy path)
5. Click on nodes to see volumes

**Expected**:
- Graph shows 15-20 nodes
- Green edges connect major activities
- Statistics show high success rate (>90%)
- Cycle time is reasonable (10-30 days)

### Scenario 2: Bottleneck Detection

**Goal**: Find slow transitions in the process

**Steps**:
1. Set granularity to 4 (Very Detailed)
2. No outcome filter (All)
3. Click "Apply Filters"
4. Look for red dashed edges
5. Click nodes connected by red edges

**Expected**:
- Red dashed edges indicate bottlenecks
- Node details show high average duration
- P95 cycle time is significantly higher
- Common bottlenecks: Prior Auth, Appeal Review

### Scenario 3: Department Analysis

**Goal**: Analyze AR department performance

**Steps**:
1. Set granularity to 3 (Detailed)
2. Filter department: "AR"
3. Click "Apply Filters"
4. Review statistics

**Expected**:
- Graph shows only AR activities
- 8-10 nodes visible
- Statistics reflect AR-specific metrics
- Activities include: Adjudication, Denials, Appeals

### Scenario 4: Outcome Comparison

**Goal**: Compare denied vs successful journeys

**Steps**:
1. Filter outcome: "Success - Full Payment"
2. Note cycle time and path
3. Change to "Denial Unresolved"
4. Compare differences

**Expected**:
- Denied journeys show appeal activities
- Cycle time is longer for denials
- Different node colors (more red)
- Lower success rates

### Scenario 5: Granularity Levels

**Goal**: Test all granularity levels

**Steps**:
1. Set to level 1, apply filters, observe
2. Increment to level 2, apply, observe
3. Continue through level 5

**Expected**:
- Level 1: 10-15 nodes (high-level)
- Level 2: 20-25 nodes (average)
- Level 3: 30-35 nodes (detailed)
- Level 4: 40-45 nodes (very detailed)
- Level 5: 50+ nodes (complete)

## Automated Testing

### Unit Tests (Future Enhancement)

Create `tests/test_process_mining.py`:

```python
import pytest
from src.process_mining import ProcessMiningEngine
import pandas as pd

def test_happy_path_identification():
    engine = ProcessMiningEngine()
    # Test with sample data
    pass

def test_bottleneck_detection():
    engine = ProcessMiningEngine()
    # Test bottleneck logic
    pass
```

### Integration Tests (Future Enhancement)

Create `tests/test_integration.py`:

```python
import pytest
from src.data_loader import RCMDataLoader

def test_data_loader_connection():
    loader = RCMDataLoader("rcm_demo", "process_mining", "rcm_events")
    # Test connection
    pass

def test_end_to_end_flow():
    # Test complete data flow
    pass
```

## Performance Testing

### Load Testing

Test with different data volumes:

```python
# Test with 10K journeys
df = data_loader.load_data(limit=10000)
# Measure: Load time, graph render time

# Test with 100K journeys
df = data_loader.load_data(limit=100000)
# Measure: Load time, graph render time

# Test with 1M journeys (full dataset)
df = data_loader.load_data()
# Measure: Load time, graph render time
```

**Expected Performance**:
- 10K journeys: < 2 seconds load, < 1 second render
- 100K journeys: < 5 seconds load, < 2 seconds render
- 1M journeys: < 15 seconds load, < 3 seconds render (with granularity 1-3)

### Concurrent User Testing

Test with multiple simultaneous users:

```bash
# Use Apache Bench or similar tool
ab -n 100 -c 10 http://localhost:8080/
```

**Expected**:
- 10 concurrent users: No errors
- Response time: < 5 seconds
- No memory leaks

## Data Quality Testing

### SQL Validation Queries

```sql
-- Check for NULL values
SELECT 
    COUNT(*) as total_rows,
    SUM(CASE WHEN entity_id IS NULL THEN 1 ELSE 0 END) as null_entity_id,
    SUM(CASE WHEN activity_code IS NULL THEN 1 ELSE 0 END) as null_activity_code,
    SUM(CASE WHEN timestamp IS NULL THEN 1 ELSE 0 END) as null_timestamp
FROM rcm_demo.process_mining.rcm_events;

-- Check activity distribution
SELECT 
    activity_code,
    COUNT(*) as count,
    COUNT(DISTINCT entity_id) as unique_journeys
FROM rcm_demo.process_mining.rcm_events
GROUP BY activity_code
ORDER BY count DESC;

-- Check journey completeness
SELECT 
    entity_id,
    COUNT(*) as activity_count,
    MIN(timestamp) as start_time,
    MAX(timestamp) as end_time
FROM rcm_demo.process_mining.rcm_events
GROUP BY entity_id
HAVING COUNT(*) < 5  -- Flag incomplete journeys
LIMIT 100;

-- Check for data anomalies
SELECT 
    activity_code,
    AVG(duration_minutes) as avg_duration,
    MAX(duration_minutes) as max_duration,
    MIN(duration_minutes) as min_duration
FROM rcm_demo.process_mining.rcm_events
GROUP BY activity_code
HAVING MAX(duration_minutes) > 100000  -- Flag suspicious durations
ORDER BY max_duration DESC;
```

## Browser Compatibility Testing

Test in multiple browsers:

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## Accessibility Testing

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Focus indicators visible
- [ ] Alt text for images
- [ ] Semantic HTML structure

## Security Testing

- [ ] No credentials in logs
- [ ] No credentials in error messages
- [ ] Secret scope access only
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection (if applicable)

## Troubleshooting Common Issues

### Issue: Graph Not Rendering

**Diagnosis**:
1. Check browser console for errors
2. Verify data is loading: Check network tab
3. Inspect Cytoscape elements in DOM

**Solutions**:
- Clear browser cache
- Reduce granularity level
- Check CSS is loading

### Issue: Slow Performance

**Diagnosis**:
1. Check data volume being loaded
2. Monitor memory usage
3. Check SQL warehouse performance

**Solutions**:
- Apply more restrictive filters
- Reduce granularity
- Optimize Delta table (OPTIMIZE, ZORDER)
- Increase app resources

### Issue: Connection Errors

**Diagnosis**:
1. Check environment variables
2. Test SQL warehouse connectivity
3. Verify secret scope access

**Solutions**:
- Verify credentials in secret scope
- Ensure SQL warehouse is running
- Check network connectivity
- Review IAM permissions

## Test Data Validation

After generating data, validate:

```python
import pandas as pd

# Load sample
df = data_loader.load_data(limit=10000)

# Validate schema
assert 'entity_id' in df.columns
assert 'activity_code' in df.columns
assert 'timestamp' in df.columns

# Validate data types
assert df['entity_id'].dtype == 'object'
assert df['activity_order'].dtype in ['int64', 'int32']
assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])

# Validate ranges
assert df['duration_minutes'].min() >= 0
assert df['cost_dollars'].min() >= 0
assert df['activity_order'].min() >= 0

# Validate referential integrity
assert df.groupby('entity_id')['activity_order'].apply(
    lambda x: list(x) == list(range(len(x)))
).all()

print("✅ All validations passed!")
```

## Reporting Issues

When reporting issues, include:

1. **Environment**: Local or Databricks Apps
2. **Browser**: Name and version
3. **Steps to Reproduce**: Detailed steps
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happened
6. **Screenshots**: If applicable
7. **Logs**: Application logs or browser console
8. **Data**: Sample query or filter settings

## Continuous Testing

For production deployments:

1. **Pre-deployment**: Run all manual scenarios
2. **Post-deployment**: Smoke test critical paths
3. **Weekly**: Review application logs
4. **Monthly**: Full regression testing
5. **Quarterly**: Performance benchmarking

## Success Criteria

Application is ready for production when:

- ✅ All checklist items pass
- ✅ All manual scenarios work
- ✅ Performance meets targets
- ✅ No critical bugs
- ✅ Data quality validated
- ✅ Security checks pass
- ✅ Documentation complete
