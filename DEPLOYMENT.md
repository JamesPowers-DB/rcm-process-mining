# Databricks Apps Deployment Guide

This guide walks through deploying the RCM Process Mining Demo as a Databricks App.

## Prerequisites

- Databricks workspace with Apps enabled
- Unity Catalog enabled
- SQL Warehouse running
- Databricks CLI installed (optional)
- Permissions to create secret scopes

## Step-by-Step Deployment

### Step 1: Generate Data

Run the data generation script to create the synthetic RCM dataset:

```python
# In a Databricks notebook
%run ./generate_rcm_data.py
```

Or submit as a job:

```bash
databricks jobs create --json '{
  "name": "Generate RCM Data",
  "tasks": [{
    "task_key": "generate_data",
    "python_file": "generate_rcm_data.py",
    "cluster": {
      "spark_version": "14.3.x-scala2.12",
      "node_type_id": "i3.xlarge",
      "num_workers": 2
    }
  }]
}'
```

**Expected Output:**
- Delta table: `rcm_demo.process_mining.rcm_events`
- ~1 million journeys
- ~30-50 million events (depending on journey complexity)

### Step 2: Create Secret Scope

Create a secret scope for storing credentials:

#### Option A: Using Databricks CLI

```bash
# Create scope
databricks secrets create-scope rcm-demo-secrets

# Add secrets (will open editor)
databricks secrets put-secret rcm-demo-secrets databricks-host
# Enter: https://your-workspace.cloud.databricks.com

databricks secrets put-secret rcm-demo-secrets databricks-http-path
# Enter: /sql/1.0/warehouses/your-warehouse-id

databricks secrets put-secret rcm-demo-secrets databricks-token
# Enter: your-personal-access-token
```

#### Option B: Using Databricks UI

1. Go to **Settings** → **Secrets**
2. Click **Create Scope**
3. Name: `rcm-demo-secrets`
4. Add three secrets:
   - Key: `databricks-host`, Value: `https://your-workspace.cloud.databricks.com`
   - Key: `databricks-http-path`, Value: `/sql/1.0/warehouses/your-warehouse-id`
   - Key: `databricks-token`, Value: your token

#### Getting SQL Warehouse HTTP Path

1. Go to **SQL Warehouses** in your workspace
2. Select your warehouse
3. Click **Connection Details**
4. Copy the **HTTP Path** (format: `/sql/1.0/warehouses/abc123def456`)

#### Creating a Personal Access Token

