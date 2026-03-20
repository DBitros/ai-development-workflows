#!/bin/bash

# Batch Status Manager for AI Orchestrator
# Manages batch-status.json for resumable ticket operations

BATCH_FILE="${BATCH_FILE:-$(dirname "$0")/batch-status.json}"

# Helper: Update metadata counts
update_metadata() {
    local total=$(jq '.items | length' "$BATCH_FILE")
    local completed=$(jq '[.items[] | select(.status == "done")] | length' "$BATCH_FILE")
    local failed=$(jq '[.items[] | select(.status == "failed")] | length' "$BATCH_FILE")
    local pending=$(jq '[.items[] | select(.status == "pending")] | length' "$BATCH_FILE")
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    jq ".metadata.total_items = $total |
        .metadata.completed = $completed |
        .metadata.failed = $failed |
        .metadata.pending = $pending |
        .metadata.last_updated = \"$now\"" "$BATCH_FILE" > "${BATCH_FILE}.tmp" && mv "${BATCH_FILE}.tmp" "$BATCH_FILE"
}

# Add new item(s)
add_item() {
    local id="$1"
    local output_file="${2:-}"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Check if item already exists
    if jq -e ".items[] | select(.id == \"$id\")" "$BATCH_FILE" > /dev/null 2>&1; then
        echo "⚠️  Item $id already exists. Use 'update' to modify it."
        return 1
    fi

    local new_item=$(cat <<EOF
{
    "id": "$id",
    "status": "pending",
    "output_file": "$output_file",
    "updated_at": "$now",
    "created_at": "$now"
}
EOF
)

    jq ".items += [$new_item]" "$BATCH_FILE" > "${BATCH_FILE}.tmp" && mv "${BATCH_FILE}.tmp" "$BATCH_FILE"
    update_metadata
    echo "✅ Added $id (status: pending)"
}

# Update item status
update_status() {
    local id="$1"
    local status="$2"
    local output_file="${3:-}"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if ! jq -e ".items[] | select(.id == \"$id\")" "$BATCH_FILE" > /dev/null 2>&1; then
        echo "❌ Item $id not found"
        return 1
    fi

    if [ -n "$output_file" ]; then
        jq "(.items[] | select(.id == \"$id\") | .status) = \"$status\" |
            (.items[] | select(.id == \"$id\") | .output_file) = \"$output_file\" |
            (.items[] | select(.id == \"$id\") | .updated_at) = \"$now\"" "$BATCH_FILE" > "${BATCH_FILE}.tmp" && mv "${BATCH_FILE}.tmp" "$BATCH_FILE"
    else
        jq "(.items[] | select(.id == \"$id\") | .status) = \"$status\" |
            (.items[] | select(.id == \"$id\") | .updated_at) = \"$now\"" "$BATCH_FILE" > "${BATCH_FILE}.tmp" && mv "${BATCH_FILE}.tmp" "$BATCH_FILE"
    fi

    update_metadata
    echo "✅ Updated $id → status: $status"
}

# Show status report
show_status() {
    echo "📊 Batch Status Report"
    echo "====================="
    jq -r '.metadata | "Total: \(.total_items) | ✅ Done: \(.completed) | ⏳ Pending: \(.pending) | ❌ Failed: \(.failed)"' "$BATCH_FILE"
    echo "Last updated: $(jq -r '.metadata.last_updated' "$BATCH_FILE")"
    echo ""
    echo "Items:"
    jq -r '.items[] | "  [\(.status)] \(.id) → \(.output_file // "no output")"' "$BATCH_FILE"
}

# Get pending items
get_pending() {
    jq -r '.items[] | select(.status == "pending") | .id' "$BATCH_FILE"
}

# Get failed items
get_failed() {
    jq -r '.items[] | select(.status == "failed") | .id' "$BATCH_FILE"
}

# Bulk add from file or args
bulk_add() {
    if [ -f "$1" ]; then
        # Read from file (one ID per line)
        while IFS= read -r id; do
            [ -n "$id" ] && add_item "$id"
        done < "$1"
    else
        # Read from arguments
        for id in "$@"; do
            add_item "$id"
        done
    fi
}

# Main command dispatcher
case "${1:-status}" in
    add)
        shift
        if [ $# -eq 0 ]; then
            echo "Usage: batch-manager.sh add <id> [output_file]"
            exit 1
        fi
        add_item "$@"
        ;;

    bulk-add)
        shift
        bulk_add "$@"
        ;;

    update)
        shift
        if [ $# -lt 2 ]; then
            echo "Usage: batch-manager.sh update <id> <status> [output_file]"
            echo "Status: pending|done|failed"
            exit 1
        fi
        update_status "$@"
        ;;

    status|show)
        show_status
        ;;

    pending)
        get_pending
        ;;

    failed)
        get_failed
        ;;

    resume)
        echo "🔄 Resumable items (pending):"
        get_pending
        ;;

    reset)
        cat > "$BATCH_FILE" <<'EOF'
{
  "items": [],
  "metadata": {
    "created_at": "2026-02-09T00:00:00Z",
    "last_updated": "2026-02-09T00:00:00Z",
    "total_items": 0,
    "completed": 0,
    "failed": 0,
    "pending": 0
  }
}
EOF
        echo "🔥 Reset batch-status.json"
        ;;

    help|--help|-h)
        cat <<'HELP'
Batch Status Manager - AI Orchestrator

Usage: batch-manager.sh <command> [args]

Commands:
  add <id> [output_file]       Add new item with pending status
  bulk-add <id1> <id2> ...     Add multiple items at once
  bulk-add <file>              Add items from file (one per line)
  update <id> <status> [file]  Update item status (pending|done|failed)
  status|show                  Show current batch status
  pending                      List pending items
  failed                       List failed items
  resume                       Show items ready to resume (pending)
  reset                        Clear all items and reset file
  help                         Show this help

Examples:
  # Add tickets for research
  batch-manager.sh bulk-add LH-101 LH-102 LH-103

  # Mark ticket as done
  batch-manager.sh update LH-101 done /path/to/research.md

  # Check progress
  batch-manager.sh status

  # Resume from pending
  batch-manager.sh resume

Environment:
  BATCH_FILE - Path to batch-status.json (default: ./batch-status.json)
HELP
        ;;

    *)
        echo "Unknown command: $1"
        echo "Run 'batch-manager.sh help' for usage"
        exit 1
        ;;
esac
