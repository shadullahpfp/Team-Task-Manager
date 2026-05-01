# Team Task Manager

A robust, full-stack task management application designed for team collaboration, productivity tracking, and administrative control. Built with a scalable architecture, it features a Python-based backend and a responsive Next.js frontend, ensuring high performance and a seamless user experience.

## System Architecture

The application relies on a decoupled client-server architecture:

- **Backend Service (FastAPI)**: Provides a RESTful API with endpoints for authentication, project management, and task operations. It uses SQLAlchemy as an ORM for database interactions and enforces security through JWT-based authentication and role-based access control (RBAC).
- **Frontend Service (Next.js)**: A responsive, React-based web interface utilizing the App Router. It securely consumes the backend API and provides distinct views and controls based on user authorization levels.
- **Database**: Defaults to SQLite for immediate development deployment, with complete structural compatibility for PostgreSQL in production environments.

## Core Features

- **Role-Based Access Control**:
  - **Administrators**: Capable of creating new projects, assigning personnel, creating tasks, and maintaining overarching oversight.
  - **Members**: Granted access to view assigned projects, update the status of personal tasks, and interact with their individual dashboard.
- **Project & Task Management**: Categorization of tasks under specific projects with detailed assignments, descriptions, and dynamic status tracking (To Do, In Progress, Done).
- **Automated Deadline Tracking**: Built-in logic to flag overdue tasks automatically on the user dashboard.
- **Secure Authentication**: End-to-end user verification using secure password hashing (bcrypt) and short-lived JSON Web Tokens (JWT).

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 18.x or higher
- Git

### Initializing the Backend
1. Navigate to the root directory and establish a Python virtual environment:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the necessary Python dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
3. Initialize the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Initializing the Frontend
1. Open a secondary terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node packages:
   ```bash
   npm install
   ```
3. Boot the Next.js development environment:
   ```bash
   npm run dev
   ```
The web interface will be accessible at `http://localhost:3000`.

## Deployment Specifications

This repository is optimized for Platform-as-a-Service (PaaS) deployments such as Railway and Vercel. 

### Backend Configuration (Railway)
The root directory contains a `Procfile` configured for Nixpacks or standard buildpacks. Railway will automatically detect the `requirements.txt` file at the root, install dependencies, and execute the server via the instructions provided in the `Procfile`. 
Ensure the following environment variables are mapped in your production environment:
- `DATABASE_URL`: Connection string for PostgreSQL (if upgrading from SQLite).
- `SECRET_KEY`: A high-entropy cryptographic key for JWT signing.
- `FRONTEND_URL`: The production URL of the Next.js application to configure CORS appropriately.

### Frontend Configuration (Vercel)
The Next.js application can be deployed directly from the `/frontend` directory. 
Ensure you define the following environment variable prior to building:
- `NEXT_PUBLIC_API_URL`: The fully qualified domain name of the deployed backend service (e.g., `https://api.yourdomain.com`).

## Licensing & Contribution
This project is proprietary and intended for internal team utilization. Source code contributions must adhere to standard linting configurations and pass all established type checks prior to submission.
