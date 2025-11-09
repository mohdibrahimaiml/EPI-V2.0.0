"""
EPI CLI View - Open .epi file in browser viewer.

Extracts the embedded viewer.html and opens it in the default browser.
No code execution, all data is pre-rendered JSON.
"""

import tempfile
import webbrowser
import zipfile
from pathlib import Path

import typer
from rich.console import Console

console = Console()

app = typer.Typer(name="view", help="View .epi file in browser")


@app.callback(invoke_without_command=True)
def view(
    ctx: typer.Context,
    epi_file: Path = typer.Argument(..., help="Path to .epi file to view"),
):
    """
    Open .epi file in browser viewer.
    
    Extracts the embedded viewer.html and opens it in your default browser.
    All data is pre-embedded, no server required.
    """
    # Validate file exists
    if not epi_file.exists():
        console.print(f"[red]❌ Error:[/red] File not found: {epi_file}")
        raise typer.Exit(1)
    
    # Validate it's a ZIP file
    if not zipfile.is_zipfile(epi_file):
        console.print(f"[red]❌ Error:[/red] Not a valid .epi file: {epi_file}")
        raise typer.Exit(1)
    
    try:
        # Create temp directory for viewer
        temp_dir = Path(tempfile.mkdtemp(prefix="epi_view_"))
        viewer_path = temp_dir / "viewer.html"
        
        # Extract viewer.html
        with zipfile.ZipFile(epi_file, "r") as zf:
            if "viewer.html" not in zf.namelist():
                console.print("[red]❌ Error:[/red] No viewer found in .epi file")
                console.print("[dim]This file may have been created with an older version of EPI[/dim]")
                raise typer.Exit(1)
            
            # Extract viewer
            zf.extract("viewer.html", temp_dir)
        
        # Open in browser
        file_url = viewer_path.as_uri()
        console.print(f"[dim]Opening viewer:[/dim] {file_url}")
        
        success = webbrowser.open(file_url)
        
        if success:
            console.print("[green]✅[/green] Viewer opened in browser")
        else:
            console.print("[yellow]⚠️  Could not open browser automatically[/yellow]")
            console.print(f"[dim]Open manually:[/dim] {file_url}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        raise typer.Exit(1)
