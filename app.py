"""
RCM Process Mining Demo - Dash Application

A Databricks App for visualizing healthcare revenue cycle management process flows.
"""

from dash import Dash, html, dcc, callback, Input, Output, State
import dash_cytoscape as cyto
from databricks.sdk import WorkspaceClient

# Import custom modules
from src.data_loader import RCMDataLoader
from src.process_mining import ProcessMiningEngine
from src.visualization import GraphBuilder
from src.glossary import ACTIVITY_GLOSSARY
from config import config

# Validate configuration
try:
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please set required environment variables. See .env.example for details.")

# Initialize Databricks workspace client
w = WorkspaceClient()

# Initialize Dash app
app = Dash(
    __name__,
    title="RCM Process Mining Demo",
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

# Server for Databricks Apps deployment
server = app.server

# Load Cytoscape extra layouts
cyto.load_extra_layouts()

# Initialize data loader and process mining engine
data_loader = RCMDataLoader(
    catalog=config.CATALOG_NAME,
    schema=config.SCHEMA_NAME,
    table=config.TABLE_NAME,
)
process_engine = ProcessMiningEngine()
graph_builder = GraphBuilder()


def create_header() -> html.Div:
    """Create the application header."""
    return html.Div(
        [
            html.H1("RCM Process Mining Demo", className="header-title"),
            html.P(
                "Visualize and analyze healthcare revenue cycle management workflows",
                className="header-subtitle",
            ),
        ],
        className="header",
    )


def create_instructions() -> html.Div:
    """Create instructions section."""
    return html.Div(
        [
            html.H3("How to Use This Demo"),
            html.Ul(
                [
                    html.Li(
                        "Use the granularity slider to adjust the level of detail in the process flow"
                    ),
                    html.Li(
                        "Filter by date range, department, or outcome to focus on specific scenarios"
                    ),
                    html.Li(
                        "Click on nodes to see activity details and statistics"
                    ),
                    html.Li(
                        "Hover over edges to view transition metrics (volume, cycle time)"
                    ),
                    html.Li(
                        "Green paths indicate optimal 'happy path' flows, red indicates bottlenecks"
                    ),
                ]
            ),
        ],
        className="instructions",
    )


def create_filters() -> html.Div:
    """Create filter controls."""
    return html.Div(
        [
            html.H3("Filters"),
            html.Div(
                [
                    html.Label("Granularity Level"),
                    dcc.Slider(
                        id="granularity-slider",
                        min=1,
                        max=5,
                        step=1,
                        value=2,
                        marks={
                            1: "High-Level",
                            2: "Average",
                            3: "Detailed",
                            4: "Very Detailed",
                            5: "Complete",
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                ],
                className="filter-group",
            ),
            html.Div(
                [
                    html.Label("Date Range"),
                    dcc.DatePickerRange(
                        id="date-range-picker",
                        start_date=config.DEFAULT_START_DATE,
                        end_date=config.DEFAULT_END_DATE,
                        display_format="YYYY-MM-DD",
                    ),
                ],
                className="filter-group",
            ),
            html.Div(
                [
                    html.Label("Department"),
                    dcc.Dropdown(
                        id="department-filter",
                        options=[
                            {"label": "All Departments", "value": "ALL"},
                            {"label": "Registration", "value": "Registration"},
                            {"label": "Clinical", "value": "Clinical"},
                            {"label": "Billing", "value": "Billing"},
                            {"label": "AR", "value": "AR"},
                            {"label": "Financial", "value": "Financial"},
                        ],
                        value="ALL",
                        clearable=False,
                    ),
                ],
                className="filter-group",
            ),
            html.Div(
                [
                    html.Label("Outcome Filter"),
                    dcc.Dropdown(
                        id="outcome-filter",
                        options=[
                            {"label": "All Outcomes", "value": "ALL"},
                            {
                                "label": "Success - Full Payment",
                                "value": "SUCCESS_FULL_PAYMENT",
                            },
                            {
                                "label": "Success - Partial Payment",
                                "value": "SUCCESS_PARTIAL_PAYMENT",
                            },
                            {"label": "Denial Resolved", "value": "DENIAL_RESOLVED"},
                            {
                                "label": "Denial Unresolved",
                                "value": "DENIAL_UNRESOLVED",
                            },
                            {"label": "Collections", "value": "COLLECTIONS"},
                        ],
                        value="ALL",
                        clearable=False,
                    ),
                ],
                className="filter-group",
            ),
            html.Div(
                [
                    html.Button(
                        "Apply Filters",
                        id="apply-filters-btn",
                        n_clicks=0,
                        className="button-primary",
                    ),
                ],
                className="filter-group",
            ),
        ],
        className="filters-panel",
    )


def create_graph_container() -> html.Div:
    """Create the main graph visualization container."""
    return html.Div(
        [
            html.H3("Process Flow Visualization"),
            html.Div(
                [
                    dcc.Loading(
                        id="loading-graph",
                        type="default",
                        children=[
                            cyto.Cytoscape(
                                id="process-graph",
                                layout={"name": "dagre", "rankDir": "LR"},
                                style={"width": "100%", "height": "800px"},
                                elements=[],
                                stylesheet=[],
                                responsive=True,
                            )
                        ],
                    )
                ],
                className="graph-container",
            ),
            html.Div(id="node-details", className="node-details"),
        ],
        className="visualization-section",
    )


def create_statistics_panel() -> html.Div:
    """Create statistics panel."""
    return html.Div(
        [
            html.H3("Process Statistics"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("Total Journeys"),
                            html.P(id="stat-total-journeys", children="0"),
                        ],
                        className="stat-card",
                    ),
                    html.Div(
                        [
                            html.H4("Avg Cycle Time"),
                            html.P(id="stat-avg-cycle-time", children="0 days"),
                        ],
                        className="stat-card",
                    ),
                    html.Div(
                        [
                            html.H4("Success Rate"),
                            html.P(id="stat-success-rate", children="0%"),
                        ],
                        className="stat-card",
                    ),
                    html.Div(
                        [
                            html.H4("Avg Cost"),
                            html.P(id="stat-avg-cost", children="$0"),
                        ],
                        className="stat-card",
                    ),
                ],
                className="stats-grid",
            ),
        ],
        className="statistics-panel",
    )


