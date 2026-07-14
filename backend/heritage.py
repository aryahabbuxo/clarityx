from __future__ import annotations

import re

from ingredient_resolver import ALIASES, CanonicalIngredient
from providers.ayush_provider import AyushProvider


HERITAGE_DISCLAIMER = "Heritage match is based on product name or ingredient keywords only, not efficacy or medical claims."


def _contains_keyword(text: str, keyword: str) -> bool:
    pattern = rf"(?<![a-z0-9]){re.escape(keyword.lower())}(?![a-z0-9])"
    return re.search(pattern, text) is not None


def heritage_matches(product_name: str, ingredients_text: str) -> list[dict]:
    haystack = f"{product_name or ''} {ingredients_text or ''}".lower()
    matches = []

    for canonical_name, record in AyushProvider.DATA.items():
        aliases = ALIASES.get(canonical_name, {}).get("aliases", [canonical_name])
        matched_keyword = next((alias for alias in aliases if _contains_keyword(haystack, alias)), None)
        if not matched_keyword:
            continue

        details = record.get("details", {})
        matches.append(
            {
                "ingredient": canonical_name,
                "matched_keyword": matched_keyword,
                "botanical_identity": details.get("botanical_identity"),
                "sanskrit_name": details.get("sanskrit_name"),
                "traditional_system": details.get("traditional_system", "Ayurveda"),
                "fun_fact": f"{canonical_name.title()} matched the {details.get('traditional_system', 'Ayurveda')} heritage reference.",
                "disclaimer": HERITAGE_DISCLAIMER,
            }
        )

    return matches


def heritage_ingredients_from_matches(matches: list[dict]) -> list[CanonicalIngredient]:
    ingredients = []
    for match in matches:
        canonical_name = match["ingredient"]
        meta = ALIASES.get(canonical_name, {})
        ingredients.append(
            CanonicalIngredient(
                canonical_name=canonical_name,
                aliases=list(meta.get("aliases", [canonical_name])),
                regulatory_identifiers=dict(meta.get("regulatory_identifiers", {})),
                source_matches=[match["matched_keyword"]],
            )
        )
    return ingredients
