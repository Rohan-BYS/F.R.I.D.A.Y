@echo off
REM ==============================================================================
REM F.R.I.D.A.Y. Midnight Protocol - Windows Task Scheduler Batch Script
REM ==============================================================================

cd /d "%~dp0..\.."

echo [%DATE% %TIME%] Triggering F.R.I.D.A.Y. Midnight Protocol...

python -c "from friday_engine.backup.midnight import MidnightProtocol; p = MidnightProtocol(); print(p.execute_backup())"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Midnight Protocol failed with error code %ERRORLEVEL%
) else (
    echo [%DATE% %TIME%] Midnight Protocol completed successfully.
)
