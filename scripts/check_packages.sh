#!/bin/bash

echo "🔍 PIP PACKAGE CHECKER"
echo "====================="

# Function to check if in venv
check_venv() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "✅ Virtual environment active: $(basename $VIRTUAL_ENV)"
        return 0
    else
        echo "❌ No virtual environment active (global mode)"
        return 1
    fi
}

# Function to count and list packages
show_packages() {
    local context=$1
    local count=$(pip list 2>/dev/null | wc -l)
    
    echo ""
    echo "📦 PACKAGES $context:"
    echo "   Total: $((count - 2)) packages"  # -2 to remove header
    echo "   Location: $(python -c "import site; print(site.getsitepackages()[0])" 2>/dev/null)"
    
    # Show some main packages
    echo "   Main packages:"
    pip list 2>/dev/null | head -10 | tail -8 | sed 's/^/     • /'
    
    if [[ $count -gt 12 ]]; then
        echo "     ... and $((count - 12)) more packages"
    fi
}

# Check current state
echo "🔧 Current state:"
echo "   Python: $(python --version)"
echo "   Pip: $(pip --version | cut -d' ' -f1-2)"
check_venv

# Show packages from current context
if [[ -n "$VIRTUAL_ENV" ]]; then
    show_packages "LOCAL (virtual environment)"
else
    show_packages "GLOBAL (system)"
fi

# If in venv, show comparison
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo ""
    echo "💡 To see global packages, run:"
    echo "   deactivate && pip list"
    echo ""
    echo "🔄 To switch contexts:"
    echo "   deactivate          # Exit virtual environment"
    echo "   source venv/bin/activate  # Enter virtual environment"
else
    echo ""
    echo "💡 To see local packages, run:"
    echo "   source venv/bin/activate && pip list"
    echo ""
    echo "🔄 To use virtual environment:"
    echo "   source venv/bin/activate  # Enter virtual environment"
fi

echo ""
echo "📋 Useful commands:"
echo "   pip list --outdated    # Outdated packages"
echo "   pip show PACKAGE       # Information about a package"
echo "   pip freeze             # Generate requirements.txt"
echo "   pip list --format=json # List in JSON format"