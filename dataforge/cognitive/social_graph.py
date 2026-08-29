"""
DataForge Watts-Strogatz Small-World Neighborhood Social Network Engine.
Simulates micro-demographic peer influence, rumor cascades, and local community opinion formation.
"""
from __future__ import annotations

import random
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class NetworkNode:
    node_id: int
    citizen_name: str
    occupation: str
    influence_weight: float
    neighbors: list[int]
    current_opinion: str


class NeighborhoodSocialGraph:
    """
    Watts-Strogatz Small-World Graph generator for district & neighborhood peer networks.
    """

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def build_neighborhood_graph(
        self,
        citizens: list[dict[str, Any]],
        k_neighbors: int = 4,
        rewire_prob: float = 0.15
    ) -> dict[int, NetworkNode]:
        """
        Constructs a small-world network from a pool of synthetic citizens.
        """
        n = len(citizens)
        if n < k_neighbors + 1:
            k_neighbors = max(1, n - 1)

        nodes: dict[int, NetworkNode] = {}

        # 1. Calculate local opinion leaders (muhtar, doctor, teacher, shopkeeper have higher weight)
        for i, c in enumerate(citizens):
            occ_l = c.get("meslek", c.get("occupation", "")).lower()
            if any(w in occ_l for w in ["muhtar", "doktor", "hekim"]):
                influence = 2.5
            elif any(w in occ_l for w in ["öğretmen", "komiser", "esnaf"]):
                influence = 1.8
            else:
                influence = 1.0

            nodes[i] = NetworkNode(
                node_id=i,
                citizen_name=c.get("ad_soyad", f"Yurttaş #{i+1}"),
                occupation=c.get("meslek", c.get("occupation", "Vatandaş")),
                influence_weight=influence,
                neighbors=[],
                current_opinion=c.get("karar", "Kararsız")
            )

        # 2. Ring Lattice Initialization
        for i in range(n):
            for j in range(1, k_neighbors // 2 + 1):
                left = (i - j) % n
                right = (i + j) % n
                if left not in nodes[i].neighbors:
                    nodes[i].neighbors.append(left)
                if right not in nodes[i].neighbors:
                    nodes[i].neighbors.append(right)

        # 3. Small-World Rewiring
        for i in range(n):
            for idx, neighbor in enumerate(list(nodes[i].neighbors)):
                if self.rng.random() < rewire_prob:
                    new_target = self.rng.randint(0, n - 1)
                    if new_target != i and new_target not in nodes[i].neighbors:
                        nodes[i].neighbors[idx] = new_target

        return nodes

    def propagate_opinion_cascade(
        self,
        graph: dict[int, NetworkNode],
        iterations: int = 3
    ) -> dict[str, Any]:
        """
        Simulates iterative peer pressure and opinion cascades across the neighborhood.
        """
        for _ in range(iterations):
            for i, node in graph.items():
                if not node.neighbors:
                    continue

                neighbor_kabul = sum(graph[nb].influence_weight for nb in node.neighbors if "Kabul" in graph[nb].current_opinion)
                neighbor_ret = sum(graph[nb].influence_weight for nb in node.neighbors if "Red" in graph[nb].current_opinion)
                total_inf = max(0.1, neighbor_kabul + neighbor_ret)

                # If peer consensus exceeds 65%, neutral nodes flip
                if (neighbor_ret / total_inf) > 0.65 and self.rng.random() < 0.40:
                    node.current_opinion = "Kesinlikle Reddeder"
                elif (neighbor_kabul / total_inf) > 0.65 and self.rng.random() < 0.40:
                    node.current_opinion = "Kabul Eder / Destekler"

        kabul_cnt = sum(1 for n in graph.values() if "Kabul" in n.current_opinion)
        ret_cnt = sum(1 for n in graph.values() if "Red" in n.current_opinion)
        total = len(graph)

        return {
            "toplam_dugum": total,
            "nihai_kabul_yuzde": round((kabul_cnt / max(1, total)) * 100, 1),
            "nihai_ret_yuzde": round((ret_cnt / max(1, total)) * 100, 1),
            "nihai_kararsiz_yuzde": round(((total - kabul_cnt - ret_cnt) / max(1, total)) * 100, 1)
        }
