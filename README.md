# 🍔✨ INJOO — Smart Food Ordering & Delivery Platform

> **INJOO** is a modern food ordering and delivery ecosystem built for **customers**, **restaurants**, and **delivery staff**.
> Fast. Clear. Automated. Delicious. 😋

---

## 🌈 Overview

**INJOO** streamlines the entire food ordering lifecycle — from browsing dishes to delivery confirmation.

### 🚀 What problems does INJOO solve?

✅ **For customers**

* Easy dish browsing with images 🍕
* Simple and fast ordering 🛒
* Real-time order status tracking ⏱️

✅ **For restaurants**

* Automated order flow (accepted → ready → delivered)
* Centralized menu & order management
* Less manual work, fewer mistakes

✅ **For admins**

* Full control over users, dishes, and orders
* Clear role-based system
* Scalable backend architecture

---

## 🎯 Key Features

* 📱 User-friendly web interface
* 🔐 Authentication & role-based access
* 🍽️ Dish & category management
* 📦 Order lifecycle tracking
* 🤖 Telegram bot integration for kitchen & couriers
* 🐳 Fully Dockerized setup

---

## 🧱 Tech Stack

### 🎨 Frontend

* ⚡ **Vue.js (Vite)**
* 🎨 **Tailwind CSS**
* 🔄 **Axios**

### ⚙️ Backend

* 🚀 **FastAPI**
* 🐍 **Python**
* 🗄️ **SQLAlchemy**
* 🔗 **REST API**

### 🗃️ Database

* 🐘 **PostgreSQL** (production)

### 🧰 DevOps & Tools

* 🐳 Docker & Docker Compose
* 🌐 Nginx (reverse proxy)
* 🤖 Telegram Bot API
* 🧠 Git & GitHub

---

## 🗂️ Project Structure

```text
INJOO/
├── backend/           # FastAPI backend source code
├── frontend/          # Vue.js frontend source code
├── docs/              # Documentation & diagrams
├── uploaded_images/   # Uploaded dish images
├── ssl/               # HTTPS certificates & configs
└── docker-compose.yml
```

---

## ▶️ How to Run the Project

### 🧩 System Requirements

* 🐳 Docker & Docker Compose
* 🐍 Python **3.10+**
* 🟢 Node.js **18+**
* 🔧 Git

---

### ⚡ Installation Steps

1️⃣ **Clone the repository**

```bash
git clone https://github.com/IlyasNartay/INJOOdep.git
cd INJOOdep
```

2️⃣ **Run with Docker**

```bash
docker compose up -d --build
```

3️⃣ **Open in browser** 🌍

```text
Frontend: https://injoo.kz
Backend API: https://server.injoo.kz
```
P.S.

⚠️ This project can only run on the server that has the proper DNS configuration.

⚡ If you make changes to the backend code, rebuild the Docker containers to apply updates.

🔧 Ensure .env file matches the server setup, otherwise services may not work correctly.

---

## 🧠 Architecture Highlights

* 🔄 RESTful API communication
* 🔐 JWT-based authentication
* 🧩 Modular backend structure
* 📦 Clean separation of frontend & backend

---

## 🌟 Future Plans

* 📊 Admin dashboard analytics
* 📱 Mobile-friendly PWA
* 💳 Online payments integration
* 🔔 Push notifications

---

## 👨‍💻 Authors

**Nartay Iliyas**
🎓 Computer Science Student
🚀 Backend Developer

📎 GitHub: [https://github.com/IlyasNartay](https://github.com/IlyasNartay)

**Bolekbay Alisher**
🎓 Computer Science Student
🚀 Frontend Developer

📎 GitHub: [https://github.com/AlisherB-01](https://github.com/AlisherB-01)

**Lazarev Alikhan**
🎓 Computer Science Student
🚀 Tester | Project Manager  

📎 GitHub: [https://github.com/AlisherB-01](https://github.com/AlisherB-01)

---

## 💙 Final Note

INJOO is not just MVP — it’s a **production‑ready foundation** for a real food delivery business.

If you like it — ⭐ star the repo(private) and feel free to contribute!

🍜 Happy coding & bon appétit!