#!/bin/bash

# AI Medicine Vending Machine - Docker Startup Script
# This script helps you start the development or production environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if required files exist
check_requirements() {
    local env_type=$1
    
    if [ "$env_type" = "development" ]; then
        if [ ! -f "docker-compose.dev.yml" ]; then
            print_error "docker-compose.dev.yml not found!"
            exit 1
        fi
    elif [ "$env_type" = "production" ]; then
        if [ ! -f "docker-compose.prod.yml" ]; then
            print_error "docker-compose.prod.yml not found!"
            exit 1
        fi
        if [ ! -f ".env" ]; then
            print_warning ".env file not found. Please create it based on .env.example"
        fi
    fi
    
    print_success "Required files found"
}

# Function to start development environment
start_development() {
    print_status "Starting development environment..."
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Creating from template..."
        if [ -f "backend/.env.example" ]; then
            cp backend/.env.example .env
            print_status "Please edit .env file with your configuration"
        fi
    fi
    
    # Build and start services
    print_status "Building and starting containers..."
    docker-compose -f docker-compose.dev.yml up --build -d
    
    print_success "Development environment started!"
    echo ""
    echo "Services available at:"
    echo "  Frontend (Vite): http://localhost:5173"
    echo "  Backend (FastAPI): http://localhost:8000"
    echo "  pgAdmin: http://localhost:5050"
    echo "  API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
    echo "To stop: docker-compose -f docker-compose.dev.yml down"
}

# Function to start production environment
start_production() {
    print_status "Starting production environment..."
    
    # Check for required environment variables
    if [ ! -f ".env" ]; then
        print_error ".env file is required for production. Please create it."
        exit 1
    fi
    
    # Check for SSL certificates
    if [ ! -d "nginx/ssl" ]; then
        print_warning "SSL certificates not found in nginx/ssl/"
        print_status "Creating self-signed certificates for testing..."
        mkdir -p nginx/ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/key.pem \
            -out nginx/ssl/cert.pem \
            -subj "/C=VN/ST=HCM/L=HCMC/O=Medicine Vending/CN=ai-vending-machine.com"
        print_success "Self-signed certificates created"
    fi
    
    # Build and start services
    print_status "Building and starting production containers..."
    docker-compose -f docker-compose.prod.yml up --build -d
    
    print_success "Production environment started!"
    echo ""
    echo "Services available at:"
    echo "  Application: https://ai-vending-machine.com (or https://localhost)"
    echo "  HTTP Redirect: http://ai-vending-machine.com"
    echo ""
    echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo "To stop: docker-compose -f docker-compose.prod.yml down"
}

# Function to stop services
stop_services() {
    local env_type=$1
    
    if [ "$env_type" = "development" ]; then
        print_status "Stopping development environment..."
        docker-compose -f docker-compose.dev.yml down
    elif [ "$env_type" = "production" ]; then
        print_status "Stopping production environment..."
        docker-compose -f docker-compose.prod.yml down
    else
        print_status "Stopping all environments..."
        docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
    fi
    
    print_success "Services stopped"
}

# Function to show status
show_status() {
    print_status "Container status:"
    docker ps --filter "name=medicine_vending" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Function to show logs
show_logs() {
    local env_type=$1
    local service=$2
    
    if [ "$env_type" = "development" ]; then
        if [ -z "$service" ]; then
            docker-compose -f docker-compose.dev.yml logs -f
        else
            docker-compose -f docker-compose.dev.yml logs -f "$service"
        fi
    elif [ "$env_type" = "production" ]; then
        if [ -z "$service" ]; then
            docker-compose -f docker-compose.prod.yml logs -f
        else
            docker-compose -f docker-compose.prod.yml logs -f "$service"
        fi
    fi
}

# Main script logic
case "$1" in
    "dev"|"development")
        check_docker
        check_requirements "development"
        start_development
        ;;
    "prod"|"production")
        check_docker
        check_requirements "production"
        start_production
        ;;
    "stop")
        stop_services "$2"
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs "$2" "$3"
        ;;
    "help"|*)
        echo "AI Medicine Vending Machine - Docker Management Script"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  dev, development     Start development environment"
        echo "  prod, production     Start production environment"
        echo "  stop [env]          Stop services (env: dev/prod/all)"
        echo "  status              Show container status"
        echo "  logs [env] [service] Show logs (env: dev/prod, service: optional)"
        echo "  help                Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 dev              Start development environment"
        echo "  $0 prod             Start production environment"
        echo "  $0 stop dev         Stop development environment"
        echo "  $0 logs dev backend View backend logs in development"
        echo ""
        exit 0
        ;;
esac
