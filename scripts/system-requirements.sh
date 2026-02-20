#!/bin/bash

#############################################################################
# Ochuko AI v5.0 - System Requirements Checker
#
# Validates that your system meets all requirements for deployment
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
NC='\033[0m'

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

#############################################################################
# OUTPUT FUNCTIONS
#############################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  System Requirements Check${NC}"
    echo -e "${BLUE}  Ochuko AI v5.0${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

check_pass() {
    echo -e "${GREEN}✅ PASS${NC} - $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC} - $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC} - $1"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

print_category() {
    echo -e "\n${BLUE}→ $1${NC}"
}

print_detail() {
    echo "  $1"
}

#############################################################################
# CHECKS
#############################################################################

check_docker() {
    print_category "Docker"

    if command -v docker &> /dev/null; then
        version=$(docker --version 2>/dev/null)
        check_pass "Docker installed: $version"
    else
        check_fail "Docker not installed (required)"
        print_detail "Install from: https://docs.docker.com/get-docker/"
        return 1
    fi

    if docker ps &> /dev/null; then
        check_pass "Docker daemon running"
    else
        check_fail "Docker daemon not running"
        print_detail "Try: sudo systemctl start docker"
        return 1
    fi

    return 0
}

check_docker_compose() {
    print_category "Docker Compose"

    if command -v docker-compose &> /dev/null; then
        version=$(docker-compose --version 2>/dev/null)
        check_pass "Docker Compose installed: $version"
        return 0
    elif docker compose version &> /dev/null; then
        version=$(docker compose version 2>/dev/null)
        check_pass "Docker Compose installed (new format): $version"
        return 0
    else
        check_fail "Docker Compose not installed (required)"
        print_detail "Docker Desktop includes Compose"
        return 1
    fi
}

check_git() {
    print_category "Git (Optional)"

    if command -v git &> /dev/null; then
        version=$(git --version)
        check_pass "$version (optional but recommended)"
    else
        check_warn "Git not installed (optional)"
        print_detail "Can download code as ZIP instead"
    fi
}

check_disk_space() {
    print_category "Disk Space"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        available=$(df -k . | tail -1 | awk '{print $4}')
    else
        # Linux
        available=$(df . | tail -1 | awk '{print $4}')
    fi

    available_gb=$((available / 1024 / 1024))
    required_gb=10

    if [ "$available_gb" -ge "$required_gb" ]; then
        check_pass "$available_gb GB available (need $required_gb GB)"
    elif [ "$available_gb" -ge 5 ]; then
        check_warn "$available_gb GB available (recommend $required_gb GB)"
    else
        check_fail "Only $available_gb GB available (need $required_gb GB)"
    fi
}

check_memory() {
    print_category "Memory (RAM)"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        available=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
        available_gb=$((available * 4096 / 1024 / 1024 / 1024))
    else
        # Linux
        available=$(free -b | awk '/^Mem:/ {print $7}')
        available_gb=$((available / 1024 / 1024 / 1024))
    fi

    required_gb=4
    recommended_gb=8

    if [ "$available_gb" -ge "$recommended_gb" ]; then
        check_pass "$available_gb GB available (recommended $recommended_gb GB)"
    elif [ "$available_gb" -ge "$required_gb" ]; then
        check_warn "$available_gb GB available (recommended $recommended_gb GB)"
    else
        check_warn "Only $available_gb GB available (minimum $required_gb GB)"
    fi
}

check_network() {
    print_category "Network"

    if ping -c 1 8.8.8.8 &> /dev/null; then
        check_pass "Internet connection available"
    else
        check_warn "Internet connection check failed (may still work)"
    fi

    # Check if ports are available
    for port in 3000 8000 5432 27017 6379; do
        if ! nc -z localhost "$port" 2>/dev/null; then
            check_pass "Port $port available"
        else
            check_warn "Port $port may be in use"
        fi
    done
}

check_permissions() {
    print_category "Permissions"

    # Check if we can write to current directory
    test_file="/tmp/ochukoai_test_$$"
    
    if touch "$test_file" 2>/dev/null; then
        check_pass "Can create files in /tmp"
        rm -f "$test_file"
    else
        check_fail "Cannot write to /tmp directory"
    fi

    # Check if Docker can be run
    if docker info &> /dev/null; then
        check_pass "Can run Docker commands"
    else
        check_fail "Cannot run Docker (may need sudo)"
        print_detail "Either: Add user to docker group, or use sudo"
    fi
}

check_os() {
    print_category "Operating System"

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v lsb_release &> /dev/null; then
            distro=$(lsb_release -ds)
            check_pass "Linux: $distro"
        else
            check_pass "Linux detected"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        version=$(sw_vers -productVersion)
        check_pass "macOS: $version"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        check_warn "Windows detected (needs WSL2 for Docker)"
    else
        check_warn "Unknown OS: $OSTYPE"
    fi
}

check_cpu() {
    print_category "CPU"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        cores=$(sysctl -n hw.ncpu)
    else
        cores=$(nproc 2>/dev/null || echo "unknown")
    fi

    if [ "$cores" != "unknown" ]; then
        if [ "$cores" -ge 4 ]; then
            check_pass "$cores CPU cores"
        elif [ "$cores" -ge 2 ]; then
            check_warn "Only $cores CPU cores (4+ recommended)"
        else
            check_fail "Only $cores CPU cores (minimum 2 needed)"
        fi
    else
        check_pass "CPU cores check skipped"
    fi
}

check_python() {
    print_category "Python (Optional)"

    if command -v python3 &> /dev/null; then
        version=$(python3 --version 2>&1)
        check_pass "$version (optional - for local development)"
    else
        check_warn "Python3 not installed (optional)"
    fi
}

check_curl() {
    print_category "cURL (Optional)"

    if command -v curl &> /dev/null; then
        check_pass "curl installed (optional - for health checks)"
    else
        check_warn "curl not installed (optional)"
    fi
}

#############################################################################
# SUMMARY
#############################################################################

print_summary() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Summary${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"

    echo "Total checks: $TOTAL_CHECKS"
    echo -e "  ${GREEN}Passed: $PASSED_CHECKS${NC}"
    echo -e "  ${YELLOW}Warnings: $WARNING_CHECKS${NC}"
    echo -e "  ${RED}Failed: $FAILED_CHECKS${NC}"
    echo ""

    if [ "$FAILED_CHECKS" -eq 0 ]; then
        echo -e "${GREEN}✅ All required checks passed!${NC}"
        echo -e "${GREEN}You can proceed with deployment.${NC}"
        echo ""
        echo "Next steps:"
        echo "  bash deploy.sh --quick-start"
        echo "  OR"
        echo "  bash setup.sh"
        return 0
    else
        echo -e "${RED}❌ Some required checks failed!${NC}"
        echo ""
        echo "Please fix the failed items above before proceeding."
        return 1
    fi

    echo ""
}

#############################################################################
# MAIN
#############################################################################

main() {
    print_header

    check_os
    check_docker || exit 1
    check_docker_compose || exit 1
    check_git
    check_disk_space
    check_memory
    check_cpu
    check_network
    check_permissions
    check_python
    check_curl

    print_summary || exit 1
}

main
