#!/bin/bash

#############################################################################
# Ochuko AI v5.0 - One-Click Deployment Script
# 
# Usage: bash deploy.sh [OPTIONS]
#   --quick-start       Deploy locally with minimal config (default)
#   --production        Deploy on server for production
#   --help              Show this help message
#
# Author: David Akpoviroro Oke (MrIridescent)
# Version: 5.0.0
#############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEPLOYMENT_TYPE=${1:-"--quick-start"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="ochuko-ai"

#############################################################################
# UTILITY FUNCTIONS
#############################################################################

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

#############################################################################
# SYSTEM CHECKS
#############################################################################

check_system_requirements() {
    print_header "Checking System Requirements"

    local missing_tools=()

    # Check Docker
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
        print_error "Docker not found"
    else
        docker_version=$(docker --version)
        print_success "Docker installed: $docker_version"
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        # Try new format
        if ! docker compose version &> /dev/null; then
            missing_tools+=("docker-compose")
            print_error "Docker Compose not found"
        else
            print_success "Docker Compose installed"
        fi
    else
        print_success "Docker Compose installed"
    fi

    # Check Git (optional)
    if command -v git &> /dev/null; then
        print_success "Git installed"
    else
        print_warning "Git not installed (optional, can download ZIP instead)"
    fi

    # Check available disk space (minimum 10GB)
    disk_available=$(df "$SCRIPT_DIR" | tail -1 | awk '{print $4}')
    disk_available_gb=$((disk_available / 1024 / 1024))
    
    if [ "$disk_available_gb" -lt 10 ]; then
        print_error "Only ${disk_available_gb}GB disk space available (minimum 10GB required)"
        missing_tools+=("disk-space")
    else
        print_success "Disk space: ${disk_available_gb}GB available"
    fi

    # Check available RAM (minimum 2GB)
    ram_available=$(free -b | awk '/^Mem:/ {print $7}')
    ram_available_gb=$((ram_available / 1024 / 1024 / 1024))
    
    if [ "$ram_available_gb" -lt 2 ]; then
        print_warning "Only ${ram_available_gb}GB RAM available (minimum 4GB recommended)"
    else
        print_success "RAM available: ${ram_available_gb}GB"
    fi

    # Report missing tools
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_error "\nMissing required tools: ${missing_tools[*]}"
        print_info "Please install Docker from: https://docs.docker.com/get-docker/"
        return 1
    fi

    print_success "\nAll system requirements met!"
    return 0
}

#############################################################################
# ENVIRONMENT SETUP
#############################################################################

setup_environment() {
    print_header "Setting Up Environment"

    # Check if .env exists
    if [ -f "$SCRIPT_DIR/.env" ]; then
        print_warning ".env file already exists"
        read -p "Do you want to use existing .env? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_success "Using existing .env"
            return 0
        fi
    fi

    # Create .env from template
    if [ ! -f "$SCRIPT_DIR/.env.example" ]; then
        print_error ".env.example not found!"
        return 1
    fi

    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    print_success ".env file created from template"

    # For quick-start, generate a safe secret key
    if [ "$DEPLOYMENT_TYPE" = "--quick-start" ]; then
        random_secret=$(openssl rand -hex 32)
        sed -i.bak "s/SECRET_KEY=.*/SECRET_KEY=$random_secret/" "$SCRIPT_DIR/.env"
        rm -f "$SCRIPT_DIR/.env.bak"
        print_success "Generated secure SECRET_KEY"

        # For development, set DEBUG
        sed -i.bak "s/ENV=.*/ENV=development/" "$SCRIPT_DIR/.env"
        sed -i.bak "s/DEBUG=.*/DEBUG=true/" "$SCRIPT_DIR/.env"
        rm -f "$SCRIPT_DIR/.env.bak"
        print_success "Configured for development environment"
    fi

    if [ "$DEPLOYMENT_TYPE" = "--production" ]; then
        random_secret=$(openssl rand -hex 32)
        sed -i.bak "s/SECRET_KEY=.*/SECRET_KEY=$random_secret/" "$SCRIPT_DIR/.env"
        rm -f "$SCRIPT_DIR/.env.bak"
        print_success "Generated secure SECRET_KEY"

        # For production, disable debug
        sed -i.bak "s/ENV=.*/ENV=production/" "$SCRIPT_DIR/.env"
        sed -i.bak "s/DEBUG=.*/DEBUG=false/" "$SCRIPT_DIR/.env"
        rm -f "$SCRIPT_DIR/.env.bak"
        print_success "Configured for production environment"
    fi

    print_info "\nEdit .env file to add API keys (optional)"
    print_info "nano .env"
    echo
}

