# Install git pre-push hook for AI log submission (Windows PowerShell).
# Run once after cloning: powershell -ExecutionPolicy Bypass -File scripts\setup_hooks.ps1

$ErrorActionPreference = 'Stop'

$HookFile = '.git/hooks/pre-push'

# Git on Windows spawns hooks via cmd.exe by default, so use a .cmd (batch)
# script to avoid the "cannot spawn" error when bash is not on PATH.
$HookBody = @'
@echo off
rem Pre-push hook for Windows: sweep Antigravity logs, then submit to server.
rem Avoids bash dep — pure Windows batch calling python directly.

setlocal
cd /d "%~dp0.."

rem Sweep recent Antigravity / Gemini prompts into .ai-log/session.jsonl
python scripts\log_antigravity.py --auto

rem Submit pending logs to grading server (never blocks push)
python scripts\submit_log.py
if errorlevel 1 (
  echo [ai-log] submit_log.py exited %errorlevel% -- logs kept locally.
)

endlocal
exit /b 0
'@

Set-Content -Path $HookFile -Value $HookBody -Encoding UTF8 -NoNewline
Write-Host "[ai-log] Git pre-push hook installed."

if (-not (Test-Path .ai-log)) { New-Item -ItemType Directory -Path .ai-log | Out-Null }
if (-not (Test-Path .ai-log/.gitkeep)) { New-Item -ItemType File -Path .ai-log/.gitkeep | Out-Null }

Write-Host "[ai-log] Setup complete. Configure AI_LOG_SERVER in your .env file."
