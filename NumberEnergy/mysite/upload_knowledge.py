#!/usr/bin/env python3
"""
Upload a file to your existing Gemini File Search store (knowledge base).
Run from mysite with venv activated and .env set (GOOGLE_GEMINI_API_KEY, GEMINI_FILE_SEARCH_STORE_NAME).

  python upload_knowledge.py path/to/your/file.pdf
  python upload_knowledge.py knowledge/易数参考.txt

Supported: PDF, TXT, DOCX, etc. (see Gemini API docs).
"""
import os
import sys
import time

# Load .env from mysite or parent
_app_dir = os.path.dirname(os.path.abspath(__file__))
_env_root = os.path.join(os.path.dirname(_app_dir), '.env')
_env_mysite = os.path.join(_app_dir, '.env')
for _p in (_env_root, _env_mysite):
    if os.path.isfile(_p):
        try:
            from dotenv import load_dotenv
            load_dotenv(_p)
            break
        except ImportError:
            with open(_p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, _, v = line.partition('=')
                        k, v = k.strip(), v.strip()
                        if k and k not in os.environ:
                            if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
                                v = v[1:-1]
                            os.environ[k] = v
            break

def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_knowledge.py <path/to/file.pdf>")
        sys.exit(1)
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        print("File not found:", path)
        sys.exit(1)

    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    store_name = (os.environ.get("GEMINI_FILE_SEARCH_STORE_NAME") or "").strip()
    if not api_key:
        print("Set GOOGLE_GEMINI_API_KEY (or GEMINI_API_KEY) in .env")
        sys.exit(1)
    if not store_name:
        print("Set GEMINI_FILE_SEARCH_STORE_NAME in .env (create a store first; see GEMINI_SETUP.md)")
        sys.exit(1)

    # Map extension to MIME type so the SDK accepts the file (e.g. .md is not auto-detected)
    _ext = (os.path.splitext(path)[1] or "").lower()
    _mime = {
        ".md": "text/plain",
        ".markdown": "text/plain",
        ".txt": "text/plain",
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }.get(_ext)
    upload_config = {"mime_type": _mime} if _mime else {}

    try:
        from google import genai
    except ImportError:
        try:
            import google.genai as genai
        except ImportError:
            print("Install the SDK: pip install google-genai")
            sys.exit(1)

    client = genai.Client(api_key=api_key)
    print("Uploading to store", store_name, "...")
    kwargs = {"file_search_store_name": store_name, "file": path}
    if upload_config:
        kwargs["config"] = upload_config
    try:
        operation = client.file_search_stores.upload_to_file_search_store(**kwargs)
    except Exception as e:
        err = str(e).lower()
        if "404" in err or "not_found" in err or "does not exist" in err or "corpora" in err:
            print("ERROR: That store name does not exist. Use the EXACT ID from when you created the store.")
            print("  Run: python create_file_search_store.py --list   to see your stores and their IDs.")
            print("  Or run: python create_file_search_store.py --reset   to create a new store and get a new ID for .env")
        raise
    while not operation.done:
        time.sleep(2)
        operation = client.operations.get(operation)
    print("Done. The new document is in your knowledge base.")
    try:
        client.close()
    except Exception:
        pass

if __name__ == "__main__":
    main()