#############################################################################
# DIRECTORY SETUP
#############################################################################

setup_directories() {
    print_header "Creating Required Directories"

    mkdir -p "$SCRIPT_DIR/data/postgres"
    print_success "Created data/postgres"

    mkdir -p "$SCRIPT_DIR/data/mongodb"
    print_success "Created data/mongodb"

    mkdir -p "$SCRIPT_DIR/data/redis"
    print_success "Created data/redis"

    mkdir -p "$SCRIPT_DIR/logs"
    print_success "Created logs directory"

    mkdir -p "$SCRIPT_DIR/uploads"
    print_success "Created uploads directory"

    mkdir -p "$SCRIPT_DIR/scripts"
    print_success "Created scripts directory"

    # Fix permissions
    chmod -R 755 "$SCRIPT_DIR/data"
    chmod -R 755 "$SCRIPT_DIR/logs"
    chmod -R 755 "$SCRIPT_DIR/uploads"
}

#############################################################################
# SERVICE DEPLOYMENT
#############################################################################

deploy_services() {
    print_header "Starting Services"

    cd "$SCRIPT_DIR"

    # Check if using old or new docker-compose command
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi

    print_info "Using: $COMPOSE_CMD"
    print_info "Starting services (this may take 2-5 minutes)..."
    echo

    $COMPOSE_CMD down 2>/dev/null || true
    print_info "Cleaned up old containers"

    $COMPOSE_CMD up -d
    print_success "Services started"

    # Wait for services to be healthy
    print_info "\nWaiting for services to become healthy..."
    sleep 5

    # Check backend health
    print_info "Checking backend health..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health &> /dev/null; then
            print_success "Backend is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Backend health check timeout (may still be starting)"
        fi
        sleep 1
    done
}

#############################################################################
# VERIFICATION
#############################################################################

verify_deployment() {
    print_header "Verifying Deployment"

    # Check if using old or new docker-compose command
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi

    # Count running containers
    running=$($COMPOSE_CMD ps -q | wc -l)
    total=$(grep "^  [a-z]" "$SCRIPT_DIR/docker-compose.yml" | wc -l)

    if [ "$running" -ge 3 ]; then
        print_success "Services running: $running/$total"
    else
        print_warning "Only $running/$total services running"
    fi

    # Check backend
    if curl -s http://localhost:8000/health | grep -q "healthy\|status"; then
        print_success "Backend API responding ✓"
    else
        print_warning "Backend API not responding yet (still starting)"
    fi

    # Check frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend accessible ✓"
    else
        print_warning "Frontend not responding yet (still starting)"
    fi

    # Check databases
    $COMPOSE_CMD ps | grep -q "postgres" && print_success "PostgreSQL running ✓"
    $COMPOSE_CMD ps | grep -q "mongodb" && print_success "MongoDB running ✓"
    $COMPOSE_CMD ps | grep -q "redis" && print_success "Redis running ✓"
}

#############################################################################
# INFO OUTPUT
#############################################################################

show_deployment_info() {
    print_header "🎉 DEPLOYMENT COMPLETE!"

    echo -e "${GREEN}Your Ochuko AI v5.0 is now running!${NC}\n"

    echo "Access your system:"
    echo -e "${BLUE}  Web Interface:  ${GREEN}http://localhost:3000${NC}"
    echo -e "${BLUE}  API Docs:       ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "${BLUE}  Backend API:    ${GREEN}http://localhost:8000${NC}"
    echo -e "${BLUE}  Health Check:   ${GREEN}http://localhost:8000/health${NC}\n"

    echo "Useful commands:"
    echo -e "  ${YELLOW}bash scripts/health-check.sh${NC}     - Check system status"
    echo -e "  ${YELLOW}bash scripts/logs.sh${NC}             - View logs"
    echo -e "  ${YELLOW}bash scripts/restart-services.sh${NC} - Restart services"
    echo -e "  ${YELLOW}bash scripts/stop.sh${NC}             - Stop all services"
    echo -e "  ${YELLOW}docker-compose logs -f${NC}          - Real-time logs\n"

    if [ "$DEPLOYMENT_TYPE" = "--quick-start" ]; then
        echo "Next steps:"
        echo -e "  1. Open ${GREEN}http://localhost:3000${NC} in your browser"
        echo -e "  2. Start chatting with Ochuko AI"
        echo -e "  3. (Optional) Add API keys to .env for full features\n"
    fi

    echo "Documentation:"
    echo "  - DEPLOYMENT_READY.md - Full deployment guide"
    echo "  - README.md - System overview"
    echo "  - V5_INTEGRATION_ARCHITECTURE.md - Technical details"
}

