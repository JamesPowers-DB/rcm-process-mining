# RCM Process Mining Demo - File Index

Quick reference guide to all project files and their purposes.

## 📖 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Main project documentation | All users |
| [QUICKSTART.md](QUICKSTART.md) | 15-minute setup guide | New users |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Databricks Apps deployment | DevOps/Admins |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete project overview | Stakeholders |
| [TESTING.md](TESTING.md) | Testing procedures | QA/Developers |
| [INDEX.md](INDEX.md) | This file | All users |

## 🚀 Application Files

| File | Purpose | Description |
|------|---------|-------------|
| [app.py](app.py) | Main application | Dash web app with routing and callbacks |
| [config.py](config.py) | Configuration | Centralized config and validation |
| [generate_rcm_data.py](generate_rcm_data.py) | Data generator | Creates 1M+ synthetic RCM journeys |

## 📦 Source Modules (`src/`)

| File | Purpose | Key Functions |
|------|---------|---------------|
| [src/__init__.py](src/__init__.py) | Package init | Version and metadata |
| [src/data_loader.py](src/data_loader.py) | Data loading | Delta table connection, filtering |
| [src/process_mining.py](src/process_mining.py) | Analytics | Process discovery, statistics |
| [src/visualization.py](src/visualization.py) | Graph building | Cytoscape elements and styling |
| [src/glossary.py](src/glossary.py) | Activity definitions | 50+ RCM activity descriptions |

## 🎨 Assets (`assets/`)

| File | Purpose | Description |
|------|---------|-------------|
| [assets/custom.css](assets/custom.css) | Styling | Milligram + Databricks branding |

## ⚙️ Configuration Files

| File | Purpose | Description |
|------|---------|-------------|
| [requirements.txt](requirements.txt) | Python dependencies | Pip installable packages |
| [setup.py](setup.py) | Package setup | Setuptools configuration |
| [app.yaml](app.yaml) | Databricks Apps config | Main deployment configuration |
| [.databricks-app.json](.databricks-app.json) | App metadata | JSON format app definition |
| [.env.example](.env.example) | Environment template | Example environment variables |

## 📓 Notebooks (`notebooks/`)

| File | Purpose | Description |
|------|---------|-------------|
| [notebooks/generate_data.py](notebooks/generate_data.py) | Data generation | Databricks notebook for data setup |

## 📋 Project Rules (`rules/`)

| File | Purpose | Description |
|------|---------|-------------|
| [rules/frontend_strategy.mdc](rules/frontend_strategy.mdc) | Frontend standards | Dash, CSS, branding guidelines |
| [rules/databricks_strategy.mdc](rules/databricks_strategy.mdc) | Databricks patterns | SDK usage, authentication |
| [rules/database_strategy.mdc](rules/database_strategy.mdc) | Database patterns | SQLAlchemy, migrations |
| [rules/style_strategy.mdc](rules/style_strategy.mdc) | Code style | Logging, formatting, naming |
| [rules/performance_strategy.mdc](rules/performance_strategy.mdc) | Performance | Optimization guidelines |
| [rules/documentation_strategy.mdc](rules/documentation_strategy.mdc) | Documentation | Doc standards |
| [rules/error_fix_strategy.mdc](rules/error_fix_strategy.mdc) | Error handling | Debugging approach |

## 🗂️ File Organization

```
rcm-process-mining/
├── 📖 Documentation (7 files)
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── DEPLOYMENT.md
│   ├── PROJECT_SUMMARY.md
│   ├── TESTING.md
│   └── INDEX.md
│
├── 🚀 Application (3 files)
│   ├── app.py
│   ├── config.py
│   └── generate_rcm_data.py
│
├── 📦 Source Modules (5 files)
│   └── src/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── process_mining.py
│       ├── visualization.py
│       └── glossary.py
│
├── 🎨 Assets (1 file)
│   └── assets/
│       └── custom.css
│
├── ⚙️ Configuration (6 files)
│   ├── requirements.txt
│   ├── setup.py
│   ├── app.yaml
│   ├── .databricks-app.json
│   └── .env.example
│
├── 📓 Notebooks (1 file)
│   └── notebooks/
│       └── generate_data.py
│
└── 📋 Rules (7 files)
    └── rules/
        ├── frontend_strategy.mdc
        ├── databricks_strategy.mdc
        ├── database_strategy.mdc
        ├── style_strategy.mdc
        ├── performance_strategy.mdc
        ├── documentation_strategy.mdc
        └── error_fix_strategy.mdc
```

