// Single script.js file for Employee Leave Management System
let currentUser = null;

// Set default dates to today once DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
    const fromInput = document.getElementById('leave-from');
    const toInput = document.getElementById('leave-to');
    if (fromInput && toInput) {
        const today = new Date().toISOString().split('T')[0];
        fromInput.value = today;
        toInput.value = today;
    }
});

function fillDemo(email, pass) {
    document.getElementById('email').value = email;
    document.getElementById('password').value = pass;
}

// 1. Handle Login
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errBox = document.getElementById('login-error');
    errBox.style.display = 'none';

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });
        const data = await res.json();

        if (data.success) {
            currentUser = data;
            showDashboard();
        } else {
            errBox.innerText = data.error || 'Invalid email or password.';
            errBox.style.display = 'block';
        }
    } catch (err) {
        console.error(err);
        errBox.innerText = 'Unable to connect to server. Please ensure App is running.';
        errBox.style.display = 'block';
    }
}

// 2. Show Employee or Admin View
function showDashboard() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'flex';
    
    // Header Profile
    const nameEl = document.getElementById('user-name-display');
    if (nameEl) nameEl.innerText = currentUser.name;

    const roleEl = document.getElementById('user-role-display');
    if (roleEl) {
        roleEl.innerText = currentUser.role === 'ADMIN' ? 'ADMIN' : 'EMPLOYEE';
        roleEl.className = currentUser.role === 'ADMIN' ? 'role-pill role-pill-admin' : 'role-pill';
    }

    if (currentUser.role === 'ADMIN') {
        document.getElementById('admin-section').style.display = 'block';
        document.getElementById('employee-section').style.display = 'none';
    } else {
        document.getElementById('admin-section').style.display = 'none';
        document.getElementById('employee-section').style.display = 'block';
    }

    loadData();
}

// 3. Load Leaves and Balance from Server
async function loadData() {
    try {
        const res = await fetch('/api/data?email=' + encodeURIComponent(currentUser.email));
        const data = await res.json();

        if (currentUser.role === 'EMPLOYEE') {
            const balanceEl = document.getElementById('emp-balance');
            if (balanceEl) balanceEl.innerText = data.balance;

            const tbody = document.getElementById('emp-leaves-table');
            if (data.leaves.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 24px; color:var(--text-tertiary);">No leave applications yet.</td></tr>';
            } else {
                tbody.innerHTML = data.leaves.map(l => `
                    <tr>
                        <td class="cell-id">#00${l.id}</td>
                        <td style="color:var(--text-primary); font-weight:600;">${l.type}</td>
                        <td style="color:var(--text-secondary);">${l.from} → ${l.to}</td>
                        <td><span style="color:var(--text-primary); font-weight:600;">${l.days}</span> day${l.days > 1 ? 's' : ''}</td>
                        <td style="color:var(--text-secondary); max-width:240px;">${l.reason}</td>
                        <td><span class="badge badge-${l.status.toLowerCase()}">${l.status}</span></td>
                    </tr>
                `).join('');
            }
        } else {
            // ADMIN VIEW
            const leaves = data.leaves || [];
            
            // Calculate KPI metrics
            const kpiTotal = document.getElementById('admin-kpi-total');
            const kpiPending = document.getElementById('admin-kpi-pending');
            const kpiApproved = document.getElementById('admin-kpi-approved');
            const kpiRejected = document.getElementById('admin-kpi-rejected');

            if (kpiTotal) kpiTotal.innerText = leaves.length;
            if (kpiPending) kpiPending.innerText = leaves.filter(l => l.status === 'PENDING').length;
            if (kpiApproved) kpiApproved.innerText = leaves.filter(l => l.status === 'APPROVED').length;
            if (kpiRejected) kpiRejected.innerText = leaves.filter(l => l.status === 'REJECTED').length;

            const tbody = document.getElementById('admin-leaves-table');
            if (leaves.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; padding: 24px; color:var(--text-tertiary);">No requests found.</td></tr>';
            } else {
                tbody.innerHTML = leaves.map(l => {
                    const isPending = (l.status === 'PENDING');
                    return `
                        <tr>
                            <td class="cell-id">#00${l.id}</td>
                            <td>
                                <strong style="color:var(--text-primary);">${l.name}</strong><br>
                                <span style="font-size:11px; color:var(--text-tertiary);">${l.email}</span>
                            </td>
                            <td style="color:var(--text-secondary);">${l.type}</td>
                            <td style="color:var(--text-secondary);">${l.from} → ${l.to}</td>
                            <td><strong style="color:var(--text-primary);">${l.days}</strong></td>
                            <td style="color:var(--text-secondary); max-width:200px;">${l.reason}</td>
                            <td><span class="badge badge-${l.status.toLowerCase()}">${l.status}</span></td>
                            <td>
                                ${isPending ? `
                                    <button onclick="handleAction(${l.id}, 'APPROVED')" class="btn btn-success btn-sm">Approve</button>
                                    <button onclick="handleAction(${l.id}, 'REJECTED')" class="btn btn-danger btn-sm">Reject</button>
                                ` : '<span style="color:var(--text-tertiary); font-size:11px;">Completed</span>'}
                            </td>
                        </tr>
                    `;
                }).join('');
            }
        }
    } catch (e) {
        console.error(e);
    }
}

