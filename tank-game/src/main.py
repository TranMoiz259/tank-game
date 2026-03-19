import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server.server import Server
from src.client.menu import Menu
import threading
import time

def main():
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()