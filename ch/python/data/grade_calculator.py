#!/usr/bin/env python3
"""
Student Grade Calculator - Real world UV example
Dependencies: pandas, rich

Setup commands:
uv init
uv add pandas rich
uv run grade_calculator.py
"""

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
import statistics
from pathlib import Path

def create_sample_data():
    """Create sample student data if CSV doesn't exist"""
    if not Path("students.csv").exists():
        data = {
            'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 
                    'Eva Brown', 'Frank Miller', 'Grace Lee', 'Henry Clark', 
                    'Ivy Taylor', 'Jack Anderson'],
            'math': [95, 78, 88, 92, 85, 90, 88, 92, 85, 90],
            'science': [88, 91, 95, 85, 92, 88, 90, 88, 95, 85],
            'english': [92, 85, 90, 88, 95, 85, 92, 90, 88, 92],
            'history': [85, 88, 92, 90, 88, 92, 85, 88, 90, 88]
        }
        df = pd.DataFrame(data)
        df.to_csv('students.csv', index=False)
        return df
    return None

def load_student_data():
    """Load student data from CSV file"""
    try:
        df = pd.read_csv('students.csv')
        return df
    except FileNotFoundError:
        console = Console()
        console.print("[red]Error: students.csv not found. Creating sample data...[/red]")
        return create_sample_data()

def calculate_grades(df):
    """Calculate grades and statistics"""
    # Calculate average for each student
    subject_columns = ['math', 'science', 'english', 'history']
    df['average'] = df[subject_columns].mean(axis=1)
    
    # Assign letter grades
    def get_letter_grade(avg):
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'
    
    df['letter_grade'] = df['average'].apply(get_letter_grade)
    
    return df

def display_student_report(df, console):
    """Display individual student grades"""
    table = Table(
        title="📚 Student Grade Report",
        show_header=True,
        header_style="bold blue",
        border_style="green"
    )
    
    table.add_column("Student", style="cyan", width=15)
    table.add_column("Math", justify="center", style="yellow")
    table.add_column("Science", justify="center", style="yellow")
    table.add_column("English", justify="center", style="yellow")
    table.add_column("History", justify="center", style="yellow")
    table.add_column("Average", justify="center", style="magenta")
    table.add_column("Grade", justify="center", style="bold green")
    
    for _, student in track(df.iterrows(), description="Processing grades...", total=len(df)):
        # Color code the letter grade
        grade_color = {
            'A': 'bold green',
            'B': 'green', 
            'C': 'yellow',
            'D': 'orange1',
            'F': 'red'
        }.get(student['letter_grade'], 'white')
        
        table.add_row(
            student['name'],
            str(int(student['math'])),
            str(int(student['science'])),
            str(int(student['english'])),
            str(int(student['history'])),
            f"{student['average']:.1f}",
            f"[{grade_color}]{student['letter_grade']}[/{grade_color}]"
        )
    
    console.print(table)

def display_class_statistics(df, console):
    """Display class-wide statistics"""
    subject_columns = ['math', 'science', 'english', 'history']
    
    # Calculate statistics
    stats_table = Table(
        title="📊 Class Statistics",
        show_header=True,
        header_style="bold magenta",
        border_style="blue"
    )
    
    stats_table.add_column("Subject", style="cyan")
    stats_table.add_column("Average", justify="center")
    stats_table.add_column("Highest", justify="center", style="green")
    stats_table.add_column("Lowest", justify="center", style="red")
    stats_table.add_column("Std Dev", justify="center")
    
    for subject in subject_columns:
        avg = df[subject].mean()
        highest = df[subject].max()
        lowest = df[subject].min()
        std_dev = df[subject].std()
        
        stats_table.add_row(
            subject.title(),
            f"{avg:.1f}",
            str(int(highest)),
            str(int(lowest)),
            f"{std_dev:.1f}"
        )
    
    console.print(stats_table)
    
    # Grade distribution
    grade_dist = df['letter_grade'].value_counts().sort_index()
    
    console.print("\n[bold yellow]📈 Grade Distribution:[/bold yellow]")
    for grade, count in grade_dist.items():
        percentage = (count / len(df)) * 100
        console.print(f"  {grade}: {count} students ({percentage:.1f}%)")

def generate_report_file(df):
    """Generate a detailed report file"""
    report_content = []
    report_content.append("STUDENT GRADE REPORT")
    report_content.append("=" * 50)
    report_content.append("")
    
    for _, student in df.iterrows():
        report_content.append(f"Student: {student['name']}")
        report_content.append(f"  Math: {student['math']}")
        report_content.append(f"  Science: {student['science']}")
        report_content.append(f"  English: {student['english']}")
        report_content.append(f"  History: {student['history']}")
        report_content.append(f"  Average: {student['average']:.1f}")
        report_content.append(f"  Letter Grade: {student['letter_grade']}")
        report_content.append("")
    
    # Class statistics
    report_content.append("CLASS STATISTICS")
    report_content.append("-" * 30)
    subject_columns = ['math', 'science', 'english', 'history']
    for subject in subject_columns:
        avg = df[subject].mean()
        report_content.append(f"{subject.title()} Average: {avg:.1f}")
    
    report_content.append(f"\nClass Average: {df['average'].mean():.1f}")
    
    # Save to file
    with open('grade_report.txt', 'w') as f:
        f.write('\n'.join(report_content))

def main():
    console = Console()
    
    # Header
    header_panel = Panel(
        "[bold blue]🎓 Student Grade Calculator[/bold blue]",
        subtitle="Powered by UV Package Manager",
        border_style="green"
    )
    console.print(header_panel)
    
    # Load data
    with console.status("[bold green]Loading student data...", spinner="dots"):
        df = load_student_data()
        if df is None:
            console.print("[red]Failed to load data![/red]")
            return
    
    console.print(f"[green]✅[/green] Loaded data for {len(df)} students")
    
    # Calculate grades
    with console.status("[bold blue]Calculating grades...", spinner="bouncingBall"):
        df = calculate_grades(df)
    
    console.print("[green]✅[/green] Grades calculated successfully!")
    
    # Display results
    display_student_report(df, console)
    console.print("")
    display_class_statistics(df, console)
    
    # Generate report file
    generate_report_file(df)
    console.print(f"\n[bold green]💾 Detailed report saved to grade_report.txt[/bold green]")
    
    # Summary
    class_avg = df['average'].mean()
    console.print(f"\n[bold cyan]📊 Class Average: {class_avg:.1f}[/bold cyan]")
    
    highest_student = df.loc[df['average'].idxmax()]
    console.print(f"[bold green]🏆 Top Student: {highest_student['name']} ({highest_student['average']:.1f})[/bold green]")
    
    console.print("\n[italic]This calculator demonstrates UV's dependency management![/italic]")
    console.print("[dim]Dependencies: pandas, rich[/dim]")

if __name__ == "__main__":
    main()
