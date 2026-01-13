# RCM Process Mining Demo

An interactive Dash web application for visualizing and analyzing healthcare revenue cycle management (RCM) process flows. Built for deployment as a Databricks App with Delta Lake integration.

## Overview

This application provides a comprehensive process mining solution for healthcare RCM, featuring:

- **Interactive Process Visualization**: Node-based graph showing the complete patient journey through 50+ RCM activities
- **Granular Analysis**: Adjustable detail levels from high-level overview to complete process flows
- **Path Analytics**: Identification of "happy paths" (optimal flows) and bottlenecks
- **Real-time Filtering**: Filter by date range, department, outcome, and more
- **Comprehensive Statistics**: Journey counts, cycle times, success rates, and cost metrics
- **Activity Glossary**: Detailed definitions of all RCM process steps

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Databricks Workspace                      │
│                                                               │
│  ┌──────────────────┐         ┌────────────────────────┐   │
│  │  Databricks App  │         │   Unity Catalog        │   │
│  │                  │         │                        │   │
│  │  ┌────────────┐  │         │  ┌──────────────────┐ │   │
│  │  │ Dash Web   │──┼────────▶│  │ Delta Table:     │ │   │
│  │  │ Application│  │         │  │ rcm_events       │ │   │
│  │  └────────────┘  │         │  │ (1M+ journeys)   │ │   │
│  │                  │         │  └──────────────────┘ │   │
│  │  ┌────────────┐  │         │                        │   │
│  │  │ Cytoscape  │  │         └────────────────────────┘   │
│  │  │ Graph Viz  │  │                                       │
│  │  └────────────┘  │         ┌────────────────────────┐   │
│  └──────────────────┘         │   Secret Scope         │   │
│                                │   (Credentials)        │   │
│                                └────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
rcm-process-mining/
├── app.py                      # Main Dash application
├── generate_rcm_data.py        # Synthetic data generation script
├── requirements.txt            # Python dependencies
├── app.yaml                    # Databricks Apps configuration
├── .databricks-app.json        # App metadata
├── setup.py                    # Package setup
├── README.md                   # This file
├── src/                        # Source modules
│   ├── __init__.py
│   ├── data_loader.py          # Delta table data loading
│   ├── process_mining.py       # Process mining analytics engine
│   ├── visualization.py        # Cytoscape graph builder
│   └── glossary.py             # Activity definitions
├── assets/                     # Static assets
│   └── custom.css              # Milligram + Databricks styling
└── rules/                      # Project coding rules
    ├── frontend_strategy.mdc
    ├── databricks_strategy.mdc
    ├── database_strategy.mdc
    ├── style_strategy.mdc
    └── ...
```

## Data Model

### Delta Table Schema: `rcm_demo.process_mining.rcm_events`

| Column | Type | Description |
|--------|------|-------------|
| `entity_id` | STRING | Unique patient journey ID |
| `patient_id` | BIGINT | Unique patient ID (patients can have multiple journeys) |
| `doctor_id` | BIGINT | Unique doctor ID |
| `hospital_id` | BIGINT | Unique hospital ID |
| `insurance_id` | BIGINT | Unique insurance ID |
| `activity_id` | BIGINT | Unique activity ID |
| `activity` | STRING | Human-readable activity name |
| `activity_code` | STRING | Uppercase activity code (e.g., "PATIENT_CHECK_IN") |
| `timestamp` | TIMESTAMP | Event timestamp |
| `activity_order` | INT | Sequence number in journey |
| `duration_minutes` | INT | Time spent in this step |
| `cost_dollars` | DECIMAL | Associated cost |
| `outcome` | STRING | Activity outcome (SUCCESS/DENIED/etc) |
| `department` | STRING | Responsible department |

### RCM Process Phases

The dataset covers 50+ activities across 6 phases:

1. **Intake** (5 activities): Patient registration, demographics, insurance capture
2. **Pre-Service** (8 activities): Scheduling, verification, authorization
3. **Service** (12 activities): Check-in, clinical encounter, procedures, discharge
4. **Coding & Billing** (10 activities): Charge capture, coding, claim submission
5. **AR Management** (10 activities): Adjudication, denials, appeals, follow-up
6. **Payment** (7 activities): Statements, payments, collections, closure

## Setup Instructions

### 1. Generate Synthetic Data

First, generate the synthetic RCM journey data:

```bash
# Run the data generation script in a Databricks notebook or job
python generate_rcm_data.py
```

This will create 1 million patient journeys with realistic RCM workflows and store them in a Delta table at `rcm_demo.process_mining.rcm_events`.

### 2. Create Secret Scope

Create a Databricks secret scope to store credentials:

```bash
# Using Databricks CLI
databricks secrets create-scope rcm-demo-secrets

