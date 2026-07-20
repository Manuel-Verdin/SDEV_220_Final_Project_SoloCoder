import tkinter as tk
from tkinter import ttk, messagebox

from models import Customer, RepairShop, RepairTicket


class RepairShopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Manny's Computer Repair")
        self.root.geometry("850x600")

        self.shop = RepairShop()
        self.next_customer_id = 1
        self.next_ticket_id = 1

        self.create_widgets()

    def create_widgets(self) -> None:
        title = ttk.Label(
            self.root,
            text="Computer Repair Shop Management System",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=12)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.customer_tab = ttk.Frame(notebook)
        self.ticket_tab = ttk.Frame(notebook)
        self.records_tab = ttk.Frame(notebook)

        notebook.add(self.customer_tab, text="Add Customer")
        notebook.add(self.ticket_tab, text="Create Repair Ticket")
        notebook.add(self.records_tab, text="View Records")

        self.build_customer_tab()
        self.build_ticket_tab()
        self.build_records_tab()

    def build_customer_tab(self) -> None:
        frame = ttk.Frame(self.customer_tab, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Customer Name:").grid(row=0, column=0, sticky="w", pady=8)
        self.customer_name = ttk.Entry(frame, width=40)
        self.customer_name.grid(row=0, column=1, pady=8)

        ttk.Label(frame, text="Phone Number:").grid(row=1, column=0, sticky="w", pady=8)
        self.customer_phone = ttk.Entry(frame, width=40)
        self.customer_phone.grid(row=1, column=1, pady=8)

        ttk.Label(frame, text="Email Address:").grid(row=2, column=0, sticky="w", pady=8)
        self.customer_email = ttk.Entry(frame, width=40)
        self.customer_email.grid(row=2, column=1, pady=8)

        ttk.Button(frame, text="Add Customer", command=self.add_customer).grid(
            row=3, column=0, columnspan=2, pady=18
        )

    def build_ticket_tab(self) -> None:
        frame = ttk.Frame(self.ticket_tab, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Customer ID:").grid(row=0, column=0, sticky="w", pady=8)
        self.ticket_customer_id = ttk.Entry(frame, width=40)
        self.ticket_customer_id.grid(row=0, column=1, pady=8)

        ttk.Label(frame, text="Device Type:").grid(row=1, column=0, sticky="w", pady=8)
        self.device_type = ttk.Entry(frame, width=40)
        self.device_type.grid(row=1, column=1, pady=8)

        ttk.Label(frame, text="Problem Description:").grid(row=2, column=0, sticky="w", pady=8)
        self.problem_description = ttk.Entry(frame, width=40)
        self.problem_description.grid(row=2, column=1, pady=8)

        ttk.Label(frame, text="Estimated Cost:").grid(row=3, column=0, sticky="w", pady=8)
        self.repair_cost = ttk.Entry(frame, width=40)
        self.repair_cost.grid(row=3, column=1, pady=8)

        ttk.Button(frame, text="Create Ticket", command=self.create_ticket).grid(
            row=4, column=0, columnspan=2, pady=18
        )

    def build_records_tab(self) -> None:
        frame = ttk.Frame(self.records_tab, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Customers", font=("Arial", 12, "bold")).pack(anchor="w")
        self.customer_list = tk.Listbox(frame, height=8)
        self.customer_list.pack(fill="x", pady=(5, 15))

        ttk.Label(frame, text="Repair Tickets", font=("Arial", 12, "bold")).pack(anchor="w")
        self.ticket_list = tk.Listbox(frame, height=12)
        self.ticket_list.pack(fill="both", expand=True, pady=(5, 10))

        status_frame = ttk.Frame(frame)
        status_frame.pack(fill="x", pady=5)

        ttk.Label(status_frame, text="Ticket ID:").pack(side="left")
        self.update_ticket_id = ttk.Entry(status_frame, width=8)
        self.update_ticket_id.pack(side="left", padx=5)

        ttk.Label(status_frame, text="New Status:").pack(side="left", padx=(10, 0))
        self.status_box = ttk.Combobox(
            status_frame,
            values=self.shop.status_options,
            state="readonly",
            width=15,
        )
        self.status_box.set("In Progress")
        self.status_box.pack(side="left", padx=5)

        ttk.Button(
            status_frame,
            text="Update Status",
            command=self.update_status,
        ).pack(side="left", padx=10)

    def add_customer(self) -> None:
        name = self.customer_name.get().strip()
        phone = self.customer_phone.get().strip()
        email = self.customer_email.get().strip()

        if not name or not phone or not email:
            messagebox.showerror("Missing Information", "Please complete all customer fields.")
            return

        customer = Customer(self.next_customer_id, name, phone, email)
        self.shop.add_customer(customer)
        self.next_customer_id += 1

        self.customer_name.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)

        self.refresh_records()
        messagebox.showinfo("Success", "Customer added successfully.")

    def create_ticket(self) -> None:
        try:
            customer_id = int(self.ticket_customer_id.get())
            cost_text = self.repair_cost.get().strip()
            cost = float(cost_text) if cost_text else 0.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Customer ID and cost must be numbers.")
            return

        device = self.device_type.get().strip()
        problem = self.problem_description.get().strip()

        if not device or not problem:
            messagebox.showerror("Missing Information", "Please enter the device and problem.")
            return

        ticket = RepairTicket(
            self.next_ticket_id,
            customer_id,
            device,
            problem,
            cost,
        )

        try:
            self.shop.create_ticket(ticket)
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        self.next_ticket_id += 1
        self.ticket_customer_id.delete(0, tk.END)
        self.device_type.delete(0, tk.END)
        self.problem_description.delete(0, tk.END)
        self.repair_cost.delete(0, tk.END)

        self.refresh_records()
        messagebox.showinfo("Success", "Repair ticket created successfully.")

    def update_status(self) -> None:
        try:
            ticket_id = int(self.update_ticket_id.get())
            self.shop.update_ticket_status(ticket_id, self.status_box.get())
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        self.update_ticket_id.delete(0, tk.END)
        self.refresh_records()
        messagebox.showinfo("Success", "Repair status updated.")

    def refresh_records(self) -> None:
        self.customer_list.delete(0, tk.END)
        for customer in self.shop.customers.values():
            self.customer_list.insert(tk.END, customer.display_info())

        self.ticket_list.delete(0, tk.END)
        for ticket in self.shop.get_all_tickets():
            self.ticket_list.insert(tk.END, ticket.display_ticket())


def main() -> None:
    root = tk.Tk()
    RepairShopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
