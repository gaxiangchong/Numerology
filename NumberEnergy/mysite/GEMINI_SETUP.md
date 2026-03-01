# Gemini AI + File Search (Pro feature)

Pro users can ask the AI whether a number or car plate suits their needs. Answers use your Google File Search knowledge base.

## 1. Install

```bash
pip install google-genai
```

**If the app still says "GenAI SDK not available" or "No module named 'google'":**  
Flask must use the **same** Python environment where you ran `pip install google-genai`.

1. **Activate your venv** (e.g. `.\venv\Scripts\Activate.ps1` on Windows in `NumberEnergy\mysite`).
2. In that same terminal, run:
   ```bash
   pip install google-genai
   python -c "import google.genai; print('OK')"
   ```
   If the last line prints `OK`, that environment has the SDK.
3. **Start Flask in that same terminal** (e.g. `python app.py` or `flask run`). Do not start Flask from a different terminal or IDE run config that might use another Python.

## 2. Where to set the API key

**Get a key:** [Google AI Studio](https://aistudio.google.com/apikey) → Create API key.

Then set it in one of these ways:

### Option A: `.env` file (recommended for local dev)

1. In the **`NumberEnergy/mysite`** folder, create a file named **`.env`**.
2. Add a line (replace with your real key):
   ```env
   GOOGLE_GEMINI_API_KEY=your_api_key_here
   ```
3. Optional: add the file search store name if you created one:
   ```env
   GEMINI_FILE_SEARCH_STORE_NAME=fileSearchStores/your_store_id
   ```
4. **Do not commit `.env`** to git (it should be in `.gitignore`). The app loads `.env` automatically if `python-dotenv` is installed.

### Option B: System environment

- **Windows (PowerShell, current session):**
  ```powershell
  $env:GOOGLE_GEMINI_API_KEY="your_api_key_here"
  ```
- **Windows (permanent):** Settings → System → About → Advanced system settings → Environment Variables → New (User or System) → Variable name: `GOOGLE_GEMINI_API_KEY`, Value: your key.
- **Mac/Linux (current session):**
  ```bash
  export GOOGLE_GEMINI_API_KEY=your_api_key_here
  ```
- **Mac/Linux (permanent):** Add the `export` line to `~/.bashrc` or `~/.zshrc`.

Restart the Flask app after changing the environment.

## 3. Environment variables reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_GEMINI_API_KEY` or `GEMINI_API_KEY` | Yes | Your Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). |
| `GEMINI_FILE_SEARCH_STORE_NAME` | No | Name of an existing File Search store (e.g. `fileSearchStores/abc123`). If unset, the model answers without the knowledge base. |

## 4. Create the File Search store (one-time)

**Option A – Use the helper script (recommended)**  
From `NumberEnergy/mysite` with venv activated and `GOOGLE_GEMINI_API_KEY` in `.env`:

```bash
python create_file_search_store.py
```

The script creates a store named **易数 Knowledge Base** and prints a line like:

```text
GEMINI_FILE_SEARCH_STORE_NAME=fileSearchStores/xxxxxxxxxx
```

Add that line to your `.env` file (in `mysite` or `NumberEnergy`). Then upload your knowledge file:

```bash
python upload_knowledge.py knowledge/AGENT_易数_Phone_CarPlate_Specialist.md
```

**Optional:** Create the store and upload a file in one step:

```bash
python create_file_search_store.py knowledge/AGENT_易数_Phone_CarPlate_Specialist.md
```

**List existing stores:**  
If you already have stores and want to see their names:

```bash
python create_file_search_store.py --list
```

**Option B – Run Python manually**  
If you prefer not to use the script:

```python
import os
# load .env then:
from google import genai
client = genai.Client(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])
store = client.file_search_stores.create(config={"display_name": "易数 Knowledge Base"})
print("GEMINI_FILE_SEARCH_STORE_NAME=" + store.name)
```

Then set `GEMINI_FILE_SEARCH_STORE_NAME` in `.env` to that value.

## 5. Reset the knowledge base (clear and start fresh)

If answers are wrong or outdated, the cleanest way is to **create a new store** and point the app at it. The API does not support clearing a store’s contents; creating a new store is the supported “reset.”

**Steps:**

1. From `NumberEnergy/mysite` (venv activated, `GOOGLE_GEMINI_API_KEY` in `.env`):
   ```bash
   python create_file_search_store.py --reset
   ```
   This creates a **new** store and uploads the default knowledge file (`knowledge/AGENT_Phone_CarPlate_Specialist.md` or similar). To upload a specific file instead:
   ```bash
   python create_file_search_store.py --reset knowledge/AGENT_Phone_CarPlate_Specialist.md
   ```
   Or multiple files:
   ```bash
   python create_file_search_store.py --reset knowledge/file1.md knowledge/file2.md
   ```

2. The script prints a line like:
   ```text
   GEMINI_FILE_SEARCH_STORE_NAME=fileSearchStores/xxxxxxxxxx
   ```

3. **Update your `.env`** (in `mysite` or `NumberEnergy`): set `GEMINI_FILE_SEARCH_STORE_NAME` to that **new** value.

4. Restart the app. The AI will use the new store. The old store remains in Google but is no longer used.

---

## 6. Update your knowledge base (add or replace documents)

The knowledge base is **not** in your project folder — it lives in Google’s File Search store. To update it:

1. **Store name**  
   You must have created a store (section 4) and set `GEMINI_FILE_SEARCH_STORE_NAME` in `.env` (e.g. `fileSearchStores/abc123`).

2. **Add or update documents**  
   Use the same API to upload files into that **existing** store. Each upload adds a new document (it does not delete old ones unless you remove them via the API).

   **Option A – Run the helper script (recommended)**  
   From `NumberEnergy/mysite` (with venv activated and `.env` with `GOOGLE_GEMINI_API_KEY` and `GEMINI_FILE_SEARCH_STORE_NAME` set):

   ```bash
   python upload_knowledge.py path/to/your/knowledge_file.pdf
   ```

   You can run it multiple times with different files to add more documents to the same store.

   **Option B – Run Python yourself**  
   In a script or REPL:

   ```python
   import time
   import os
   from dotenv import load_dotenv
   load_dotenv()  # or load_dotenv('path/to/.env')

   from google import genai  # or: import google.genai as genai

   client = genai.Client(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])
   store_name = os.environ["GEMINI_FILE_SEARCH_STORE_NAME"]  # e.g. fileSearchStores/...

   # Add one file (repeat for more files)
   operation = client.file_search_stores.upload_to_file_search_store(
       file_search_store_name=store_name,
       file=r"path\to\your\knowledge_file.pdf"
   )
   while not operation.done:
       time.sleep(2)
       operation = client.operations.get(operation)
   print("Upload done.")
   ```

3. **Where to keep your source files**  
   Keep your PDF/TXT/DOCX files anywhere you like (e.g. `NumberEnergy/mysite/knowledge/`). Only the **upload step** (script or script above) sends them to the store; the app does not read from that folder at runtime.

4. **Pre-built agent guide (phone & car plate specialist)**  
   The file `mysite/knowledge/AGENT_易数_Phone_CarPlate_Specialist.md` is a ready-to-upload knowledge document that specializes the AI in 易数 analysis for **phone numbers** and **car plate numbers**. It includes the eight energy types, pair mappings, ending-digit warnings, special combinations, and multi-digit patterns from the app. Upload it to your File Search store so the AI answers using this framework:

   ```bash
   python upload_knowledge.py knowledge/AGENT_易数_Phone_CarPlate_Specialist.md
   ```

## 7. Usage (in the app)

- **Pro users** see the **AI** item in the nav and can open the AI page to ask questions.
- They can type a question (e.g. "Is this number suitable for business?") and optionally check "Use current number/plate as context" so the AI knows which number they mean.
- The app calls Gemini (with your file search store if configured) and shows the answer.