// 4. Employee Applies for Leave
async function handleApply(e) {
    e.preventDefault();
    const msgBox = document.getElementById('apply-msg');
    const errBox = document.getElementById('apply-err');
    msgBox.style.display = 'none';
    errBox.style.display = 'none';

    const payload = {
        email: currentUser.email,
        type: document.getElementById('leave-type').value,
        days: document.getElementById('leave-days').value,
        from: document.getElementById('leave-from').value,
        to: document.getElementById('leave-to').value,
        reason: document.getElementById('leave-reason').value
    };

    try {
        const res = await fetch('/api/apply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (data.success) {
            msgBox.innerText = data.message || 'Leave request successfully submitted!';
            msgBox.style.display = 'block';
            document.getElementById('leave-reason').value = '';
            loadData();
        } else {
            errBox.innerText = data.error;
            errBox.style.display = 'block';
        }
    } catch (err) {
        errBox.innerText = 'Error submitting leave request.';
        errBox.style.display = 'block';
    }
}

// 5. Admin Approves or Rejects Leave
async function handleAction(leaveId, status) {
    try {
        const res = await fetch('/api/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: String(leaveId), status: status })
        });
        const data = await res.json();
        if (data.success) {
            loadData();
        } else {
            alert('Action failed: ' + (data.error || 'Server error'));
        }
    } catch (e) {
        alert('Action failed: ' + e.message);
    }
}

// 6. Logout
function logout() {
    currentUser = null;
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('employee-section').style.display = 'none';
    document.getElementById('admin-section').style.display = 'none';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
}

// 7. Preview Helpers for Documentation Screenshots
window.addEventListener('load', () => {
    const params = new URLSearchParams(window.location.search);
    const view = params.get('preview');
    if (view === 'employee') {
        currentUser = { name: 'Rahul Sharma', email: 'employee@gmail.com', role: 'EMPLOYEE', balance: 15 };
        showDashboard();
    } else if (view === 'admin') {
        currentUser = { name: 'Admin User', email: 'admin@gmail.com', role: 'ADMIN', balance: 0 };
        showDashboard();
    } else if (view === 'error_login') {
        document.getElementById('email').value = 'employee@gmail.com';
        document.getElementById('password').value = 'wrongpassword123';
        const err = document.getElementById('login-error');
        err.innerText = 'Invalid email or password.';
        err.style.display = 'block';
    } else if (view === 'error_balance') {
        currentUser = { name: 'Rahul Sharma', email: 'employee@gmail.com', role: 'EMPLOYEE', balance: 15 };
        showDashboard();
        setTimeout(() => {
            const err = document.getElementById('apply-err');
            err.innerText = 'Insufficient balance! You have only 15 days left.';
            err.style.display = 'block';
            document.getElementById('leave-days').value = '20';
            document.getElementById('leave-reason').value = 'Annual vacation abroad (Requested 20 days)';
        }, 200);
    } else if (view === 'approved') {
        currentUser = { name: 'Rahul Sharma', email: 'employee@gmail.com', role: 'EMPLOYEE', balance: 12 };
        showDashboard();
    }
});
