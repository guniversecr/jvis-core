"""Utility commands — information display."""

from __future__ import annotations

import logging

import click

from jvis.utils import ui
from jvis.utils.config import read_version
from jvis.utils.paths import get_jvis_home, get_templates_dir

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------


@click.command("version")
def version_cmd() -> None:
    """Show JVIS version."""
    click.echo(f"JVIS Manager v{read_version()}")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

PIPELINE_PLATFORMS = {
    "github": ("GitHub Actions", "github-actions", ".github/workflows/ci.yaml"),
    "gitlab": ("GitLab CI", "gitlab-ci", ".gitlab-ci.yml"),
    "azure": ("Azure DevOps", "azure-devops", "azure-pipelines.yml"),
}


@click.command()
@click.argument("platform", default="github")
def pipeline(platform: str) -> None:
    """List CI/CD pipeline templates. PLATFORM: github, gitlab, azure."""
    click.echo(ui.header("CI/CD PIPELINE GENERATOR"))
    info = PIPELINE_PLATFORMS.get(platform)
    if info is None:
        click.echo(f"  Platform not recognized: {platform}\n")
        click.echo("  Available platforms:")
        for key, (label, _, _) in PIPELINE_PLATFORMS.items():
            click.echo(f"    {key:<12s}{label}")
        click.echo()
        return

    label, subdir, dest = info
    templates_dir = get_templates_dir() / "pipelines" / subdir
    click.echo(f"  {ui.green(f'{label} Templates:')}\n")
    if templates_dir.is_dir():
        for f in sorted(templates_dir.iterdir()):
            if f.is_file():
                click.echo(f"    - {f.stem}")
    else:
        click.echo("    (no templates found)")
    click.echo(f"\n  {ui.cyan('Usage:')}")
    click.echo(f"    cp {templates_dir}/<template>.yaml {dest}\n")


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


@click.command()
def hooks() -> None:
    """List available JVIS hooks."""
    hooks_dir = get_jvis_home() / ".jvis" / "hooks"
    click.echo(ui.header("Available JVIS Hooks"))
    if not hooks_dir.is_dir():
        click.echo(f"  {ui.yellow('No hooks directory found')}")
        return
    for hook in sorted(hooks_dir.iterdir()):
        if hook.is_file():
            desc = ""
            try:
                for line in hook.read_text().splitlines():
                    if line.startswith("# ") and ("cleanup" in line.lower() or "hook" in line.lower()):
                        desc = line.removeprefix("# ").strip()
                        break
            except OSError as exc:
                logger.debug("Cannot read hook file %s: %s", hook, exc)
            click.echo(f"  {ui.green(hook.name)}")
            click.echo(f"    {desc or 'No description'}\n")
