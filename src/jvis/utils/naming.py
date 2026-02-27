"""Entity naming utilities — pluralization and case-variant replacement pairs."""

from __future__ import annotations


def pluralize(word: str) -> str:
    """Naive English pluralization for single-word entity names.

    Handles ~95% of common domain entities (product, category, address, etc.).
    Not a general-purpose pluralizer — designed for scaffold entity names only.
    """
    if not word:
        return word

    lower = word.lower()

    # Already plural (simple heuristic: ends in 's' but not 'ss')
    if lower.endswith("s") and not lower.endswith("ss"):
        return word

    # -s, -x, -z, -sh, -ch → +es
    if lower.endswith(("s", "x", "z", "sh", "ch")):
        return word + "es"

    # consonant + y → -y + ies
    if lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        return word[:-1] + "ies"

    return word + "s"


def entity_replacements(old: str, new: str) -> list[tuple[str, str]]:
    """Build ordered replacement pairs for entity rename.

    Returns pairs from longest/most-specific to shortest to avoid partial
    replacements (e.g., replacing "Item" before "Items" would break "Items").

    Order:
      1. ITEMS  → PRODUCTS   (UPPER plural)
      2. Items  → Products   (PascalCase plural)
      3. items  → products   (lowercase plural)
      4. ITEM   → PRODUCT    (UPPER singular)
      5. Item   → Product    (PascalCase singular)
      6. item   → product    (lowercase singular)
    """
    if old == new:
        return []

    old_lower = old.lower()
    new_lower = new.lower()

    old_pascal = old_lower.capitalize()
    new_pascal = new_lower.capitalize()

    old_upper = old_lower.upper()
    new_upper = new_lower.upper()

    old_plural = pluralize(old_lower)
    new_plural = pluralize(new_lower)

    old_pascal_plural = old_plural.capitalize()
    new_pascal_plural = new_plural.capitalize()

    old_upper_plural = old_plural.upper()
    new_upper_plural = new_plural.upper()

    return [
        (old_upper_plural, new_upper_plural),
        (old_pascal_plural, new_pascal_plural),
        (old_plural, new_plural),
        (old_upper, new_upper),
        (old_pascal, new_pascal),
        (old_lower, new_lower),
    ]
