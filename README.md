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
- React + Vite frontend with responsive gallery layout
- Flask backend with modular Route → Controller → Service → Repository structure
- PostgreSQL image metadata persistence
- Telegram Saved Messages image storage through Telethon
- Telegram-based authentication flow and protected frontend routes
- Image validation, Pillow processing, metadata extraction, and temporary upload cleanup
- Image gallery with lazy-loaded thumbnails, download actions, and responsive layout
- Photo detail viewer with dimensions, file size, MIME type, upload date, description editing, and tag management
- Search by title, filename, description, AI description, detected text, tags, people, and upload date
- Batch image upload with per-file progress, failed-file reporting, and automatic dashboard refresh
- Gallery selection mode with bulk deletion and single-photo deletion from the detail viewer
- Favorites, albums, people, tags, and health API modules

Planned or optional integrations
- Ollama vision analysis for richer image descriptions and detected text
- CompreFace face recognition and people grouping
- Advanced full-text and vector search

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

## Feature guide

### Photos dashboard
- Upload one image or select multiple images from the file picker.
- Watch completed/total upload progress while the batch is running.
- Successful uploads appear in the dashboard automatically after completion.
- Select photos to delete several images at once.
- Open any photo to view metadata, edit its description, add/remove tags, download the original, or delete it.

### Search
Open **Search** from the sidebar and search using a text query, an upload date, or both. Text matching covers titles, filenames, descriptions, AI descriptions, detected text, tags, and people.

### API endpoints
Important endpoints include:

```text
GET    /api/health
GET    /api/images?user_id=<id>
POST   /api/images
GET    /api/images/<id>/file
PUT    /api/images/<id>
DELETE /api/images/<id>
GET    /api/images/<id>/tags
POST   /api/images/<id>/tags/<tag_id>
DELETE /api/images/<id>/tags/<tag_id>
GET    /api/search?user_id=<id>&q=<text>&date=YYYY-MM-DD
```

The frontend uses `http://127.0.0.1:5000/api` as its API base URL by default.

## Notes

- Use http://127.0.0.1:5000 for backend API calls instead of localhost:5000.
- Use http://localhost:5173 for the frontend dev server.
- Do not commit local credential files or Telegram session files.
- Keep all project work modular and incremental.
