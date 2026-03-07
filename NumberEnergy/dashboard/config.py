# Dashboard config: uses same DB as main app. Set in .env or environment.
import os

def _load_dotenv():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if not os.path.isfile(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.isfile(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, _, v = line.partition('=')
                k, v = k.strip(), v.strip()
                if k and k not in os.environ:
                    if len(v) >= 2 and v[0] in '"\'' and v[-1] == v[0]:
                        v = v[1:-1]
                    os.environ[k] = v
    except Exception:
        pass

_load_dotenv()

SECRET_KEY = os.environ.get('DASHBOARD_SECRET_KEY') or os.environ.get('SECRET_KEY') or 'dashboard-secret-change-in-production'

# Default DB path: absolute path to mysite/instance/users.db (same as main app)
_dashboard_dir = os.path.dirname(os.path.abspath(__file__))
_default_db = os.path.normpath(os.path.join(_dashboard_dir, '..', 'mysite', 'instance', 'users.db'))
# Ensure parent dir exists so SQLite can create the file
_default_db_dir = os.path.dirname(_default_db)
if not os.path.isdir(_default_db_dir):
    try:
        os.makedirs(_default_db_dir, exist_ok=True)
    except OSError:
        pass
_default_uri = 'sqlite:///' + _default_db.replace('\\', '/')
SQLALCHEMY_DATABASE_URI = (
    os.environ.get('SQLALCHEMY_DATABASE_URI') or
    os.environ.get('DATABASE_URL') or
    _default_uri
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
