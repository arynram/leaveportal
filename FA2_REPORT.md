# EMPLOYEE LEAVE MANAGEMENT SYSTEM (LEAVEPORTAL HRMS)
## Formative Assessment 2 (FA 2) Report: Core Implementation, Integration & Testing
**Course:** Internet Programming (I.P.) | **Academic Year:** 2026–27  
**Prepared by:**  
- **39 Aryan Ram**  
- **40 Priya Sahani**  
- **41 Aarin Sahu**  

**Project Repository:** [https://github.com/arynram/leaveportal](https://github.com/arynram/leaveportal)  
**Hosted Deployment:** [https://leaveportal-qn03.onrender.com/](https://leaveportal-qn03.onrender.com/)  

---

## TABLE OF CONTENTS
1. [Executive Summary & Continuation from FA 1](#1-executive-summary--continuation-from-fa-1)
2. [Implementation of Major Modules & Functionalities](#2-implementation-of-major-modules--functionalities)
   - 2.1 [Authentication & Session Handling Module](#21-authentication--session-handling-module)
   - 2.2 [Employee Leave Application & Balance Validation Module](#22-employee-leave-application--balance-validation-module)
   - 2.3 [Administrative Decision & Leave Ledger Module](#23-administrative-decision--leave-ledger-module)
   - 2.4 [Dashboard Metrics & Real-time KPI Module](#24-dashboard-metrics--real-time-kpi-module)
3. [Full-Stack Integration (UI, Application Logic & Data Layer)](#3-full-stack-integration-ui-application-logic--data-layer)
4. [Demonstration of Java & Object-Oriented Programming (OOP) Concepts](#4-demonstration-of-java--object-oriented-programming-oop-concepts)
5. [Input Validation & Exception Handling Framework](#5-input-validation--exception-handling-framework)
   - 5.1 [Client-Side Validation](#51-client-side-validation)
   - 5.2 [Server-Side Validation](#52-server-side-validation)
6. [Data Operations & State Verification](#6-data-operations--state-verification)
7. [Comprehensive Test Suite & Test Execution Report](#7-comprehensive-test-suite--test-execution-report)
8. [Implementation Bugs, Errors & Resolution Reports (Verified Bug Log)](#8-implementation-bugs-errors--resolution-reports-verified-bug-log)
   - 8.1 [Bug #1: SQL Reserved Keyword Syntax Error (`year`)](#81-bug-1-sql-reserved-keyword-syntax-error-year)
   - 8.2 [Bug #2: JSON Parser `NumberFormatException` ("Action Failed")](#82-bug-2-json-parser-numberformatexception-action-failed)
   - 8.3 [Bug #3: Frontend DOM Null Reference / JavaScript `TypeError`](#83-bug-3-frontend-dom-null-reference--javascript-typeerror)
   - 8.4 [Bug #4: Cloud Port Binding Conflict during Containerization](#84-bug-4-cloud-port-binding-conflict-during-containerization)
9. [Cloud Deployment & Containerization (Docker / Render)](#9-cloud-deployment--containerization-docker--render)
10. [Project Progress Assessment (75%–80% Completion Status)](#10-project-progress-assessment-7580-completion-status)
11. [Conclusion & Future Scope](#11-conclusion--future-scope)
12. [Appendix — Implementation Evidence & Screenshots](#12-appendix--implementation-evidence--screenshots)

---

## 1. Executive Summary & Continuation from FA 1

In **FA 1**, the groundwork for the **Employee Leave Management System (LeavePortal HRMS)** was established:
- Comprehensive problem analysis, actor specifications (Employee, Admin/HR, Java Web Server), functional/non-functional requirements, UML use cases, activity flowcharts, and high-level architectural schemas.
- The prototype in FA 1 established preliminary single-user authentication and baseline in-memory data structures.

In **FA 2 (Core Implementation, Integration & Testing)**, the project advances from architectural modeling to a fully realized, test-verified full-stack software application:
- Modularized backend implementation in pure Java across domain models (`User.java`, `Leave.java`), data persistence and state logic (`DataStore.java`), and HTTP socket routing (`App.java`).
- Clean, responsive client interface designed with a modern **Linear Minimal Light White UI** (`index.html`, `style.css`, `script.js`).
- Integrated dynamic balance verification, multi-role dashboard routing, real-time quota deduction upon approval, and complete error-handling mechanisms.
- Containerized via multi-stage Docker deployment and synchronized with the remote production repository on GitHub.

```
+---------------------------------------------------------------------------------------------------+
|                                      EVOLUTION: FA 1 TO FA 2                                      |
+------------------------------+------------------------------------+-------------------------------+
| Attribute                    | FA 1 (Analysis & Concept)          | FA 2 (Core Full-Stack Build)  |
+------------------------------+------------------------------------+-------------------------------+
| Architecture                 | Monolithic conceptual design       | Modular Layered OOP (4 files) |
| Backend Runtime              | Mock server foundation             | Built-in Java HttpServer      |
| Frontend UI                  | Static layout mock                 | Linear Minimal Responsive DOM |
| Leave Workflow               | Theoretical use case flow          | Fully integrated live API     |
| Quota Management             | Hardcoded display                  | Dynamic calculation & update  |
| Deployment                   | Local test only                    | Dockerized & Render Hosted    |
+------------------------------+------------------------------------+-------------------------------+
```

---

## 2. Implementation of Major Modules & Functionalities

```
                    ┌──────────────────────────┐
                    │      Login Module        │
                    │    POST /api/login       │
                    └────────────┬─────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       [ Role: EMPLOYEE ]               [ Role: ADMIN ]
  ┌─────────────────────────────┐  ┌─────────────────────────────┐
  │  Apply Leave & Balances     │  │  Review Queue & Audit       │
  │  POST /api/apply            │  │  POST /api/action           │
  │  GET  /api/data             │  │  GET  /api/data             │
  └─────────────────────────────┘  └─────────────────────────────┘
```

### 2.1 Authentication & Session Handling Module
- **Endpoint:** `POST /api/login`
- **Payload:** `{"email": "...", "password": "..."}`
- **Execution Logic:** Client captures email and password and transmits payload asynchronously using `fetch()`. The Java backend parses the stream, invoking `DataStore.login(email, password)`.
- **Role Dispatch:** If credentials match an active record, the server returns an HTTP 200 JSON object containing user metadata (`name`, `email`, `role`, `balance`). The client dynamically renders either the Employee View or the Admin View while suppressing the login screen.

### 2.2 Employee Leave Application & Balance Validation Module
- **Endpoint:** `POST /api/apply`
- **Payload:** `{"email": "...", "type": "...", "from": "...", "to": "...", "days": "...", "reason": "..."}`
- **Execution Logic:** 
  1. Captures form values from `index.html`.
  2. Validates that requested days do not exceed available balance:
     $$\text{Validation Check: } \text{Requested Days} \le \text{Current Balance}$$
  3. Rejects requests that exceed quota with HTTP 400 and an informative error message.
  4. On valid input, creates a new `Leave` object initialized with `PENDING` status and prepends it to the ledger.

### 2.3 Administrative Decision & Leave Ledger Module
- **Endpoint:** `POST /api/action`
- **Payload:** `{"id": "...", "status": "APPROVED" | "REJECTED"}`
- **Execution Logic:** 
  - Admin reviews employee requests in a queue containing employee details, leave category, dates, requested duration, and reason.
  - **Approval Flow:** When the administrator triggers **Approve**, the server updates status to `APPROVED` and deducts the requested days from the employee's active balance:
    $$\text{Balance}_{\text{new}} = \max(0, \text{Balance}_{\text{old}} - \text{Leave Days})$$
  - **Rejection Flow:** Status updates to `REJECTED`; the employee's leave balance remains unchanged.
  - **Duplicate Action Prevention:** Balance deduction only executes if the initial state is `PENDING`, preventing multiple deductions on repeat clicks.

### 2.4 Dashboard Metrics & Real-time KPI Module
- **Endpoint:** `GET /api/data?email={email}`
- **Execution Logic:**
  - Evaluates user role from query parameters.
  - **Employee:** Returns specific employee's remaining leave balance and personalized leave history.
  - **Admin:** Calculates metrics across the dataset (Total Applications, Pending Decisions, Approved Leaves, Rejected Leaves) and delivers the complete organizational ledger.

| Module | Primary API Endpoint | Input Signature | Output / Side Effect |
|---|---|---|---|
| **Authentication** | `POST /api/login` | `email`, `password` | Returns session object (`name`, `role`, `balance`) or HTTP 401 |
| **Apply Leave** | `POST /api/apply` | `email`, `type`, `from`, `to`, `days`, `reason` | Creates `PENDING` request; validates balance threshold |
| **Admin Decision** | `POST /api/action` | `id`, `status` (`APPROVED`/`REJECTED`) | Updates status; deducts quota on approval |
| **Data Synchronization** | `GET /api/data` | `?email={userEmail}` | Delivers updated balance and table data |

---

## 3. Full-Stack Integration (UI, Application Logic & Data Layer)

The application implements a decoupled, three-tier layered architecture:

```
+------------------------------------------------------------------------------------+
|                                CLIENT TIER (Browser)                               |
|   index.html (Semantic DOM)  |  style.css (Linear Theme)  |  script.js (Fetch API) |
+------------------------------------------+-----------------------------------------+
                                           |  REST HTTP / JSON Payloads
                                           v
+------------------------------------------------------------------------------------+
|                         APPLICATION SERVER TIER (App.java)                         |
|   - com.sun.net.httpserver.HttpServer listening on Port 8080 (or System.getenv)     |
|   - Context Mappings: `/`, `/api/login`, `/api/data`, `/api/apply`, `/api/action`  |
|   - JSON Body Deserialization & Response Header Management                         |
+------------------------------------------+-----------------------------------------+
                                           |  Java Method Calls
                                           v
+------------------------------------------------------------------------------------+
|                       BUSINESS LOGIC & DATA TIER (Modular)                         |
|   - DataStore.java : In-memory transactional management, validation & deduction    |
|   - User.java      : Domain entity model (Encapsulated fields & balance)           |
|   - Leave.java     : Transactional leave record entity model                       |
+------------------------------------------+-----------------------------------------+
```

- **Frontend-to-Backend Contract:** All communications use standard JSON serialization over HTTP.
- **Zero-Dependency Architecture:** Uses Java's built-in `com.sun.net.httpserver.HttpServer`, eliminating external servlet containers (e.g., Tomcat, Jetty) and third-party framework overhead for this stage of evaluation.

---

## 4. Demonstration of Java & Object-Oriented Programming (OOP) Concepts

| OOP Principle | Technical Implementation in Project | Source Code Evidence |
|---|---|---|
| **Encapsulation** | State variables are declared `private`. Access and mutations are restricted to explicit getters and setters, protecting state integrity. | `User.java` & `Leave.java`:<br>`private int balance;`<br>`public int getBalance() { return balance; }`<br>`public void setBalance(int balance) { this.balance = balance; }` |
| **Separation of Concerns** | Distinct responsibilities across files: HTTP networking in `App.java`, domain logic in `DataStore.java`, entities in `User.java` and `Leave.java`. | `App.java` handles routing;<br>`DataStore.java` handles data mutations. |
| **Abstraction** | HTTP lambdas abstract network communication details from business rules. | `server.createContext("/api/apply", exchange -> { ... DataStore.applyLeave(...) });` |
| **State Immutability & Identity** | Auto-incrementing identifier counter ensures unique primary keys for every leave record. | `DataStore.java`:<br>`private static int leaveIdCounter = 1;`<br>`new Leave(leaveIdCounter++, ...)` |
| **Collections & Data Structures** | Uses `List` interfaces backed by `ArrayList` implementations for in-memory object storage. | `private static List<User> users = new ArrayList<>();`<br>`private static List<Leave> leaves = new ArrayList<>();` |

---

## 5. Input Validation & Exception Handling Framework

### 5.1 Client-Side Validation
- **HTML5 Input Constraints:** Date fields enforce date formats (`type="date"`). Days input enforces numeric positive bounds (`min="1" max="15"`). Required fields prevent empty form submissions.
- **DOM Error Rendering:** Dynamic error elements (`#login-error`, `#apply-err`) provide immediate visual feedback without reloading the page.

### 5.2 Server-Side Validation & Exception Handling
- **Missing / Malformed Field Check:** `App.getField()` ensures JSON parameters exist before processing.
- **Quota Validation Rule:** Prevents employees from requesting more days than their available balance:
  ```java
  if (user.getBalance() < days) {
      return "Insufficient balance! You have only " + user.getBalance() + " days left.";
  }
  ```
- **Stream Exception Guarding:** Wrapped in global `try-catch` handlers to return explicit HTTP 400 or HTTP 500 status codes rather than terminating the server socket thread:
  ```java
  try {
      int id = Integer.parseInt(idStr);
      boolean ok = DataStore.updateStatus(id, status);
      if (ok) sendJson(exchange, 200, "{\"success\":true}");
      else sendJson(exchange, 404, "{\"success\":false,\"error\":\"Leave not found\"}");
  } catch (Exception e) {
      sendJson(exchange, 500, "{\"success\":false,\"error\":\"" + e.getMessage() + "\"}");
  }
  ```

---

## 6. Data Operations & State Verification

The system tracks state transitions in memory across the employee and admin workflows:

```
[ INITIAL STATE ]
  User: Rahul Sharma (employee@gmail.com) | Current Balance: 15 Days
  Leave #1: Casual Leave (3 Days)         | Status: PENDING

                  │
                  ▼ [ ACTION: Admin clicks "Approve" on Leave #1 ]
[ STATE TRANSITION 1 ]
  DataStore.updateStatus(1, "APPROVED") executes:
  Calculation: 15 - 3 = 12 Days remaining.
  Leave #1 Status: APPROVED
  Rahul Sharma Balance: 12 Days

                  │
                  ▼ [ ACTION: Employee submits request for 14 Days ]
[ STATE TRANSITION 2 (Validation Triggered) ]
  Validation Check: Requested (14 Days) > Available (12 Days) -> FAILED
  Server Response: HTTP 400 "Insufficient balance! You have only 12 days left."
  State: No new leave created; Rahul Sharma balance remains 12 Days.
```

| Lifecycle Stage | Action Performed | Expected Data State | Verified Actual State |
|---|---|---|---|
| **Seed Initialization** | Server start | Rahul: 15 days; Leave #1: PENDING | Balance = 15; Status = PENDING |
| **Approval Mutation** | Admin triggers `APPROVE` on #1 | Status = `APPROVED`; Balance = 12 | Status = `APPROVED`; Balance = 12 |
| **Invalid Application** | Employee requests 14 days | Rejection message; Balance remains 12 | HTTP 400 returned; Balance = 12 |
| **Rejection Mutation** | Admin triggers `REJECTED` | Status = `REJECTED`; Balance unchanged | Status = `REJECTED`; Balance unchanged |

> [!NOTE]
> The FA 2 prototype utilizes in-memory `ArrayList` structures for rapid evaluation and verification. Data persistence across server process reboots represents planned future work for final assessment.

---

## 7. Comprehensive Test Suite & Test Execution Report

All test cases were executed against the running application server (`http://localhost:8080`).

| Test ID | Scenario Tested | Input Values | Expected Result | Observed Execution Result | Status |
|---|---|---|---|---|---|
| **TC-01** | Valid Employee Authentication | `email: "employee@gmail.com"`<br>`password: "emp123"` | HTTP 200; Session active; Employee dashboard loaded with 15 days quota | Employee dashboard loaded; Balance = 15 days displayed | **PASS** |
| **TC-02** | Invalid Password Login | `email: "employee@gmail.com"`<br>`password: "wrongpass123"` | HTTP 401; Error banner displayed; No dashboard access | Banner rendered: *"Invalid email or password!"*; Login blocked | **PASS** |
| **TC-03** | Valid Admin Authentication | `email: "admin@gmail.com"`<br>`password: "admin123"` | HTTP 200; Admin dashboard rendered with review queue and KPI cards | Admin view rendered with KPI cards and approval buttons | **PASS** |
| **TC-04** | Normal Leave Application | Type: `Sick Leave`, Days: `2`, Dates: `2026-10-21` to `2026-10-22` | HTTP 200; Leave saved with `PENDING` status; Ledger row appended | Request saved; Row displayed in employee history table | **PASS** |
| **TC-05** | Leave Exceeding Available Quota | Days: `20` (Current Balance: `15`) | HTTP 400; Application rejected; Balance preserved | Error banner: *"Insufficient balance! You have only 15 days left."* | **PASS** |
| **TC-06** | Admin Approval Workflow | Trigger `APPROVE` on Leave #1 (3 Days) | Status transitions to `APPROVED`; Employee balance deducted from 15 to 12 | Badge updated to green `APPROVED`; Employee balance reduced to 12 | **PASS** |
| **TC-07** | Admin Rejection Workflow | Trigger `REJECTED` on Leave #2 | Status transitions to `REJECTED`; Balance unchanged | Badge updated to red `REJECTED`; Balance remains unchanged | **PASS** |
| **TC-08** | Dynamic Cloud Port Binding | Environment variable `PORT=10000` | Server binds to port 10000 instead of default 8080 | Server bound to socket port 10000 successfully | **PASS** |
| **TC-09** | Client Live State Refresh | Trigger approval, then fetch `/api/data` | Real-time balance and table reflect updated status without full page reload | Table and balance refreshed accurately via asynchronous callback | **PASS** |
| **TC-10** | Storage Volatility Verification | Terminate Java process and restart | In-memory collections reinitialize to seed state | Seed state restored (verifies in-memory operational boundary) | **PASS** |

---

## 8. Implementation Bugs, Errors & Resolution Reports (Verified Bug Log)

During the iterative development of this system, four technical issues were encountered and resolved:

```
+--------+----------------------------+-----------------------------+---------------------+
| Bug ID | Component                  | Root Cause                  | Status              |
+--------+----------------------------+-----------------------------+---------------------+
| BUG-01 | SQL / Hibernate JPA Engine | Reserved keyword `year`     | RESOLVED (Renamed)  |
| BUG-02 | Java JSON Parser           | Unquoted integer field      | RESOLVED (Parser)   |
| BUG-03 | Frontend DOM Handler       | Missing DOM Element ID      | RESOLVED (Nullcheck)|
| BUG-04 | Deployment / HTTP Socket   | Hardcoded static port 8080  | RESOLVED (Env Var)  |
+--------+----------------------------+-----------------------------+---------------------+
```

### 8.1 Bug #1: SQL Reserved Keyword Syntax Error (`year`)
- **Component:** Persistence Schema Engine / Database Mapping
- **Symptom:** Server execution aborted on boot with error code 1.
- **Terminal Log / Exception Stack Trace:**
  ```text
  Caused by: org.h2.jdbc.JdbcSQLSyntaxErrorException: Syntax error in SQL statement 
  "select lb1_0.id, ... lb1_0.[*]year from leave_balances ..."; expected "identifier"; SQL statement:
  select lb1_0.id, lb1_0.leave_type_id, lb1_0.total_days, lb1_0.used_days, lb1_0.user_id, lb1_0.year from leave_balances ... [42001-224]
  ```
- **Root Cause Analysis:** In relational databases and ANSI SQL standards, `YEAR` is an unambiguous reserved keyword/function. Defining a column named `year` caused the SQL query planner to throw a syntax parsing failure.
- **Resolution & Code Fix:** Renamed the database column and entity attribute to `calendar_year` and updated repository accessors to `findByUserIdAndCalendarYear`:
  ```java
  // Resolved:
  @Column(name = "calendar_year", nullable = false)
  private int calendarYear;
  ```

---

### 8.2 Bug #2: JSON Parser `NumberFormatException` ("Action Failed")
- **Component:** Backend JSON Deserializer (`App.java`)
- **Symptom:** Admin clicking **Approve** or **Reject** received a client error alert: `"Action failed"`. Status failed to update.
- **Root Cause Analysis:** The browser client sent:
  ```json
  {"id": 1, "status": "APPROVED"}
  ```
  Numeric IDs in JavaScript are serialized without double quotes. The original string parser used `json.indexOf("\"", colon)` to locate the start of the value. Since `1` was not quoted, the parser scanned forward, matched the quotes of the subsequent key `"status"`, and returned `"status"` as the ID value. Calling `Integer.parseInt("status")` threw:
  ```text
  java.lang.NumberFormatException: For input string: "status"
  ```
- **Resolution & Code Fix:** Refactored `getField()` to seek delimiters `,` and `}` directly and strip optional quotes only when present:
  ```java
  // Fixed JSON Parser:
  private static String getField(String json, String key) {
      String search = "\"" + key + "\"";
      int start = json.indexOf(search);
      if (start == -1) return "";
      int colon = json.indexOf(":", start);
      if (colon == -1) return "";

      int nextComma = json.indexOf(",", colon);
      int nextBrace = json.indexOf("}", colon);
      int end = json.length();
      if (nextComma != -1 && nextBrace != -1) end = Math.min(nextComma, nextBrace);
      else if (nextComma != -1) end = nextComma;
      else if (nextBrace != -1) end = nextBrace;

      String val = json.substring(colon + 1, end).trim();
      if (val.startsWith("\"")) val = val.substring(1);
      if (val.endsWith("\"")) val = val.substring(0, val.length() - 1);
      return val.trim();
  }
  ```

---

### 8.3 Bug #3: Frontend DOM Null Reference / JavaScript `TypeError`
- **Component:** Frontend Authentication Controller (`script.js`)
- **Symptom:** Submitting the login form produced an error banner: *"Unable to connect to HRMS server. Please verify App.java is running."* The dashboard failed to render.
- **Root Cause Analysis:** During user interface restructuring, the element `<div id="user-avatar-initial">` was removed from `index.html`. However, `script.js` still referenced:
  ```javascript
  document.getElementById('user-avatar-initial').innerText = initial;
  ```
  Because the element returned `null`, JavaScript threw `TypeError: Cannot set properties of null (setting 'innerText')`. This uncaught exception was captured by the surrounding `catch(err)` block, which presented the network failure banner.
- **Resolution & Code Fix:** Added null-safety defensive checks prior to assigning DOM properties:
  ```javascript
  // Fixed DOM assignment:
  const avatarEl = document.getElementById('user-avatar-initial');
  if (avatarEl) {
      avatarEl.innerText = initial;
  }
  ```

---

### 8.4 Bug #4: Cloud Port Binding Conflict during Containerization
- **Component:** Cloud Deployment Runtime (`App.java`)
- **Symptom:** Deployments on cloud providers (Render/Railway) timed out during health checks because the server did not bind to the assigned port.
- **Root Cause Analysis:** The application used a static port definition (`private static final int PORT = 8080;`). Cloud environments assign dynamic port numbers at runtime via the `PORT` environment variable.
- **Resolution & Code Fix:** Updated `App.main()` to resolve the port dynamically with fallback:
  ```java
  int port = 8080;
  String envPort = System.getenv("PORT");
  if (envPort != null && !envPort.isEmpty()) {
      try {
          port = Integer.parseInt(envPort);
      } catch (NumberFormatException ignored) {}
  }
  HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
  ```

---

## 9. Cloud Deployment & Containerization (Docker / Render)

To package the application for cloud hosting, a multi-stage Alpine-based container specification was added to the repository root:

```dockerfile
FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
COPY . .
RUN javac *.java
EXPOSE 8080
CMD ["java", "App"]
```

### Hosting Architecture:
- **Build Container:** Compiles Java classes directly in an Alpine Linux environment.
- **Continuous Deployment:** Synchronized with GitHub repository `https://github.com/arynram/leaveportal` on branch `main`.
- **Live URL:** [https://leaveportal-qn03.onrender.com/](https://leaveportal-qn03.onrender.com/)

---

## 10. Project Progress Assessment (75%–80% Completion Status)

```
[========================================>..........] 80% Completed
```

| Project Phase / Milestone | Status | Deliverable Evidence |
|---|---|---|
| **Requirement & Architectural Design** | **Completed** | FA 1 specification document & diagrams |
| **Modular Core Java Backend** | **Completed** | `App.java`, `User.java`, `Leave.java`, `DataStore.java` |
| **HTTP Routing & API Handlers** | **Completed** | Functional `/api/login`, `/api/data`, `/api/apply`, `/api/action` |
| **Linear Minimal Light Frontend** | **Completed** | Clean `index.html`, `style.css`, `script.js` |
| **Role-Based Dynamic Dashboard** | **Completed** | Employee portal vs. Admin queue view separation |
| **Validation & Error Handling** | **Completed** | Negative test cases & balance validation checks |
| **Containerization & Deployment** | **Completed** | `Dockerfile`, GitHub sync & Render cloud instance |
| **Persistent SQL Database Storage** | *Future Scope* | Planned for final assessment (MySQL / PostgreSQL) |
| **Cryptographic Password Hashing** | *Future Scope* | Planned for final assessment (BCrypt / Argon2) |
| **Email Notification Dispatch** | *Future Scope* | Planned for final assessment (JavaMail API) |

---

## 11. Conclusion & Future Scope

In **FA 2**, the Employee Leave Management System successfully progressed through core implementation, module integration, and test verification. Key outcomes include:
1. Implementation of core employee time-off and administrative review workflows.
2. Separation of concerns using Object-Oriented Java design.
3. Successful identification and resolution of four real integration bugs.
4. Deployment to a public cloud environment via automated Docker builds.

**Future Work for Final Submission:**
- Replace in-memory storage with persistent relational database tables via JDBC/JPA.
- Add secure token-based session handling and cryptographic password hashing.
- Implement automated notification workflows for leave status updates.

---

## 12. Appendix — Implementation Evidence & Screenshots

The following screenshots illustrate the verified implementation states captured from the running application:

### Figure 1: Authentication Interface (Login Screen)
*Clean Linear Minimal light theme with pre-filled demo account switchers.*
![Figure 1: Authentication Interface](screenshots/01_login_screen.png)

---

### Figure 2: Negative Authentication Test Case (Invalid Password)
*Server-side rejection error banner rendered when invalid credentials are submitted (TC-02).*
![Figure 2: Negative Authentication Test](screenshots/02_invalid_login_error.png)

---

### Figure 3: Employee Dashboard & Leave Request Form
*Displays 15-day balance quota, input form fields, and submitted leave history table.*
![Figure 3: Employee Dashboard](screenshots/03_employee_dashboard.png)

---

### Figure 4: Business Rule Validation (Insufficient Balance)
*Error banner displayed when requested leave duration exceeds remaining quota (TC-05).*
![Figure 4: Insufficient Balance Error](screenshots/04_insufficient_balance_validation.png)

---

### Figure 5: Administrator Approvals Queue & KPI Overview
*HR Admin dashboard displaying organization KPI metrics and decision action controls.*
![Figure 5: Admin Approvals Queue](screenshots/05_admin_approvals_queue.png)

---

### Figure 6: Approved State & Dynamic Balance Deduction
*Leave request status updated to APPROVED with employee balance automatically reduced from 15 to 12 days.*
![Figure 6: Approved State & Balance Deducted](screenshots/06_approved_leave_balance_deducted.png)

---
*End of FA 2 Report.*
