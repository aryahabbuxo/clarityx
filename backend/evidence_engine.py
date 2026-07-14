from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from evidence_graph import EvidenceGraph
from ingredient_resolver import CanonicalIngredient
from providers import (
    AyushProvider,
    CdscoProvider,
    CodexProvider,
    EfsaProvider,
    FdaProvider,
    FssaiProvider,
    NinProvider,
    ReachProvider,
)


class EvidenceEngine:
    def __init__(self):
        self.providers = (
            EfsaProvider(),
            FdaProvider(),
            CodexProvider(),
            FssaiProvider(),
            ReachProvider(),
            CdscoProvider(),
            AyushProvider(),
            NinProvider(),
        )

    def build_graph(self, product_id: str, ingredients: list[CanonicalIngredient], traceability_evidence=None) -> EvidenceGraph:
        graph = EvidenceGraph(product_id=product_id)
        records = []
        if traceability_evidence:
            records.append(traceability_evidence)

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [
                executor.submit(provider.lookup, ingredient)
                for ingredient in ingredients
                for provider in self.providers
            ]
            for future in as_completed(futures):
                try:
                    records.append(future.result())
                except Exception as exc:
                    print(f"[EvidenceEngine] provider failure isolated: {exc}")

        graph.add_records(records)
        return graph

