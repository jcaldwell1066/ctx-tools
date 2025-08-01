#!/bin/bash
# Quick Review Finder - Fast access to in-review items
# Usage: quick-review-finder.sh [action]

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

case "${1:-list}" in
    "list"|"")
        echo -e "${BLUE}🔍 Finding all in-review items...${NC}"
        echo ""
        ctx list | grep "👀 in-review" | while read line; do
            name=$(echo "$line" | awk '{print $1}')
            echo -e "${GREEN}📋${NC} $name"
            ctx switch "$name" > /dev/null 2>&1
            echo "   $(ctx notes | tail -1 | cut -c1-80)..."
            echo ""
        done
        ;;
    "quick")
        echo -e "${YELLOW}⚡ Quick status of in-review items:${NC}"
        ctx list | grep "👀 in-review" | awk '{print "  🔍 " $1 " (" $4 " notes)"}'
        ;;
    "switch")
        if [[ -z "$2" ]]; then
            echo "Usage: quick-review-finder.sh switch <context-name>"
            exit 1
        fi
        ctx switch "$2"
        echo -e "${GREEN}✅ Switched to review context: $2${NC}"
        ;;
    *)
        echo "Usage: quick-review-finder.sh [list|quick|switch <name>]"
        ;;
esac