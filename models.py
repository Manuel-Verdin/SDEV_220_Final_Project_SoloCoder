class Customer:
    """Stores information about one repair-shop customer."""

    def __init__(self, customer_id: int, name: str, phone: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    def update_contact(self, phone: str, email: str) -> None:
        self.phone = phone
        self.email = email

    def display_info(self) -> str:
        return f"{self.customer_id}: {self.name} | {self.phone} | {self.email}"


class RepairTicket:
    """Stores information about one computer repair job."""

    VALID_STATUSES = ("Waiting", "In Progress", "Completed")

    def __init__(
        self,
        ticket_id: int,
        customer_id: int,
        device_type: str,
        problem_description: str,
        repair_cost: float = 0.0,
        status: str = "Waiting",
    ):
        self.ticket_id = ticket_id
        self.customer_id = customer_id
        self.device_type = device_type
        self.problem_description = problem_description
        self.repair_cost = repair_cost
        self.status = status if status in self.VALID_STATUSES else "Waiting"

    def update_status(self, new_status: str) -> None:
        if new_status not in self.VALID_STATUSES:
            raise ValueError("Invalid repair status.")
        self.status = new_status

    def display_ticket(self) -> str:
        return (
            f"Ticket #{self.ticket_id} | Customer #{self.customer_id} | "
            f"{self.device_type} | {self.problem_description} | "
            f"{self.status} | ${self.repair_cost:.2f}"
        )


class RepairShop:
    """Manages all customers and repair tickets."""

    def __init__(self):
        self.customers = {}          # Dictionary: customer ID -> Customer
        self.repair_tickets = []     # List of RepairTicket objects
        self.status_options = RepairTicket.VALID_STATUSES  # Tuple

    def add_customer(self, customer: Customer) -> None:
        self.customers[customer.customer_id] = customer

    def create_ticket(self, ticket: RepairTicket) -> None:
        if ticket.customer_id not in self.customers:
            raise ValueError("Customer ID does not exist.")
        self.repair_tickets.append(ticket)

    def search_customer(self, customer_id: int):
        return self.customers.get(customer_id)

    def find_ticket(self, ticket_id: int):
        for ticket in self.repair_tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def update_ticket_status(self, ticket_id: int, new_status: str) -> None:
        ticket = self.find_ticket(ticket_id)
        if ticket is None:
            raise ValueError("Repair ticket was not found.")
        ticket.update_status(new_status)

    def get_all_tickets(self):
        return self.repair_tickets
