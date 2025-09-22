@echo off
echo ========================================
echo        EventApp Git Setup
echo ========================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/4] Initializing Git repository...
git init

echo [2/4] Adding all files to Git...
git add .

echo [3/4] Creating initial commit...
git commit -m "Initial EventApp commit with all features"

echo [4/4] Git repository initialized successfully!
echo.
echo Next steps:
echo 1. Create a repository on GitHub/GitLab/Bitbucket
echo 2. Add remote origin: git remote add origin YOUR_REPO_URL
echo 3. Push to remote: git push -u origin main
echo.
echo For detailed instructions, see GIT_DEPLOYMENT.md
echo.
pause