#############################################################################
# CREATE HELPER SCRIPTS
#############################################################################

create_helper_scripts() {
    print_header "Creating Helper Scripts"

    # Health check script
    cat > "$SCRIPT_DIR/scripts/health-check.sh" << 'EOF'
#!/bin/bash
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi
echo "🏥 System Health Check"
echo "====================="
echo ""
$COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}"
echo ""
echo "API Check:"
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "API not responding"
EOF
    chmod +x "$SCRIPT_DIR/scripts/health-check.sh"
    print_success "Created health-check.sh"

    # Logs script
    cat > "$SCRIPT_DIR/scripts/logs.sh" << 'EOF'
#!/bin/bash
if command -v docker-compose &> /dev/null; then
    docker-compose logs -f --tail 100
else
    docker compose logs -f --tail 100
fi
EOF
    chmod +x "$SCRIPT_DIR/scripts/logs.sh"
    print_success "Created logs.sh"

    # Restart script
    cat > "$SCRIPT_DIR/scripts/restart-services.sh" << 'EOF'
#!/bin/bash
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi
echo "Restarting services..."
$COMPOSE_CMD restart
echo "Done!"
EOF
    chmod +x "$SCRIPT_DIR/scripts/restart-services.sh"
    print_success "Created restart-services.sh"

    # Stop script
    cat > "$SCRIPT_DIR/scripts/stop.sh" << 'EOF'
#!/bin/bash
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi
echo "Stopping services..."
$COMPOSE_CMD down
echo "Done!"
EOF
    chmod +x "$SCRIPT_DIR/scripts/stop.sh"
    print_success "Created stop.sh"

    # Access info script
    cat > "$SCRIPT_DIR/scripts/access-info.sh" << 'EOF'
#!/bin/bash
echo "🌐 Access Information"
echo "===================="
echo "Web Interface:  http://localhost:3000"
echo "API Docs:       http://localhost:8000/docs"
echo "Backend API:    http://localhost:8000"
echo "Health Check:   http://localhost:8000/health"
echo ""
echo "On a server?"
echo "  Replace 'localhost' with your server IP or domain"
echo "  Example: http://your-domain.com:3000"
EOF
    chmod +x "$SCRIPT_DIR/scripts/access-info.sh"
    print_success "Created access-info.sh"
}

#############################################################################
# SHOW HELP
#############################################################################

show_help() {
    cat << EOF
Ochuko AI v5.0 - Deployment Script

Usage: bash deploy.sh [OPTIONS]

Options:
  --quick-start       Deploy locally with minimal config (default, best for testing)
  --production        Deploy on server for production use
  --help              Show this help message

Examples:
  # Quick local deployment (easiest)
  bash deploy.sh --quick-start

  # Production deployment on server
  bash deploy.sh --production

  # Show help
  bash deploy.sh --help

What it does:
  1. Checks system requirements (Docker, space, memory)
  2. Creates .env configuration file
  3. Creates necessary directories
  4. Starts all services (backend, frontend, databases)
  5. Verifies everything is working
  6. Shows access information

Requirements:
  - Docker (with Docker Compose)
  - 2GB RAM minimum (4GB+ recommended)
  - 10GB disk space minimum
  - Linux/macOS/Windows WSL2

For more information, see DEPLOYMENT_READY.md

EOF
}

#############################################################################
# MAIN EXECUTION
#############################################################################

main() {
    echo ""
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════╗"
    echo "║  Ochuko AI v5.0                       ║"
    echo "║  One-Click Deployment Script                   ║"
    echo "║  Author: David Akpoviroro Oke (MrIridescent)  ║"
    echo "╚════════════════════════════════════════════════╝"
    echo -e "${NC}"

    # Handle help
    if [ "$DEPLOYMENT_TYPE" = "--help" ] || [ "$DEPLOYMENT_TYPE" = "-h" ]; then
        show_help
        exit 0
    fi

    # Validate deployment type
    if [ "$DEPLOYMENT_TYPE" != "--quick-start" ] && [ "$DEPLOYMENT_TYPE" != "--production" ]; then
        print_error "Unknown deployment type: $DEPLOYMENT_TYPE"
        show_help
        exit 1
    fi

    print_info "Deployment mode: $DEPLOYMENT_TYPE"
    echo

    # Run deployment steps
    check_system_requirements || exit 1
    setup_environment
    setup_directories
    create_helper_scripts
    deploy_services
    verify_deployment
    show_deployment_info

    print_success "\n✨ Deployment successful! Enjoy Ochuko AI v5.0! ✨\n"
}

# Run main function
main
