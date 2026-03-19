import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server.server import Server
from src.client.menu import Menu
from src.shared.network import NetworkClient
import threading

def main():
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()