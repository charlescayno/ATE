@echo off
REM Sync cursor/poll-effective-integration-ccf6 with GitHub (run from repo root).
setlocal
set BRANCH=cursor/poll-effective-integration-ccf6

cd /d "%~dp0.."
echo Repo: %CD%
echo.

git fetch origin
if errorlevel 1 goto :fail

git show-ref --verify --quiet refs/heads/%BRANCH%
if errorlevel 1 (
  git checkout -b %BRANCH% origin/%BRANCH% 2>nul || git checkout -b %BRANCH%
) else (
  git checkout %BRANCH%
)
if errorlevel 1 goto :fail

git pull --rebase origin %BRANCH%
if errorlevel 1 (
  echo [ERROR] Rebase failed. Resolve conflicts, then: git rebase --continue
  exit /b 1
)

git push -u origin %BRANCH%
if errorlevel 1 goto :fail

echo.
echo OK  Branch %BRANCH% is synced with origin.
exit /b 0

:fail
echo.
echo [ERROR] Sync failed. Ensure GitHub auth: gh auth login  OR  Git Credential Manager
exit /b 1
