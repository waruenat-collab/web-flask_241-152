# web-flask_241-152

# 🍽️ Food Review Website (Flask)

โปรเจกต์เว็บไซต์รีวิวร้านอาหาร พัฒนาด้วย **Flask Framework**  
ผู้ใช้สามารถสมัครสมาชิก, เพิ่มร้านอาหาร, ให้คะแนนรีวิว และดูข้อมูลโปรไฟล์ผู้ใช้  
จัดทำขึ้นเพื่อใช้ส่งงานรายวิชา Web Programming

---

## 📌 Features (ความสามารถของระบบ)

### 👤 ระบบผู้ใช้ (User System)
- สมัครสมาชิก (Register)
- เข้าสู่ระบบ / ออกจากระบบ (Login / Logout)
- เก็บข้อมูลผู้ใช้ในฐานข้อมูล
- หน้า Profile แสดงข้อมูลผู้ใช้จริง

### 🍴 ร้านอาหาร (Restaurant)
- เพิ่มร้านอาหารใหม่ (เฉพาะผู้ที่ Login)
- แสดงร้านอาหารทั้งหมด
- ค้นหาร้านอาหาร
- ดูรายละเอียดร้านอาหาร
- ลบร้านอาหารได้ **เฉพาะผู้ที่เคยรีวิวร้านนั้น**

### ⭐ รีวิว (Review)
- ให้คะแนนร้านอาหาร (1–5 ดาว)
- แก้ไขคะแนนรีวิวได้
- ดูรีวิวของตัวเอง (My Reviews)
- ดูรีวิวล่าสุด (Recent Reviews)

### 🏆 ระบบเสริม (Advanced Features)
- หน้า Top Restaurants (ร้านคะแนนสูงสุด)
- ระบบ Badge / Level ผู้ใช้ (จากจำนวนรีวิว)
  - 🥚 Newbie (0 รีวิว)
  - 🍔 Food Lover (1–3 รีวิว)
  - ⭐ Critic (4–6 รีวิว)
  - 🏆 Master Reviewer (7+ รีวิว)

---

## 🌐 Pages (หน้าเว็บทั้งหมด)

มีหน้าเว็บมากกว่า **10 หน้า** ตามข้อกำหนดอาจารย์

| หน้าเว็บ | URL |
|------|------|
Home | `/`
Restaurants | `/restaurants`
Restaurant Detail | `/restaurants/<id>`
Add Restaurant | `/add-restaurant`
My Reviews | `/my-reviews`
Profile | `/profile`
Top Restaurants | `/top-restaurants`
Recent Reviews | `/recent-reviews`
Login | `/login`
Register | `/register`
Logout | `/logout`

---

## 🛠️ Tech Stack

- Backend: Flask (Python)
- Frontend: HTML + Bootstrap 5
- Database: SQLite
- ORM: SQLAlchemy
- Authentication: Session + Werkzeug
- Version Control: Git & GitHub

---

## 🗂️ Database Structure

### User
- id
- username
- password_hash

### Restaurant
- id
- name
- location
- description

### Review
- id
- rating
- restaurant_id
- user_id

**Relationships**
- User 1 คน → รีวิวได้หลายร้าน
- Restaurant 1 ร้าน → มีหลายรีวิว

---

## 🧠 Code Explanation (อธิบายโค้ด)

📁 โครงสร้างโปรเจกต์
web-flask_241-152/
│
├── app.py                  # ไฟล์หลักของ Flask
├── food.db                 # ฐานข้อมูล SQLite
├── README.md               # เอกสารอธิบายโปรเจกต์
├── requirements.txt        # รายการ library ที่ใช้
│
├── templates/              # HTML Templates (Jinja2)
│   ├── base.html
│   ├── navbar.html
│   ├── home.html
│   ├── restaurants.html
│   ├── restaurant_detail.html
│   ├── add_restaurant.html
│   ├── my_reviews.html
│   ├── profile.html
│   ├── top_restaurants.html
│   ├── recent_reviews.html
│   ├── login.html
│   └── register.html
│
└── venv/                   # Virtual Environment
⚙️ app.py (ไฟล์หลักของระบบ)
1️⃣ App Configuration
app = Flask(__name__)
app.secret_key = "day8-secret-key"

