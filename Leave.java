/**
 * Model class representing a single Leave Application.
 */
public class Leave {
    private int id;
    private String empName;
    private String empEmail;
    private String leaveType; // "Casual Leave", "Sick Leave", "Earned Leave"
    private String fromDate;
    private String toDate;
    private int days;
    private String reason;
    private String status;    // "PENDING", "APPROVED", "REJECTED"

    public Leave(int id, String empName, String empEmail, String leaveType, String fromDate, String toDate, int days, String reason, String status) {
        this.id = id;
        this.empName = empName;
        this.empEmail = empEmail;
        this.leaveType = leaveType;
        this.fromDate = fromDate;
        this.toDate = toDate;
        this.days = days;
        this.reason = reason;
        this.status = status;
    }

    // Getters and Setters
    public int getId() { return id; }
    public String getEmpName() { return empName; }
    public String getEmpEmail() { return empEmail; }
    public String getLeaveType() { return leaveType; }
    public String getFromDate() { return fromDate; }
    public String getToDate() { return toDate; }
    public int getDays() { return days; }
    public String getReason() { return reason; }
    public String getStatus() { return status; }

    public void setStatus(String status) {
        this.status = status;
    }
}
