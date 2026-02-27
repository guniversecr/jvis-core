"""Interactive stack selection with hierarchical drill-down menu."""

from __future__ import annotations

import logging
from collections import defaultdict

import click

from jvis.stacks.registry import StackInfo, discover_stacks, get_stacks_by_type
from jvis.utils import ui

logger = logging.getLogger(__name__)

# Category labels shown in the top-level menu
_CATEGORY_ORDER = ["backend", "frontend", "fullstack", "custom"]
_CATEGORY_LABELS = {
    "backend": "Backend (API / Server)",
    "frontend": "Frontend (Web App)",
    "fullstack": "Full-Stack (Frontend + Backend)",
    "custom": "Custom (Minimal)",
}


def select_stack(stack_type: str = "", label: str = "stack") -> StackInfo:
    """Prompt the user to select a stack via hierarchical drill-down.

    For ``stack_type=""`` (single project), shows category → language → framework.
    For a specific type (e.g. ``"backend"``), shows only stacks of that type.
    """
    if stack_type:
        stacks = get_stacks_by_type(stack_type)
        if not stacks:
            click.echo(f"  {ui.yellow('No stacks found')} for type '{stack_type}'.")
            click.echo("  Falling back to all stacks.")
            stacks = discover_stacks()
        return _select_framework(list(stacks.values()), label)

    # No type filter → hierarchical selection
    all_stacks = discover_stacks()
    if not all_stacks:
        raise click.ClickException("No stacks found.")

    # Group by type
    by_type: dict[str, list[StackInfo]] = defaultdict(list)
    for s in all_stacks.values():
        by_type[s.type].append(s)

    # 1. Select category
    available_cats = [c for c in _CATEGORY_ORDER if c in by_type]
    if not available_cats:
        return _select_framework(list(all_stacks.values()), label)

    category = _select_category(available_cats)
    candidates = by_type[category]

    # If only one stack in category, return it directly
    if len(candidates) == 1:
        selected = candidates[0]
        click.echo(f"  {ui.green('✓')} {label.capitalize()}: {selected.name}")
        return selected

    # 2. Group by language
    by_lang: dict[str, list[StackInfo]] = defaultdict(list)
    for s in candidates:
        lang_key = s.language or "other"
        by_lang[lang_key].append(s)

    # If only one language, skip language selection
    lang_stacks = list(by_lang.values())[0] if len(by_lang) == 1 else _select_by_language(by_lang)

    # 3. If only one framework in selected language, return it
    if len(lang_stacks) == 1:
        selected = lang_stacks[0]
        click.echo(f"  {ui.green('✓')} {label.capitalize()}: {selected.name}")
        return selected

    # 4. Select framework
    return _select_framework(lang_stacks, label)


def select_stacks_for_type(project_type: str) -> dict[str, StackInfo | None]:
    """Select stacks based on project type.

    Returns a dict with keys: stack, backend, frontend, mobile (values may be None).
    """
    result: dict[str, StackInfo | None] = {
        "stack": None,
        "backend": None,
        "frontend": None,
        "mobile": None,
    }

    if project_type == "single":
        result["stack"] = select_stack(label="stack")
    elif project_type in ("fullstack", "fullstack-mobile", "saas-platform"):
        result["backend"] = select_stack("backend", label="backend")
        result["frontend"] = select_stack("frontend", label="frontend")

        if project_type in ("fullstack-mobile", "saas-platform"):
            if project_type == "saas-platform":
                if click.confirm("  Include mobile app?", default=False):
                    result["mobile"] = _select_mobile()
            else:
                result["mobile"] = _select_mobile()

    return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_LANGUAGE_LABELS = {
    "python": "Python",
    "typescript": "Node.js (TypeScript)",
    "php": "PHP",
    "rust": "Rust",
    "other": "Other",
}


def _select_category(categories: list[str]) -> str:
    """Prompt user to pick a stack category."""
    return ui.prompt_choice(
        categories,
        "category",
        display_fn=lambda cat: _CATEGORY_LABELS.get(cat, cat),
    )


def _select_by_language(by_lang: dict[str, list[StackInfo]]) -> list[StackInfo]:
    """Prompt user to pick a language, returns the stacks for that language."""
    langs = list(by_lang.keys())
    selected = ui.prompt_choice(
        langs,
        "language",
        display_fn=lambda lang: _LANGUAGE_LABELS.get(lang, lang.capitalize()),
    )
    return by_lang[selected]


def _select_framework(stacks: list[StackInfo], label: str = "stack") -> StackInfo:
    """Prompt user to pick a specific framework from a list."""
    return ui.prompt_choice(
        stacks,
        label,
        display_fn=lambda s: s.name,
        detail_fn=lambda s: s.description,
    )


def _select_mobile() -> StackInfo | None:
    """Prompt for mobile platform selection.

    Hardcoded because we don't ship mobile stack manifests yet (no template files).
    When mobile stacks are added to data/stacks/, this should use prompt_choice() instead.
    """
    click.echo("")
    click.echo(f"  {ui.cyan('Mobile platform:')}")
    click.echo("    1) React Native (Expo) — cross-platform")
    click.echo("    2) Kotlin (Android) — native Android")
    click.echo("    3) Swift (iOS) — native iOS")
    click.echo("    4) Skip mobile for now")
    click.echo("")

    while True:
        choice = click.prompt("  Select mobile", default="4", show_default=True)
        if choice == "4":
            click.echo(f"  {ui.green('✓')} Mobile: skipped")
            return None
        if choice in ("1", "2", "3"):
            names = {"1": "React Native (Expo)", "2": "Kotlin (Android)", "3": "Swift (iOS)"}
            ids = {"1": "react-native-expo", "2": "kotlin-android", "3": "swift-ios"}
            click.echo(f"  {ui.green('✓')} Mobile: {names[choice]}")
            return StackInfo(
                id=ids[choice],
                name=names[choice],
                description="",
                type="mobile",
                language="",
                framework="",
                directory=None,
            )
        click.echo(f"  {ui.red('Invalid')}. Enter 1-4.")
