"""CLI entry point for ai-steward."""

import click


@click.group()
@click.version_option()
def main() -> None:
    """ai-steward: autonomous software evolution."""


@main.command()
@click.argument("repo", type=click.Path(exists=True))
def run(repo: str) -> None:
    """Run the evolution pipeline against REPO."""
    click.echo(f"ai-steward: pipeline not yet implemented for {repo}")
