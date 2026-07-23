# 🦄 Miss Lilah's Classroom Portal

Welcome to **Miss Lilah's Classroom Portal**—a custom, full-stack web application designed for an elite teacher to manage her digital classroom! Built using a robust three-tier architecture, this system moves completely away from temporary short-term memory (RAM) to a permanent, secure data layer.

🔗 **Live Application:** [https://school-website-portal.onrender.com/](https://school-website-portal.onrender.com/)

---

## 🚀 System Architecture
This application implements a clean **MVC (Model-View-Controller)** pattern:
*   **View (Frontend):** Pure HTML5 and modern CSS styling with structural layouts, dynamic feedback alerts, and a custom pastel unicorn interface.
*   **Controller (Backend Engine):** Python 3 powered by the **Flask** microframework to handle URL routing, request parsing, and template engine rendering.
*   **Model (Data Tier):** A permanent **MySQL** relational database engine that reads, writes, and deletes student records directly on persistent hardware storage.
*   **Media Pipeline (Cloud Storage):** Direct integration with **Cloudinary** SDK for handling dynamic multipart file uploads and secure image hosting for student homework.

---

## ✨ System Features
1.  **Dynamic Search Engine:** A student lookup bar that fetches and displays high-fidelity individual report cards on demand using template variable injection.
2.  **Digital Intake Matrix:** An interactive enrollment form that accepts student data along with homework image attachments directly into the data layer. 
3.  **Cloud-Based Homework Uploads:** In-line file upload functionality right inside student report cards and enrollment forms to attach and view Math and Reading homework images stored on Cloudinary.
4.  **Auto-Incrementing Roster:** A live attendance matrix that reflects all registered students, their corresponding primary key index IDs, and quick-access links to uploaded homework files.
5.  **Database Persistence:** Full protection against application power cycles. All data is committed directly to disk plates rather than volatile local variables.
6.  **Administrative Record Removal (CRUD):** Instant structural record pruning via inline delete forms targeted directly at specific row IDs.
7.  **Custom Theme Design:** A beautifully styled pastel layout optimized perfectly for its primary operator, Miss Lilah.

---

## 🛠️ Local Environment Setup

### 1. Database Creation
Before launching the application layer, ensure your MySQL service is running and execute the database schema instructions:

```sql
CREATE DATABASE classroom_db;
USE classroom_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    grade_level VARCHAR(20),
    math VARCHAR(5),
    reading VARCHAR(5),
    notes TEXT,
    math_hw_url TEXT,
    reading_hw_url TEXT
);
