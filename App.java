import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;

/**
 * Main Web Server class.
 * Starts built-in Java HTTP server on port 8080 and handles HTTP API endpoints.
 */
public class App {
    private static final int PORT = 8080;

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        // 1. Static Files (HTML, CSS, JS)
        server.createContext("/", exchange -> {
            String path = exchange.getRequestURI().getPath();
            if (path.equals("/") || path.isEmpty()) path = "/index.html";

            File file = new File("." + path);
            if (!file.exists()) {
                sendText(exchange, 404, "404 Not Found");
                return;
            }

            String contentType = "text/html";
            if (path.endsWith(".css")) contentType = "text/css";
            else if (path.endsWith(".js")) contentType = "application/javascript";

            byte[] bytes = Files.readAllBytes(file.toPath());
            exchange.getResponseHeaders().set("Content-Type", contentType);
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) { os.write(bytes); }
        });

        // 2. API: Login
        server.createContext("/api/login", exchange -> {
            String body = readBody(exchange);
            String email = getField(body, "email");
            String password = getField(body, "password");

            User user = DataStore.login(email, password);
            if (user != null) {
                String json = String.format("{\"success\":true,\"name\":\"%s\",\"email\":\"%s\",\"role\":\"%s\",\"balance\":%d}",
                        user.getName(), user.getEmail(), user.getRole(), user.getBalance());
                sendJson(exchange, 200, json);
            } else {
                sendJson(exchange, 401, "{\"success\":false,\"error\":\"Invalid email or password!\"}");
            }
        });

        // 3. API: Get Leaves & Balance
        server.createContext("/api/data", exchange -> {
            String query = exchange.getRequestURI().getQuery();
            String email = (query != null && query.contains("email=")) ? query.split("email=")[1].split("&")[0] : "";
            
            User user = DataStore.getUser(email);
            List<Leave> leaves = DataStore.getLeaves(email);

            StringBuilder sb = new StringBuilder();
            sb.append("{");
            sb.append("\"balance\":").append(user != null ? user.getBalance() : 0).append(",");
            sb.append("\"leaves\":[");

            for (int i = 0; i < leaves.size(); i++) {
                Leave l = leaves.get(i);
                sb.append(String.format("{\"id\":%d,\"name\":\"%s\",\"email\":\"%s\",\"type\":\"%s\",\"from\":\"%s\",\"to\":\"%s\",\"days\":%d,\"reason\":\"%s\",\"status\":\"%s\"}",
                        l.getId(), l.getEmpName(), l.getEmpEmail(), l.getLeaveType(), l.getFromDate(), l.getToDate(), l.getDays(), escape(l.getReason()), l.getStatus()));
                if (i < leaves.size() - 1) sb.append(",");
            }
            sb.append("]}");

            sendJson(exchange, 200, sb.toString());
        });

        // 4. API: Apply Leave
        server.createContext("/api/apply", exchange -> {
            String body = readBody(exchange);
            String email = getField(body, "email");
            String type = getField(body, "type");
            String from = getField(body, "from");
            String to = getField(body, "to");
            int days = 1;
            try { days = Integer.parseInt(getField(body, "days")); } catch (Exception ignored) {}
            String reason = getField(body, "reason");

            String result = DataStore.applyLeave(email, type, from, to, days, reason);
            if ("SUCCESS".equals(result)) {
                sendJson(exchange, 200, "{\"success\":true,\"message\":\"Leave application submitted!\"}");
            } else {
                sendJson(exchange, 400, "{\"success\":false,\"error\":\"" + result + "\"}");
            }
        });

        // 5. API: Approve or Reject
        server.createContext("/api/action", exchange -> {
            try {
                String body = readBody(exchange);
                String idStr = getField(body, "id");
                String status = getField(body, "status"); // "APPROVED" or "REJECTED"

                if (idStr.isEmpty()) {
                    sendJson(exchange, 400, "{\"success\":false,\"error\":\"Missing Leave ID\"}");
                    return;
                }

                int id = Integer.parseInt(idStr);
                boolean ok = DataStore.updateStatus(id, status);

                if (ok) {
                    sendJson(exchange, 200, "{\"success\":true}");
                } else {
                    sendJson(exchange, 404, "{\"success\":false,\"error\":\"Leave not found\"}");
                }
            } catch (Exception e) {
                sendJson(exchange, 500, "{\"success\":false,\"error\":\"" + e.getMessage() + "\"}");
            }
        });

        server.start();
        System.out.println("==================================================");
        System.out.println(" Leave Management System Server Started!");
        System.out.println(" Open in browser: http://localhost:" + PORT);
        System.out.println("==================================================");
    }

    // Helper: Send JSON response
    private static void sendJson(HttpExchange exchange, int status, String json) throws IOException {
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) { os.write(bytes); }
    }

    // Helper: Send Plain text
    private static void sendText(HttpExchange exchange, int status, String text) throws IOException {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) { os.write(bytes); }
    }

    // Helper: Read HTTP request body
    private static String readBody(HttpExchange exchange) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line);
        return sb.toString();
    }

    // Helper: Extract field from simple JSON string
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

    private static String escape(String s) {
        if (s == null) return "";
        return s.replace("\"", "\\\"").replace("\n", " ").replace("\r", "");
    }
}
