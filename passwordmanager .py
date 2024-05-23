import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import json
import os

# By Tonio and O Vqxnz

class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Gestore Password")
        master.configure(bg="#000000")  

        self.button_frame = tk.Frame(master, bg="#000000")  
        self.button_frame.pack(pady=20)

        # Creazione dei pulsanti e delle azioni associate
        actions = [("Salva una password", self.save_password),
                   ("Recupera una password", self.retrieve_password),
                   ("Cancella una password", self.delete_password),
                   ("Chiudi", master.quit)]

        for text, command in actions:
            button = tk.Button(self.button_frame, text=text, command=command, width=20, bg="#1E88E5", fg="#FFFFFF")  
            button.pack(side=tk.LEFT, padx=10)

        self.manager = PasswordManager()

        # Etichetta di firma
        self.signature_label = tk.Label(master, text="By Tonio and O Vqxnz", bg="#000000", fg="#1E88E5", font=("Arial", 10, "italic"))
        self.signature_label.pack(side=tk.BOTTOM, pady=10)

    def save_password(self):
        # Finestra per salvare una password
        self.new_window = tk.Toplevel(self.master)
        self.app = SavePasswordWindow(self.new_window, self.manager)

    def retrieve_password(self):
        # Finestra per recuperare una password
        self.new_window = tk.Toplevel(self.master)
        self.app = RetrievePasswordWindow(self.new_window, self.manager)

    def delete_password(self):
        # Finestra per cancellare una password
        self.new_window = tk.Toplevel(self.master)
        self.app = DeletePasswordWindow(self.new_window, self.manager)

class SavePasswordWindow:
    def __init__(self, master, manager):
        self.master = master
        self.manager = manager
        master.title("Salva una Password")
        master.configure(bg="#000000")  

        # Etichette e campi di input per inserire le informazioni della password
        tk.Label(master, text="Nome del servizio:", bg="#000000", fg="#FFFFFF").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(master, text="Nome utente:", bg="#000000", fg="#FFFFFF").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(master, text="Password:", bg="#000000", fg="#FFFFFF").grid(row=2, column=0, padx=10, pady=5)

        self.service_entry = tk.Entry(master)
        self.service_entry.grid(row=0, column=1, padx=10, pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Pulsante per salvare la password
        self.save_button = tk.Button(master, text="Salva", command=self.save, bg="#EF6C00", fg="#FFFFFF")  
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save(self):
        # Salvataggio delle informazioni della password
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.manager.save_password(service, username, password)
        messagebox.showinfo("Successo", "Password salvata con successo!")
        self.master.destroy()

class RetrievePasswordWindow:
    def __init__(self, master, manager):
        self.master = master
        self.manager = manager
        master.title("Recupera una Password")
        master.configure(bg="#000000")  

        # Etichetta e campo di input per il nome del servizio
        tk.Label(master, text="Nome del servizio:", bg="#000000", fg="#FFFFFF").pack(pady=5)
        self.service_entry = tk.Entry(master)
        self.service_entry.pack(pady=5)

        # Pulsante per recuperare la password
        self.retrieve_button = tk.Button(master, text="Recupera", command=self.retrieve, bg="#0277BD", fg="#FFFFFF")  
        self.retrieve_button.pack(pady=5)

        # Pulsanti per copiare il nome utente e la password negli appunti
        self.copy_username_button = tk.Button(master, text="Copia Nome Utente", command=self.copy_username, bg="#FFA000", fg="#FFFFFF")  
        self.copy_username_button.pack(pady=5)
        self.copy_password_button = tk.Button(master, text="Copia Password", command=self.copy_password, bg="#FFA000", fg="#FFFFFF")  
        self.copy_password_button.pack(pady=5)

    def retrieve(self):
        # Recupero della password e visualizzazione delle informazioni
        service = self.service_entry.get()
        result = self.manager.retrieve_password(service)
        if result:
            username, password = result
            messagebox.showinfo("Successo", f"Nome utente: {username}\nPassword: {password}")
        else:
            messagebox.showinfo("Errore", "Password non trovata.")
        self.master.destroy()

    def copy_username(self):
        # Copia del nome utente negli appunti
        service = self.service_entry.get()
        result = self.manager.retrieve_password(service)
        if result:
            username, _ = result
            self.master.clipboard_clear()
            self.master.clipboard_append(username)
            messagebox.showinfo("Copia Nome Utente", "Nome utente copiato negli appunti!")
        else:
            messagebox.showinfo("Errore", "Password non trovata.")

    def copy_password(self):
        # Copia della password negli appunti
        service = self.service_entry.get()
        result = self.manager.retrieve_password(service)
        if result:
            _, password = result
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copia Password", "Password copiata negli appunti!")
        else:
            messagebox.showinfo("Errore", "Password non trovata.")

class DeletePasswordWindow:
    def __init__(self, master, manager):
        self.master = master
        self.manager = manager
        master.title("Cancella una Password")
        master.configure(bg="#000000")  

        # Etichetta e campo di input per il nome del servizio
        tk.Label(master, text="Nome del servizio:", bg="#000000", fg="#FFFFFF").pack(pady=5)
        self.service_entry = tk.Entry(master)
        self.service_entry.pack(pady=5)

        # Pulsante per cancellare la password
        self.delete_button = tk.Button(master, text="Cancella", command=self.delete, bg="#C62828", fg="#FFFFFF")  
        self.delete_button.pack(pady=5)

    def delete(self):
        # Cancellazione della password
        service = self.service_entry.get()
        result = self.manager.delete_password(service)
        if result:
            messagebox.showinfo("Successo", f"Password per {service} cancellata con successo!")
        else:
            messagebox.showinfo("Errore", "Password non trovata o non cancellabile.")
        self.master.destroy()

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()

    def load_key(self):
        if not os.path.exists(self.key_file):
            print("Errore: File chiave 'key.key' non trovato. Si prega di generare un file chiave.")
            exit()

        with open(self.key_file, 'rb') as key_file:
            self.key = key_file.read()

        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    def save_password(self, service, username, password):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}

        data[service] = {
            'username': self.encrypt_data(username).decode(),
            'password': self.encrypt_data(password).decode()
        }

        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def retrieve_password(self, service):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                if service in data:
                    username = self.decrypt_data(data[service]['username'])
                    password = self.decrypt_data(data[service]['password'])
                    return username, password
                else:
                    return None
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def delete_password(self, service):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                if service in data:
                    data.pop(service)
                    with open(self.data_file, 'w') as file:
                        json.dump(data, file)
                    return True
                else:
                    return False
        except (json.JSONDecodeError, FileNotFoundError):
            return False

def main():
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

    # By Tonio and O Vqxnz
