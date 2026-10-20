import java.util.ArrayList;
import java.util.List;

/**
 * DataStore manages in-memory data (Users & Leaves)
 * and handles the core business logic (authenticating, balance deduction).
 */
public class DataStore {
    private static List<User> users = new ArrayList<>();
    private static List<Leave> leaves = new ArrayList<>();
    private static int leaveIdCounter = 1;

    static {
        // Pre-seeded Demo Users
        users.add(new User("Admin User", "admin@gmail.com", "admin123", "ADMIN", 0));
        users.add(new User("Rahul Sharma", "employee@gmail.com", "emp123", "EMPLOYEE", 15));

        // Pre-seeded Sample Leave Request
        leaves.add(new Leave(leaveIdCounter++, "Rahul Sharma", "employee@gmail.com", 
                             "Casual Leave", "2026-10-25", "2026-10-27", 3, "Family Function", "PENDING"));
    }

    // 1. Authenticate user
    public static User login(String email, String password) {
        for (User u : users) {
            if (u.getEmail().equalsIgnoreCase(email.trim()) && u.getPassword().equals(password.trim())) {
                return u;
            }
        }
        return null;
    }

    // 2. Find user by email
    public static User getUser(String email) {
        for (User u : users) {
            if (u.getEmail().equalsIgnoreCase(email.trim())) {
                return u;
            }
        }
        return null;
    }

    // 3. Get leaves (Admin sees all; Employee sees only their own)
    public static List<Leave> getLeaves(String email) {
        User user = getUser(email);
        List<Leave> result = new ArrayList<>();

        for (Leave l : leaves) {
            if (user != null && "ADMIN".equalsIgnoreCase(user.getRole())) {
                result.add(l); // Admin sees all records
            } else if (l.getEmpEmail().equalsIgnoreCase(email.trim())) {
                result.add(l); // Employee sees their own
            }
        }
        return result;
    }

    // 4. Apply for a new leave (Checks available balance)
    public static String applyLeave(String email, String type, String from, String to, int days, String reason) {
        User user = getUser(email);
        if (user == null) {
            return "User not found";
        }
        if (user.getBalance() < days) {
            return "Insufficient balance! You have only " + user.getBalance() + " days left.";
        }

        Leave newLeave = new Leave(leaveIdCounter++, user.getName(), email, type, from, to, days, reason, "PENDING");
        leaves.add(0, newLeave); // Add at top of list
        return "SUCCESS";
    }

    // 5. Approve or Reject leave (Deducts balance on approval)
    public static boolean updateStatus(int leaveId, String status) {
        for (Leave l : leaves) {
            if (l.getId() == leaveId) {
                // If approving a pending leave, deduct from employee's balance
                if ("APPROVED".equalsIgnoreCase(status) && "PENDING".equalsIgnoreCase(l.getStatus())) {
                    User u = getUser(l.getEmpEmail());
                    if (u != null) {
                        int remaining = Math.max(0, u.getBalance() - l.getDays());
                        u.setBalance(remaining);
                    }
                }
                l.setStatus(status.toUpperCase());
                return true;
            }
        }
        return false;
    }
}
