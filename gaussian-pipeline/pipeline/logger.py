from rich.console import Console #lib to make terminal outputs look nice

console = Console()

def info(msg):
    console.print(f"[cyan]{msg}[/cyan]") #[cyan] is a color code for rich library to print the text in cyan color

def success(msg):
    console.print(f"[green]{msg}[/green]")

def warning(msg):
    console.print(f"[yellow]{msg}[/yellow]")

def error(msg):
    console.print(f"[red]{msg}[/red]")