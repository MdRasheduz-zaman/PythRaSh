#!/usr/bin/env python3
"""
Rich Library Demo
Run with: uv run --with rich rich_demo.py
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
import time

def main():
    console = Console()
    
    # Welcome message
    welcome_text = Text("🚀 UV Package Manager Demo", style="bold blue")
    panel = Panel(welcome_text, title="Python Tutorial", border_style="green")
    console.print(panel)
    
    # Create a comparison table
    console.print("\n[bold yellow]Package Manager Comparison:[/bold yellow]")
    
    table = Table(title="pip vs UV Comparison")
    table.add_column("Feature", style="cyan", no_wrap=True)
    table.add_column("pip", style="red")
    table.add_column("UV", style="green")
    
    comparisons = [
        ("Installation Speed", "🐌 Slow (10-60s)", "⚡ Lightning Fast (<2s)"),
        ("Dependency Resolution", "❌ Basic", "✅ Advanced SAT solver"),
        ("Virtual Environment", "❌ Manual setup", "✅ Automatic"),
        ("Lock Files", "❌ No lock files", "✅ uv.lock for reproducibility"),
        ("Python Version Mgmt", "❌ Needs pyenv", "✅ Built-in"),
        ("Parallel Downloads", "❌ Sequential", "✅ Parallel processing"),
        ("Caching", "❌ Limited", "✅ Smart global cache")
    ]
    
    # Add rows with animation
    for feature, pip_val, uv_val in track(comparisons, description="Loading comparison..."):
        table.add_row(feature, pip_val, uv_val)
        time.sleep(0.3)
    
    console.print(table)
    
    # Summary
    console.print("\n[bold green]🎉 UV makes Python development 10x easier and faster![/bold green]")
    console.print("[italic]This rich formatting was installed temporarily with --with flag![/italic]")

if __name__ == "__main__":
    main()
