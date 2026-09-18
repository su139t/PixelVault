# PixelVault

PixelVault is a smart image hosting and management platform inspired by Google Photos. The project stores image metadata in PostgreSQL, keeps actual image files in Telegram Saved Messages using Telethon, and uses local AI tools for image understanding, OCR-like text detection, and future smart search.

## Project stack

Frontend
- React
- Vite
- Axios
- Tailwind CSS

Backend
- Python
- Flask
- Flask-CORS
- PostgreSQL with psycopg
- Telethon
- Pillow (planned)
- Ollama (planned)
- CompreFace (planned)

## Current project status

Completed
- React + Vite frontend initialized
- Flask backend initialized
- PostgreSQL configured and connected
- Modular backend structure created
- Users module implemented in Route → Controller → Service → Repository pattern
- Health and DB test endpoints working
- Frontend centralized API service created
- Telethon dependency installed and verified
- Telegram login service scaffold created

In progress
- Telegram user authentication flow
- Saved Messages validation
- Image upload pipeline
- AI vision processing
- Face recognition integration
- Smart search

## Main project structure

```text
PixelVault/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── controllers/
│   │   │   ├── health_controller.py
│   │   │   └── users_controller.py
│   │   ├── repositories/
│   │   │   ├── health_repository.py
│   │   │   └── users_repository.py
│   │   ├── routes/
│   │   │   ├── health_route.py
│   │   │   └── users_route.py
│   │   ├── services/
│   │   │   ├── health_service.py
│   │   │   ├── telegram_service.py
│   │   │   └── users_service.py
│   │   └── utils/
│   │       ├── exceptions.py
│   │       ├── responses.py
│   │       └── validators.py
│   ├── scripts/
│   │   └── telegram_login.py
│   ├── .env
│   ├── .gitignore
│   ├── requirements.txt
│   ├── run.py
│   └── pixelvault.session  (generated locally, do not commit)
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── .venv/
├── .gitignore
└── README.md
```

## Environment setup

### 1. Create Python environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd ../frontend
npm install
```

## Installed packages currently used in this project

### Backend

From [backend/requirements.txt](backend/requirements.txt):

```text
blinker==1.9.0
click==4.4?  # version in environment may vary
Flask==3.1.3
flask-cors==6.0.5
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
psycopg==3.3.5
psycopg-binary==3.3.5
pyaes==1.6.1
pyasn1==0.6.4
python-dotenv==1.2.3
rsa==4.9.1
Telethon==1.44.0
Werkzeug==3.1.8
```

Note: Use the exact requirements file as the source of truth. Do not hardcode package versions here beyond the installed state.

### Frontend

From [frontend/package.json](frontend/package.json):

```json
{
  "dependencies": {
    "@tailwindcss/vite": "^4.3.3",
    ""axios": "^1.20.0",
    "react": "^19.2.8",
    "react-dom": "^19.2.8",
    "tailwindcss": "^4.3.3"
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.4",
    "eslint": "^10.8.0",
    "eslint-plugin-react-hooks": "^7.1.1",
    "eslint-plugin-react-refresh": "^0.5.3",
    "globals": "^17.7.0",
    "vite": "^8.2.0"
  }
}
```

## Backend environment variables

Create [backend/.env](backend/.env) with values similar to:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=pixelvault
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+919876543210
```

Important
- Never commit this file
- Never share the API hash in GitHub or chat
- Keep it only in local environment

## Git ignore rules

The backend ignores these files:

```gitignore
.env
.env.*
!.env.example
venv/
.venv/
env/
__pycache__/
*.py[cod]
*$py.class
*.session
*.session-journal
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.ruff_cache/
.DS_Store
```

## Run commands

### Backend

```bash
cd /Users/sumitbirla/Downloads/PixelVault/backend
source /Users/sumitbirla/Downloads/PixelVault/.venv/bin/activate
python run.py
```

Expected URL:

```text
http://127.0.0.1:5000
```

### Frontend

```bash
cd /Users/sumitbirla/Downloads/PixelVault/frontend
npm install
npm run dev
```

Expected URL:

```text
http://localhost:5173
```

### Telethon login test

```bash
cd /Users/sumitbirla/Downloads/PixelVault/backend
source /Users/sumitbirla/Downloads/PixelVault/.venv/bin/activate
python scripts/telegram_login.py
```

This starts the one-time Telegram login flow and creates a session file if successful.

## API checks already verified

The following endpoints were checked successfully:

```bash
curl http://127.0.0.1:5000/api/health
curl http://127.0.0.1:5000/api/db-test
curl http://127.0.0.1:5000/api/users
curl -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" -d '{"telegram_user_id":987654322,"name":"Phase Two Test 2","username":"phase_two_test_2","email":"phase2b@example.com"}'
```

Expected results:
- Health returns status success
- DB test returns database info
- GET users returns user list
- POST users returns created user payload

## Useful project commands

### Python syntax check

```bash
cd /Users/sumitbirla/Downloads/PixelVault/backend
source /Users/sumitbirla/Downloads/PixelVault/.venv/bin/activate
python -m compileall -q app scripts
```

### Frontend lint

```bash
cd /Users/sumitbirla/Downloads/PixelVault/frontend
npm run lint
```

### Frontend build

```bash
cd /Users/sumitbirla/Downloads/PixelVault/frontend
npm run build
```

### Git status

```bash
cd /Users/sumitbirla/Downloads/PixelVault
git status
```

### Git commit

```bash
git add backend/.gitignore backend/app backend/run.py backend/requirements.txt frontend/src frontend/package.json frontend/package-lock.json
git commit -m "complete phase 2 modular backend"
```

## Next phase plan

Phase 3: Telegram authentication
- secure environment-based login
- Telethon session management
- verify Saved Messages access
- do not expose secrets in frontend or GitHub

Phase 4: Image upload
- Pillow processing
- Telegram Saved Messages storage
- PostgreSQL metadata save

Phase 5: AI image understanding
- Ollama local vision model
- image description and visible text extraction

Phase 6: Face recognition
- CompreFace
- people grouping

Phase 7: Smart search
- tag, title, AI text, date, and people search

## Notes

- Use http://127.0.0.1:5000 for backend API calls instead of localhost:5000.
- Use http://localhost:5173 for the frontend dev server.
- Do not commit local credential files or Telegram session files.
- Keep all project work modular and incremental.
