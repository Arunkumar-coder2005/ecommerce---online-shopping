# ShopUniq — Django E-Commerce Project
### Built with: Python + Django + MySQL + HTML + CSS

---

## STEP 1 — Install Requirements

Open terminal / command prompt inside the `shopuniq` folder:

```
pip install -r requirements.txt
```

---

## STEP 2 — Setup MySQL Database

Open MySQL (XAMPP or MySQL Workbench) and run:

```sql
CREATE DATABASE shopuniq_db;
```

Then open `shopuniq/settings.py` and update:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopuniq_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',   # ← change this
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## STEP 3 — Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

## STEP 4 — Create Admin User

```
python manage.py createsuperuser
```

Enter username, email, and password.

---

## STEP 5 — Run the Server

```
python manage.py runserver
```

Open browser → http://127.0.0.1:8000/

Admin panel → http://127.0.0.1:8000/admin/

---

## PROJECT STRUCTURE

```
shopuniq/
├── manage.py
├── requirements.txt
├── shopuniq/
│   ├── settings.py       ← Database config here
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── models.py         ← Database tables
    ├── views.py          ← Page logic
    ├── urls.py           ← URL routes
    ├── admin.py          ← Admin panel setup
    ├── context_processors.py
    ├── templates/store/
    │   ├── base.html         ← Navbar + Footer
    │   ├── home.html         ← Home page
    │   ├── product_list.html ← All products
    │   ├── product_detail.html
    │   ├── cart.html
    │   ├── checkout.html
    │   ├── order_detail.html
    │   ├── my_orders.html
    │   ├── login.html
    │   ├── register.html
    │   └── profile.html
    └── static/store/
        ├── css/style.css
        └── js/main.js
```

---

## ADDING PRODUCTS (via Admin Panel)

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. First add Categories (e.g., Electronics, Fashion, Books)
4. Then add Products with name, price, image, stock

---

## PAGES / URLS

| URL | Page |
|-----|------|
| / | Home |
| /products/ | All Products |
| /products/?category=electronics | Filter by category |
| /products/?q=phone | Search |
| /product/phone-name/ | Product Detail |
| /cart/ | Shopping Cart |
| /checkout/ | Checkout |
| /my-orders/ | Order History |
| /login/ | Login |
| /register/ | Register |
| /profile/ | Profile |
| /admin/ | Admin Panel |
