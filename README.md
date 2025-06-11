# AI Medicine Vending Machine

A full-stack web application that provides AI-powered medicine recommendations based on user symptoms, built with FastAPI (Python) backend and React (Vite) frontend.

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL database, Google Gemini AI integration
- **Frontend**: React + Vite with Tailwind CSS
- **Database**: PostgreSQL with comprehensive medicine and patient data
- **AI**: Google Gemini API for symptom analysis and medicine recommendations
- **Infrastructure**: Docker containers with nginx reverse proxy

## 📋 Prerequisites

- **Docker** and **Docker Compose** (v2.0+)
- **Node.js** (v18+) and **npm** (for local frontend development)
- **Python 3.12+** (for local backend development)
- **Google Gemini API Key** (required for AI functionality)

## 🚀 Quick Start (Docker - Recommended)

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd ai-vending-machine.com

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Configure Environment Variables

Edit the `.env` file and set your Google Gemini API key:

```bash
# Required: Set your actual Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: Other configurations are pre-configured for development
SECRET_KEY=your_secret_key_here
```

### 3. Start Development Environment

```bash
# Start all services (database, backend, frontend, pgAdmin)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database Admin (pgAdmin)**: http://localhost:5050
  - Email: `admin@medicine.com`
  - Password: `admin123`

## 🛠️ Local Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Setup environment
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
```

## 🐳 Docker Configuration

### Development Environment (`docker-compose.dev.yml`)

- **PostgreSQL**: Database with sample data
- **Backend**: FastAPI with hot reload
- **Frontend**: Vite dev server with hot reload
- **pgAdmin**: Database administration interface

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View specific service logs
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend

# Rebuild specific service
docker-compose -f docker-compose.dev.yml up -d --build backend
```

### Production Environment (`docker-compose.prod.yml`)

- **PostgreSQL**: Production database
- **Backend**: Optimized FastAPI container
- **Frontend**: Built React app served by nginx
- **Nginx**: Reverse proxy with SSL support

```bash
# Setup production environment
cp .env.prod.example .env.prod
# Edit .env.prod with production values

# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 📚 API Documentation

The backend provides comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/analyze_input` - AI symptom analysis
- `POST /api/v1/confirm_prescription` - Prescription confirmation
- `GET /api/v1/medications` - Available medications
- `GET /health` - Health check endpoint

## 🗄️ Database

### Schema Overview

- **Patients**: Patient information and medical history
- **Medications**: Comprehensive medicine catalog
- **Prescriptions**: AI-generated prescriptions and dosages
- **Symptoms**: Symptom catalog and medication relationships

## 📁 Project Structure

```
ai-vending-machine.com/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application code
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── README.md             # Backend documentation
├── frontend/                  # React frontend
│   ├── src/                  # Source code
│   ├── package.json          # Node dependencies
│   ├── Dockerfile            # Frontend container
│   └── Dockerfile.dev        # Frontend dev container
├── nginx/                     # Nginx configuration
├── docker-compose.dev.yml     # Development environment
├── docker-compose.prod.yml    # Production environment
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🎯 Development Workflow

1. **Start Development**: `docker-compose -f docker-compose.dev.yml up -d`
2. **Make Changes**: Edit files in `backend/` or `frontend/`
3. **Hot Reload**: Changes automatically reflected (backend & frontend)
4. **Test**: Use API docs at http://localhost:8000/docs
5. **Database**: Use pgAdmin at http://localhost:5050
6. **Deploy**: Use production compose file for deployment


## 📄 License

Author: [Galvin Nguyen](https://github.com/galvin1912)
