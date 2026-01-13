"""
Process Mining Engine

Analyzes RCM event data to discover process flows, calculate statistics,
and identify optimal paths and bottlenecks.
"""

from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from collections import defaultdict, Counter


class ProcessMiningEngine:
    """Discovers and analyzes process flows from event data."""

    def __init__(self):
        """Initialize the process mining engine."""
        self.happy_path = None
        self.bottlenecks = None

    def build_process_graph(
        self, df: pd.DataFrame, granularity_level: int = 2
    ) -> Dict:
        """
        Build process graph from event data.

        Args:
            df: DataFrame with RCM events
            granularity_level: Level of detail (1=high-level, 5=complete)

        Returns:
            Dictionary containing nodes, edges, and metadata
        """
        if df.empty:
            return {"nodes": [], "edges": [], "metadata": {}}

        # Calculate activity frequencies
        activity_counts = df.groupby("activity_code").size().reset_index(name="count")
        activity_counts = activity_counts.sort_values("count", ascending=False)

        # Determine which activities to include based on granularity
        num_activities = self._calculate_activities_to_show(
            len(activity_counts), granularity_level
        )
        top_activities = set(activity_counts.head(num_activities)["activity_code"])

        # Build nodes
        nodes = self._build_nodes(df, top_activities)

        # Build edges (transitions between activities)
        edges = self._build_edges(df, top_activities)

        # Identify happy path
        self.happy_path = self._identify_happy_path(edges)

        # Identify bottlenecks
        self.bottlenecks = self._identify_bottlenecks(edges)

        return {
            "nodes": nodes,
            "edges": edges,
            "happy_path": self.happy_path,
            "bottlenecks": self.bottlenecks,
            "metadata": {
                "total_activities": len(activity_counts),
                "shown_activities": len(nodes),
                "granularity_level": granularity_level,
            },
        }

    def _calculate_activities_to_show(
        self, total_activities: int, granularity_level: int
    ) -> int:
        """
        Calculate how many activities to show based on granularity level.

        Args:
            total_activities: Total number of unique activities
            granularity_level: User-selected granularity (1-5)

        Returns:
            Number of activities to display
        """
        # Map granularity level to percentage of activities
        granularity_map = {
            1: 0.20,  # High-level: top 20%
            2: 0.40,  # Average: top 40%
            3: 0.60,  # Detailed: top 60%
            4: 0.80,  # Very detailed: top 80%
            5: 1.00,  # Complete: all activities
        }

        percentage = granularity_map.get(granularity_level, 0.40)
        return max(5, int(total_activities * percentage))  # Show at least 5 activities

    def _build_nodes(self, df: pd.DataFrame, activities: set) -> List[Dict]:
        """
        Build node data for each activity.

        Args:
            df: DataFrame with RCM events
            activities: Set of activity codes to include

        Returns:
            List of node dictionaries
        """
        nodes = []

        # Filter to selected activities
        filtered_df = df[df["activity_code"].isin(activities)]

        # Group by activity
        for activity_code, group in filtered_df.groupby("activity_code"):
            node = {
                "id": activity_code,
                "label": group["activity"].iloc[0],
                "count": len(group),
                "unique_entities": group["entity_id"].nunique(),
                "avg_duration": group["duration_minutes"].mean(),
                "total_cost": group["cost_dollars"].sum(),
                "avg_cost": group["cost_dollars"].mean(),
                "department": group["department"].iloc[0],
                "success_rate": (group["outcome"] == "SUCCESS").mean() * 100,
            }
            nodes.append(node)

        return nodes

    def _build_edges(self, df: pd.DataFrame, activities: set) -> List[Dict]:
        """
        Build edge data for transitions between activities.

        Args:
            df: DataFrame with RCM events
            activities: Set of activity codes to include

        Returns:
            List of edge dictionaries
        """
        edges = []
        edge_stats = defaultdict(
            lambda: {
                "count": 0,
                "entities": set(),
                "durations": [],
                "repeat_entities": 0,
            }
        )

        # Sort by entity and activity order
        df_sorted = df.sort_values(["entity_id", "activity_order"])

        # Track entities that repeat transitions
        entity_transition_counts = defaultdict(Counter)

        # Find transitions
        for entity_id, entity_group in df_sorted.groupby("entity_id"):
            activities_list = entity_group["activity_code"].tolist()
            durations = entity_group["duration_minutes"].tolist()

            for i in range(len(activities_list) - 1):
                source = activities_list[i]
                target = activities_list[i + 1]

                # Only include if both activities are in our filtered set
                if source in activities and target in activities:
                    edge_key = (source, target)

                    # Track this transition
                    edge_stats[edge_key]["count"] += 1
                    edge_stats[edge_key]["entities"].add(entity_id)
                    edge_stats[edge_key]["durations"].append(durations[i + 1])

                    # Track repeat transitions
                    entity_transition_counts[entity_id][edge_key] += 1
                    if entity_transition_counts[entity_id][edge_key] > 1:
                        edge_stats[edge_key]["repeat_entities"] += 1

        # Convert to edge list
        for (source, target), stats in edge_stats.items():
            edge = {
                "source": source,
                "target": target,
                "count": stats["count"],
                "unique_entities": len(stats["entities"]),
                "repeat_entities": stats["repeat_entities"],
                "avg_cycle_time": np.mean(stats["durations"]),
                "median_cycle_time": np.median(stats["durations"]),
                "p95_cycle_time": np.percentile(stats["durations"], 95),
            }
            edges.append(edge)

        return edges

    def _identify_happy_path(self, edges: List[Dict]) -> List[Tuple[str, str]]:
        """
        Identify the most common "happy path" through the process.

        Args:
            edges: List of edge dictionaries

        Returns:
            List of (source, target) tuples representing the happy path
        """
        if not edges:
            return []

        # Sort edges by count (most common transitions)
        sorted_edges = sorted(edges, key=lambda x: x["count"], reverse=True)

        # Build happy path by following most common transitions
        happy_path = []
        used_sources = set()

        for edge in sorted_edges:
            source = edge["source"]
            target = edge["target"]

            # Add edge if source hasn't been used yet (avoid cycles)
            if source not in used_sources:
                happy_path.append((source, target))
                used_sources.add(source)

        return happy_path

    def _identify_bottlenecks(self, edges: List[Dict]) -> List[Tuple[str, str]]:
        """
        Identify bottlenecks based on cycle time.

        Args:
            edges: List of edge dictionaries

        Returns:
            List of (source, target) tuples representing bottlenecks
        """
        if not edges:
            return []

        # Calculate overall median cycle time
        all_cycle_times = [edge["avg_cycle_time"] for edge in edges]
        overall_median = np.median(all_cycle_times)

        # Identify edges with significantly higher cycle time (>2x median)
        bottlenecks = []
        for edge in edges:
            if edge["avg_cycle_time"] > 2 * overall_median:
                bottlenecks.append((edge["source"], edge["target"]))

        return bottlenecks

    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate overall process statistics.

        Args:
            df: DataFrame with RCM events

        Returns:
            Dictionary with statistics
        """
        if df.empty:
            return {
                "total_journeys": 0,
                "total_events": 0,
                "avg_cycle_time_days": 0,
                "success_rate": 0,
                "avg_cost": 0,
                "total_cost": 0,
            }

        # Calculate journey-level statistics
        journey_stats = (
            df.groupby("entity_id")
            .agg(
                {
                    "timestamp": ["min", "max"],
                    "cost_dollars": "sum",
                    "outcome": "last",
                }
            )
            .reset_index()
        )

        journey_stats.columns = [
            "entity_id",
            "start_time",
            "end_time",
            "total_cost",
            "outcome",
        ]

        # Calculate cycle time in days
        journey_stats["cycle_time_days"] = (
            journey_stats["end_time"] - journey_stats["start_time"]
        ).dt.total_seconds() / (24 * 3600)

        # Calculate success rate (successful outcomes)
        success_outcomes = [
            "SUCCESS",
            "SUCCESS_FULL_PAYMENT",
            "SUCCESS_PARTIAL_PAYMENT",
            "APPROVED",
        ]
        journey_stats["is_success"] = journey_stats["outcome"].isin(success_outcomes)

        return {
            "total_journeys": len(journey_stats),
            "total_events": len(df),
            "avg_cycle_time_days": journey_stats["cycle_time_days"].mean(),
            "median_cycle_time_days": journey_stats["cycle_time_days"].median(),
            "success_rate": journey_stats["is_success"].mean() * 100,
            "avg_cost": journey_stats["total_cost"].mean(),
            "total_cost": journey_stats["total_cost"].sum(),
        }

    def get_path_analysis(
        self, df: pd.DataFrame, source: str, target: str
    ) -> Dict:
        """
        Analyze a specific path between two activities.

        Args:
            df: DataFrame with RCM events
            source: Source activity code
            target: Target activity code

        Returns:
            Dictionary with path analysis
        """
        # Find all journeys that have this transition
        df_sorted = df.sort_values(["entity_id", "activity_order"])

        matching_journeys = []

        for entity_id, entity_group in df_sorted.groupby("entity_id"):
            activities = entity_group["activity_code"].tolist()

            # Check if this journey has the source -> target transition
            for i in range(len(activities) - 1):
                if activities[i] == source and activities[i + 1] == target:
                    matching_journeys.append(entity_id)
                    break

        # Get statistics for matching journeys
        matching_df = df[df["entity_id"].isin(matching_journeys)]

        return {
            "matching_journeys": len(matching_journeys),
            "total_journeys": df["entity_id"].nunique(),
            "percentage": len(matching_journeys) / df["entity_id"].nunique() * 100,
            "avg_cost": matching_df.groupby("entity_id")["cost_dollars"].sum().mean(),
        }
