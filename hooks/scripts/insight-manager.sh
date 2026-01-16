#!/bin/bash
# Insight Chain Manager
# Usage: insight-manager.sh [save|load|clear|health] [content]

INSIGHT_DIR="${HOME}/.imlazy"
INSIGHT_FILE="${INSIGHT_DIR}/insight-chain.md"
INSIGHT_HISTORY="${INSIGHT_DIR}/insight-history"

# Ensure directory exists
mkdir -p "${INSIGHT_DIR}"
mkdir -p "${INSIGHT_HISTORY}"

case "$1" in
    save)
        # Save insight chain content
        if [ -n "$2" ]; then
            # Backup current if exists
            if [ -f "${INSIGHT_FILE}" ]; then
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                cp "${INSIGHT_FILE}" "${INSIGHT_HISTORY}/insight-chain_${TIMESTAMP}.md"
            fi
            echo "$2" > "${INSIGHT_FILE}"
            echo "saved"
        else
            echo "error: no content provided"
            exit 1
        fi
        ;;

    load)
        # Load current insight chain
        if [ -f "${INSIGHT_FILE}" ]; then
            cat "${INSIGHT_FILE}"
        else
            echo ""
        fi
        ;;

    append)
        # Append new insight to chain
        if [ -n "$2" ]; then
            echo "" >> "${INSIGHT_FILE}"
            echo "$2" >> "${INSIGHT_FILE}"
            echo "appended"
        else
            echo "error: no content provided"
            exit 1
        fi
        ;;

    clear)
        # Archive and clear
        if [ -f "${INSIGHT_FILE}" ]; then
            TIMESTAMP=$(date +%Y%m%d_%H%M%S)
            mv "${INSIGHT_FILE}" "${INSIGHT_HISTORY}/insight-chain_${TIMESTAMP}.md"
            echo "archived to insight-chain_${TIMESTAMP}.md"
        else
            echo "nothing to clear"
        fi
        ;;

    health)
        # Check insight chain health
        if [ ! -f "${INSIGHT_FILE}" ]; then
            echo "status: empty"
            echo "count: 0"
            exit 0
        fi

        COUNT=$(grep -c "^## Insight:" "${INSIGHT_FILE}" 2>/dev/null || echo 0)
        echo "status: active"
        echo "count: ${COUNT}"

        if [ "${COUNT}" -gt 10 ]; then
            echo "warning: consolidation-needed"
        elif [ "${COUNT}" -gt 7 ]; then
            echo "warning: approaching-limit"
        fi
        ;;

    *)
        echo "Usage: insight-manager.sh [save|load|append|clear|health] [content]"
        exit 1
        ;;
esac
