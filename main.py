import tkinter as tk
from tkinter import ttk, messagebox
from models import RepairShop, RepairTicket
from storage import DataStorage

class RepairShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manny's Computer Repair")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)
        self.storage = DataStorage()
        try:
            self.shop = self.storage.load()
        except ValueError as error:
            messagebox.showwarning("Load Warning", str(error))
            self.shop = RepairShop()
        self.selected_customer_id = None
        self.selected_ticket_id = None
        self.build_ui()
        self.refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_ui(self):
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="Computer Repair Shop Management System", font=("Arial", 20, "bold")).pack(side="left")
        self.summary_label = ttk.Label(header, font=("Arial", 10, "bold"))
        self.summary_label.pack(side="right")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.customer_tab = ttk.Frame(self.notebook)
        self.ticket_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customer_tab, text="Customers")
        self.notebook.add(self.ticket_tab, text="Repair Tickets")
        self.notebook.add(self.report_tab, text="Report")
        self.build_customer_tab()
        self.build_ticket_tab()
        self.build_report_tab()

    def build_customer_tab(self):
        form = ttk.LabelFrame(self.customer_tab, text="Customer Information", padding=15)
        form.pack(fill="x", padx=15, pady=15)
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(form, text="Phone:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(form, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form, width=45)
        self.phone_entry = ttk.Entry(form, width=45)
        self.email_entry = ttk.Entry(form, width=45)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=8)
        self.phone_entry.grid(row=1, column=1, sticky="ew", padx=8)
        self.email_entry.grid(row=2, column=1, sticky="ew", padx=8)
        form.columnconfigure(1, weight=1)
        buttons = ttk.Frame(form)
        buttons.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(buttons, text="Add Customer", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(buttons, text="Update Selected", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(buttons, text="Clear", command=self.clear_customer_form).pack(side="left", padx=5)

        search = ttk.Frame(self.customer_tab)
        search.pack(fill="x", padx=15)
        ttk.Label(search, text="Search:").pack(side="left")
        self.customer_search = ttk.Entry(search, width=35)
        self.customer_search.pack(side="left", padx=8)
        self.customer_search.bind("<KeyRelease>", lambda e: self.refresh_customers())

        self.customer_tree = ttk.Treeview(self.customer_tab, columns=("id", "name", "phone", "email"), show="headings")
        for key, title, width in [("id", "ID", 60), ("name", "Name", 220), ("phone", "Phone", 150), ("email", "Email", 260)]:
            self.customer_tree.heading(key, text=title)
            self.customer_tree.column(key, width=width)
        self.customer_tree.pack(fill="both", expand=True, padx=15, pady=10)
        self.customer_tree.bind("<<TreeviewSelect>>", self.select_customer)
        ttk.Button(self.customer_tab, text="Delete Selected Customer", command=self.delete_customer).pack(pady=(0, 12))

    def build_ticket_tab(self):
        form = ttk.LabelFrame(self.ticket_tab, text="Repair Ticket Information", padding=15)
        form.pack(fill="x", padx=15, pady=15)
        labels = ["Customer:", "Device Type:", "Problem:", "Estimated Cost:", "Status:"]
        for row, text in enumerate(labels):
            ttk.Label(form, text=text).grid(row=row, column=0, sticky="w", pady=5)
        self.customer_combo = ttk.Combobox(form, state="readonly", width=45)
        self.device_entry = ttk.Entry(form, width=45)
        self.problem_entry = ttk.Entry(form, width=45)
        self.cost_entry = ttk.Entry(form, width=20)
        self.cost_entry.insert(0, "0.00")
        self.status_combo = ttk.Combobox(form, values=RepairTicket.VALID_STATUSES, state="readonly", width=20)
        self.status_combo.set("Waiting")
        for row, widget in enumerate([self.customer_combo, self.device_entry, self.problem_entry, self.cost_entry, self.status_combo]):
            widget.grid(row=row, column=1, sticky="ew", padx=8)
        form.columnconfigure(1, weight=1)
        buttons = ttk.Frame(form)
        buttons.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(buttons, text="Create Ticket", command=self.create_ticket).pack(side="left", padx=5)
        ttk.Button(buttons, text="Update Selected", command=self.update_ticket).pack(side="left", padx=5)
        ttk.Button(buttons, text="Clear", command=self.clear_ticket_form).pack(side="left", padx=5)

        search = ttk.Frame(self.ticket_tab)
        search.pack(fill="x", padx=15)
        ttk.Label(search, text="Search:").pack(side="left")
        self.ticket_search = ttk.Entry(search, width=35)
        self.ticket_search.pack(side="left", padx=8)
        self.ticket_search.bind("<KeyRelease>", lambda e: self.refresh_tickets())

        columns = ("id", "customer", "device", "problem", "status", "cost")
        self.ticket_tree = ttk.Treeview(self.ticket_tab, columns=columns, show="headings")
        settings = [("id", "Ticket ID", 70), ("customer", "Customer", 170), ("device", "Device", 120), ("problem", "Problem", 270), ("status", "Status", 105), ("cost", "Cost", 80)]
        for key, title, width in settings:
            self.ticket_tree.heading(key, text=title)
            self.ticket_tree.column(key, width=width)
        self.ticket_tree.pack(fill="both", expand=True, padx=15, pady=10)
        self.ticket_tree.bind("<<TreeviewSelect>>", self.select_ticket)
        ttk.Button(self.ticket_tab, text="Delete Selected Completed Ticket", command=self.delete_ticket).pack(pady=(0, 12))

    def build_report_tab(self):
        frame = ttk.Frame(self.report_tab, padding=15)
        frame.pack(fill="both", expand=True)
        self.report_text = tk.Text(frame, wrap="word", font=("Courier New", 10), state="disabled")
        self.report_text.pack(fill="both", expand=True)
        ttk.Button(frame, text="Save Data", command=lambda: self.save_data(True)).pack(pady=10)

    def add_customer(self):
        try:
            customer = self.shop.add_customer(self.name_entry.get(), self.phone_entry.get(), self.email_entry.get())
        except ValueError as error:
            messagebox.showerror("Customer Error", str(error)); return
        self.save_data(False); self.clear_customer_form(); self.refresh_all()
        messagebox.showinfo("Success", f"Customer #{customer.customer_id} was added.")

    def update_customer(self):
        if self.selected_customer_id is None:
            messagebox.showerror("No Selection", "Select a customer first."); return
        try:
            self.shop.update_customer(self.selected_customer_id, self.name_entry.get(), self.phone_entry.get(), self.email_entry.get())
        except ValueError as error:
            messagebox.showerror("Customer Error", str(error)); return
        self.save_data(False); self.clear_customer_form(); self.refresh_all(); messagebox.showinfo("Success", "Customer updated.")

    def delete_customer(self):
        if self.selected_customer_id is None:
            messagebox.showerror("No Selection", "Select a customer first."); return
        if not messagebox.askyesno("Confirm", "Delete this customer?"): return
        try:
            self.shop.delete_customer(self.selected_customer_id)
        except ValueError as error:
            messagebox.showerror("Delete Error", str(error)); return
        self.save_data(False); self.clear_customer_form(); self.refresh_all()

    def create_ticket(self):
        try:
            customer_id = self.get_customer_id()
            cost = float(self.cost_entry.get())
            ticket = self.shop.create_ticket(customer_id, self.device_entry.get(), self.problem_entry.get(), cost)
            ticket.update_status(self.status_combo.get())
        except ValueError as error:
            messagebox.showerror("Ticket Error", str(error)); return
        self.save_data(False); self.clear_ticket_form(); self.refresh_all(); messagebox.showinfo("Success", f"Ticket #{ticket.ticket_id} created.")

    def update_ticket(self):
        if self.selected_ticket_id is None:
            messagebox.showerror("No Selection", "Select a ticket first."); return
        try:
            ticket = self.shop.get_ticket(self.selected_ticket_id)
            if ticket is None: raise ValueError("Ticket not found.")
            ticket.customer_id = self.get_customer_id()
            ticket.device_type = self.device_entry.get().strip()
            ticket.problem_description = self.problem_entry.get().strip()
            if not ticket.device_type or not ticket.problem_description: raise ValueError("Device and problem are required.")
            self.shop.update_ticket(ticket.ticket_id, self.status_combo.get(), float(self.cost_entry.get()))
        except ValueError as error:
            messagebox.showerror("Ticket Error", str(error)); return
        self.save_data(False); self.clear_ticket_form(); self.refresh_all(); messagebox.showinfo("Success", "Ticket updated.")

    def delete_ticket(self):
        if self.selected_ticket_id is None:
            messagebox.showerror("No Selection", "Select a ticket first."); return
        if not messagebox.askyesno("Confirm", "Delete this completed ticket?"): return
        try:
            self.shop.delete_ticket(self.selected_ticket_id)
        except ValueError as error:
            messagebox.showerror("Delete Error", str(error)); return
        self.save_data(False); self.clear_ticket_form(); self.refresh_all()

    def select_customer(self, event=None):
        selected = self.customer_tree.selection()
        if not selected: return
        values = self.customer_tree.item(selected[0], "values")
        self.selected_customer_id = int(values[0])
        self.set_entry(self.name_entry, values[1]); self.set_entry(self.phone_entry, values[2]); self.set_entry(self.email_entry, values[3])

    def select_ticket(self, event=None):
        selected = self.ticket_tree.selection()
        if not selected: return
        ticket_id = int(self.ticket_tree.item(selected[0], "values")[0])
        ticket = self.shop.get_ticket(ticket_id)
        if ticket is None: return
        self.selected_ticket_id = ticket_id
        self.customer_combo.set(self.customer_value(ticket.customer_id))
        self.set_entry(self.device_entry, ticket.device_type); self.set_entry(self.problem_entry, ticket.problem_description); self.set_entry(self.cost_entry, f"{ticket.repair_cost:.2f}")
        self.status_combo.set(ticket.status)

    def get_customer_id(self):
        value = self.customer_combo.get().strip()
        if not value: raise ValueError("Select a customer.")
        return int(value.split(" - ", 1)[0])

    def customer_value(self, customer_id):
        customer = self.shop.get_customer(customer_id)
        return f"{customer_id} - {customer.name if customer else 'Unknown'}"

    def refresh_all(self):
        self.customer_combo["values"] = [self.customer_value(c.customer_id) for c in sorted(self.shop.customers.values(), key=lambda x: x.customer_id)]
        self.refresh_customers(); self.refresh_tickets(); self.refresh_report()
        summary = self.shop.get_ticket_summary()
        self.summary_label.config(text=f"Customers: {len(self.shop.customers)}   Waiting: {summary['Waiting']}   In Progress: {summary['In Progress']}   Completed: {summary['Completed']}")

    def refresh_customers(self):
        for item in self.customer_tree.get_children(): self.customer_tree.delete(item)
        for c in self.shop.search_customers(self.customer_search.get()):
            self.customer_tree.insert("", "end", values=(c.customer_id, c.name, c.phone, c.email))

    def refresh_tickets(self):
        for item in self.ticket_tree.get_children(): self.ticket_tree.delete(item)
        for t in self.shop.search_tickets(self.ticket_search.get()):
            customer = self.shop.get_customer(t.customer_id)
            self.ticket_tree.insert("", "end", values=(t.ticket_id, customer.name if customer else "Unknown", t.device_type, t.problem_description, t.status, f"${t.repair_cost:.2f}"))

    def refresh_report(self):
        summary = self.shop.get_ticket_summary()
        lines = ["MANNY'S COMPUTER REPAIR", "FINAL PROJECT REPORT", "="*70, "", f"Customers: {len(self.shop.customers)}", f"Tickets: {len(self.shop.repair_tickets)}", f"Waiting: {summary['Waiting']} | In Progress: {summary['In Progress']} | Completed: {summary['Completed']}", "", "CUSTOMERS", "-"*70]
        lines += [c.display_info() for c in self.shop.customers.values()] or ["No customers entered."]
        lines += ["", "REPAIR TICKETS", "-"*70]
        for t in self.shop.repair_tickets:
            customer = self.shop.get_customer(t.customer_id)
            lines.append(t.display_ticket(customer.name if customer else "Unknown"))
        if not self.shop.repair_tickets: lines.append("No tickets entered.")
        self.report_text.config(state="normal"); self.report_text.delete("1.0", tk.END); self.report_text.insert("1.0", "\n".join(lines)); self.report_text.config(state="disabled")

    def clear_customer_form(self):
        self.selected_customer_id = None
        for entry in (self.name_entry, self.phone_entry, self.email_entry): entry.delete(0, tk.END)

    def clear_ticket_form(self):
        self.selected_ticket_id = None; self.customer_combo.set("")
        for entry in (self.device_entry, self.problem_entry, self.cost_entry): entry.delete(0, tk.END)
        self.cost_entry.insert(0, "0.00"); self.status_combo.set("Waiting")

    def set_entry(self, entry, value):
        entry.delete(0, tk.END); entry.insert(0, value)

    def save_data(self, show_message=True):
        try: self.storage.save(self.shop)
        except OSError as error: messagebox.showerror("Save Error", str(error)); return
        if show_message: messagebox.showinfo("Saved", "Data saved successfully.")

    def close_app(self):
        try: self.storage.save(self.shop)
        except OSError: pass
        self.root.destroy()

def main():
    root = tk.Tk(); RepairShopApp(root); root.mainloop()

if __name__ == "__main__":
    main()
