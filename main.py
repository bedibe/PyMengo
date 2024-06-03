import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os

# Funções de Utilidade
def log_login(username):
    with open("login_log.txt", "a") as f:
        f.write(f"{username} logged in at {datetime.now()}\n")

def clear_monthly_log():
    log_file = "login_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)

# Limpar log mensalmente (simulação)
clear_monthly_log()

# Funções de Login/Cadastro
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    with open("login.txt", "a") as file:
        file.write(f"{username},{password}\n")
    messagebox.showinfo("Registration", "Registration successful!")
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    
    with open("login.txt", "r") as file:
        users = file.readlines()
    
    for user in users:
        stored_username, stored_password = user.strip().split(',')
        if stored_username == username and stored_password == password:
            log_login(username)
            open_task_manager(username)
            return
    
    messagebox.showerror("Login Failed", "Invalid username or password")

class TaskManager:
    def __init__(self, username):
        self.username = username
        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

        self.window = tk.Tk()
        self.window.title(f"Task Manager - {self.username}")

        self.setup_ui()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def setup_ui(self):
        # Código do layout
        self.frame_top = tk.Frame(self.window)
        self.frame_top.pack(pady=10, padx=10)

        self.frame_middle = tk.Frame(self.window)
        self.frame_middle.pack(pady=10, padx=10)

        self.frame_bottom = tk.Frame(self.window)
        self.frame_bottom.pack(pady=10)

        # Código de widgets de tarefa
        tk.Label(self.frame_top, text="Tarefa", font="Playfair", foreground="black").pack(side=tk.TOP, padx=5)
        self.title_entry = tk.Entry(self.frame_top, width=50, borderwidth="10", bg="red", font="arial", foreground="black")
        self.title_entry.pack(side=tk.LEFT, padx=5)

        # Código de widgets de descrição
        tk.Label(self.frame_middle, text="Descrição", font="Playfair", foreground="black").pack(side=tk.TOP, padx=5)
        self.description_entry = tk.Entry(self.frame_middle, width=50, borderwidth="10", bg="red", font="arial", foreground="black")
        self.description_entry.pack(side=tk.LEFT, padx=5)
