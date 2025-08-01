#!/bin/bash
# Daily CTX Manager - Practical day-to-day context tracking system
# Combines all the best patterns from docs/examples into a usable tool

set -e

# Configuration
CTX_DAILY_CONFIG="$HOME/.ctx-daily-config"
CTX_TEMPLATES_DIR="$(dirname "$0")/templates"
CTX_WORKFLOWS_DIR="$(dirname "$0")/workflows"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[CTX-DAILY]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

error() {
    echo -e "${RED}❌${NC} $1"
}

# Load configuration
load_config() {
    if [[ -f "$CTX_DAILY_CONFIG" ]]; then
        source "$CTX_DAILY_CONFIG"
    else
        # Default configuration
        DEFAULT_TEAM_NAME="my-team"
        DEFAULT_PROJECT_PREFIX="PROJ"
        DEFAULT_WORK_HOURS="09:00-17:00"
        DEFAULT_REVIEW_TIME="17:00"
        
        cat > "$CTX_DAILY_CONFIG" << EOF
# CTX Daily Configuration
TEAM_NAME="$DEFAULT_TEAM_NAME"
PROJECT_PREFIX="$DEFAULT_PROJECT_PREFIX"
WORK_HOURS="$DEFAULT_WORK_HOURS"
REVIEW_TIME="$DEFAULT_REVIEW_TIME"
GITHUB_ORG=""
JIRA_BASE_URL=""
EOF
        warn "Created default config at $CTX_DAILY_CONFIG - please customize"
        source "$CTX_DAILY_CONFIG"
    fi
}

# Daily startup routine
daily_start() {
    local date=$(date +"%Y-%m-%d")
    local daily_context="daily-$date"
    
    log "Starting your daily context tracking..."
    
    # Create or switch to daily context
    if ctx list | grep -q "$daily_context"; then
        ctx switch "$daily_context"
        log "Resumed daily context: $daily_context"
    else
        ctx create "$daily_context" --description "Daily work tracking for $date"
        ctx switch "$daily_context"
        ctx set-state active
        ctx note "DAILY_START: $(date '+%H:%M') | WORK_HOURS: $WORK_HOURS"
        success "Created daily context: $daily_context"
    fi
    
    # Show current team status
    echo ""
    log "Team Status:"
    ctx list --format=table | head -8
    
    # Check for blocked contexts
    local blocked=$(ctx list | grep "🚫" | wc -l)
    if [[ $blocked -gt 0 ]]; then
        warn "$blocked contexts are blocked - need attention"
        ctx list | grep "🚫"
    fi
    
    echo ""
    log "Today's Focus (add with: ctx-daily focus \"Your main priority\")"
    ctx notes | grep "FOCUS:" | tail -1 || echo "  No focus set yet"
}

# Set daily focus
set_focus() {
    if [[ -z "$1" ]]; then
        echo "Usage: ctx-daily focus \"Your main priority for today\""
        return 1
    fi
    
    ctx note "FOCUS: $1 | SET: $(date '+%H:%M')"
    success "Daily focus set: $1"
}

# Quick work session start
start_work() {
    local task_id="$1"
    local description="$2"
    
    if [[ -z "$task_id" ]]; then
        echo "Usage: ctx-daily work TASK-123 \"Optional description\""
        echo "   or: ctx-daily work hotfix \"Quick fix description\""
        return 1
    fi
    
    local context_name
    if [[ "$task_id" =~ ^[A-Z]+-[0-9]+$ ]]; then
        # JIRA ticket format
        context_name="$task_id"
    else
        # Generate context name
        context_name="${task_id}-$(date +%m%d)"
    fi
    
    # Create work context
    ctx create "$context_name" --description "${description:-Working on $task_id}"
    ctx switch "$context_name"
    ctx set-state in-progress
    
    # Standard work setup
    ctx note "TASK: $task_id | TYPE: ${description:-Development work}"
    ctx note "STARTED: $(date '+%Y-%m-%d %H:%M')"
    
    if [[ -n "$JIRA_BASE_URL" && "$task_id" =~ ^[A-Z]+-[0-9]+$ ]]; then
        ctx note "JIRA: $JIRA_BASE_URL/browse/$task_id"
    fi
    
    success "Started work context: $context_name"
    log "Use 'ctx-daily progress \"what you accomplished\"' to track progress"
}

# Track progress
track_progress() {
    if [[ -z "$1" ]]; then
        echo "Usage: ctx-daily progress \"What you accomplished\""
        return 1
    fi
    
    ctx note "PROGRESS: $1 | TIME: $(date '+%H:%M')"
    success "Progress tracked"
}

