#!/usr/bin/env python3
"""
News Scraper - Real world UV example
Dependencies: requests, beautifulsoup4, rich

Setup commands:
uv init
uv add requests beautifulsoup4 rich
uv run news_scraper.py
"""

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track, Progress
from rich.spinner import Spinner
import time
import json

def scrape_sample_data():
    """
    Simulated news scraping (for demo purposes)
    In real scenario, you'd scrape actual news sites
    """
    # Sample tech news data
    return [
        {
            "title": "AI Technology Adoption Increases Globally",
            "source": "TechNews24",
            "time": "2 hours ago",
            "category": "Technology"
        },
        {
            "title": "Python Programming Demand Increases by 300%",
            "source": "DevWorld",
            "time": "4 hours ago", 
            "category": "Programming"
        },
        {
            "title": "UV Package Manager: The Fastest Alternative to pip",
            "source": "CodeDaily",
            "time": "6 hours ago",
            "category": "Tools"
        },
        {
            "title": "New Tech Hub Established in Silicon Valley",
            "source": "StartupNews",
            "time": "8 hours ago",
            "category": "Business"
        },
        {
            "title": "Developer GitHub Contributions Rise Significantly",
            "source": "OpenSource Weekly",
            "time": "12 hours ago",
            "category": "Development"
        }
    ]

def fetch_api_data():
    """
    Fetch real data from a public API
    """
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)
        response.raise_for_status()
        posts = response.json()[:3]  # Get first 3 posts
        
        return [
            {
                "title": f"Tech Post #{post['id']}: {post['title'][:50]}...",
                "source": "JSONPlaceholder API",
                "time": f"{post['id']} hours ago",
                "category": "API Data"
            }
            for post in posts
        ]
    except requests.RequestException:
        return []

def main():
    console = Console()
    
    # Header
    header_panel = Panel(
        "[bold blue]🌐 Tech News Scraper[/bold blue]",
        subtitle="Powered by UV Package Manager",
        border_style="green"
    )
    console.print(header_panel)
    
    all_news = []
    
    # Scrape local sample data
    with console.status("[bold green]Scraping local tech news...", spinner="dots"):
        time.sleep(1.5)  # Simulate scraping delay
        local_news = scrape_sample_data()
        all_news.extend(local_news)
    
    console.print("[green]✅[/green] Local news scraped successfully!")
    
    # Fetch API data
    with console.status("[bold blue]Fetching data from API...", spinner="bouncingBall"):
        time.sleep(1)
        api_news = fetch_api_data()
        all_news.extend(api_news)
    
    if api_news:
        console.print("[green]✅[/green] API data fetched successfully!")
    else:
        console.print("[yellow]⚠️[/yellow] API data unavailable (offline demo)")
    
    # Process and display results
    console.print(f"\n[bold cyan]📊 Total articles found: {len(all_news)}[/bold cyan]")
    
    # Create results table
    table = Table(
        title="Latest Tech News",
        show_header=True,
        header_style="bold magenta",
        border_style="blue"
    )
    table.add_column("Title", style="cyan", width=45)
    table.add_column("Source", style="yellow", width=15)
    table.add_column("Category", style="green", width=12)
    table.add_column("Time", style="bright_black", width=15)
    
    # Add news with progress animation
    for news in track(all_news, description="Processing articles..."):
        table.add_row(
            news["title"],
            news["source"],
            news["category"],
            news["time"]
        )
        time.sleep(0.2)  # Animation delay
    
    console.print(table)
    
    # Save results
    output_file = "tech_news.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    console.print(f"\n[bold green]💾 Results saved to {output_file}[/bold green]")
    
    # Summary statistics
    categories = {}
    for news in all_news:
        cat = news["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    console.print("\n[bold yellow]📈 Category Statistics:[/bold yellow]")
    for category, count in categories.items():
        console.print(f"  • {category}: {count} articles")
    
    console.print("\n[italic]This scraper uses UV's fast dependency management![/italic]")
    console.print("[dim]Dependencies: requests, beautifulsoup4, rich[/dim]")

if __name__ == "__main__":
    main()
