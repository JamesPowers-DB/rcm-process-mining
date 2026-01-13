# Quick Start Guide

Get the RCM Process Mining Demo running in 15 minutes.

## Prerequisites

- Databricks workspace
- Python 3.11+
- SQL Warehouse running

## 5-Minute Local Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/your-warehouse-id"
export DATABRICKS_TOKEN="your-token"
```

### 3. Generate Sample Data

```bash
python generate_rcm_data.py
```

This creates 1M journeys (~5-10 minutes on a 2-node cluster).

### 4. Run the App

```bash
python app.py
```

Open `http://localhost:8080` in your browser.

## 10-Minute Databricks Apps Deployment

### 1. Create Secret Scope

```bash
databricks secrets create-scope rcm-demo-secrets
databricks secrets put-secret rcm-demo-secrets databricks-host
databricks secrets put-secret rcm-demo-secrets databricks-http-path
databricks secrets put-secret rcm-demo-secrets databricks-token
```

### 2. Deploy App

```bash
databricks apps deploy --config app.yaml
```

### 3. Access

Get the app URL from deployment output and open in browser.

## Using the Demo

### Basic Workflow

1. **Adjust Granularity**: Use slider to control detail level
   - Start with level 2 (Average) for overview
   - Increase to 4-5 for detailed analysis

2. **Apply Filters**: 
   - Select date range
   - Choose department or outcome
   - Click "Apply Filters"

3. **Explore Graph**:
   - Green paths = optimal "happy path"
   - Red dashed = bottlenecks
   - Thicker edges = higher volume
   - Click nodes for details

4. **Review Statistics**: Check the metrics panel for KPIs

5. **Consult Glossary**: Visit `/glossary` for activity definitions

### Example Analyses

**Find Bottlenecks:**
1. Set granularity to 3-4
2. Look for red dashed edges
3. Click nodes to see cycle times
4. Focus on high P95 times

**Compare Outcomes:**
1. Filter by "Success - Full Payment"
2. Note the path and statistics
3. Change to "Denial Unresolved"
4. Compare paths and cycle times

**Department Analysis:**
1. Filter by department (e.g., "AR")
2. See activities specific to that department
3. Review success rates and costs

## Troubleshooting

**Can't connect to Databricks:**
- Verify credentials are correct
- Check SQL warehouse is running
- Test with: `databricks workspace list`

**No data showing:**
- Ensure data generation completed
- Check table exists: `SELECT COUNT(*) FROM rcm_demo.process_mining.rcm_events`
- Verify permissions on table

**Graph not rendering:**
- Check browser console for errors
- Try reducing granularity level
- Clear browser cache

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Customize visualizations in `src/visualization.py`
- Add new activities in `generate_rcm_data.py`

## Support

For issues, check logs:
```bash
# Local
tail -f app.log

# Databricks Apps
databricks apps logs rcm-process-mining-demo
```