def create_main_page() -> html.Div:
    """Create the main visualization page layout."""
    return html.Div(
        [
            create_header(),
            html.Div(
                [
                    html.Div(
                        [create_instructions(), create_filters()],
                        className="sidebar",
                    ),
                    html.Div(
                        [create_statistics_panel(), create_graph_container()],
                        className="main-content",
                    ),
                ],
                className="app-container",
            ),
        ]
    )


def create_glossary_page() -> html.Div:
    """Create the glossary page layout."""
    glossary_items = []

    for phase, activities in ACTIVITY_GLOSSARY.items():
        glossary_items.append(html.H3(phase.replace("_", " ").title()))

        for activity in activities:
            glossary_items.append(
                html.Div(
                    [
                        html.H4(activity["name"]),
                        html.P(activity["description"], className="activity-description"),
                        html.Div(
                            [
                                html.Span(
                                    f"Department: {activity['department']}",
                                    className="activity-meta",
                                ),
                                html.Span(
                                    f"Typical Duration: {activity['typical_duration']}",
                                    className="activity-meta",
                                ),
                            ],
                            className="activity-meta-container",
                        ),
                    ],
                    className="glossary-item",
                )
            )

    return html.Div(
        [
            create_header(),
            html.Div(
                [
                    html.H2("Activity Glossary"),
                    html.P(
                        "Comprehensive definitions of all RCM process activities",
                        className="glossary-intro",
                    ),
                    html.Div(glossary_items, className="glossary-content"),
                ],
                className="glossary-page",
            ),
        ]
    )


# App layout with navigation
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dcc.Link("Process Mining", href="/", className="nav-link"),
                dcc.Link("Glossary", href="/glossary", className="nav-link"),
            ],
            className="navigation",
        ),
        html.Div(id="page-content"),
    ]
)


# Navigation callback
@callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    """Route to appropriate page based on URL."""
    if pathname == "/glossary":
        return create_glossary_page()
    else:
        return create_main_page()


# Main graph update callback
@callback(
    [
        Output("process-graph", "elements"),
        Output("process-graph", "stylesheet"),
        Output("stat-total-journeys", "children"),
        Output("stat-avg-cycle-time", "children"),
        Output("stat-success-rate", "children"),
        Output("stat-avg-cost", "children"),
    ],
    [Input("apply-filters-btn", "n_clicks")],
    [
        State("granularity-slider", "value"),
        State("date-range-picker", "start_date"),
        State("date-range-picker", "end_date"),
        State("department-filter", "value"),
        State("outcome-filter", "value"),
    ],
)
def update_graph(n_clicks, granularity, start_date, end_date, department, outcome):
    """Update the process graph based on filters."""
    # Load data with filters
    df = data_loader.load_data(
        start_date=start_date,
        end_date=end_date,
        department=department if department != "ALL" else None,
        outcome=outcome if outcome != "ALL" else None,
    )

    # Build process mining graph
    graph_data = process_engine.build_process_graph(df, granularity_level=granularity)

    # Generate Cytoscape elements and stylesheet
    elements = graph_builder.create_cytoscape_elements(graph_data)
    stylesheet = graph_builder.create_cytoscape_stylesheet(graph_data)

    # Calculate statistics
    stats = process_engine.calculate_statistics(df)

    return (
        elements,
        stylesheet,
        f"{stats['total_journeys']:,}",
        f"{stats['avg_cycle_time_days']:.1f} days",
        f"{stats['success_rate']:.1f}%",
        f"${stats['avg_cost']:,.2f}",
    )


# Node click callback
@callback(
    Output("node-details", "children"),
    Input("process-graph", "tapNodeData"),
)
def display_node_details(node_data):
    """Display details when a node is clicked."""
    if not node_data:
        return html.Div("Click on a node to see details", className="node-details-empty")

    return html.Div(
        [
            html.H4(node_data.get("label", "Unknown")),
            html.P(f"Activity Code: {node_data.get('id', 'N/A')}"),
            html.P(f"Total Visits: {node_data.get('count', 0):,}"),
            html.P(f"Unique Entities: {node_data.get('unique_entities', 0):,}"),
            html.P(f"Avg Duration: {node_data.get('avg_duration', 0):.1f} minutes"),
            html.P(f"Department: {node_data.get('department', 'N/A')}"),
        ],
        className="node-details-content",
    )


if __name__ == "__main__":
    # For local development
    app.run_server(
        debug=config.APP_DEBUG,
        host=config.APP_HOST,
        port=config.APP_PORT,
    )
