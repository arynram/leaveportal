/**
 * Model class representing an Employee or Admin user in the system.
 */
public class User {
    private String name;
    private String email;
    private String password;
    private String role;     // "EMPLOYEE" or "ADMIN"
    private int balance;     // Remaining leave days

    public User(String name, String email, String password, String role, int balance) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.role = role;
        this.balance = balance;
    }

    // Getters and Setters
    public String getName() { return name; }
    public String getEmail() { return email; }
    public String getPassword() { return password; }
    public String getRole() { return role; }
    public int getBalance() { return balance; }

    public void setBalance(int balance) {
        this.balance = balance;
    }
}