# Handle blockers
handle_blocker() {
    if [[ -z "$1" ]]; then
        echo "Usage: ctx-daily blocked \"What's blocking you\""
        return 1
    fi
    
    ctx set-state blocked
    ctx note "BLOCKED: $1 | TIME: $(date '+%H:%M')"
    ctx note "NEED: Please specify what's needed to unblock"
    
    error "Context marked as blocked: $1"
    log "Use 'ctx-daily unblock \"resolution\"' when resolved"
}

# Unblock work
unblock_work() {
    if [[ -z "$1" ]]; then
        echo "Usage: ctx-daily unblock \"How it was resolved\""
        return 1
    fi
    
    ctx note "UNBLOCKED: $1 | TIME: $(date '+%H:%M')"
    ctx set-state in-progress
    success "Context unblocked: $1"
}

# Handoff to team
handoff() {
    local phase="${1:-review}"
    local message="$2"
    
    case "$phase" in
        "review"|"qa"|"deploy"|"team")
            ctx set-state in-review
            ;;
        *)
            error "Unknown handoff phase: $phase"
            echo "Available phases: review, qa, deploy, team"
            return 1
            ;;
    esac
    
    ctx note "HANDOFF: Ready for $phase | TIME: $(date '+%H:%M')"
    if [[ -n "$message" ]]; then
        ctx note "HANDOFF_MSG: $message"
    fi
    
    success "Ready for handoff to $phase"
}

# Daily wrap-up
daily_end() {
    local date=$(date +"%Y-%m-%d")
    local daily_context="daily-$date"
    
    log "Daily wrap-up for $date..."
    
    # Switch to daily context
    if ctx list | grep -q "$daily_context"; then
        ctx switch "$daily_context"
    else
        warn "No daily context found for $date"
        return 1
    fi
    
    # Summary
    echo ""
    log "Today's Summary:"
    echo "├─ Contexts worked on:"
    ctx list | grep -E "(💻|👀|✅)" | sed 's/^/│  /'
    
    echo "├─ Progress notes:"
    ctx notes | grep "PROGRESS:" | tail -3 | sed 's/^/│  /'
    
    echo "└─ Status:"
    local completed=$(ctx list | grep "✅" | wc -l)
    local in_progress=$(ctx list | grep "💻" | wc -l)
    local blocked=$(ctx list | grep "🚫" | wc -l)
    echo "   Completed: $completed | In Progress: $in_progress | Blocked: $blocked"
    
    # Set daily context to completed
    ctx note "DAILY_END: $(date '+%H:%M') | SUMMARY: $completed completed, $in_progress in progress"
    ctx set-state completed
    
    success "Daily tracking completed"
}

# Show help
show_help() {
    cat << EOF
CTX Daily - Practical day-to-day context tracking

USAGE:
    ctx-daily <command> [arguments]

COMMANDS:
    start                           Start daily tracking
    focus "priority"                Set today's main focus
    work TASK-123 "description"     Start working on a task
    progress "what you did"         Track progress on current work
    blocked "what's blocking"       Mark current work as blocked
    unblock "how resolved"          Unblock current work
    handoff [review|qa|deploy]      Mark ready for team handoff
    end                             End daily tracking and summarize
    status                          Show current status
    team                            Show team status
    config                          Edit configuration

EXAMPLES:
    ctx-daily start
    ctx-daily focus "Complete payment API integration"
    ctx-daily work PAYMENT-5320 "Refund service implementation"
    ctx-daily progress "Completed database schema and service layer"
    ctx-daily blocked "Need API keys from DevOps team"
    ctx-daily handoff review "PR #1234 ready for code review"
    ctx-daily end

CONFIGURATION:
    Edit ~/.ctx-daily-config to customize team settings
EOF
}

# Main command dispatch
main() {
    load_config
    
    case "${1:-help}" in
        "start")
            daily_start
            ;;
        "focus")
            set_focus "$2"
            ;;
        "work")
            start_work "$2" "$3"
            ;;
        "progress")
            track_progress "$2"
            ;;
        "blocked")
            handle_blocker "$2"
            ;;
        "unblock")
            unblock_work "$2"
            ;;
        "handoff")
            handoff "$2" "$3"
            ;;
        "end")
            daily_end
            ;;
        "status")
            ctx status
            ;;
        "team")
            ctx list --format=table
            ;;
        "config")
            ${EDITOR:-nano} "$CTX_DAILY_CONFIG"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"