## 📊 File Statistics

- **Total Files**: 30
- **Python Files**: 9
- **Documentation Files**: 7
- **Configuration Files**: 6
- **CSS Files**: 1
- **Strategy Files**: 7

## 🎯 Quick Navigation

### For First-Time Users
1. Start with [QUICKSTART.md](QUICKSTART.md)
2. Read [README.md](README.md) for details
3. Check [.env.example](.env.example) for configuration

### For Developers
1. Review [src/](src/) modules
2. Check [rules/](rules/) for coding standards
3. See [TESTING.md](TESTING.md) for testing

### For Deployment
1. Follow [DEPLOYMENT.md](DEPLOYMENT.md)
2. Configure [app.yaml](app.yaml)
3. Set up secrets per deployment guide

### For Data Generation
1. Run [generate_rcm_data.py](generate_rcm_data.py)
2. Or use [notebooks/generate_data.py](notebooks/generate_data.py)
3. Verify with SQL queries in TESTING.md

## 🔍 Finding Specific Content

### Authentication & Security
- Secret Scope setup: [DEPLOYMENT.md](DEPLOYMENT.md) Step 2
- Environment variables: [.env.example](.env.example)
- Configuration validation: [config.py](config.py)
- Databricks SDK usage: [src/data_loader.py](src/data_loader.py)

### Data & Analytics
- Data generation: [generate_rcm_data.py](generate_rcm_data.py)
- Process mining logic: [src/process_mining.py](src/process_mining.py)
- Activity definitions: [src/glossary.py](src/glossary.py)
- Data loading: [src/data_loader.py](src/data_loader.py)

### Visualization
- Graph building: [src/visualization.py](src/visualization.py)
- Styling: [assets/custom.css](assets/custom.css)
- Layout: [app.py](app.py) - layout functions
- Callbacks: [app.py](app.py) - callback functions

### Configuration
- App settings: [config.py](config.py)
- Dependencies: [requirements.txt](requirements.txt)
- Databricks config: [app.yaml](app.yaml)
- Package setup: [setup.py](setup.py)

## 📝 File Modification Guide

### When to Edit Each File

**app.py** - Modify when:
- Adding new pages or routes
- Changing layout structure
- Adding new callbacks
- Modifying UI components

**config.py** - Modify when:
- Adding new configuration options
- Changing default values
- Adding validation rules

**generate_rcm_data.py** - Modify when:
- Adding new RCM activities
- Changing journey logic
- Adjusting data volumes
- Modifying outcome distributions

**src/data_loader.py** - Modify when:
- Changing data source
- Adding new query filters
- Optimizing data loading
- Adding caching

**src/process_mining.py** - Modify when:
- Changing analytics algorithms
- Adding new metrics
- Modifying bottleneck detection
- Adjusting happy path logic

**src/visualization.py** - Modify when:
- Changing graph styling
- Adding new node/edge types
- Modifying color schemes
- Adding new layouts

**src/glossary.py** - Modify when:
- Adding new activities
- Updating descriptions
- Adding new metadata

**assets/custom.css** - Modify when:
- Changing visual design
- Updating branding
- Adding responsive breakpoints
- Modifying colors/fonts

## 🔗 External Dependencies

### Python Packages (requirements.txt)
- dash: Web framework
- dash-cytoscape: Graph visualization
- databricks-sdk: Databricks integration
- pandas: Data processing
- numpy: Numerical operations

### CSS Frameworks (assets/custom.css)
- Milligram: Base CSS framework (CDN)
- Custom styles: Databricks branding

### Databricks Resources
- Unity Catalog: Data governance
- Delta Lake: Data storage
- SQL Warehouse: Query engine
- Secret Scope: Credential management

## 📞 Support

For questions about specific files:
- **Documentation**: Check README.md first
- **Code**: Review inline comments
- **Configuration**: See .env.example
- **Deployment**: Follow DEPLOYMENT.md
- **Testing**: Consult TESTING.md

## ✅ Completeness Checklist

All required files present:
- ✅ Application files (3)
- ✅ Source modules (5)
- ✅ Configuration files (6)
- ✅ Documentation files (7)
- ✅ Assets (1)
- ✅ Notebooks (1)
- ✅ Rules (7)

**Total: 30 files - Complete!**
