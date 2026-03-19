from tkinter import Tk, Frame, Button, Label, Entry, StringVar, messagebox
import random
import socket

class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tank Game")
        self.master.geometry("400x300")

        self.room_code = StringVar()
        self.player_name = StringVar()

        self.create_widgets()

    def create_widgets(self):
        Label(self.master, text="Welcome to Tank Game").pack(pady=10)

        Label(self.master, text="Enter your name:").pack(pady=5)
        Entry(self.master, textvariable=self.player_name).pack(pady=5)

        Button(self.master, text="Create Room", command=self.create_room).pack(pady=10)
        Button(self.master, text="Join Room", command=self.join_room).pack(pady=10)

        self.room_code_label = Label(self.master, text="")
        self.room_code_label.pack(pady=10)

    def create_room(self):
        code = self.generate_room_code()
        self.room_code.set(code)
        self.room_code_label.config(text=f"Room Code: {code}")
        # Here you would add the logic to create a room on the server

    def join_room(self):
        code = self.room_code.get()
        if code:
            # Here you would add the logic to join a room on the server
            messagebox.showinfo("Join Room", f"Joining room: {code}")
        else:
            messagebox.showwarning("Warning", "Please create or enter a room code.")

    def generate_room_code(self):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

def main():
    root = Tk()
    ui = UI(root)
    root.mainloop()

if __name__ == "__main__":
    main()