# Add secrets
databricks secrets put-secret rcm-demo-secrets databricks-host
databricks secrets put-secret rcm-demo-secrets databricks-http-path
databricks secrets put-secret rcm-demo-secrets databricks-token
```

Required secrets:
- `databricks-host`: Your Databricks workspace URL (e.g., `https://your-workspace.cloud.databricks.com`)
- `databricks-http-path`: SQL warehouse HTTP path (e.g., `/sql/1.0/warehouses/abc123`)
- `databricks-token`: Personal access token or service principal token

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Local Development

For local testing:

```bash
# Set environment variables
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/abc123"
export DATABRICKS_TOKEN="your-token"

# Run the app
python app.py
```

Access the app at `http://localhost:8080`

### 5. Deploy to Databricks Apps

Deploy using Databricks CLI or UI:

```bash
# Using Databricks CLI
databricks apps deploy --config app.yaml

# Or use the Databricks UI:
# 1. Navigate to "Apps" in your workspace
# 2. Click "Create App"
# 3. Upload your project files
# 4. Configure secrets and permissions
# 5. Deploy
```

## Features

### Process Mining Graph

- **Nodes**: Represent RCM activities
  - Color-coded by success rate (green = high, blue = medium, red = low)
  - Size indicates activity volume
  - Click to view detailed statistics

- **Edges**: Represent transitions between activities
  - Thickness indicates transition volume
  - Green solid lines = "happy path" (most common)
  - Red dashed lines = bottlenecks (slow transitions)
  - Hover to view cycle time metrics

### Filters

- **Granularity Slider**: Adjust detail level (1-5)
  - Level 1: High-level (top 20% of activities)
  - Level 2: Average (top 40%)
  - Level 3: Detailed (top 60%)
  - Level 4: Very detailed (top 80%)
  - Level 5: Complete (all activities)

- **Date Range**: Filter by event timestamp
- **Department**: Filter by responsible department
- **Outcome**: Filter by journey outcome

### Statistics Panel

Real-time metrics:
- Total journeys analyzed
- Average cycle time (days)
- Success rate (%)
- Average cost per journey

### Glossary Page

Comprehensive definitions for all 50+ RCM activities including:
- Activity name and code
- Detailed description
- Responsible department
- Typical duration

## Technology Stack

- **Frontend**: Dash (Plotly), Dash Cytoscape
- **Backend**: Python 3.11
- **Data Storage**: Databricks Delta Lake
- **Deployment**: Databricks Apps
- **Styling**: Milligram CSS + Databricks branding
- **Data Processing**: Pandas, NumPy
- **Authentication**: Databricks Secret Scope

## Performance Considerations

- Data is queried on-demand with filters applied server-side
- Graph rendering is optimized for up to ~100 nodes
- Use granularity slider to reduce complexity for large datasets
- Statistics are calculated in-memory after data loading

## Customization

### Adding New Activities

1. Update `generate_rcm_data.py` with new activities in `RCM_ACTIVITIES`
2. Add definitions to `src/glossary.py` in `ACTIVITY_GLOSSARY`
3. Regenerate data

### Modifying Visualizations

- Edit `src/visualization.py` to change graph styling
- Update `assets/custom.css` for UI styling
- Modify `src/process_mining.py` for analytics logic

### Changing Color Scheme

Update CSS variables in `assets/custom.css`:

```css
:root {
    --databricks-coral: #FF3621;
    --databricks-dark: #1B1B1D;
    /* ... other colors ... */
}
```

## Troubleshooting

### Connection Issues

- Verify secret scope credentials are correct
- Check SQL warehouse is running
- Ensure network connectivity to Databricks

### Performance Issues

- Reduce granularity level
- Apply more restrictive filters
- Consider sampling data for very large datasets

### Graph Not Rendering

- Check browser console for errors
- Verify Cytoscape layout is loading
- Ensure data is being returned from queries

## License

Copyright © 2026 Your Organization. All rights reserved.

## Support

For issues or questions, contact your Databricks administrator or the development team.
