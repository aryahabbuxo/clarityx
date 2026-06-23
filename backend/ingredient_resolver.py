from __future__ import annotations

import re
from dataclasses import dataclass


ALIASES = {
    # ── Additives / preservatives ──────────────────────────────────────────────
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

    # ── Heritage / Ayurvedic botanicals ───────────────────────────────────────
    "turmeric": {
        "aliases": [
            "turmeric",
            "curcuma longa",
            "haldi",
            "haridra",
            "curcuma longa root powder",
            "curcuma longa extract",
            "curcuma longa powder",
        ],
        "regulatory_identifiers": {"botanical": "Curcuma longa"},
    },
    "neem": {
        "aliases": [
            "neem",
            "azadirachta indica",
            "nimba",
            "neem leaf",
            "neem oil",
            "azadirachta indica leaf extract",
            "azadirachta indica leaf powder",
        ],
        "regulatory_identifiers": {"botanical": "Azadirachta indica"},
    },
    "aloe vera": {
        "aliases": [
            "aloe vera",
            "aloe barbadensis",
            "kumari",
            "aloe barbadensis miller",
            "aloe barbadensis leaf extract",
            "aloe barbadensis leaf juice",
            "aloe vera gel",
            "aloe vera extract",
            "aloe vera juice",
        ],
        "regulatory_identifiers": {"botanical": "Aloe barbadensis"},
    },
    "shikakai": {
        "aliases": [
            "shikakai",
            "shikakaï",
            "shikaki",
            "acacia concinna",
            "acacia concinna fruit powder",
            "acacia concinna pod extract",
            "acacia concinna extract",
            "acacia concinna fruit",
            "acacia concinna pods",
        ],
        "regulatory_identifiers": {"botanical": "Acacia concinna"},
    },
    "amla": {
        "aliases": [
            "amla",
            "amalaki",
            "emblica officinalis",
            "phyllanthus emblica",
            "indian gooseberry",
            "amla fruit powder",
            "emblica officinalis fruit powder",
            "emblica officinalis extract",
            "amla extract",
            "amla powder",
        ],
        "regulatory_identifiers": {"botanical": "Emblica officinalis"},
    },
    "ashwagandha": {
        "aliases": [
            "ashwagandha",
            "withania somnifera",
            "winter cherry",
            "indian ginseng",
            "ashwagandha root powder",
            "withania somnifera root extract",
            "withania somnifera extract",
            "ashwagandha extract",
            "ashwagandha powder",
        ],
        "regulatory_identifiers": {"botanical": "Withania somnifera"},
    },
    "tulsi": {
        "aliases": [
            "tulsi",
            "holy basil",
            "ocimum sanctum",
            "ocimum tenuiflorum",
            "tulasi",
            "tulsi leaf extract",
            "ocimum sanctum leaf extract",
            "ocimum sanctum extract",
            "tulsi extract",
            "tulsi powder",
        ],
        "regulatory_identifiers": {"botanical": "Ocimum sanctum"},
    },
    "bhringraj": {
        "aliases": [
            "bhringraj",
            "bhringaraj",
            "bhringraj oil",
            "eclipta alba",
            "false daisy",
            "eclipta prostrata",
            "eclipta alba leaf extract",
            "eclipta alba extract",
            "bhringraj extract",
            "bhringraj powder",
        ],
        "regulatory_identifiers": {"botanical": "Eclipta alba"},
    },
    "licorice": {
        "aliases": [
            "licorice",
            "liquorice",
            "glycyrrhiza glabra",
            "mulethi",
            "yashtimadhu",
            "licorice root",
            "licorice root extract",
            "glycyrrhiza glabra root extract",
            "glycyrrhiza glabra extract",
            "licorice extract",
        ],
        "regulatory_identifiers": {"botanical": "Glycyrrhiza glabra"},
    },
    "fenugreek": {
        "aliases": [
            "fenugreek",
            "trigonella foenum-graecum",
            "methi",
            "methika",
            "fenugreek seed powder",
            "fenugreek extract",
            "trigonella foenum-graecum seed extract",
            "trigonella foenum graecum",
            "fenugreek seed extract",
            "fenugreek powder",
        ],
        "regulatory_identifiers": {"botanical": "Trigonella foenum-graecum"},
    },
    "ginger": {
        "aliases": [
            "ginger",
            "zingiber officinale",
            "sunthi",
            "adrak",
            "ginger root",
            "ginger extract",
            "zingiber officinale root extract",
            "zingiber officinale extract",
            "ginger root extract",
            "ginger powder",
        ],
        "regulatory_identifiers": {"botanical": "Zingiber officinale"},
    },
    "brahmi": {
        "aliases": [
            "brahmi",
            "bacopa monnieri",
            "water hyssop",
            "bacopa monnieri extract",
            "bacopa extract",
            "brahmi extract",
            "brahmi powder",
        ],
        "regulatory_identifiers": {"botanical": "Bacopa monnieri"},
    },
    "hibiscus": {
        "aliases": [
            "hibiscus",
            "hibiscus rosa-sinensis",
            "hibiscus sabdariffa",
            "jaswand",
            "gudhal",
            "hibiscus flower extract",
            "hibiscus extract",
            "hibiscus powder",
        ],
        "regulatory_identifiers": {"botanical": "Hibiscus rosa-sinensis"},
    },
    "coconut oil": {
        "aliases": [
            "coconut oil",
            "cocos nucifera oil",
            "coconut",
            "cocos nucifera",
            "virgin coconut oil",
            "sodium cocoate",
            "hydrogenated coconut oil",
        ],
        "regulatory_identifiers": {"botanical": "Cocos nucifera"},
    },
    "sesame oil": {
        "aliases": [
            "sesame oil",
            "sesamum indicum oil",
            "sesame seed oil",
            "sesamum indicum",
            "til oil",
            "gingelly oil",
        ],
        "regulatory_identifiers": {"botanical": "Sesamum indicum"},
    },
    "castor oil": {
        "aliases": [
            "castor oil",
            "ricinus communis seed oil",
            "ricinus communis",
            "eranda oil",
        ],
        "regulatory_identifiers": {"botanical": "Ricinus communis"},
    },

    # ── Common base ingredients ───────────────────────────────────────────────
    "water": {
        "aliases": ["water", "aqua", "purified water", "deionized water"],
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
    "glycerin": {
        "aliases": ["glycerin", "glycerol", "glycerine", "vegetable glycerin", "vegetable glycerol"],
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
