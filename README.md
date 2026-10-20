# 🏢 Employee Leave Management System (HRMS Mini Project)
A lightweight Java Full Stack Mini Project with **Linear Minimal Dark UI** (inspired by Linear.app: razor-sharp 1px borders, matte obsidian surfaces, Inter & JetBrains Mono typography) and clean **Modular Java Backend**.

---

## 📁 Clean File Structure & Explanations

### ☕ Backend (Java):
1. **[`User.java`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/User.java)** — **User Model Entity**
   - Holds user properties: `name`, `email`, `password`, `role` (EMPLOYEE / ADMIN), and `balance` (leave quota).
2. **[`Leave.java`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/Leave.java)** — **Leave Request Model Entity**
   - Holds leave application data: `id`, `empName`, `empEmail`, `leaveType`, `fromDate`, `toDate`, `days`, `reason`, and `status` (PENDING / APPROVED / REJECTED).
3. **[`DataStore.java`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/DataStore.java)** — **Database & Business Logic Layer**
   - Stores users and leaves in `ArrayList`.
   - Contains business logic: authenticating login, checking leave balances, deducting quota when approved.
4. **[`App.java`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/App.java)** — **Server & Controller Routing**
   - Starts the built-in Java HTTP server on port 8080.
   - Maps API endpoints (`/api/login`, `/api/data`, `/api/apply`, `/api/action`) and serves frontend files.

---

### 🎨 Frontend:
1. **[`index.html`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/index.html)** — Glassmorphism Portal page containing Login, Employee view, and HR Admin queue.
2. **[`style.css`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/style.css)** — Glassmorphic styling with frosted cards, glowing status pills, and ambient dark theme.
3. **[`script.js`](file:///c:/Users/engar/Documents/IP%20Mini%20Project/script.js)** — Frontend interaction (sends fetch requests to Java backend and updates tables).

---

### 🚀 How to Run:
Double-click **`run.bat`** in this folder!  
It compiles all `.java` files using `javac *.java` and opens `http://localhost:8080` in your browser.

---

### 🔑 Demo Login Accounts:
- **Employee**: `employee@gmail.com` / `emp123`
- **HR Admin**: `admin@gmail.com` / `admin123`
*(Or click the **"Fill Employee"** and **"Fill HR Admin"** buttons on the login card).*
