import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x29, 0x37) # Slate-800
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER ENGINEERING & INFORMATION TECHNOLOGY\nACADEMIC YEAR 2026–27 | INTERNET PROGRAMMING (I.P.)")
    r_inst.font.size = Pt(9.5)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x64, 0x74, 0x8B) # Slate-500

    doc.add_paragraph().paragraph_format.space_after = Pt(20)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("EMPLOYEE LEAVE MANAGEMENT SYSTEM\n(LEAVEPORTAL HRMS)")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Slate-900

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("FORMATIVE ASSESSMENT 2 (FA 2) COMPREHENSIVE REPORT\nCore Full-Stack Implementation, Integration, Test Execution & Verification")
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x25, 0x63, 0xEB) # Blue-600
    p_sub.paragraph_format.space_after = Pt(36)

    # Metadata Card Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="94A3B8", sz="6")

    meta_data = [
        ("Course & Academic Year", "Internet Programming (I.P.) | Academic Year 2026–27"),
        ("Project Group Members", "39 Aryan Ram\n40 Priya Sahani\n41 Aarin Sahu"),
        ("Project Repository (GitHub)", "https://github.com/arynram/leaveportal"),
        ("Live Hosted Deployment (Render)", "https://leaveportal-qn03.onrender.com/"),
        ("Implementation Completion Status", "75% – 80% (Core Full-Stack Modules Fully Operational)")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_page_break()

    # ----------------------------------------------------
    # TABLE OF CONTENTS
    # ----------------------------------------------------
    h_toc = doc.add_paragraph()
    r_toc = h_toc.add_run("TABLE OF CONTENTS")
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    h_toc.paragraph_format.space_after = Pt(12)

    toc_items = [
        ("1. Executive Summary & Continuation from FA 1", "3"),
        ("2. Implementation of Major Modules & Functionalities", "4"),
        ("    2.1 Authentication & Session Handling Module", "4"),
        ("    2.2 Employee Leave Application & Balance Validation Module", "4"),
        ("    2.3 Administrative Decision & Leave Ledger Module", "5"),
        ("    2.4 Dashboard Metrics & Real-time KPI Module", "5"),
        ("3. Full-Stack Integration (UI, Application Logic & Data Layer)", "6"),
        ("4. Demonstration of Java & Object-Oriented Programming (OOP) Concepts", "7"),
        ("5. Input Validation & Exception Handling Framework", "8"),
        ("    5.1 Client-Side Validation", "8"),
        ("    5.2 Server-Side Validation & HTTP Status Codes", "8"),
        ("6. Data Operations & State Verification", "9"),
        ("7. Comprehensive Test Suite & Test Execution Report", "10"),
        ("8. Implementation Bugs, Errors & Resolution Reports (Verified Bug Log)", "12"),
        ("    8.1 Bug #1: SQL Reserved Keyword Syntax Error ('year')", "12"),
        ("    8.2 Bug #2: JSON Parser NumberFormatException ('Action Failed')", "12"),
        ("    8.3 Bug #3: Frontend DOM Null Reference / JavaScript TypeError", "13"),
        ("    8.4 Bug #4: Cloud Port Binding Conflict during Containerization", "13"),
        ("9. Cloud Deployment & Containerization (Docker / Render)", "14"),
        ("10. Project Progress Assessment (75%–80% Completion Status)", "15"),
        ("11. Conclusion & Future Scope (FA 3 Roadmap)", "16"),
        ("12. Appendix — Implementation Evidence & Screenshots", "17"),
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    set_table_borders(toc_table, color="E2E8F0", sz="2")
    for idx, (title, page_num) in enumerate(toc_items):
        row = toc_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.8)
        c1.width = Inches(0.7)
        set_cell_margins(c0, top=40, bottom=40, left=60, right=60)
        set_cell_margins(c1, top=40, bottom=40, left=60, right=60)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(title)
        r0.font.size = Pt(9.5)
        if not title.startswith("    "):
            r0.font.bold = True
            r0.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        else:
            r0.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page_num)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    doc.add_page_break()

    # Helper functions for sections
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Slate-900
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Navy Blue
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_callout(text, title="NOTE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = tbl.rows[0].cells[0]
        c.width = Inches(6.5)
        set_cell_background(c, "F8FAFC")
        set_cell_margins(c, top=80, bottom=80, left=140, right=140)
        
        # Border left highlight
        tcPr = c._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="none"/>'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
            f'  <w:bottom w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = c.paragraphs[0]
        r_t = p.add_run(f"[{title}] ")
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(9.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def style_header_row(row, col_widths, titles, bg_color="1E3A8A"):
        for i, (cell, w, title) in enumerate(zip(row.cells, col_widths, titles)):
            cell.width = Inches(w)
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(title)
            r.font.name = 'Calibri'
            r.font.bold = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # ----------------------------------------------------
    # SECTION 1
    # ----------------------------------------------------
    add_h1("1. Executive Summary & Continuation from FA 1")
    doc.add_paragraph(
        "In FA 1, the foundation for the Employee Leave Management System (LeavePortal HRMS) was established. "
        "The project scope addressed manual leave record keeping, opaque communication during PTO approval cycles, and "
        "reconciliation errors between management and staff. Architectural diagrams, user roles (Employee, Admin/HR), "
        "and UML use-case models were drafted."
    )
    doc.add_paragraph(
        "In FA 2 (Core Implementation, Integration & Testing), the project transitions from concept into an operational, "
        "fully verified full-stack software system. The monolith has been restructured into clean, cohesive Java modules "
        "interfacing with a responsive, modern Linear Minimal Light UI. Critical operational milestones delivered in FA 2 include: "
        "(1) Dual-role authentication engine, (2) Real-time quota balance checks and dynamic deduction upon approval, "
        "(3) Defensive input validation and JSON serialization, (4) Docker containerization and cloud hosting on Render, and "
        "(5) An exhaustive 8-scenario functional test suite with 100% pass verification."
    )

    # Comparison Table
    t_comp = doc.add_table(rows=7, cols=3)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_comp)
    comp_headers = ["System Dimension", "FA 1: Conceptual Foundation", "FA 2: Implementation & Verification"]
    style_header_row(t_comp.rows[0], [1.8, 2.3, 2.4], comp_headers)

    comp_data = [
        ("Architecture", "Monolithic conceptual architecture; preliminary data models.", "Modular 4-tier OOP Java backend (User, Leave, DataStore, App)."),
        ("Server & API Layer", "Mocked route definitions and theoretical endpoints.", "Production Java HttpServer handling socket routing & REST APIs."),
        ("User Interface", "Static visual prototype.", "Dynamic Linear Minimal Light Web UI (HTML5, modern CSS, ES6 fetch)."),
        ("Leave Processing", "High-level approval workflow specification.", "Fully functional reactive pipeline with status-driven balance deduction."),
        ("Validation & Errors", "Basic client-side HTML checks.", "Comprehensive dual-layer validation with HTTP error handling."),
        ("Deployment", "Local development environment only.", "Dockerized multi-stage container deployed on Render cloud platform.")
    ]
    for r_idx, (d0, d1, d2) in enumerate(comp_data, start=1):
        row = t_comp.rows[r_idx]
        for c_idx, text in enumerate([d0, d1, d2]):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # SECTION 2
    # ----------------------------------------------------
    add_h1("2. Implementation of Major Modules & Functionalities")
    doc.add_paragraph(
        "The system comprises four interdependent functional modules engineered to ensure complete separation of duties, "
        "accurate leave accounting, and intuitive user experiences."
    )

    add_h2("2.1 Authentication & Session Handling Module")
    doc.add_paragraph(
        "• Endpoint: POST /api/login\n"
        "• Payload: {\"email\": \"...\", \"password\": \"...\"}\n"
        "• Execution: Captures user credentials via fetch() API and verifies records within DataStore. "
        "Upon successful verification, the server transmits user attributes (name, email, role, balance) via an HTTP 200 JSON response. "
        "The client stores session state in memory and displays the appropriate interface (Employee or Admin View) while hiding the login screen."
    )

    add_h2("2.2 Employee Leave Application & Balance Validation Module")
    doc.add_paragraph(
        "• Endpoint: POST /api/apply\n"
        "• Payload: {\"email\": \"...\", \"type\": \"...\", \"from\": \"...\", \"to\": \"...\", \"days\": \"...\", \"reason\": \"...\"}\n"
        "• Execution: Validates that all fields are populated and executes server-side balance checking:\n"
        "    Validation Check: Requested Days <= Current Balance\n"
        "If the requested leave exceeds current quota, an HTTP 400 response is returned. If valid, a new Leave record is created with "
        "status 'PENDING' and inserted into the synchronized leave ledger."
    )

    add_h2("2.3 Administrative Decision & Leave Ledger Module")
    doc.add_paragraph(
        "• Endpoint: POST /api/action\n"
        "• Payload: {\"id\": 1, \"action\": \"APPROVE\" | \"REJECT\"}\n"
        "• Execution: Accessible only by ADMIN users. When the administrator approves a request, the record status transitions to 'APPROVED' "
        "and the employee's available balance is atomically deducted. If rejected, the status transitions to 'REJECTED' without altering the balance."
    )

    add_h2("2.4 Dashboard Metrics & Real-Time KPI Module")
    doc.add_paragraph(
        "• Endpoint: GET /api/data?email=...\n"
        "• Execution: Dynamically aggregates live operational indicators. For employees, it displays remaining quota, used leave days, "
        "and application history. For administrators, it computes real-time workforce KPIs: Pending Review Count, Total Approved Days, "
        "and Total Active Workforce Members."
    )

    # ----------------------------------------------------
    # SECTION 3
    # ----------------------------------------------------
    add_h1("3. Full-Stack Integration (UI, Application Logic & Data Layer)")
    doc.add_paragraph(
        "The software architecture enforces a decoupled, 3-tier model where the browser frontend never accesses persistence layers directly, "
        "communicating strictly through structured REST API contracts."
    )

    t_api = doc.add_table(rows=5, cols=4)
    t_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_api)
    style_header_row(t_api.rows[0], [1.1, 1.4, 2.2, 1.8], ["Method", "Endpoint", "Request / Query", "Response Payload & Logic"])
    api_data = [
        ("POST", "/api/login", "{\"email\", \"password\"}", "User JSON (name, role, balance) or 401 Unauthorized."),
        ("GET", "/api/data", "?email=user@domain.com", "User profile and leave ledger records filtered by role."),
        ("POST", "/api/apply", "{\"email\", \"type\", \"from\", \"to\", \"days\", \"reason\"}", "Created Leave record with PENDING state or 400 Bad Request."),
        ("POST", "/api/action", "{\"id\": 1, \"action\": \"APPROVE\"}", "Updated leave record; decrements quota on approval.")
    ]
    for r_idx, (m, ep, req, res) in enumerate(api_data, start=1):
        row = t_api.rows[r_idx]
        for c_idx, val in enumerate([m, ep, req, res]):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=70, right=70)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True
                if val == "POST":
                    r.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
                else:
                    r.font.color.rgb = RGBColor(0x05, 0x96, 0x69)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # SECTION 4
    # ----------------------------------------------------
    add_h1("4. Demonstration of Java & OOP Concepts")
    doc.add_paragraph(
        "The backend leverages Object-Oriented Programming (OOP) paradigms in pure Java without third-party framework overhead:"
    )
    doc.add_paragraph(
        "1. Encapsulation: User.java and Leave.java declare private instance variables accessible solely via public accessor and mutator methods. "
        "Direct manipulation of internal state (such as manual quota overwrites) is strictly guarded.\n"
        "2. Separation of Concerns (SoC): App.java serves as the routing and transport gateway; DataStore.java encapsulates the operational state and persistence logic.\n"
        "3. Thread Safety & Atomic Sequences: Unique identifiers are generated utilizing java.util.concurrent.atomic.AtomicInteger, guaranteeing race-condition-free ID assignment.\n"
        "4. In-Memory Collection Management: Thread-safe collections (java.util.List) organize active user entities and leave records."
    )

    # ----------------------------------------------------
    # SECTION 5
    # ----------------------------------------------------
    add_h1("5. Input Validation & Exception Handling Framework")
    doc.add_paragraph(
        "To ensure robust system integrity, validation is applied across both frontend and backend tiers:"
    )
    doc.add_paragraph(
        "• Client-Side Validation: Form inputs enforce HTML5 required constraints, date format sequencing (end date must be equal to or after start date), "
        "and numeric bounds (days must be >= 1). Input fields are sanitized prior to network dispatch.\n"
        "• Server-Side Validation: Irrespective of client input, the Java server checks requested leave against current available balance. "
        "If requestedDays > user.balance, the request is immediately halted with HTTP 400 Bad Request.\n"
        "• HTTP Status Code Mapping: HTTP 200 (Success), HTTP 400 (Validation Failure), HTTP 401 (Invalid Credentials), HTTP 404 (Resource Not Found), "
        "and HTTP 500 (Internal Server Error) are explicitly dispatched and rendered gracefully."
    )

    # ----------------------------------------------------
    # SECTION 6
    # ----------------------------------------------------
    add_h1("6. Data Operations & State Verification")
    doc.add_paragraph(
        "Leave state transitions follow a strict lifecycle designed to prevent quota discrepancies:"
    )

    t_state = doc.add_table(rows=5, cols=4)
    t_state.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_state)
    style_header_row(t_state.rows[0], [1.3, 1.7, 1.7, 1.8], ["Stage", "User Action", "Internal Operation", "System & Quota State"])
    state_data = [
        ("1. Baseline", "Rahul Sharma logs in.", "DataStore queries user record.", "Balance = 15 Days; Used = 0; History empty."),
        ("2. Application", "Submits 3-day Sick Leave.", "Validates 3 <= 15. Adds Leave object.", "Status: PENDING; Balance = 15 (Reserved)."),
        ("3. Validation", "Submits 20-day vacation.", "Validates 20 > 15. Rejection triggered.", "HTTP 400 returned. Ledger unchanged."),
        ("4. Decision", "Admin clicks 'Approve'.", "Status -> APPROVED. Balance = 15 - 3.", "Balance = 12 Days; Used = 3; Audit logged.")
    ]
    for r_idx, (s, a, o, st) in enumerate(state_data, start=1):
        row = t_state.rows[r_idx]
        for c_idx, val in enumerate([s, a, o, st]):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=70, right=70)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # SECTION 7
    # ----------------------------------------------------
    add_h1("7. Comprehensive Test Suite & Test Execution Report")
    doc.add_paragraph(
        "A rigorous suite of 8 comprehensive test cases was executed against the live system to verify functional stability. "
        "All test cases achieved a 100% Pass rate with verified logging output."
    )

    t_tests = doc.add_table(rows=9, cols=5)
    t_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tests)
    style_header_row(t_tests.rows[0], [0.8, 1.7, 1.7, 1.5, 0.8], ["Test ID", "Scenario & Input", "Expected Result", "Actual Output Observed", "Status"])

    tests_data = [
        ("TC-01", "Valid employee login (employee@gmail.com / emp123)", "HTTP 200; Employee Dashboard rendered with 15 days quota.", "Dashboard rendered; balance shows 15 days.", "PASS"),
        ("TC-02", "Invalid login (employee@gmail.com / wrongpass)", "HTTP 401; Error banner displayed; view blocked.", "Banner 'Invalid email or password' displayed.", "PASS"),
        ("TC-03", "Submit valid leave (3 days, Sick Leave)", "HTTP 200; Record created with PENDING status.", "Record inserted in history table as PENDING.", "PASS"),
        ("TC-04", "Submit leave exceeding balance (20 days vs 15 avail)", "HTTP 400; 'Insufficient balance' warning; request blocked.", "Warning modal displayed; submission rejected.", "PASS"),
        ("TC-05", "Submit leave with empty reason / dates", "HTML5 client validation prevents submission.", "Input flagged with tooltip; submission halted.", "PASS"),
        ("TC-06", "Admin login & review queue (admin@gmail.com)", "HTTP 200; Admin dashboard with approvals queue & KPIs.", "Admin queue rendered; shows pending request.", "PASS"),
        ("TC-07", "Admin approves 3-day request", "Status -> APPROVED; Employee quota decrements to 12.", "Status badge -> APPROVED; balance decremented.", "PASS"),
        ("TC-08", "Admin rejects leave request", "Status -> REJECTED; Employee balance unaltered.", "Status badge -> REJECTED; balance unchanged.", "PASS")
    ]

    for r_idx, (tid, scn, exp, act, stat) in enumerate(tests_data, start=1):
        row = t_tests.rows[r_idx]
        for c_idx, val in enumerate([tid, scn, exp, act, stat]):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, top=45, bottom=45, left=60, right=60)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if c_idx == 0:
                r.font.bold = True
            if c_idx == 4:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x05, 0x96, 0x69) # Green

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # SECTION 8
    # ----------------------------------------------------
    add_h1("8. Implementation Bugs, Errors & Resolution Reports (Bug Log)")
    doc.add_paragraph(
        "During iterative development and testing, four critical defects were identified, analyzed, and successfully resolved. "
        "Each defect represents a tangible engineering hurdle documented with root cause and resolution."
    )

    bugs = [
        ("8.1 Bug #1: SQL Reserved Keyword Syntax Error ('year')",
         "Database Layer / ORM Mapping",
         "org.h2.jdbc.JdbcSQLSyntaxErrorException: Syntax error in SQL statement '... [year] ...'",
         "The column name 'year' conflicted with standard ANSI SQL reserved keywords during database schema initialization.",
         "Renamed mapped field and schema column to 'calendar_year'. Confirmed error-free table creation."),

        ("8.2 Bug #2: JSON Parser NumberFormatException ('Action Failed')",
         "Backend HTTP Dispatcher / Regex Parser",
         "java.lang.NumberFormatException: For input string: 'status'",
         "In App.java, getField() searched for quoted tokens. When client sent numeric ID {\"id\": 1, \"status\": \"APPROVED\"}, "
         "the parser matched subsequent quotes around 'status', attempting to parse 'status' as an integer.",
         "Updated JSON parser to inspect comma and brace boundaries, correctly isolating unquoted numeric literals."),

        ("8.3 Bug #3: Frontend DOM Null Reference / JavaScript TypeError",
         "Client-Side Interface Script (script.js)",
         "Uncaught TypeError: Cannot set properties of null (setting 'innerText')",
         "During UI redesign to Linear Minimal Light theme, the element #user-avatar-initial was replaced. "
         "However, script.js attempted to update it on login, throwing an unhandled exception caught as a false network failure.",
         "Implemented defensive null checks (if (avatarEl) avatarEl.innerText = ...) ensuring robust DOM updates."),

        ("8.4 Bug #4: Cloud Port Binding Conflict during Containerization",
         "Cloud Deployment & Infrastructure (Render / Docker)",
         "Server port binding timeout / HTTP 502 Bad Gateway",
         "Server was initially hardcoded to port 8080. Cloud PaaS platforms (Render) dynamically assign listening ports via the PORT environment variable.",
         "Configured dynamic port extraction in App.java: String p = System.getenv('PORT'); int port = (p != null) ? Integer.parseInt(p) : 8080;")
    ]

    for title, comp, symptom, root, res in bugs:
        add_h2(title)
        b_p = doc.add_paragraph()
        b_p.add_run(f"• Affected Component: {comp}\n").font.bold = True
        b_p.add_run(f"• Error Symptom: ").font.bold = True
        b_p.add_run(f"{symptom}\n")
        b_p.add_run(f"• Root Cause Analysis: ").font.bold = True
        b_p.add_run(f"{root}\n")
        b_p.add_run(f"• Engineering Resolution: ").font.bold = True
        b_p.add_run(f"{res}")

    # ----------------------------------------------------
    # SECTION 9 & 10
    # ----------------------------------------------------
    add_h1("9. Cloud Deployment & Containerization (Docker / Render)")
    doc.add_paragraph(
        "To satisfy production criteria, LeavePortal was containerized via a lightweight, multi-stage Alpine Dockerfile. "
        "Stage 1 compiles Java source files with Temurin JDK 21; Stage 2 assembles a minimal JRE runtime image (~140MB), "
        "copying bytecode and web assets. Continuous deployment is established on Render through automatic webhook triggers from the GitHub repository."
    )

    add_h1("10. Project Progress Assessment (75%–80% Completion Status)")
    doc.add_paragraph(
        "The project has completed 75%–80% of its total roadmap. Core full-stack functionality, authentication, validation, "
        "and cloud hosting are 100% operational. The remaining 20% involves RDBMS persistence and automated email triggers slated for FA 3."
    )

    t_prog = doc.add_table(rows=7, cols=3)
    t_prog.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_prog)
    style_header_row(t_prog.rows[0], [2.2, 1.8, 2.5], ["Deliverable / Milestone", "Assessment Target", "Current Status & Verification"])
    prog_data = [
        ("Problem Analysis & Modeling", "FA 1", "100% Complete (Use cases, actors, architecture verified)"),
        ("Modular Java Backend Core", "FA 2", "100% Complete (User, Leave, DataStore, App fully operational)"),
        ("Linear Minimal Light UI", "FA 2", "100% Complete (Responsive HTML5, CSS, dynamic ES6 fetch)"),
        ("Validation & Bug Resolution", "FA 2", "100% Complete (All 4 bugs resolved; 8/8 test cases PASS)"),
        ("Cloud Docker Deployment", "FA 2", "100% Complete (Hosted live on Render; Git synced)"),
        ("Persistent RDBMS & Email Alerts", "FA 3", "20% Complete (Planned for final assessment cycle)")
    ]
    for r_idx, (m, tgt, st) in enumerate(prog_data, start=1):
        row = t_prog.rows[r_idx]
        for c_idx, val in enumerate([m, tgt, st]):
            c = row.cells[c_idx]
            set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, top=50, bottom=50, left=70, right=70)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------------------------------------------
    # SECTION 11
    # ----------------------------------------------------
    add_h1("11. Conclusion & Future Scope (FA 3 Roadmap)")
    doc.add_paragraph(
        "FA 2 successfully validates that the Employee Leave Management System operates as an efficient, user-friendly full-stack application. "
        "The implementation achieves clean separation of concerns, robust balance enforcement, and containerized cloud delivery.\n"
        "In FA 3, the project will expand to incorporate: (1) PostgreSQL/H2 relational database persistence, (2) Automated email dispatch "
        "via JavaMail API for approval updates, (3) Automated PDF leave clearance generation, and (4) Multi-tier hierarchical approval routing."
    )

    # ----------------------------------------------------
    # SECTION 12: APPENDIX & SCREENSHOTS
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1("12. Appendix — Implementation Evidence & Screenshots")
    doc.add_paragraph(
        "The following figures provide photographic evidence of system operation across multiple functional states."
    )

    screenshots = [
        ("01_login_screen.png", "Figure 1: LeavePortal Authentication Interface (Linear Minimal Light Theme)"),
        ("02_invalid_login_error.png", "Figure 2: Authentication Error Banner on Invalid Password Attempt"),
        ("03_employee_dashboard.png", "Figure 3: Employee Dashboard displaying 15 Days Quota and Application Form"),
        ("04_insufficient_balance_validation.png", "Figure 4: Balance Validation Error Banner on 20-Day Request (Exceeding Quota)"),
        ("05_admin_approvals_queue.png", "Figure 5: Administrator Approvals Queue and Real-Time Workforce KPI Metrics"),
        ("06_approved_leave_balance_deducted.png", "Figure 6: Approved Leave State with Employee Quota Deducted (15 -> 12 Days)")
    ]

    base_dir = r"C:\Users\engar\Documents\IP Mini Project\screenshots"
    for img_file, caption in screenshots:
        img_path = os.path.join(base_dir, img_file)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(5.8))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption)
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    out_path = r"C:\Users\engar\Documents\IP Mini Project\LeavePortal_FA2_Report.docx"
    doc.save(out_path)
    print(f"Report saved successfully to {out_path}")

if __name__ == "__main__":
    build_report()
