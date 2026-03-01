#!/usr/bin/env python3
"""
Create a Gemini File Search Store (knowledge base) and get the store name for .env.
Run from mysite with venv activated and .env containing GOOGLE_GEMINI_API_KEY.

  python create_file_search_store.py              # create store, print name
  python create_file_search_store.py --list       # list existing stores (if any)
  python create_file_search_store.py file.pdf     # create store and upload file
  python create_file_search_store.py --reset      # RESET: create new store, upload default knowledge, print new name
  python create_file_search_store.py --reset path/to/file.md   # reset and upload specific file(s)

After creating (or --reset), add/update .env:
  GEMINI_FILE_SEARCH_STORE_NAME=<printed store name>
"""
import os
import sys
import time

# Load .env from mysite or parent (same as upload_knowledge.py)
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


def get_client():
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Set GOOGLE_GEMINI_API_KEY (or GEMINI_API_KEY) in .env")
        sys.exit(1)
    try:
        from google import genai
    except ImportError:
        try:
            import google.genai as genai
        except ImportError:
            print("ERROR: Install the SDK: python -m pip install google-genai")
            sys.exit(1)
    return genai.Client(api_key=api_key)


def list_stores(client):
    """List existing file search stores."""
    try:
        # Paginated list; method name may be list() or list_file_search_stores()
        stores = list(client.file_search_stores.list())
        if not stores:
            print("No file search stores found.")
            return
        for s in stores:
            name = getattr(s, "name", None) or getattr(s, "id", str(s))
            disp = getattr(s, "display_name", None) or getattr(s, "displayName", "")
            print(f"  {name}  (display: {disp})")
    except Exception as e:
        print("Could not list stores:", e)
        print("(Listing may not be available in this SDK version.)")


def _upload_file(client, store_name, path):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        print("ERROR: File not found:", path)
        return False
    print("  Uploading:", path, "...")
    try:
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store_name,
            file=path,
        )
        while not op.done:
            time.sleep(2)
            op = client.operations.get(op)
        print("  Done.")
        return True
    except Exception as e:
        print("  Upload failed:", e)
        return False


def main():
    do_list = "--list" in sys.argv or "-l" in sys.argv
    do_reset = "--reset" in sys.argv or "-r" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    upload_path = args[0] if args else None
    if upload_path and not os.path.isfile(upload_path):
        print("ERROR: File not found:", upload_path)
        sys.exit(1)

    existing = (os.environ.get("GEMINI_FILE_SEARCH_STORE_NAME") or "").strip()
    if existing and not do_list and not do_reset and not upload_path:
        print("GEMINI_FILE_SEARCH_STORE_NAME is already set in .env:")
        print(" ", existing)
        print("To reset the knowledge base, run: python create_file_search_store.py --reset")
        print("To list stores: python create_file_search_store.py --list")
        return

    client = get_client()

    if do_list:
        print("Existing file search stores:")
        list_stores(client)
        return

    # --reset: create a NEW store and upload file(s), then tell user to update .env
    if do_reset:
        display_name = "易数 Knowledge Base"
        print("RESET: Creating a NEW file search store (fresh knowledge base)...")
        try:
            store = client.file_search_stores.create(config={"display_name": display_name})
        except Exception as e:
            print("ERROR creating store:", e)
            sys.exit(1)
        store_name = getattr(store, "name", None) or getattr(store, "id", str(store))
        # Upload: specified file(s) or default knowledge file
        knowledge_dir = os.path.join(_app_dir, "knowledge")
        default_file = os.path.join(knowledge_dir, "AGENT_Phone_CarPlate_Specialist.md")
        if not os.path.isfile(default_file):
            for name in ("AGENT_易数_Phone_CarPlate_Specialist.md", "AGENT_Phone_CarPlate_Specialist.md"):
                p = os.path.join(knowledge_dir, name)
                if os.path.isfile(p):
                    default_file = p
                    break
        to_upload = args if args else ([default_file] if os.path.isfile(default_file) else [])
        if to_upload:
            for p in to_upload:
                _upload_file(client, store_name, p)
        else:
            print("No file to upload. Run: python create_file_search_store.py --reset knowledge/YourFile.md")
        print()
        print("New store created. Update your .env with:")
        print()
        print("  GEMINI_FILE_SEARCH_STORE_NAME=" + store_name)
        print()
        print("(You can leave the old store as-is; the app will use this new one once .env is updated.)")
        try:
            client.close()
        except Exception:
            pass
        return

    # Create store (non-reset)
    display_name = "易数 Knowledge Base"
    print("Creating file search store:", display_name, "...")
    try:
        store = client.file_search_stores.create(config={"display_name": display_name})
    except Exception as e:
        print("ERROR creating store:", e)
        sys.exit(1)

    store_name = getattr(store, "name", None) or getattr(store, "id", str(store))
    print()
    print("Store created successfully.")
    print()
    print("Add this line to your .env file (in mysite or NumberEnergy):")
    print()
    print("  GEMINI_FILE_SEARCH_STORE_NAME=" + store_name)
    print()
    print("Then upload knowledge files with:")
    print("  python upload_knowledge.py knowledge/AGENT_易数_Phone_CarPlate_Specialist.md")
    print()

    if upload_path:
        _upload_file(client, store_name, upload_path)

    try:
        client.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()
