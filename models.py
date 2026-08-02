from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, List, Optional, Tuple

@dataclass
class Customer:
    customer_id: int
    name: str
    phone: str
    email: str

    def update_contact(self, phone: str, email: str) -> None:
        self.phone = phone.strip()
        self.email = email.strip()

    def display_info(self) -> str:
        return f"Customer #{self.customer_id}: {self.name} | {self.phone} | {self.email}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        return cls(int(data["customer_id"]), str(data["name"]), str(data["phone"]), str(data["email"]))

@dataclass
class RepairTicket:
    VALID_STATUSES: ClassVar[Tuple[str, ...]] = ("Waiting", "In Progress", "Completed")
    ticket_id: int = 0
    customer_id: int = 0
    device_type: str = ""
    problem_description: str = ""
    repair_cost: float = 0.0
    status: str = "Waiting"

    def __post_init__(self) -> None:
        if self.status not in self.VALID_STATUSES:
            raise ValueError("Invalid repair status.")
        if self.repair_cost < 0:
            raise ValueError("Repair cost cannot be negative.")

    def update_status(self, new_status: str) -> None:
        if new_status not in self.VALID_STATUSES:
            raise ValueError("Invalid repair status.")
        self.status = new_status

    def update_cost(self, new_cost: float) -> None:
        if new_cost < 0:
            raise ValueError("Repair cost cannot be negative.")
        self.repair_cost = float(new_cost)

    def display_ticket(self, customer_name: str = "") -> str:
        owner = f" | Customer: {customer_name}" if customer_name else ""
        return (f"Ticket #{self.ticket_id}{owner} | Device: {self.device_type} | "
                f"Problem: {self.problem_description} | Status: {self.status} | "
                f"Cost: ${self.repair_cost:.2f}")

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "customer_id": self.customer_id,
            "device_type": self.device_type,
            "problem_description": self.problem_description,
            "repair_cost": self.repair_cost,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RepairTicket":
        return cls(int(data["ticket_id"]), int(data["customer_id"]), str(data["device_type"]),
                   str(data["problem_description"]), float(data.get("repair_cost", 0.0)),
                   str(data.get("status", "Waiting")))

class RepairShop:
    STATUS_OPTIONS: Tuple[str, ...] = RepairTicket.VALID_STATUSES

    def __init__(self) -> None:
        self.customers: Dict[int, Customer] = {}
        self.repair_tickets: List[RepairTicket] = []
        self.next_customer_id = 1
        self.next_ticket_id = 1

    def add_customer(self, name: str, phone: str, email: str) -> Customer:
        name, phone, email = name.strip(), phone.strip(), email.strip()
        if not name or not phone or not email:
            raise ValueError("Name, phone, and email are required.")
        customer = Customer(self.next_customer_id, name, phone, email)
        self.customers[customer.customer_id] = customer
        self.next_customer_id += 1
        return customer

    def update_customer(self, customer_id: int, name: str, phone: str, email: str) -> Customer:
        customer = self.get_customer(customer_id)
        if customer is None:
            raise ValueError("Customer was not found.")
        name, phone, email = name.strip(), phone.strip(), email.strip()
        if not name or not phone or not email:
            raise ValueError("Name, phone, and email are required.")
        customer.name = name
        customer.update_contact(phone, email)
        return customer

    def delete_customer(self, customer_id: int) -> None:
        if customer_id not in self.customers:
            raise ValueError("Customer was not found.")
        if any(t.customer_id == customer_id for t in self.repair_tickets):
            raise ValueError("Delete this customer's repair tickets first.")
        del self.customers[customer_id]

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.customers.get(customer_id)

    def search_customers(self, text: str) -> List[Customer]:
        text = text.strip().lower()
        if not text:
            return list(self.customers.values())
        return [c for c in self.customers.values() if text in c.name.lower() or text in c.phone.lower() or text in c.email.lower() or text == str(c.customer_id)]

    def create_ticket(self, customer_id: int, device_type: str, problem: str, cost: float = 0.0) -> RepairTicket:
        if customer_id not in self.customers:
            raise ValueError("The selected customer does not exist.")
        device_type, problem = device_type.strip(), problem.strip()
        if not device_type or not problem:
            raise ValueError("Device type and problem description are required.")
        ticket = RepairTicket(self.next_ticket_id, customer_id, device_type, problem, float(cost), "Waiting")
        self.repair_tickets.append(ticket)
        self.next_ticket_id += 1
        return ticket

    def get_ticket(self, ticket_id: int) -> Optional[RepairTicket]:
        return next((t for t in self.repair_tickets if t.ticket_id == ticket_id), None)

    def update_ticket(self, ticket_id: int, status: str, cost: float) -> RepairTicket:
        ticket = self.get_ticket(ticket_id)
        if ticket is None:
            raise ValueError("Repair ticket was not found.")
        ticket.update_status(status)
        ticket.update_cost(cost)
        return ticket

    def delete_ticket(self, ticket_id: int, completed_only: bool = True) -> None:
        ticket = self.get_ticket(ticket_id)
        if ticket is None:
            raise ValueError("Repair ticket was not found.")
        if completed_only and ticket.status != "Completed":
            raise ValueError("Only completed tickets can be deleted.")
        self.repair_tickets.remove(ticket)

    def search_tickets(self, text: str) -> List[RepairTicket]:
        text = text.strip().lower()
        if not text:
            return list(self.repair_tickets)
        results = []
        for ticket in self.repair_tickets:
            customer = self.get_customer(ticket.customer_id)
            haystack = " ".join([str(ticket.ticket_id), str(ticket.customer_id), customer.name.lower() if customer else "", ticket.device_type.lower(), ticket.problem_description.lower(), ticket.status.lower()])
            if text in haystack:
                results.append(ticket)
        return results

    def get_ticket_summary(self) -> Dict[str, int]:
        summary = {status: 0 for status in self.STATUS_OPTIONS}
        for ticket in self.repair_tickets:
            summary[ticket.status] += 1
        return summary

    def to_dict(self) -> dict:
        return {
            "customers": [c.to_dict() for c in sorted(self.customers.values(), key=lambda x: x.customer_id)],
            "repair_tickets": [t.to_dict() for t in sorted(self.repair_tickets, key=lambda x: x.ticket_id)],
            "next_customer_id": self.next_customer_id,
            "next_ticket_id": self.next_ticket_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RepairShop":
        shop = cls()
        for item in data.get("customers", []):
            customer = Customer.from_dict(item)
            shop.customers[customer.customer_id] = customer
        shop.repair_tickets = [RepairTicket.from_dict(item) for item in data.get("repair_tickets", [])]
        shop.next_customer_id = max(int(data.get("next_customer_id", 1)), max(shop.customers.keys(), default=0) + 1)
        shop.next_ticket_id = max(int(data.get("next_ticket_id", 1)), max((t.ticket_id for t in shop.repair_tickets), default=0) + 1)
        return shop
