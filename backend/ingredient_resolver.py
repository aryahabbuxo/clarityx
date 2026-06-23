from __future__ import annotations

import re
from dataclasses import dataclass


ALIASES = {
    "citric acid": {
        "aliases": ["citric acid", "e330"],
        "regulatory_identifiers": {"INS": "330", "E": "E330"},
    },
    "sodium benzoate": {
        "aliases": ["sodium benzoate", "e211", "sodium salt of benzoic acid"],
        "regulatory_identifiers": {"INS": "211", "E": "E211"},
    },
    "ascorbic acid": {
        "aliases": ["ascorbic acid", "vitamin c", "e300"],
        "regulatory_identifiers": {"INS": "300", "E": "E300"},
    },
    "turmeric": {
        "aliases": ["turmeric", "curcuma longa", "haldi"],
        "regulatory_identifiers": {"botanical": "Curcuma longa"},
    },
    "neem": {
        "aliases": ["neem", "azadirachta indica", "nimba"],
        "regulatory_identifiers": {"botanical": "Azadirachta indica"},
    },
    "aloe vera": {
        "aliases": ["aloe vera", "aloe barbadensis", "kumari"],
        "regulatory_identifiers": {"botanical": "Aloe barbadensis"},
    },
    "water": {
        "aliases": ["water", "aqua"],
        "regulatory_identifiers": {},
    },
    "sugar": {
        "aliases": ["sugar", "sucrose"],
        "regulatory_identifiers": {},
    },
    "salt": {
        "aliases": ["salt", "sodium chloride"],
        "regulatory_identifiers": {},
    },
}


@dataclass(frozen=True)
class CanonicalIngredient:
    canonical_name: str
    aliases: list[str]
    regulatory_identifiers: dict[str, str]
    source_matches: list[str]

    def to_dict(self) -> dict:
        return {
            "canonical_name": self.canonical_name,
            "aliases": self.aliases,
            "regulatory_identifiers": self.regulatory_identifiers,
            "source_matches": self.source_matches,
        }


def split_ingredients(ingredients_text: str) -> list[str]:
    parts = re.split(r"[,;()\[\]\n]+", ingredients_text or "")
    return [part.strip().lower() for part in parts if part.strip()]


def resolve_ingredient(name: str) -> CanonicalIngredient:
    normalized = re.sub(r"\s+", " ", (name or "").strip().lower())
    for canonical, meta in ALIASES.items():
        matches = [alias for alias in meta["aliases"] if alias == normalized]
        if matches:
            return CanonicalIngredient(
                canonical_name=canonical,
                aliases=list(meta["aliases"]),
                regulatory_identifiers=dict(meta["regulatory_identifiers"]),
                source_matches=matches,
            )
    return CanonicalIngredient(
        canonical_name=normalized,
        aliases=[normalized] if normalized else [],
        regulatory_identifiers={},
        source_matches=[normalized] if normalized else [],
    )


def resolve_ingredients(ingredients_text: str) -> list[CanonicalIngredient]:
    seen = set()
    resolved = []
    for ingredient in split_ingredients(ingredients_text):
        canonical = resolve_ingredient(ingredient)
        if canonical.canonical_name and canonical.canonical_name not in seen:
            seen.add(canonical.canonical_name)
            resolved.append(canonical)
    return resolved

