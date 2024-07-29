import tkinter as tk
from tkinter import messagebox
import os
import json
from datetime import datetime

ENTRIES_FILE = "diary_entries.json"
entries = []

def setup_window():
    root = tk.Tk()
    root.title("Personal Diary App")
    root.geometry("400x500")
    return root

def create_input_field(root):
    tk.Label(root, text="Date:").pack(pady=5)
    date_label = tk.Label(root, text=datetime.now().strftime("%Y-%m-%d"))
    date_label.pack(pady=5)

    tk.Label(root, text="Diary Entry:").pack(pady=5)
    entry_text = tk.Text(root, height=10, width=50)
    entry_text.pack(pady=5)
    return date_label, entry_text

def create_buttons(root, date_label, entry_text, entry_list):
    save_button = tk.Button(root, text="Save Entry", command=lambda: save_entry(date_label, entry_text, entry_list))
    save_button.pack(pady=5)

    view_button = tk.Button(root, text="View Entry", command=lambda: view_entry(entry_list))
    view_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Entry", command=lambda: delete_entry(entry_list))
    delete_button.pack(pady=5)

def create_entry_list(root):
    entry_list = tk.Listbox(root, width=50, height=10)
    entry_list.pack(pady=10)
    return entry_list

def save_entry(date_label, entry_text, entry_list):
    date = date_label.cget("text")
    entry = entry_text.get("1.0", tk.END).strip()

    if entry:
        entries.append({"date": date, "entry": entry})
        entry_list.insert(tk.END, date)
        entry_text.delete("1.0", tk.END)
        save_entries()
    else:
        messagebox.showwarning("Warning", "Diary entry cannot be empty.")

def view_entry(entry_list):
    selected_index = entry_list.curselection()
    if selected_index:
        index = selected_index[0]
        entry = entries[index]
        view_window = tk.Toplevel()
        view_window.title(entry["date"])
        view_window.geometry("400x400")
        tk.Label(view_window, text="Date:").pack(pady=5)
        tk.Label(view_window, text=entry["date"]).pack(pady=5)
        tk.Label(view_window, text="Entry:").pack(pady=5)
        tk.Label(view_window, text=entry["entry"], wraplength=380, justify="left").pack(pady=5)
    else:
        messagebox.showwarning("Warning", "Please select an entry to view.")

def delete_entry(entry_list):
    selected_index = entry_list.curselection()
    if selected_index:
        index = selected_index[0]
        entry_list.delete(index)
        del entries[index]
        save_entries()
    else:
        messagebox.showwarning("Warning", "Please select an entry to delete.")

def save_entries():
    with open(ENTRIES_FILE, "w") as file:
        json.dump(entries, file)

def load_entries():
    if os.path.exists(ENTRIES_FILE):
        with open(ENTRIES_FILE, "r") as file:
            return json.load(file)
    return []

def main():
    global entries
    root = setup_window()
    
    date_label, entry_text = create_input_field(root)
    entry_list = create_entry_list(root)
    create_buttons(root, date_label, entry_text, entry_list)
    
    entries = load_entries()
    for entry in entries:
        entry_list.insert(tk.END, entry["date"])
    
    root.mainloop()

if __name__ == "__main__":
    main()
