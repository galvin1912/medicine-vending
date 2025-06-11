#!/bin/bash
# Script to activate the Python virtual environment for the AI Vending Machine backend
echo "Activating Python virtual environment..."
source ./venv/bin/activate
echo "Virtual environment activated!"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo ""
echo "You can now run your FastAPI application with:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
