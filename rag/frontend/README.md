# Frontend (Next.js)

## Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local  # edit NEXT_PUBLIC_BACKEND_BASE if your API is not localhost:8000
npm run dev
# Open http://localhost:3000
```

The UI has:
- A **Run Daily Screen** button that calls `POST /run-daily` on the backend.
- Renders the returned Markdown tables for Short-Premium ideas and Long-Term buys.
