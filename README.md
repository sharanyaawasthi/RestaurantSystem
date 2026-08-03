# CS4092 - Database Design and Development: Final Project
## Requirements Document: Online Restaurant & Delivery System

**Course:** CS4092 - Database Design and Development (Summer 2026)  
**Project Title:** Online Restaurant & Delivery System  
**Author:** Student / Team Submission  

---

### 1. Project Overview & Motivation

For my final database project, I wanted to build something practical that mimics a real-world application people use every day—an online restaurant ordering and delivery management system. In a fast-paced food service environment, keeping customer data, address records, menu items, order history, and staff management in sync can easily become chaotic without a well-structured relational database behind it.

My goal with this project was to design a robust MySQL database backend coupled with an intuitive Python command-line interface (CLI). The application cleanly separates two primary user roles: **Customers** (who need to sign up, log in, browse items, build multi-item orders, and check their order history) and **Staff Members** (who manage the menu, update live delivery statuses, and track overall sales statistics).

By structuring the backend into six normalized tables with strict primary/foreign key relationships, the system ensures data integrity, prevents duplicate customer registrations, calculates billing accurately, and delivers real-time business insights for restaurant operations.

---

### 2. User Roles & Detailed Use Cases

The system supports two distinct roles: Customers and Staff. Here is how each user interacts with the system:

#### A. Customer Use Cases

1. **Customer Registration (Sign Up)**
   - *Description:* A new customer creates an account by entering their full name, unique email address, and phone number.
   - *Data Flow:* The system saves the profile in the `Customers` table, generates an auto-incremented `customer_id`, and immediately prompts for their delivery address (`street_address`, `city`, `state`, `zip_code`) to save in the `Addresses` table.
   - *Outcome:* The customer receives their generated `customer_id`, which serves as their key to sign in later.

2. **Customer Sign In**
   - *Description:* Existing customers sign in using their unique `customer_id`.
   - *Outcome:* The system validates the ID against the database. If valid, the customer enters the personalized Customer Portal.

3. **Menu Browsing**
   - *Description:* Customers can view all currently available food and beverage items.
   - *Outcome:* Displays a clean menu list showing each item's `item_id`, `item_name`, `category`, and `price`.

4. **Multi-Item Order Placement**
   - *Description:* Customers can build a complete order in a single session.
   - *Data Flow:*
     - The customer selects a saved delivery address ID.
     - The system creates a new record in `Orders` with initial status `'Placed'`.
     - In an interactive loop, the customer inputs a `item_id` and `quantity`. The item is logged into `OrderItems`, and the running total cost is updated.
     - The system asks if they want to add more items (`y/n`). Once finished, the transaction commits.
   - *Outcome:* The customer sees their assigned `order_id` and the final total bill cost.

5. **Order History & Tracking**
   - *Description:* Customers can check the progress and past records of all orders placed under their account.
   - *Outcome:* Displays order IDs, timestamps, item details, calculated totals, and live statuses (e.g., `Placed`, `Preparing`, `Out for Delivery`, `Completed`).

---

#### B. Staff & Admin Use Cases

1. **Staff Sign In & Registration**
   - *Description:* Staff members sign in using their assigned `staff_id`.
   - *Outcome:* If the ID exists, they are logged into the Staff Portal. If an unrecognized ID is entered, the system seamlessly prompts for their full name and role to register them into the `Staff` table and outputs their new `staff_id`.

2. **Menu Management (Add Items)**
   - *Description:* Staff members can expand the restaurant menu by adding new food items.
   - *Outcome:* Prompts for item name, category (e.g., Main, Appetizer, Dessert), and unit price, inserting the entry into `MenuItems`.

3. **Live Order Status Updates**
   - *Description:* Staff members manage restaurant operations by updating the progress of orders.
   - *Outcome:* Displays recent customer orders and allows staff to change an order's status from `'Placed'` to `'Preparing'`, `'Out for Delivery'`, or `'Completed'`.

4. **Sales Statistics & Business Analytics**
   - *Description:* Staff members monitor financial performance and item popularity.
   - *Outcome:* Performs SQL aggregation queries to display:
     - **Total Revenue Collected:** The sum of all ordered item prices multiplied by quantities across all orders.
     - **Most Purchased Item:** The top-selling menu item based on total units sold.

---

### 3. Data Requirements & Database Schema Design

To fulfill these use cases without data redundancy, the system uses **6 relational tables**:

1. **`Customers`**
   - Stores customer contact details.
   - *Attributes:* `customer_id` (PK, Auto-Increment), `full_name`, `email` (UNIQUE), `phone_nb`.

2. **`Addresses`**
   - Stores customer delivery addresses (1-to-Many relationship with `Customers`).
   - *Attributes:* `address_id` (PK, Auto-Increment), `customer_id` (FK -> `Customers`), `address_label`, `street_address`, `city`, `state`, `zip_code`.

3. **`Staff`**
   - Stores restaurant employee details.
   - *Attributes:* `staff_id` (PK, Auto-Increment), `full_name`, `staff_role`.

4. **`MenuItems`**
   - Stores food and beverage inventory.
   - *Attributes:* `item_id` (PK, Auto-Increment), `item_name`, `category`, `price`, `is_available`.

5. **`Orders`**
   - Header table for orders placed by customers.
   - *Attributes:* `order_id` (PK, Auto-Increment), `customer_id` (FK -> `Customers`), `address_id` (FK -> `Addresses`), `staff_id` (FK -> `Staff`, Nullable), `order_date` (Timestamp), `order_status`.

6. **`OrderItems`**
   - Junction line-item table connecting orders to menu items (Many-to-Many resolution).
   - *Attributes:* `order_item_id` (PK, Auto-Increment), `order_id` (FK -> `Orders`), `item_id` (FK -> `MenuItems`), `quantity` (CHECK quantity > 0).

---

### 4. Technical Requirements & Implementation Details

- **Database Engine:** MySQL 8.0+ Relational Database Management System.
- **Application Language:** Python 3.12 utilizing `mysql.connector`.
- **User Interface:** Interactive Command Line Interface (CLI).
- **Data Integrity:** Enforced via Foreign Keys with `ON DELETE CASCADE`, `UNIQUE` constraints on emails, and explicit SQL transactions (`db.commit()`).
