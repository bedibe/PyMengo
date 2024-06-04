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

        # Layout dos botoes da funcionalidades
        tk.Button(self.frame_bottom, text="Add Task", command=self.add_task, borderwidth="10", bg="black", font="arial", foreground="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_bottom, text="Update Task", command=self.update_task, borderwidth="10", bg="black", font="arial", foreground="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_bottom, text="Delete Task", command=self.delete_task, borderwidth="10", bg="black", font="arial", foreground="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_bottom, text="View Tasks", command=self.view_tasks, borderwidth="10", bg="black", font="arial", foreground="white").pack(side=tk.LEFT, padx=5)
       
        # Box de listagem para exibir tarefas
        self.tasks_listbox = tk.Listbox(self.window, width=100, height=10,  borderwidth="10", bg="black", font="oswald", foreground="white")
        self.tasks_listbox.pack(pady=10)

        self.window.mainloop()
        
        #alerts para os botões 
    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
        self.conn.commit()

        messagebox.showinfo("Success", "Task added successfully")
        self.view_tasks()

    def update_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split(" ")[0]
            title = self.title_entry.get()
            description = self.description_entry.get()

            cursor = self.conn.cursor()
            cursor.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?', (title, description, task_id))
            self.conn.commit()

            messagebox.showinfo("Success", "Task updated successfully")
            self.view_tasks()
        except:
            messagebox.showerror("Error", "No task selected")

    def delete_task(self):
        try:
            selected_task = self.tasks_listbox.get(self.tasks_listbox.curselection())
            task_id = selected_task.split(" ")[0]

            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Task deleted successfully")
            self.view_tasks()
        except:
            messagebox.showerror("Error", "No task selected")

    def view_tasks(self):
        self.tasks_listbox.delete(0, tk.END)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()

        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"{task[0]} - {task[1]}: {task[2]}")

def open_task_manager(username):
    login_window.destroy()
    TaskManager(username)

# Interface de Login
login_window = tk.Tk()
login_window.title("Login/Register")
login_window.geometry("1000x1000")

# layout do background
frame_login = tk.Frame(login_window, padx=250, pady=200, bg="red")
frame_login.pack(pady=25)

# Layout da interface do usuario
tk.Label(frame_login, borderwidth="10", text="Usuário", bg="black", font="arial", foreground="white").grid(row=0, column=0, pady=20, padx=5)
entry_username = tk.Entry(frame_login, borderwidth="10")
entry_username.grid(row=0, column=1, pady=10)

# layout da interface de senha
tk.Label(frame_login, borderwidth="10", text="Senha",bg="black",font="arial", foreground="white").grid(row=1, column=0, pady=50)
entry_password = tk.Entry(frame_login, borderwidth="10")
entry_password.grid(row=1, column=1, pady=10)

# Botoões da interface de login e registro
tk.Button(frame_login, text="Login", command=login_user, borderwidth="10", bg="black", font="arial", foreground="white").grid(row=2, column=0, pady=20, padx=10)
tk.Button(frame_login, text="Register", command=register_user, borderwidth="10", bg="black", font="arial", foreground="white").grid(row=2, column=1, pady=20)

login_window.mainloop()

