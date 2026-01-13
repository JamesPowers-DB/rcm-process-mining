"""
Visualization Module

Builds Cytoscape graph elements and stylesheets for process mining visualization.
"""

from typing import Dict, List
import numpy as np


class GraphBuilder:
    """Builds Cytoscape graph elements and styles."""

    def __init__(self):
        """Initialize the graph builder."""
        # Databricks color palette
        self.colors = {
            "coral": "#FF3621",
            "dark": "#1B1B1D",
            "gray": "#333333",
            "light_gray": "#F5F5F5",
            "green_dark": "#095A35",
            "green_medium": "#00A972",
            "green_light": "#70C4AB",
            "lava_dark": "#801C17",
            "lava_medium": "#FF3621",
            "lava_light": "#FF9E94",
            "blue_dark": "#04355D",
            "blue_medium": "#2272B4",
            "blue_light": "#8ACAFF",
        }

    def create_cytoscape_elements(self, graph_data: Dict) -> List[Dict]:
        """
        Create Cytoscape elements from graph data.

        Args:
            graph_data: Dictionary with nodes, edges, and metadata

        Returns:
            List of Cytoscape element dictionaries
        """
        elements = []

        # Add nodes
        for node in graph_data.get("nodes", []):
            elements.append(
                {
                    "data": {
                        "id": node["id"],
                        "label": node["label"],
                        "count": node["count"],
                        "unique_entities": node["unique_entities"],
                        "avg_duration": node["avg_duration"],
                        "total_cost": node["total_cost"],
                        "avg_cost": node["avg_cost"],
                        "department": node["department"],
                        "success_rate": node["success_rate"],
                    },
                    "classes": self._get_node_class(node),
                }
            )

        # Add edges
        happy_path = set(graph_data.get("happy_path", []))
        bottlenecks = set(graph_data.get("bottlenecks", []))

        for edge in graph_data.get("edges", []):
            edge_key = (edge["source"], edge["target"])
            is_happy_path = edge_key in happy_path
            is_bottleneck = edge_key in bottlenecks

            elements.append(
                {
                    "data": {
                        "id": f"{edge['source']}-{edge['target']}",
                        "source": edge["source"],
                        "target": edge["target"],
                        "count": edge["count"],
                        "unique_entities": edge["unique_entities"],
                        "repeat_entities": edge["repeat_entities"],
                        "avg_cycle_time": edge["avg_cycle_time"],
                        "median_cycle_time": edge["median_cycle_time"],
                        "p95_cycle_time": edge["p95_cycle_time"],
                        "label": f"{edge['count']:,}",
                    },
                    "classes": self._get_edge_class(
                        edge, is_happy_path, is_bottleneck
                    ),
                }
            )

        return elements

    def _get_node_class(self, node: Dict) -> str:
        """
        Determine CSS class for a node based on its properties.

        Args:
            node: Node dictionary

        Returns:
            CSS class name
        """
        # Classify by success rate
        if node["success_rate"] >= 90:
            return "node-high-success"
        elif node["success_rate"] >= 70:
            return "node-medium-success"
        else:
            return "node-low-success"

    def _get_edge_class(
        self, edge: Dict, is_happy_path: bool, is_bottleneck: bool
    ) -> str:
        """
        Determine CSS class for an edge based on its properties.

        Args:
            edge: Edge dictionary
            is_happy_path: Whether edge is part of happy path
            is_bottleneck: Whether edge is a bottleneck

        Returns:
            CSS class name
        """
        if is_happy_path:
            return "edge-happy-path"
        elif is_bottleneck:
            return "edge-bottleneck"
        else:
            return "edge-normal"

    def create_cytoscape_stylesheet(self, graph_data: Dict) -> List[Dict]:
        """
        Create Cytoscape stylesheet.

        Args:
            graph_data: Dictionary with nodes, edges, and metadata

        Returns:
            List of style dictionaries
        """
        # Calculate edge width scaling
        edges = graph_data.get("edges", [])
        if edges:
            max_count = max(edge["count"] for edge in edges)
            min_count = min(edge["count"] for edge in edges)
        else:
            max_count = 1
            min_count = 1

        stylesheet = [
            # Default node style
            {
                "selector": "node",
                "style": {
                    "content": "data(label)",
                    "text-valign": "center",
                    "text-halign": "center",
                    "background-color": self.colors["blue_medium"],
                    "color": "#FFFFFF",
                    "font-size": "12px",
                    "width": "80px",
                    "height": "80px",
                    "text-wrap": "wrap",
                    "text-max-width": "70px",
                    "border-width": "2px",
                    "border-color": self.colors["blue_dark"],
                },
            },
            # High success nodes (green)
            {
                "selector": ".node-high-success",
                "style": {
                    "background-color": self.colors["green_medium"],
                    "border-color": self.colors["green_dark"],
                },
            },
            # Medium success nodes (blue)
            {
                "selector": ".node-medium-success",
                "style": {
                    "background-color": self.colors["blue_medium"],
                    "border-color": self.colors["blue_dark"],
                },
            },
            # Low success nodes (coral/red)
            {
                "selector": ".node-low-success",
                "style": {
                    "background-color": self.colors["lava_medium"],
                    "border-color": self.colors["lava_dark"],
                },
            },
            # Default edge style
            {
                "selector": "edge",
                "style": {
                    "width": "mapData(count, {}, {}, 2, 10)".format(
                        min_count, max_count
                    ),
                    "line-color": self.colors["gray"],
                    "target-arrow-color": self.colors["gray"],
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                    "arrow-scale": 1.5,
                    "opacity": 0.7,
                },
            },
            # Happy path edges (green, thicker)
            {
                "selector": ".edge-happy-path",
                "style": {
                    "line-color": self.colors["green_medium"],
                    "target-arrow-color": self.colors["green_medium"],
                    "width": "mapData(count, {}, {}, 4, 12)".format(
                        min_count, max_count
                    ),
                    "opacity": 0.9,
                    "z-index": 100,
                },
            },
            # Bottleneck edges (red, highlighted)
            {
                "selector": ".edge-bottleneck",
                "style": {
                    "line-color": self.colors["lava_medium"],
                    "target-arrow-color": self.colors["lava_medium"],
                    "width": "mapData(count, {}, {}, 3, 10)".format(
                        min_count, max_count
                    ),
                    "opacity": 0.9,
                    "line-style": "dashed",
                    "z-index": 99,
                },
            },
            # Normal edges
            {
                "selector": ".edge-normal",
                "style": {
                    "line-color": self.colors["gray"],
                    "target-arrow-color": self.colors["gray"],
                    "opacity": 0.6,
                },
            },
            # Selected/hover states
            {
                "selector": "node:selected",
                "style": {
                    "border-width": "4px",
                    "border-color": self.colors["coral"],
                    "z-index": 999,
                },
            },
            {
                "selector": "edge:selected",
                "style": {
                    "line-color": self.colors["coral"],
                    "target-arrow-color": self.colors["coral"],
                    "width": "mapData(count, {}, {}, 5, 15)".format(
                        min_count, max_count
                    ),
                    "opacity": 1.0,
                    "z-index": 999,
                },
            },
            # Edge labels
            {
                "selector": "edge[label]",
                "style": {
                    "label": "data(label)",
                    "font-size": "10px",
                    "text-background-color": "#FFFFFF",
                    "text-background-opacity": 0.8,
                    "text-background-padding": "3px",
                    "color": self.colors["dark"],
                },
            },
        ]

        return stylesheet

    def create_legend_elements(self) -> List[Dict]:
        """
        Create legend elements explaining the visualization.

        Returns:
            List of HTML div elements for the legend
        """
        from dash import html

        return html.Div(
            [
                html.H4("Legend"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "width": "20px",
                                        "height": "20px",
                                        "background-color": self.colors["green_medium"],
                                        "border-radius": "50%",
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    }
                                ),
                                html.Span("High Success Rate (≥90%)"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "width": "20px",
                                        "height": "20px",
                                        "background-color": self.colors["blue_medium"],
                                        "border-radius": "50%",
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    }
                                ),
                                html.Span("Medium Success Rate (70-90%)"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "width": "20px",
                                        "height": "20px",
                                        "background-color": self.colors["lava_medium"],
                                        "border-radius": "50%",
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    }
                                ),
                                html.Span("Low Success Rate (<70%)"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "width": "40px",
                                        "height": "4px",
                                        "background-color": self.colors["green_medium"],
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                    }
                                ),
                                html.Span("Happy Path (Most Common)"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    style={
                                        "width": "40px",
                                        "height": "4px",
                                        "background-color": self.colors["lava_medium"],
                                        "display": "inline-block",
                                        "margin-right": "10px",
                                        "border-top": f"4px dashed {self.colors['lava_medium']}",
                                    }
                                ),
                                html.Span("Bottleneck (Slow)"),
                            ],
                            style={"margin-bottom": "10px"},
                        ),
                        html.Div(
                            [
                                html.Span(
                                    "Edge thickness represents volume",
                                    style={"font-style": "italic"},
                                )
                            ],
                            style={"margin-top": "15px"},
                        ),
                    ]
                ),
            ],
            className="legend",
            style={
                "padding": "15px",
                "background-color": self.colors["light_gray"],
                "border-radius": "5px",
                "margin-top": "20px",
            },
        )
