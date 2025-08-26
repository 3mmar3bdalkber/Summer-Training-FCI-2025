<h1 align="center"> Summer-Training-FCI-2025 — E-Commerce</h1>

<p align="center">
  A clean, modern, Arabic-first e-commerce website built with <strong>Python Flask</strong> for Summer Training (FCI 2025).<br/>
  Browse products, manage a cart, and place orders for electronics & accessories.
</p>

<p align="center">
  <!-- Shields -->
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-Framework-000000?logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://getbootstrap.com/"><img src="https://img.shields.io/badge/Bootstrap-Responsive-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap"></a>
  <img src="https://img.shields.io/badge/Database-SQLite%20%7C%20MySQL-4479A1?logo=mysql&logoColor=white" alt="DB">
  <img src="https://img.shields.io/badge/License-MIT-2ea44f" alt="License">
  <a href="https://github.com/your-username/Summer-Training-FCI-2025/stargazers"><img src="https://img.shields.io/github/stars/your-username/Summer-Training-FCI-2025?style=social" alt="Stars"></a>
</p>

<p align="center">
  <a href="#-live-demo">Demo</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#-contributors">Contributors</a>
</p>

---

##  Highlight Reel

-  **Arabic-first UX** with RTL layout.
-  **Products & categories**, with search and filters.
-  **Cart** (add / update / remove), **orders** flow.
-  **Responsive** (Bootstrap) — great on mobile/desktop.
-  **SQLite/MySQL** support via config.
-  Ready for **extensions** (auth, payments, admin).

---

## 🎬 Live Demo

 <img src="assets/demo.gif" width="100%"/> 

---

## Tech Stack

- **Backend:** Python (Flask), Jinja2  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript  
- **Database:** SQLite (default) or MySQL  
- **Tools:** Git/GitHub, virtualenv, pip  

---

## Project Structure

```bash
Summer-Training-FCI-2025/
├─ app.py
├─ routes.py
├─ requirements.txt
├─ requirements.txt
├─ .env.example
├─ templates/
│ ├─ about.html
│ ├─ base.html
│ ├─ cart.html
│ ├─ contact.html
│ ├─ index.html
│ ├─ login.html
│ ├─ products.html
│ ├─ profile.html
│ ├─ register.html
│ ├─ search_results.html
│ └─ wishlist_page.html
├─ static/ 
│ ├─ css/
│ ├─ js/
│ └─ uploads/
├─ assets/
│ ├─ demo.gif
└─ README.md
```
---

## Quickstart

```bash
# 1) Clone
git clone https://github.com/your-username/Summer-Training-FCI-2025.git
cd Summer-Training-FCI-2025

# 2) Create & activate venv
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Configure env
cp .env.example .env
# open .env and set SECRET_KEY and DATABASE_URL

# 5) Run
flask run
# open http://127.0.0.1:5000
```
---

## Roadmap
Authentication (signup/login)

Admin dashboard (CRUD products, orders)

Payments (Stripe/PayPal)

Inventory management

---

## 👥 Contributors

**Team Name** : **Mesh Sam3ak men El DP**

**Ammar Abdalkber** — Full Stack & Docs

**Ahmed Rabee** — front End

**Ahmed Khalifa** — Data Base

**Taha Sabry** — Testing

**Ahmed Khulf** — Ai Effectors

**Hazem Ali** — DB & Frontend

---

## 📄 License
MIT © 2025 — Summer Training FCI Team ( **Mesh Sam3ak men El DP**)

Summer Training — Faculty of Computers & Information (2025).
