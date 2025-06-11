# AI Medicine Vending Machine - Backend

## Quick Start

### Prerequisites ✅
- Python 3.12.3 (installed)
- pip 24.0 (installed)
- Virtual environment (created)
- All dependencies (installed)

### Activate Environment & Run
```bash
# Activate virtual environment
source venv/bin/activate

# Or use the convenience script
./activate_venv.sh

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test Setup
```bash
python test_setup.py
```

### Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql://user:password@localhost/medicine_vending_db
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
```

---

# Backend folder structure
app/
├── __init__.py              # Makes app a Python package
├── main.py                  # FastAPI application entry point
├── core/                    # Core application configuration
│   ├── __init__.py
│   ├── config.py           # Settings and configuration
│   └── security.py         # Security utilities (if needed)
├── database/                # Database configuration and session
│   ├── __init__.py
│   ├── connection.py       # Database connection setup
│   ├── base.py            # Base database class
│   └── session.py         # Database session management
├── models/                  # SQLAlchemy ORM models (database tables)
│   ├── __init__.py
│   ├── patient.py          # Patient model
│   ├── medication.py       # Medication model
│   ├── prescription.py     # Prescription models
│   └── symptom.py          # Symptom model
├── schemas/                 # Pydantic models for request/response
│   ├── __init__.py
│   ├── patient.py          # Patient schemas
│   ├── medication.py       # Medication schemas
│   ├── prescription.py     # Prescription schemas
│   └── ai_response.py      # AI response schemas
├── api/                     # API routes
│   ├── __init__.py
│   ├── v1/                 # API version 1
│   │   ├── __init__.py
│   │   ├── patients.py     # Patient endpoints
│   │   ├── medications.py  # Medication endpoints
│   │   ├── prescriptions.py # Prescription endpoints
│   │   └── ai_analysis.py  # AI analysis endpoints
│   └── deps.py             # Dependencies (database session, etc.)
└── services/                # Business logic
    ├── __init__.py
    ├── ai_service.py        # AI/LangChain integration
    ├── prescription_service.py # Prescription logic
    ├── medication_service.py   # Medication management
    └── patient_service.py      # Patient management

# Additional files at backend root:
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── alembic.ini            # Database migration configuration
├── alembic/               # Database migrations
└── Dockerfile             # Docker configuration
