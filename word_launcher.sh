#!/bin/bash

BANK_DIR="$HOME/word_at_bank"
STATE_FILE="$HOME/.word_at_state"
source "$STATE_FILE" 2>/dev/null
[ -z "$ACTIVE_TARGET" ] && ACTIVE_TARGET="NONE"

ORANGE='\033[38;5;208m'
WHITE='\033[1;37m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${ORANGE}========================================${NC}"
echo -e "${WHITE} word@ GAME CONSOLE${NC}"
echo -e "${ORANGE}========================================${NC}"

shopt -s nullglob
bank_games=("$BANK_DIR"/games/*.py)
floppy_games=("$ACTIVE_TARGET"/*.py)
shopt -u nullglob

all_games=("${bank_games[@]}" "${floppy_games[@]}")
if [ ${#all_games[@]} -eq 0 ]; then echo -e "${RED}No game cartridges found in Bank or Media.${NC}"; exit 1; fi

i=1
for g in "${all_games[@]}"; do
    basename=$(basename "$g")
    location="Bank"
    [[ "$g" == "$ACTIVE_TARGET"* ]] && location="Hardware Media"
    echo -e "  ${WHITE}$i)${NC} $basename ${ORANGE}[$location]${NC}"
    ((i++))
done

read -p " Select game cartridge: " choice
if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#all_games[@]}" ]; then
    SELECTED_GAME="${all_games[$((choice-1))]}"
    clear
    GAME_DIR=$(dirname "$SELECTED_GAME")
    GAME_FILE=$(basename "$SELECTED_GAME")
    
    (cd "$GAME_DIR" && nice -n -10 python3 "$GAME_FILE")
    
    stty sane
    tput cnorm
    clear
    echo -e "${WHITE}Game session ended. OS control restored.${NC}"
else
    echo -e "${RED}Invalid selection.${NC}"
fi
