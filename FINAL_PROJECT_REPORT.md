# Final Project Report

## Client
Manny's Computer Repair, a small local computer repair business.

## Purpose
The system organizes customer information and repair jobs in one graphical application.

## Scope
The program adds, updates, searches, and deletes customers; creates and updates repair tickets; tracks status and cost; displays reports; and saves data. It does not include online payments, employee accounts, inventory, or mobile access so the scope remains realistic for an eight-week course.

## Classes
- Customer: stores customer information.
- RepairTicket: stores repair information.
- RepairShop: manages customer and ticket collections.
- DataStorage: saves and loads JSON data.

## Sample Output
```text
MANNY'S COMPUTER REPAIR
FINAL PROJECT REPORT
Customers: 1
Tickets: 1
Waiting: 0 | In Progress: 1 | Completed: 0

Customer #1: Alex Smith | 555-0100 | alex@example.com
Ticket #1 | Customer: Alex Smith | Device: Laptop | Problem: Will not start | Status: In Progress | Cost: $95.00
```

## Testing
The included unit tests cover customer creation, ticket creation and updates, invalid customer handling, completed-ticket deletion, and saving/loading data.
