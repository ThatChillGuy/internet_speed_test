@echo off
echo Starting Internet Speed Tester...
echo.

REM Try to run the script with python command
python speed_test.py

REM If that fails, try with python3 command
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying with python3 command...
    python3 speed_test.py
)

echo.
echo Program execution completed.
echo.
pause