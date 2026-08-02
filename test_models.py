import tempfile
import unittest
from pathlib import Path
from models import RepairShop
from storage import DataStorage

class RepairShopTests(unittest.TestCase):
    def setUp(self):
        self.shop = RepairShop()
        self.customer = self.shop.add_customer("Alex Smith", "555-0100", "alex@example.com")

    def test_add_customer(self):
        self.assertEqual(len(self.shop.customers), 1)

    def test_create_and_update_ticket(self):
        ticket = self.shop.create_ticket(1, "Laptop", "Will not start", 75)
        self.shop.update_ticket(ticket.ticket_id, "In Progress", 95)
        self.assertEqual(ticket.status, "In Progress")
        self.assertEqual(ticket.repair_cost, 95)

    def test_invalid_customer(self):
        with self.assertRaises(ValueError):
            self.shop.create_ticket(999, "Desktop", "No display", 40)

    def test_completed_ticket_deletion(self):
        ticket = self.shop.create_ticket(1, "Phone", "Broken screen", 120)
        with self.assertRaises(ValueError):
            self.shop.delete_ticket(ticket.ticket_id)
        self.shop.update_ticket(ticket.ticket_id, "Completed", 120)
        self.shop.delete_ticket(ticket.ticket_id)
        self.assertEqual(len(self.shop.repair_tickets), 0)

    def test_save_and_load(self):
        self.shop.create_ticket(1, "Laptop", "Battery", 80)
        with tempfile.TemporaryDirectory() as folder:
            storage = DataStorage(Path(folder) / "data.json")
            storage.save(self.shop)
            loaded = storage.load()
        self.assertEqual(len(loaded.customers), 1)
        self.assertEqual(len(loaded.repair_tickets), 1)

if __name__ == "__main__":
    unittest.main()
