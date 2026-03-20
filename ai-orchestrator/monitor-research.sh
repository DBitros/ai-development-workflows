#!/bin/bash

# Research Progress Monitor
# Shows live progress of background research agents

TASK_DIR="/private/tmp/claude-502/-Users-dbitros-Development/tasks"
BATCH_MANAGER="$(dirname "$0")/batch-manager.sh"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Get active tasks
get_active_tasks() {
    ls -t "$TASK_DIR"/*.output 2>/dev/null | head -10
}

# Parse task output for progress
get_task_progress() {
    local task_file="$1"
    local task_id=$(basename "$task_file" .output)

    # Count tool uses (rough progress indicator)
    local tool_count=$(grep -c '"type":"tool_use"' "$task_file" 2>/dev/null || echo "0")

    # Count tokens from usage blocks
    local tokens=$(grep -o '"total_tokens":[0-9]*' "$task_file" 2>/dev/null | tail -1 | grep -o '[0-9]*' || echo "0")

    # Get last activity timestamp
    local last_activity=$(grep '"timestamp"' "$task_file" 2>/dev/null | tail -1 | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)

    # Try to get task description
    local description=$(grep -o '"description":"[^"]*"' "$task_file" 2>/dev/null | head -1 | cut -d'"' -f4)

    # Check if complete
    local status="🔄 Running"
    if grep -q '"status":"completed"' "$task_file" 2>/dev/null; then
        status="✅ Complete"
    elif grep -q '"status":"failed"' "$task_file" 2>/dev/null; then
        status="❌ Failed"
    fi

    echo "$status|$task_id|$description|$tool_count|$tokens|$last_activity"
}

# Estimate completion percentage
estimate_progress() {
    local tool_count="$1"
    local tokens="$2"

    # Rough estimates based on VLP-514 completion (45 tools, 101k tokens)
    local tool_pct=$((tool_count * 100 / 50))  # Assume ~50 tools for completion
    local token_pct=$((tokens / 1000))          # Tokens in thousands

    # Average the estimates
    local avg_pct=$(( (tool_pct + (token_pct * 100 / 100)) / 2 ))

    # Cap at 99% until actually complete
    if [ $avg_pct -gt 99 ]; then
        avg_pct=99
    fi

    echo $avg_pct
}

# Draw progress bar
draw_progress_bar() {
    local pct="$1"
    local width=50
    local filled=$((pct * width / 100))
    local empty=$((width - filled))

    printf "["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "] %3d%%" "$pct"
}

# Main monitor loop
monitor_loop() {
    local interval="${1:-5}"  # Update every 5 seconds by default

    while true; do
        clear
        echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║${NC}                    ${YELLOW}Enhanced Research Progress Monitor${NC}                     ${BLUE}║${NC}"
        echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""

        # Show batch status
        echo -e "${GREEN}📊 Batch Status:${NC}"
        "$BATCH_MANAGER" status 2>/dev/null | tail -n +3
        echo ""

        # Show active tasks
        echo -e "${YELLOW}🔬 Active Research Tasks:${NC}"
        echo ""

        local active_count=0
        for task_file in $(get_active_tasks); do
            if [ -f "$task_file" ]; then
                IFS='|' read -r status task_id description tool_count tokens last_activity <<< "$(get_task_progress "$task_file")"

                if [[ "$status" == *"Running"* ]]; then
                    active_count=$((active_count + 1))

                    # Estimate progress
                    local pct=$(estimate_progress "$tool_count" "$tokens")

                    echo -e "${BLUE}Task ID:${NC} $task_id"
                    if [ -n "$description" ]; then
                        echo -e "${GRAY}Description:${NC} $description"
                    fi
                    echo -e "${GREEN}Status:${NC} $status"
                    echo -e "${GREEN}Progress:${NC} $(draw_progress_bar $pct)"
                    echo -e "${GREEN}Tools Used:${NC} $tool_count | ${GREEN}Tokens:${NC} $(printf "%'d" $tokens)"

                    # Show time since last activity
                    if [ -n "$last_activity" ]; then
                        echo -e "${GRAY}Last Activity:${NC} $last_activity"
                    fi

                    echo ""
                fi
            fi
        done

        if [ $active_count -eq 0 ]; then
            echo -e "${GRAY}No active tasks running${NC}"
        fi

        echo ""
        echo -e "${GRAY}Refreshing every ${interval}s... Press Ctrl+C to exit${NC}"

        sleep "$interval"
    done
}

# One-shot status check
show_status() {
    echo -e "${BLUE}🔬 Enhanced Research Status:${NC}"
    echo ""

    for task_file in $(get_active_tasks); do
        if [ -f "$task_file" ]; then
            IFS='|' read -r status task_id description tool_count tokens last_activity <<< "$(get_task_progress "$task_file")"

            if [[ "$status" == *"Running"* ]] || [[ "$status" == *"Complete"* ]]; then
                local pct=$(estimate_progress "$tool_count" "$tokens")

                echo -e "${GREEN}$status${NC} $task_id"
                echo "  $(draw_progress_bar $pct)"
                echo -e "  Tools: $tool_count | Tokens: $(printf "%'d" $tokens)"
                echo ""
            fi
        fi
    done
}

# Command dispatcher
case "${1:-watch}" in
    watch)
        monitor_loop "${2:-5}"
        ;;

    status|check)
        show_status
        ;;

    help|--help|-h)
        cat <<HELP
Research Progress Monitor

Usage: monitor-research.sh [command] [interval]

Commands:
  watch [interval]    Live monitoring with auto-refresh (default: 5s)
  status              One-time status check
  help                Show this help

Examples:
  monitor-research.sh                    # Start live monitor (5s refresh)
  monitor-research.sh watch 3            # Live monitor (3s refresh)
  monitor-research.sh status             # One-time check
HELP
        ;;

    *)
        echo "Unknown command: $1"
        echo "Run 'monitor-research.sh help' for usage"
        exit 1
        ;;
esac
