<p align="center">
  <img src="assets/Banner.png" alt="Summer-Training-FCI-2025 – Flask E-Commerce (Arabic)" width="100%" />
</p>

<h1 align="center">🛒 Summer-Training-FCI-2025 — Arabic Flask E-Commerce</h1>

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
  <a href="#-features">Features</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-environment">Env</a> •
  <a href="#-docker">Docker</a> •
  <a href="#-api">API</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-contributors">Contributors</a>
</p>

---

## ✨ Highlight Reel

- 🇸🇦 **Arabic-first UX** with RTL layout.
- 🛍️ **Products & categories**, with search and filters.
- 🛒 **Cart** (add / update / remove), **orders** flow.
- 📱 **Responsive** (Bootstrap) — great on mobile/desktop.
- 🗄️ **SQLite/MySQL** support via config.
- 🧪 Ready for **extensions** (auth, payments, admin).

---

## 🎬 Live Demo

 <img src="assets/demo.gif" width="100%"/> 

---

## 📦 Tech Stack

- **Backend:** Python (Flask), Jinja2
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (default) or MySQL
- **Tools:** Git/GitHub, virtualenv, pip
---

## 📂 Project Structure

Summer-Training-FCI-2025/
├─ app.py # Flask app entry
├─ models.py # ORM/models (SQLAlchemy or raw)
├─ requirements.txt # Python deps
├─ .env.example # Sample environment variables
├─ templates/ # Jinja templates
│ ├─ base.html
│ ├─ index.html
│ ├─ product_detail.html
│ └─ cart.html
├─ static/ # CSS, JS, images for the site
│ ├─ css/
│ ├─ js/
│ └─ images/
├─ assets/ # README media (Banner.png, demo.gif)
└─ README.md

yaml
Copy
Edit

---

## ⚙️ Quickstart

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
🔧 Environment
Create .env using the sample:

ini
Copy
Edit
# .env.example
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=replace_with_a_secure_random_value

# Database (choose one)
# SQLite (default)
DATABASE_URL=sqlite:///app.db

# Or MySQL (example)
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/shopdb
Initialize DB (example):

bash
Copy
Edit
python -c "from models import init_db; init_db()"
Ensure models.py exposes init_db() or use your migration tool of choice.

🐳 Docker
bash
Copy
Edit
# Build
docker build -t summer-training-fci-2025 .

# Run (SQLite)
docker run -p 5000:5000 --env-file .env summer-training-fci-2025

# Run (MySQL)
docker run -p 5000:5000 \
  -e DATABASE_URL="mysql+pymysql://user:pass@host:3306/shopdb" \
  --env-file .env \
  summer-training-fci-2025
Optional Dockerfile:

dockerfile
Copy
Edit
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
☁️ Deployment Notes
PythonAnywhere: upload repo → set WSGI to app:app.

Render / Railway: set env vars and start command:

bash
Copy
Edit
flask run --host=0.0.0.0 --port=$PORT
Gunicorn (production):

bash
Copy
Edit
pip install gunicorn
gunicorn -w 3 -b 0.0.0.0:5000 app:app
🔌 API
If you expose JSON endpoints, document them here.

Method	Endpoint	Description	Body / Params	Response
GET	/api/products	List products	?q, ?category	200 OK
GET	/api/products/:id	Product details	:id	200 OK
POST	/api/cart	Add to cart	{ productId, qty }	201 Created
PATCH	/api/cart/:id	Update cart item quantity	{ qty }	200 OK
DELETE	/api/cart/:id	Remove cart item	—	204 No Content
POST	/api/orders	Place order	{ items, info }	201 Created

Sample JSON:

json
Copy
Edit
{
  "items": [
    { "productId": 1, "qty": 2 },
    { "productId": 7, "qty": 1 }
  ],
  "info": {
    "name": "أحمد",
    "phone": "01000000000",
    "address": "القاهرة"
  }
}
🧭 Architecture
mermaid
Copy
Edit
flowchart LR
  A[Client (RTL Arabic UI)] --> B[Flask Routes / Controllers]
  B --> C[Jinja Templates]
  B --> D[Service Layer]
  D --> E[(Database)]
  B --> F[REST API (JSON)]
  F --> A
ERD (simplified):

mermaid
Copy
Edit
erDiagram
  PRODUCT ||--o{ CART_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : includes
  ORDER }o--o{ ORDER_ITEM : consists_of
  USER ||--o{ ORDER : places

  PRODUCT {
    int id PK
    string name
    string slug
    string image_url
    string category
    float price
    int stock
  }

  USER {
    int id PK
    string name
    string phone
    string address
  }

  ORDER {
    int id PK
    int user_id FK
    string status
    datetime created_at
    float total
  }

  ORDER_ITEM {
    int id PK
    int order_id FK
    int product_id FK
    int qty
    float unit_price
  }

  CART_ITEM {
    int id PK
    int product_id FK
    int qty
    string session_id
  }
🧰 Scripts
bash
Copy
Edit
# Lint (choose one and add to requirements)
ruff check . || flake8 .

# Format
black .

# Run dev server
flask run
🐞 Troubleshooting
404 for static image
Ensure file exists under static/ and reference with:
{{ url_for('static', filename='images/yourfile.jpg') }}

DB connection errors
Check DATABASE_URL and initialize/migrate the DB.

Arabic/RTL issues
Add dir="rtl" on <html> and consider Bootstrap RTL if needed.

🗺️ Roadmap
 Authentication (signup/login)

 Admin dashboard (CRUD products, orders)

 Payments (Stripe/PayPal)

 Inventory management

 Arabic ↔ English toggle (i18n)

👥 Contributors
Ahmed Khalifa — Backend

Hazem Ali — DB & Frontend

Ammar Abdalkber — Full Stack & Docs

Want to contribute? Open an issue or PR.

📄 License
MIT © 2025 — Summer Training FCI Team
Feel free to use and modify for educational purposes.

🙏 Acknowledgements
Flask, Bootstrap, Jinja2, and the open-source community.
Summer Training — Faculty of Computers & Information (2025).

markdown
Copy
Edit

### 📎 Asset notes (so everything renders)
- Put your banner at: `assets/Banner.png` (exact case).
- Put your GIF at: `assets/demo.gif`.
- Commit them together:
  ```bash
  git add assets/Banner.png assets/demo.gif README.md
  git commit -m "Add banner and demo GIF + full README"
  git push origin main
