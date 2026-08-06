#!/bin/bash

# ==========================================
# word@ WEB MODULE - 3-IN-1 GATEWAY
# ==========================================
SHORTCUTS_FILE="$HOME/word_at_bank/text/shortcuts.txt"

ORANGE='\033[38;5;208m'
WHITE='\033[1;37m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

touch "$SHORTCUTS_FILE" 2>/dev/null

press_enter() { echo -e "\n${WHITE}Press [ENTER] to continue...${NC}"; read -r; }

while true; do
    clear
    echo -e "${ORANGE}========================================${NC}"
    echo -e "${WHITE} TERMINAL WEB INTERFACE${NC}"
    echo -e "${ORANGE}========================================${NC}"
    echo -e "${GREEN} [ SEARCH & RESEARCH ]${NC}"
    echo -e "  1) DuckDuckGo (General Search)"
    echo -e "  2) Wikipedia  (Summaries & Lore)"
    echo -e "  3) Reddit     (Forums & Troubleshooting)"
    echo -e "\n${GREEN} [ SHORTCUTS & BOOKMARKS ]${NC}"
    echo -e "  4) Open Shortcuts Menu"
    echo -e "${ORANGE}========================================${NC}"
    echo -e "  q) Exit to OS"
    read -p " Select module: " web_choice

    case "$web_choice" in
        1)
            read -p " DDG Search > " search_term
            if [ -n "$search_term" ]; then ddgr "$search_term"; fi
            ;;
        2)
            read -p " Wiki Search > " search_term
            if [ -n "$search_term" ]; then
                clear
                echo -e "${WHITE}Fetching Wikipedia for: $search_term...${NC}\n"
                wikit "$search_term" | fold -w 80 -s
                press_enter
            fi
            ;;
        3)
            tuir
            ;;
        4)
            while true; do
                clear
                echo -e "${ORANGE}========================================${NC}"
                echo -e "${WHITE} SAVED SHORTCUTS${NC}"
                echo -e "${ORANGE}========================================${NC}"
                
                if [ ! -s "$SHORTCUTS_FILE" ]; then
                    echo -e "${RED} No shortcuts saved yet.${NC}"
                else
                    nl -w2 -s") " "$SHORTCUTS_FILE"
                fi
                
                echo -e "${ORANGE}========================================${NC}"
                echo -e "  a) Add new shortcut"
                echo -e "  b) Back to Web Menu"
                read -p " Select ID to launch, or action: " sc_choice

                if [[ "$sc_choice" == "b" ]]; then break; fi
                
                if [[ "$sc_choice" == "a" ]]; then
                    read -p " Enter URL (e.g., https://example.com): " new_url
                    if [ -n "$new_url" ]; then
                        echo "$new_url" >> "$SHORTCUTS_FILE"
                        echo -e "${GREEN}Shortcut saved.${NC}"
                        sleep 1
                    fi
                    continue
                fi

                # Launching a specific shortcut
                if [[ "$sc_choice" =~ ^[0-9]+$ ]]; then
                    TARGET_URL=$(sed "${sc_choice}q;d" "$SHORTCUTS_FILE")
                    if [ -z "$TARGET_URL" ]; then continue; fi
                    
                    echo -e "\n${WHITE}Pinging $TARGET_URL...${NC}"
                    HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" --max-time 5 "$TARGET_URL")
                    
                    if [ "$HTTP_STATUS" -eq 200 ] || [ "$HTTP_STATUS" -eq 301 ] || [ "$HTTP_STATUS" -eq 302 ]; then
                        echo -e "${GREEN}Connection solid. Opening...${NC}"
                        sleep 1
                        w3m "$TARGET_URL"
                    else
                        echo -e "${RED}[Error $HTTP_STATUS] Page dead, moved, or timed out.${NC}"
                        read -p " Delete this shortcut? (y/n): " del_choice
                        if [[ "$del_choice" == "y" ]]; then
                            sed -i "${sc_choice}d" "$SHORTCUTS_FILE"
                            echo -e "${WHITE}Shortcut purged.${NC}"
                            sleep 1
                        fi
                    fi
                fi
            done
            ;;
        q)
            clear
            exit 0
            ;;
        *)
            ;;
    esac
done
