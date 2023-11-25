from rich.console import Console
from rich.panel import Panel
import time

# Create two Console instances
console1 = Console()
console2 = Console()

# Content for each part of the window
content1 = "This is the content for the first part of the window."
content2 = "This is the content for the second part of the window."

# Render each part in a Panel
panel1 = Panel(content1, border_style="blue")
panel2 = Panel(content2, border_style="green")

# Print the panels to their respective consoles
#console1.print(panel1)
#console2.print(panel2)

while True:
    console1.print("console1: LOFASZ")
    time.sleep(3)
    console2.print("console2: ASZLOF")
    time.sleep(3)
