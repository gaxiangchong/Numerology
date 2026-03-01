# Fix: pip "Unable to create process" / venv path mismatch

If you see:
```text
Fatal error in launcher: Unable to create process using '"D:\Github\NumberEnergy\venv\Scripts\python.exe" ...'
The system cannot find the file specified.
```

Your venv was created when the project was at a **different folder** (e.g. `D:\Github\NumberEnergy`). The launcher inside the venv still points to that old path.

## Quick fix: use `python -m pip`

Use the **current** Python to run pip (no need to fix the launcher):

```powershell
# From NumberEnergy (or NumberEnergy\mysite if your venv is there)
cd D:\GitHub\Numerology\NumberEnergy

# Activate venv (use the path that exists on your machine)
.\venv\Scripts\Activate.ps1
# Or if your venv is in mysite:
# .\mysite\venv\Scripts\Activate.ps1

# Install using the active Python (avoids broken pip.exe)
python -m pip install google-genai
```

## Optional: recreate the venv

To get a clean venv that matches the current project path:

```powershell
cd D:\GitHub\Numerology\NumberEnergy

# Deactivate if venv is active, then remove old venv
Remove-Item -Recurse -Force venv

# Create new venv
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Or install just what you need:
# python -m pip install google-genai
```

After that, start Flask from this same terminal (same venv): `python app.py` or `cd mysite; python app.py` as you normally do.
