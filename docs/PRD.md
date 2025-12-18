# Product Requirements Document (PRD)

## 1. Product Goal
The main objective of INJOO is to provide a simple, fast, and reliable food ordering and delivery platform that connects customers, restaurants, and couriers in a single system, automating order management and delivery workflows.

---

## 2. Problem Statement
Many small and medium restaurants lack an efficient digital system for accepting online orders, managing order statuses, and coordinating with couriers. Existing solutions are often expensive, complex, or poorly adapted to local workflows. Customers also face issues with unclear order status and slow communication.

INJOO solves these problems by offering a centralized platform with real-time order tracking and role-based access.

---

## 3. Target Audience
The target audience includes:
- Customers who want to order food online
- Restaurants that need an order management system
- Kitchen staff preparing orders
- Couriers delivering orders
- Platform administrators

---

## 4. User Roles
- **Customer** — browses menu, places orders, tracks order status  
- **Kitchen Staff** — receives orders, updates preparation status  
- **Courier** — receives delivery tasks and confirms delivery  
- **Administrator** — manages users, dishes, orders, and system settings  

---

## 5. User Scenarios
- A **customer** opens the website, browses dishes, places an order, and tracks its status.
- **Kitchen staff** receives a new order notification, prepares the order, and marks it as ready.
- A **courier** receives the order, delivers it to the customer, and marks it as delivered.
- An **administrator** manages dishes, categories, users, and monitors platform activity.

---

## 6. Functional Requirements
The system must:
1. Allow users to register and authenticate.
2. Allow customers to browse dishes and place orders.
3. Support order status lifecycle (created → accepted → ready → delivered).
4. Allow kitchens to accept and prepare orders.
5. Allow couriers to receive and complete deliveries.
6. Provide an admin panel for managing users, dishes, and orders.
7. Send notifications via Telegram bot for order updates.

---

## 7. Non-Functional Requirements
The system must satisfy:
- **performance:** API responses should be under 500ms for standard requests.
- **reliability:** The system should handle failures without data loss.
- **security:** Secure authentication, role-based access, and protected APIs.
- **usability:** Simple and intuitive UI for all user roles.
- **scalability:** Ability to support increased users and orders with minimal changes.

---

## 8. MVP Scope
Features that must enter version 0.1:
- User authentication and role management
- Dish catalog with categories
- Order creation and status tracking
- Kitchen and courier order workflows
- Admin panel (basic CRUD)
- Telegram notifications for orders

---

## 9. Out-of-Scope (Backlog)
Features that do not enter MVP:
- Online payments
- Mobile applications (iOS / Android)
- Ratings and reviews
- Loyalty programs and promo codes
- Multi-restaurant marketplace support

---

## 10. Acceptance Criteria
Clear and testable criteria for each feature:

- **User Authentication:**  
  - Users can register, log in, and log out successfully.
  - Unauthorized users cannot access protected endpoints.

- **Order Management:**  
  - Customers can create orders.
  - Orders change status according to the workflow.
  - Each role can only perform allowed actions.

- **Admin Panel:**  
  - Admin can create, update, and delete dishes and users.
  - Changes are reflected immediately in the system.

