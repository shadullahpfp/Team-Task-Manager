# Team Task Manager

A full-stack task management system with role-based access control. Built with FastAPI and Next.js.

## Features

- **Authentication**: JWT-based login and signup.
- **Roles**: Admin and Member roles.
- **Projects**: Admins can create projects and assign members.
- **Tasks**: Create, update, filter tasks. Track due dates and status.
- **Dashboard**: Real-time stats on tasks and overdue tracking.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js, Tailwind CSS, Axios

## Setup Instructions

### Backend
1. cd backend
2. python3 -m venv .venv
3. source .venv/bin/activate
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload

### Frontend
1. cd frontend
2. npm install
3. npm run dev

## Deployment

- Backend is configured for Railway deployment via Procfile.
- Frontend is configured for Vercel.
