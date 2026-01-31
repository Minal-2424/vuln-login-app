# Vulnerable Login Application (Security Learning Project)

This project demonstrates the full lifecycle of web security vulnerabilities:
**build → break → exploit → fix**.

---

## Table of Contents
1. [Overview](#overview)
2. [What This Project Covers](#what-this-project-covers)
3. [Learning Approach](#learning-approach)
4. [Tech Stack](#tech-stack)
5. [How to Run](#how-to-run)
6. [Important Notes](#important-notes)
7. [Push to GitHub](#push-to-github)

---

## Overview
This project is designed to help developers and security enthusiasts understand common web security vulnerabilities by intentionally introducing them into a simple login application. The goal is to exploit these vulnerabilities and then fix them using secure coding practices.

---

## What This Project Covers
- **SQL Injection (Authentication Bypass)**
- **Reflected Cross-Site Scripting (XSS)**
- **Password Hashing and Secure Authentication**
- **Session Security and Basic Rate Limiting**

---

## Learning Approach
1. Built a normal login system.
2. Intentionally introduced vulnerabilities.
3. Exploited them like a bug bounty hunter.
4. Fixed them using secure coding practices.

---

## Tech Stack
- **Programming Language:** Python
- **Framework:** Flask
- **Database:** SQLite

---

## How to Run
Follow these steps to set up and run the application:

1. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   python init_db.py
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

---

## Important Notes
This application was intentionally made vulnerable for learning purposes. **Do not deploy it publicly.**

---

## Push to GitHub
To push this project to GitHub, follow these steps:

1. Initialize a Git repository:
   ```bash
   git init
   ```

2. Add all files to the repository:
   ```bash
   git add .
   ```

3. Commit the changes:
   ```bash
   git commit -m "Vulnerable login app: SQLi & XSS exploit and fix"
   ```

4. Set the main branch:
   ```bash
   git branch -M main
   ```

5. Add the remote repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/vuln-login-app.git
   ```

6. Push the changes to GitHub:
   ```bash
   git push -u origin main
   ```
