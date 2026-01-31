# Vulnerability Report – Vulnerable Login Application

---

## Overview
This document presents the security vulnerabilities intentionally introduced and exploited in a vulnerable web application as part of a cybersecurity learning project.

### Objectives
- Understand how vulnerabilities occur
- Learn how attackers exploit them
- Recognize why these vulnerabilities are dangerous
- Mitigate them using secure coding practices

The project followed a full security lifecycle:
**build → break → exploit → fix**

---

## Table of Contents
1. [SQL Injection – Authentication Bypass](#1-sql-injection--authentication-bypass)
2. [Reflected Cross-Site Scripting (XSS)](#2-reflected-cross-site-scripting-xss)
3. [Additional Security Observations](#3-additional-security-observations)
4. [Conclusion](#conclusion)

---

## 1. SQL Injection – Authentication Bypass

### Vulnerability Type
- **SQL Injection**
- **OWASP A03:2021 – Injection**

### Affected Endpoint
- `POST /login`

### Vulnerable Code
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
cur.execute(query)
```

### Description
User-controlled input from the login form was directly concatenated into an SQL query without sanitization or parameterization. This allowed an attacker to manipulate the SQL query logic and bypass authentication.

### Proof of Concept (PoC)
**Payload used in login form:**
- Username: `' OR 1=1 --`
- Password: `anything`

**Resulting SQL Query:**
```sql
SELECT * FROM users 
WHERE username = '' OR 1=1 -- ' AND password = 'anything'
```

### Impact
- Authentication bypass without valid credentials
- Attacker logs in as the first user in the database
- Full account takeover possible
- Can be chained with other vulnerabilities (e.g., XSS)

### Severity
- **Critical**

### Root Cause
- Unsafe string concatenation in SQL queries
- Lack of parameterized queries
- Trusting user input directly

### Mitigation Implemented
```python
cur.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```
- Parameterized queries prevent user input from altering SQL logic.
- SQL Injection payloads are treated as data, not executable SQL.

---

## 2. Reflected Cross-Site Scripting (XSS)

### Vulnerability Type
- **Reflected XSS**
- **OWASP A03:2021 – Injection**

### Affected Endpoint
- `GET /dashboard?name=`

### Vulnerable Backend Code
```python
name = request.args.get("name")
return render_template("dashboard.html", user=name)
```

### Vulnerable Template Code
```html
<p>Welcome {{ user | safe }}</p>
```

### Description
User-controlled input from the URL query parameter was rendered directly into the HTML response. The use of the `safe` filter disabled output escaping, allowing arbitrary JavaScript execution.

### Proof of Concept (PoC)
**Payload used:**
- `/dashboard?name=<script>alert(1)</script>`

**Result:**
- JavaScript executed in the browser
- Alert popup displayed

**Additional Test – Cookie Access:**
- Payload: `<script>alert(document.cookie)</script>`
- Result: XSS executed successfully, but session cookie was not accessible due to HttpOnly flag.

### Impact
- Arbitrary JavaScript execution in authenticated user context
- DOM manipulation
- Potential for:
  - Data exfiltration
  - Phishing attacks
  - UI manipulation

### Severity
- **High**

### Root Cause
- Trusting user-controlled input
- Disabling output escaping using `safe`
- Lack of output encoding and validation

### Mitigation Implemented
```html
<p>Welcome {{ user }}</p>
```
- Removed use of `safe` filter.
- Enabled Jinja2’s default auto-escaping.
- Prevented execution of injected scripts.

---

## 3. Additional Security Observations

### Observed Issues (Before Fixes)
- Plain-text password storage
- No login rate limiting
- SQL Injection vulnerability
- Reflected XSS vulnerability

### Mitigations Implemented (Phase 3)
- Passwords are securely hashed using `werkzeug.security`.
- SQL Injection prevented using parameterized queries.
- XSS mitigated through proper output escaping.
- Basic rate limiting added to the login endpoint.
- Session cookies configured with HttpOnly and SameSite attributes.

### Vulnerability Chaining Demonstrated
- **SQL Injection → Authentication Bypass → Authenticated XSS**

---

## Conclusion
This project demonstrates how common web vulnerabilities arise due to:
- Trusting user input
- Improper SQL query construction
- Unsafe output rendering

By exploiting SQL Injection and Reflected XSS, authentication bypass and client-side code execution were achieved. Subsequently, these vulnerabilities were mitigated using industry-standard secure coding practices.

### Key Takeaways
- **Input validation**
- **Output encoding**
- **Secure authentication design**
- **Defense-in-depth**

### Project Outcome
✔ Vulnerabilities identified  
✔ Exploitation confirmed  
✔ Secure fixes implemented  
✔ Lessons documented