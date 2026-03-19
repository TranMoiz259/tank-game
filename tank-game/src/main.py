import socket
import threading
from client.menu import Menu
from server.server import Server

def main():
    # Initialize the server
    server = Server()
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    # Initialize the client menu
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()