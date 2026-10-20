@echo off
echo ========================================================
echo   Employee Leave Management System (HRMS Portal)
echo ========================================================
echo.
echo Compiling Java files (App.java, DataStore.java, User.java, Leave.java)...
javac *.java

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b %errorlevel%
)

echo Starting Server at http://localhost:8080 ...
start "" "http://localhost:8080"
java App
pause
