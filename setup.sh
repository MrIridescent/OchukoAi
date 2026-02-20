#!/bin/bash

#############################################################################
# Ochuko AI v5.0 - Interactive Setup Wizard
#
# This is the friendly, interactive setup for people who want to understand
# what's happening at each step.
#
# Author: David Akpoviroro Oke (MrIridescent)
# Version: 5.0.0
#############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#############################################################################
# FUNCTIONS
#############################################################################

print_header() {
    clear
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════╗"
    echo "║  Ochuko AI v5.0 Setup Wizard         ║"
    echo "║  Interactive Installation Guide                ║"
    echo "╚════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
}

print_step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}→ $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

prompt_yes_no() {
    while true; do
        read -p "$(echo -e ${YELLOW})$1${NC} (yes/no): " response
        case "$response" in
            [yY][eE][sS]|[yY]) return 0 ;;
            [nN][oO]|[nN]) return 1 ;;
            *) echo "Please answer yes or no" ;;
        esac
    done
}

#############################################################################
# STEP 1: WELCOME
#############################################################################

step_welcome() {
    print_header

    cat << 'EOF'
Welcome! This wizard will guide you through setting up Ochuko AI v5.0.

This process is interactive - I'll explain what happens at each step and ask
you questions to customize your setup.

Expected time: 5-10 minutes (plus 2-5 minutes for services to start)

Let's get started! Press Enter to continue...
EOF

    read -p ""
}

#############################################################################
# STEP 2: SYSTEM CHECK
#############################################################################

step_system_check() {
    print_step "Checking Your System"

    local issues=()

    echo "Checking for required tools..."

    # Docker
    if command -v docker &> /dev/null; then
        version=$(docker --version)
        print_success "$version"
    else
        print_error "Docker not found"
        issues+=("Docker")
    fi

    # Docker Compose
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose installed"
    elif docker compose version &> /dev/null; then
        print_success "Docker Compose installed (new format)"
    else
        print_error "Docker Compose not found"
        issues+=("Docker Compose")
    fi

    # Git (optional)
    if command -v git &> /dev/null; then
        print_success "Git installed"
    else
        print_info "Git not installed (optional - you can download ZIP instead)"
    fi

    # Disk space
    disk_gb=$(df "$SCRIPT_DIR" | tail -1 | awk '{print ($4 / 1024 / 1024)}')
    if (( $(echo "$disk_gb >= 10" | bc -l) )); then
        print_success "Disk space: ${disk_gb%.*}GB available"
    else
        print_error "Only ${disk_gb%.*}GB disk space (need 10GB)"
        issues+=("Disk Space")
    fi

    # RAM
    ram_gb=$(free -h | awk '/^Mem:/ {print $2}' | sed 's/G//')
    if (( $(echo "$ram_gb >= 4" | bc -l) )) 2>/dev/null; then
        print_success "RAM: ${ram_gb}GB available"
    else
        print_info "RAM: ${ram_gb}GB (4GB+ recommended, but might work)"
    fi

    if [ ${#issues[@]} -gt 0 ]; then
        echo ""
        print_error "Missing requirements: ${issues[*]}"
        echo ""
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        echo ""
        read -p "Press Enter when ready, or Ctrl+C to exit..."
        return 1
    fi

    echo ""
    print_success "All system checks passed!"
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 3: DEPLOYMENT TYPE
#############################################################################

step_deployment_type() {
    print_step "Choose Deployment Type"

    echo "How do you want to deploy?"
    echo ""
    echo "  1) LOCAL (for testing/development)"
    echo "     - Runs on http://localhost:3000"
    echo "     - Data lost when you stop it"
    echo "     - Good for: Testing, learning, experiments"
    echo ""
    echo "  2) PERSISTENT (for regular use)"
    echo "     - Runs on http://localhost:3000"
    echo "     - Data persists after restart"
    echo "     - Good for: Daily use, keeping data"
    echo ""
    echo "  3) PRODUCTION (for servers/cloud)"
    echo "     - Runs on your server/cloud"
    echo "     - Professional configuration"
    echo "     - Good for: Teams, public access"
    echo ""

    read -p "Choose (1-3): " choice

    case "$choice" in
        1)
            DEPLOYMENT_TYPE="local"
            ENV_TYPE="development"
            ;;
        2)
            DEPLOYMENT_TYPE="persistent"
            ENV_TYPE="development"
            ;;
        3)
            DEPLOYMENT_TYPE="production"
            ENV_TYPE="production"
            ;;
        *)
            print_error "Invalid choice"
            step_deployment_type
            return
            ;;
    esac

    echo ""
    print_success "Selected: $DEPLOYMENT_TYPE"
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 4: API KEYS (Optional)
#############################################################################

