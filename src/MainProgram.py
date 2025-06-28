import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Path to the exploits directory
BASE_DIR = os.path.abspath("exploits")
os.makedirs(BASE_DIR, exist_ok=True)

# The order of scripts to run
SCRIPT_SEQUENCE = [
    "nmap.py",
    "versionfinderandsearcher.py",
    "infoextracter.py",
    "APIanswergenerator.py"
]

# Path to the Python executable in virtual environment
PYTHON_PATH = "./myenv/bin/python"

# Main application class using Tkinter
class ExploitViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Exploit Automation Panel")
        self.geometry("1000x600")

        # Entry field for target IP
        self.ip_entry = tk.Entry(self)
        self.ip_entry.pack(pady=10)
        self.ip_entry.insert(0, "Enter target IP")

        # Button to trigger scanning pipeline
        self.run_button = tk.Button(self, text="Run Scan", command=self.run_pipeline_handler)
        self.run_button.pack(pady=5)

        # Text area for displaying real-time logs
        self.log_text = tk.Text(self, height=10, bg="black", fg="lime")
        self.log_text.pack(fill=tk.X, padx=10, pady=5)

        # Horizontal panel for tree + content
        self.main_frame = tk.PanedWindow(self, sashrelief=tk.RAISED, sashwidth=5)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Treeview of services and exploits
        self.tree = ttk.Treeview(self.main_frame)
        self.tree.heading("#0", text="Exploits", anchor='w')
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.main_frame.add(self.tree)

        # Right: Text preview area for selected file
        self.text_area = tk.Text(self.main_frame, wrap="word")
        self.main_frame.add(self.text_area)

        # Initial population of treeview
        self.build_tree()

    # Handler for the 'Run Scan' button
    def run_pipeline_handler(self):
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("Input Needed", "Please enter an IP address.")
            return
        self.run_pipeline(ip)
        self.build_tree()

    # Executes all scan scripts in sequence
    def run_pipeline(self, ip):
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, f"[+] Starting scan pipeline on {ip}...\n")

        for script in SCRIPT_SEQUENCE:
            try:
                self.log_text.insert(tk.END, f"\n[*] Running {script}...\n")
                self.log_text.update()

                cmd = [PYTHON_PATH, script]
                if "nmap" in script:
                    cmd.append(ip)

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.stdout:
                    self.log_text.insert(tk.END, result.stdout)
                if result.stderr:
                    self.log_text.insert(tk.END, result.stderr)
                self.log_text.insert(tk.END, "\n" + ("-" * 40) + "\n")
                self.log_text.update()
            except Exception as e:
                self.log_text.insert(tk.END, f"[!] Error: {e}\n")

        messagebox.showinfo("Done", "All scripts completed.")

    # Rebuilds the left panel tree view
    def build_tree(self):
        self.tree.delete(*self.tree.get_children())
        for service in os.listdir(BASE_DIR):
            service_path = os.path.join(BASE_DIR, service)
            if os.path.isdir(service_path):
                parent = self.tree.insert("", "end", text=service, open=False)
                for eid in os.listdir(service_path):
                    eid_path = os.path.join(service_path, eid)
                    if os.path.isdir(eid_path):
                        eid_node = self.tree.insert(parent, "end", text=eid, open=False)
                        for fname in os.listdir(eid_path):
                            if fname.endswith(".txt"):
                                self.tree.insert(eid_node, "end", text=fname, values=[os.path.join(eid_path, fname)])

    # Displays file content in the right panel when selected
    def on_tree_select(self, event):
        selected = self.tree.focus()
        item = self.tree.item(selected)
        if "values" in item and item["values"]:
            filepath = item["values"][0]
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)

# Start the GUI
if __name__ == "__main__":
    app = ExploitViewer()
    app.mainloop()