สร้าง Flask application

ใช้ secret_key สำหรับ session (login)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food.db"

ใช้ SQLite เป็นฐานข้อมูล

เหมาะกับโปรเจกต์ขนาดเล็ก–กลาง และการเรียนรู้

2️⃣ Database Models (Models)
🏪 Restaurant
class Restaurant(db.Model):

เก็บข้อมูลร้านอาหาร

name : ชื่อร้าน

location : ที่ตั้ง

description : รายละเอียดร้าน

เชื่อมกับ Review แบบ One-to-Many

มี method:

def avg_rating(self)

ใช้คำนวณคะแนนเฉลี่ยของร้าน

👤 User
class User(db.Model):

เก็บข้อมูลผู้ใช้

username

password_hash (เข้ารหัสด้วย werkzeug)

เชื่อมกับ Review

มี method:

set_password() → เข้ารหัสรหัสผ่าน

check_password() → ตรวจสอบรหัสผ่าน

⭐ Review
class Review(db.Model):

เก็บข้อมูลรีวิว

rating : คะแนน (1–5)

restaurant_id

user_id

ใช้เชื่อมความสัมพันธ์ระหว่าง User และ Restaurant

3️⃣ Authentication System (ระบบ Login/Register)

/register → สมัครสมาชิก

/login → เข้าสู่ระบบ

/logout → ออกจากระบบ

ใช้ session เก็บ user_id และ username

session["user_id"]

ใช้ตรวจสอบสถานะ login

4️⃣ Restaurant System
📄 /restaurants

แสดงร้านทั้งหมด

รองรับการค้นหา

เรียงร้านที่มีรีวิวมากก่อน

📄 /restaurants/<id>

แสดงรายละเอียดร้าน

แสดงคะแนนเฉลี่ย

ผู้ใช้สามารถเพิ่ม / แก้ไขรีวิวของตนเอง

➕ /add-restaurant

เพิ่มร้านอาหาร (เฉพาะผู้ที่ login)

❌ /restaurants/<id>/delete

ลบร้านได้เฉพาะผู้ที่เคยรีวิวร้านนั้น

5️⃣ Review System

ผู้ใช้ 1 คน รีวิวร้านเดิมได้ 1 ครั้ง

หากรีวิวซ้ำ จะเป็นการอัปเดตคะแนน

หน้า /my-reviews แสดงรีวิวของผู้ใช้คนนั้นเท่านั้น

6️⃣ Profile Page + Badge System

หน้า /profile แสดง:

Username

จำนวนรีวิว

คะแนนเฉลี่ย

Badge / Level ของผู้ใช้

🎖️ ระบบ Badge:

จำนวนรีวิว	Badge
0	🥚 Newbie
1–3	🍔 Food Lover
4–6	⭐ Critic
7+	🏆 Master Reviewer

ไม่ต้องเพิ่ม table ใหม่
คำนวณจากจำนวน Review ที่มีอยู่

7️⃣ Extra Pages (เพิ่มความสมบูรณ์)

/top-restaurants → ร้านที่คะแนนเฉลี่ยสูงสุด

/recent-reviews → รีวิวล่าสุด

Navbar เปลี่ยนเมนูตามสถานะ login

---

## ▶️ How to Run the Project (วิธีรันโปรเจกต์)

---

1️⃣ Clone Repository
```bash
git clone https://github.com/waruenat-collab/web-flask_241-152.git
cd web-flask_241-152

2️⃣ สร้าง Virtual Environment
python -m venv venv

3️⃣ Activate Virtual Environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

4️⃣ ติดตั้ง Dependencies
pip install flask flask_sqlalchemy werkzeug

5️⃣ Run Application
python app.py

6️⃣ เปิดเว็บใน Browser
http://127.0.0.1:5000