step_api_keys() {
    print_step "API Keys (Optional)"

    echo "You can add API keys now for enhanced features:"
    echo ""
    echo "  • OpenAI (GPT-4) - https://platform.openai.com/api-keys"
    echo "  • Anthropic (Claude 3) - https://console.anthropic.com/"
    echo "  • Google Cloud - https://cloud.google.com/"
    echo ""
    echo "Don't worry - the system works without them!"
    echo ""

    if prompt_yes_no "Do you have API keys to add?"; then
        echo ""
        echo "Great! Let's add them to your .env file"
        echo ""
        echo "The .env file is in: $SCRIPT_DIR/.env"
        echo ""
        echo "Format:"
        echo "  OPENAI_API_KEY=sk-..."
        echo "  CLAUDE_API_KEY=sk-ant-..."
        echo ""
        
        if prompt_yes_no "Do you want to edit .env now?"; then
            if command -v nano &> /dev/null; then
                nano "$SCRIPT_DIR/.env"
            elif command -v vim &> /dev/null; then
                vim "$SCRIPT_DIR/.env"
            else
                print_error "No text editor found"
            fi
        fi
    else
        print_info "You can add API keys later anytime"
    fi

    echo ""
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 5: ENVIRONMENT SETUP
#############################################################################

step_environment_setup() {
    print_step "Creating Configuration"

    # Create .env if needed
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        print_info "Creating .env from template..."
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        
        # Generate secret key
        secret=$(openssl rand -hex 32)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$secret/" "$SCRIPT_DIR/.env"
            sed -i '' "s/ENV=.*/ENV=$ENV_TYPE/" "$SCRIPT_DIR/.env"
        else
            sed -i "s/SECRET_KEY=.*/SECRET_KEY=$secret/" "$SCRIPT_DIR/.env"
            sed -i "s/ENV=.*/ENV=$ENV_TYPE/" "$SCRIPT_DIR/.env"
        fi
        
        print_success ".env created"
    else
        print_info ".env already exists"
    fi

    # Create directories
    print_info "Creating data directories..."
    mkdir -p "$SCRIPT_DIR/data/postgres"
    mkdir -p "$SCRIPT_DIR/data/mongodb"
    mkdir -p "$SCRIPT_DIR/data/redis"
    mkdir -p "$SCRIPT_DIR/logs"
    mkdir -p "$SCRIPT_DIR/uploads"
    mkdir -p "$SCRIPT_DIR/scripts"
    print_success "Directories created"

    echo ""
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 6: STARTUP
#############################################################################

step_startup() {
    print_step "Starting Services"

    echo "About to start:"
    echo "  • Backend API"
    echo "  • Frontend Web Interface"
    echo "  • PostgreSQL Database"
    echo "  • MongoDB Document Store"
    echo "  • Redis Cache"
    echo ""
    echo "This may take 2-5 minutes on first run."
    echo ""

    if ! prompt_yes_no "Start services now?"; then
        print_info "You can start them later with: docker-compose up -d"
        read -p "Press Enter to continue..."
        return
    fi

    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi

    echo ""
    print_info "Starting services..."
    cd "$SCRIPT_DIR"
    
    # Stop old services if running
    $COMPOSE_CMD down 2>/dev/null || true
    
    # Start new services
    $COMPOSE_CMD up -d
    
    echo ""
    print_success "Services started!"
    print_info "Waiting for services to become healthy..."
    echo ""

    # Wait and check
    for i in {1..30}; do
        echo -n "."
        if curl -s http://localhost:8000/health &> /dev/null; then
            echo ""
            print_success "Services are healthy!"
            break
        fi
        sleep 1
    done

    echo ""
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 7: VERIFICATION
#############################################################################

step_verification() {
    print_step "Checking Services"

    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi

    echo "Checking running services..."
    echo ""

    $COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}"

    echo ""
    echo "Testing API..."
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "Backend API responding"
    else
        print_error "Backend API not responding yet (still starting)"
    fi

    echo ""
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Frontend accessible"
    else
        print_error "Frontend not responding yet (still starting)"
    fi

    echo ""
    read -p "Press Enter to continue..."
}

#############################################################################
# STEP 8: ACCESS INFORMATION
#############################################################################

step_access_info() {
    print_step "Setup Complete! 🎉"

    echo -e "${GREEN}Your Ochuko AI v5.0 is ready!${NC}"
    echo ""
    echo "Access your system:"
    echo ""
    echo -e "  ${CYAN}Web Interface:${NC}  http://localhost:3000"
    echo -e "  ${CYAN}API Docs:${NC}       http://localhost:8000/docs"
    echo -e "  ${CYAN}Backend API:${NC}    http://localhost:8000"
    echo -e "  ${CYAN}Health Check:${NC}   http://localhost:8000/health"
    echo ""
    echo "Useful commands:"
    echo ""
    echo -e "  ${YELLOW}bash scripts/health-check.sh${NC}     - Check system status"
    echo -e "  ${YELLOW}bash scripts/logs.sh${NC}             - View logs"
    echo -e "  ${YELLOW}docker-compose logs -f${NC}          - Real-time logs"
    echo -e "  ${YELLOW}docker-compose restart${NC}          - Restart all services"
    echo -e "  ${YELLOW}docker-compose down${NC}             - Stop services"
    echo ""
    echo "Documentation:"
    echo ""
    echo "  • DEPLOYMENT_READY.md - Full guide"
    echo "  • README.md - System overview"
    echo "  • V5_INTEGRATION_ARCHITECTURE.md - Technical details"
    echo ""

    if prompt_yes_no "Open web interface now?"; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open "http://localhost:3000"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "http://localhost:3000"
        else
            print_info "Open http://localhost:3000 in your browser"
        fi
    fi

    echo ""
    print_success "Setup wizard complete!"
}

#############################################################################
# MAIN
#############################################################################

main() {
    step_welcome
    
    if ! step_system_check; then
        return 1
    fi

    step_deployment_type
    step_api_keys
    step_environment_setup
    step_startup
    step_verification
    step_access_info

    print_header
    echo -e "${GREEN}Thank you for using Ochuko AI v5.0!${NC}"
    echo ""
    echo "Need help? See DEPLOYMENT_READY.md"
    echo ""
}

# Run if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
