"""
EPI CLI Main - Entry point for the EPI command-line interface.

Provides the main CLI application with frictionless first-run experience.
"""

import typer
from rich.console import Console

from epi_cli.keys import generate_default_keypair_if_missing

# Create Typer app
app = typer.Typer(
    name="epi",
    help="EPI - Executable Package for AI workflows",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich"
)

console = Console()


@app.callback()
def main_callback():
    """
    Main callback - runs before any command.
    
    Implements frictionless first run by auto-generating default key pair.
    """
    # Auto-generate default keypair if missing (frictionless first run)
    generate_default_keypair_if_missing(console_output=True)


@app.command()
def version():
    """Show EPI version information."""
    from epi_core import __version__
    console.print(f"[bold]EPI[/bold] version [cyan]{__version__}[/cyan]")
    console.print("[dim]The PDF for AI workflows[/dim]")


# Import and register subcommands
# These will be added as they're implemented

# Phase 1: verify command
from epi_cli.verify import verify_app
app.add_typer(verify_app, name="verify", help="Verify .epi file integrity and authenticity")

# Phase 2: record command
from epi_cli.record import app as record_app
app.add_typer(record_app, name="record", help="Record a workflow into a .epi file")

# Phase 3: view command
from epi_cli.view import app as view_app
app.add_typer(view_app, name="view", help="View .epi file in browser")

# Phase 1: keys command (for manual key management)
@app.command()
def keys(
    action: str = typer.Argument(..., help="Action: generate, list, or export"),
    name: str = typer.Option("default", "--name", "-n", help="Key pair name"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing keys")
):
    """Manage Ed25519 key pairs for signing."""
    from epi_cli.keys import KeyManager, print_keys_table
    
    key_manager = KeyManager()
    
    if action == "generate":
        try:
            private_path, public_path = key_manager.generate_keypair(name, overwrite=overwrite)
            console.print(f"\n[bold green]✅ Generated key pair:[/bold green] {name}")
            console.print(f"  [cyan]Private:[/cyan] {private_path}")
            console.print(f"  [cyan]Public:[/cyan]  {public_path}\n")
        except FileExistsError as e:
            console.print(f"[red]❌ Error:[/red] {e}")
            raise typer.Exit(1)
    
    elif action == "list":
        keys_list = key_manager.list_keys()
        print_keys_table(keys_list)
    
    elif action == "export":
        try:
            public_key_b64 = key_manager.export_public_key(name)
            console.print(f"\n[bold]Public key for '{name}':[/bold]")
            console.print(f"[cyan]{public_key_b64}[/cyan]\n")
        except FileNotFoundError as e:
            console.print(f"[red]❌ Error:[/red] {e}")
            raise typer.Exit(1)
    
    else:
        console.print(f"[red]❌ Unknown action:[/red] {action}")
        console.print("[dim]Valid actions: generate, list, export[/dim]")
        raise typer.Exit(1)


# Entry point for CLI
def cli_main():
    """CLI entry point (called by `epi` command)."""
    app()


if __name__ == "__main__":
    cli_main()