1. Go to **Settings** → **Developer** → **Access Tokens**
2. Click **Generate New Token**
3. Set expiration (recommend 90 days for production)
4. Copy the token (you won't see it again!)

### Step 3: Configure Permissions

Grant the app access to the Delta table:

```sql
-- Grant catalog permissions
GRANT USE CATALOG ON CATALOG rcm_demo TO `your-service-principal`;

-- Grant schema permissions
GRANT USE SCHEMA ON SCHEMA rcm_demo.process_mining TO `your-service-principal`;

-- Grant table permissions
GRANT SELECT ON TABLE rcm_demo.process_mining.rcm_events TO `your-service-principal`;
```

Or use the UI:
1. Navigate to **Catalog** → `rcm_demo` → `process_mining` → `rcm_events`
2. Click **Permissions**
3. Add your service principal or user with SELECT privilege

### Step 4: Deploy the App

#### Option A: Using Databricks UI

1. Navigate to **Apps** in your workspace
2. Click **Create App**
3. Fill in details:
   - **Name**: `rcm-process-mining-demo`
   - **Description**: Interactive RCM process mining visualization
4. Upload files:
   - Upload entire project directory
   - Or connect to Git repository
5. Configure:
   - **Runtime**: Python 3.11
   - **Entry Point**: `app.py`
   - **Port**: 8080
6. Add environment variables:
   - Reference secret scope: `rcm-demo-secrets`
   - Map keys: `databricks-host`, `databricks-http-path`, `databricks-token`
7. Set resources:
   - **Memory**: 4Gi
   - **CPU**: 2 cores
8. Click **Deploy**

#### Option B: Using Databricks CLI

```bash
# Navigate to project directory
cd /path/to/rcm-process-mining

# Deploy app
databricks apps deploy \
  --app-name rcm-process-mining-demo \
  --source-path . \
  --config app.yaml
```

#### Option C: Using Databricks Asset Bundles

Create `databricks.yml`:

```yaml
bundle:
  name: rcm-process-mining

resources:
  apps:
    rcm_demo:
      name: rcm-process-mining-demo
      description: Interactive RCM process mining visualization
      source_code_path: .
      config:
        command: ["python", "app.py"]
        env:
          - name: DATABRICKS_HOST
            valueFrom:
              secretKeyRef:
                scope: rcm-demo-secrets
                key: databricks-host
          - name: DATABRICKS_HTTP_PATH
            valueFrom:
              secretKeyRef:
                scope: rcm-demo-secrets
                key: databricks-http-path
          - name: DATABRICKS_TOKEN
            valueFrom:
              secretKeyRef:
                scope: rcm-demo-secrets
                key: databricks-token
```

Deploy:

```bash
databricks bundle deploy
```

### Step 5: Verify Deployment

1. Wait for deployment to complete (2-5 minutes)
2. Check app status:
   ```bash
   databricks apps get rcm-process-mining-demo
   ```
3. Access the app URL (provided in deployment output)
4. Test functionality:
   - Main page loads with graph
   - Filters work correctly
   - Statistics update
   - Glossary page accessible

## Post-Deployment

### Monitoring

Monitor app health and performance:

```bash
# View app logs
databricks apps logs rcm-process-mining-demo

# Check app status
databricks apps get rcm-process-mining-demo --output json
```

Or use the UI:
1. Go to **Apps** → `rcm-process-mining-demo`
2. View **Logs** tab
3. Check **Metrics** tab

### Updating the App

To update the app with new code:

```bash
# Redeploy
databricks apps deploy \
  --app-name rcm-process-mining-demo \
  --source-path . \
  --config app.yaml
```

Or in the UI:
1. Go to **Apps** → `rcm-process-mining-demo`
2. Click **Update**
3. Upload new files or sync from Git
4. Click **Deploy**

### Scaling

Adjust resources based on usage:

1. Edit `app.yaml`:
   ```yaml
   resources:
     memory: "8Gi"  # Increase for larger datasets
     cpu: "4"       # Increase for more concurrent users
   ```
2. Redeploy the app

### Troubleshooting

#### App Won't Start

Check logs for errors:
```bash
databricks apps logs rcm-process-mining-demo --tail 100
```

Common issues:
- Missing dependencies: Check `requirements.txt`
- Secret scope not accessible: Verify permissions
- Port conflict: Ensure port 8080 is available

#### Connection Errors

Verify credentials:
```bash
# Test secret access
databricks secrets get-secret rcm-demo-secrets databricks-host
```

Check SQL warehouse:
- Ensure warehouse is running
- Verify HTTP path is correct
- Test connection with SQL query

#### Performance Issues

- Increase resource allocation
- Add indexes to Delta table:
  ```sql
  OPTIMIZE rcm_demo.process_mining.rcm_events
  ZORDER BY (entity_id, timestamp);
  ```
- Enable caching in data loader
- Reduce default date range

## Security Best Practices

1. **Use Service Principals**: Create a dedicated service principal for the app
2. **Rotate Tokens**: Set expiration on access tokens and rotate regularly
3. **Least Privilege**: Grant only necessary permissions (SELECT on specific tables)
4. **Audit Logging**: Enable audit logs for secret access
5. **Network Security**: Use private endpoints if available

## Cost Optimization

1. **Auto-stop SQL Warehouse**: Configure warehouse to auto-stop after inactivity
2. **Right-size Resources**: Start with smaller resources and scale up as needed
3. **Cache Data**: Implement caching for frequently accessed queries
4. **Optimize Queries**: Use filters to reduce data scanned

## Maintenance

### Regular Tasks

- **Weekly**: Review app logs for errors
- **Monthly**: Check resource utilization and adjust
- **Quarterly**: Rotate access tokens
- **As Needed**: Update dependencies for security patches

### Backup

The app is stateless, but backup:
- Source code (use Git)
- Configuration files
- Delta table (automatic with Unity Catalog)

## Support

For issues:
1. Check logs: `databricks apps logs rcm-process-mining-demo`
2. Review Databricks Apps documentation
3. Contact Databricks support
4. File issues in project repository

## Additional Resources

- [Databricks Apps Documentation](https://docs.databricks.com/apps/)
- [Unity Catalog Documentation](https://docs.databricks.com/unity-catalog/)
- [Dash Documentation](https://dash.plotly.com/)
- [Delta Lake Documentation](https://docs.delta.io/)
