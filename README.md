# 🦄 Miss Lilah's Classroom Portal

Welcome to **Miss Lilah's Classroom Portal**—a custom, full-stack web application designed for an elite teacher to manage her digital classroom! Built using a robust three-tier architecture, this system moves completely away from temporary short-term memory (RAM) to a permanent, secure data layer.

## 🚀 System Architecture
This application implements a clean **MVC (Model-View-Controller)** pattern:
*   **View (Frontend):** Pure HTML5 and modern CSS styling with structural layouts, dynamic feedback alerts, and a custom pastel unicorn interface.
*   **Controller (Backend Engine):** Python 3 powered by the **Flask** microframework to handle URL routing, request parsing, and template engine rendering.
*   **Model (Data Tier):** A permanent **MySQL** relational database engine that reads, writes, and deletes student records directly on persistent hardware storage.

---

## ✨ System Features
1.  **Dynamic Search Engine:** An student lookup bar that fetches and displays high-fidelity individual report cards on demand using template variable injection.
2.  **Digital Intake Matrix:** An interactive enrollment form that passes parameters directly to the data layer. 
3.  **Auto-Incrementing Roster:** A live attendance matrix that reflects all registered students and their corresponding primary key index IDs automatically.
4.  **Database Persistence:** Full protection against application power cycles. All data is committed directly to disk plates rather than volatile local variables.
5.  **Administrative Record Removal (CRD):** Instant structural record pruning via inline delete forms targeted directly at specific row IDs.
6.  **Custom Theme Design:** A beautifully styled pastel layout optimized perfectly for its primary operator, Miss Lilah.

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
    notes TEXT
);

## 🛠️ Technology Stack & Tools Used

This project leverages a modern, lightweight tech stack combining frontend presentation layers with robust backend execution scripts:

*   **Python 3:** The foundational backend programming language used to construct the logic, structure, and database connection bridges.
*   **Flask:** A lightweight Python microframework utilized to handle URL routing, HTTP request tracking (`GET`/`POST`), and secure server handling.
*   **MySQL:** A production-grade relational database management system (RDBMS) providing disk-persistent structural data storage.
*   **HTML5:** The structural markup language used to build the front-end user forms, layout cards, and student attendance matrices.
*   **CSS3:** Cascading Style Sheets utilized to inject the custom, high-fidelity pastel color palette and typography tailored for Miss Lilah.
*   **Git:** The distributed version control system utilized to track software builds, manage state changes, and snapshot milestones locally.
*   **GitHub:** The cloud-based repository engine providing secure remote backup and continuous integration pipelines for the application code.
*   **Linux (WSL2/Ubuntu):** The local terminal execution environment utilized to host the development workspace, background daemons, and package management utilities.
