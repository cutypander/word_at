import os
import re
import json
import random
import math

# ==========================================
# word@ NEURAL CORE (Featherweight RNN-Hybrid)
# ==========================================
BANK_DIR = os.path.expanduser("~/word_at_bank/text")
BRAIN_FILE = os.path.expanduser("~/word_at_bank/brain.json")

ORANGE = '\033[38;5;208m'
WHITE = '\033[1;37m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
NC = '\033[0m'

# Core Neural State
brain = {"weights": {}, "vocab": {}}
context_state = {}  # RNN-style hidden state

def load_brain():
    global brain
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, 'r') as f:
                brain = json.load(f)
        except:
            print(f"{RED}[System] Brain file corrupted. Starting fresh.{NC}")

def save_brain():
    with open(BRAIN_FILE, 'w') as f:
        json.dump(brain, f)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'([.?!,])', r' \1 ', text)
    return text.split()

def ingest_knowledge():
    print(f"\n{CYAN}[System] Ingesting neural data from Bank...{NC}")
    if not os.path.exists(BANK_DIR):
        print(f"{RED}[Error] Text bank not found.{NC}")
        return

    files = [f for f in os.listdir(BANK_DIR) if f.endswith('.txt')]
    if not files:
        print(f"{RED}[Error] No text files to learn from.{NC}")
        return

    word_count = 0
    for file in files:
        with open(os.path.join(BANK_DIR, file), 'r', errors='ignore') as f:
            words = clean_text(f.read())
            word_count += len(words)
            
            # Build Tri-gram paths
            for i in range(len(words) - 2):
                w1, w2, target = words[i], words[i+1], words[i+2]
                
                # Update Vocab
                brain["vocab"][w1] = brain["vocab"].get(w1, 0) + 1
                
                # Update Weights
                key = f"{w1}::{w2}"
                if key not in brain["weights"]:
                    brain["weights"][key] = {}
                
                brain["weights"][key][target] = brain["weights"][key].get(target, 0) + 1

    save_brain()
    print(f"{GREEN}[System] Synapses forged. Processed {word_count} words.{NC}\n")

def update_hidden_state(words):
    """RNN feature: updates the hidden context state based on user input."""
    global context_state
    # Decay old context
    for k in list(context_state.keys()):
        context_state[k] *= 0.5
        if context_state[k] < 0.1:
            del context_state[k]
            
    # Add new context
    for w in words:
        if w not in ['.', ',', '?', '!', 'the', 'a', 'and', 'to', 'of', 'in']:
            context_state[w] = context_state.get(w, 0) + 1.0

def generate_thought(prompt):
    words = clean_text(prompt)
    if len(words) < 2:
        return "I need more context."

    update_hidden_state(words)
    
    # Start generation with the last two words of the prompt
    w1, w2 = words[-2], words[-1]
    response = []
    
    for _ in range(30): # Max 30 words per thought
        key = f"{w1}::{w2}"
        if key not in brain["weights"]:
            break
            
        candidates = brain["weights"][key]
        choices = list(candidates.keys())
        base_weights = list(candidates.values())
        
        # Apply RNN Context Vector (Sigmoid-style boost for relevant topics)
        adjusted_weights = []
        for i, choice in enumerate(choices):
            weight = base_weights[i]
            if choice in context_state:
                # Boost weight if it aligns with active hidden state
                weight += (context_state[choice] * 5)
            adjusted_weights.append(weight)
            
        # Weighted random selection
        next_word = random.choices(choices, weights=adjusted_weights, k=1)[0]
        
        if next_word in ['.', '?', '!']:
            response.append(next_word)
            break
            
        response.append(next_word)
        w1, w2 = w2, next_word

    # Clean up output formatting
    out = " ".join(response)
    out = re.sub(r'\s+([.?!,])', r'\1', out)
    return out.capitalize()

# ==========================================
# TERMINAL UI
# ==========================================
load_brain()
print(f"{ORANGE}========================================{NC}")
print(f"{WHITE} word@ NEURAL CORE (Hybrid Model){NC}")
print(f"{ORANGE}========================================{NC}")
print(f" Commands:")
print(f"  {WHITE}\\learn{NC} : Train network on word_at_bank text files.")
print(f"  {WHITE}\\q{NC}     : Exit to OS.")
print(f"{ORANGE}========================================{NC}")

while True:
    try:
        user_input = input(f"{CYAN}You > {NC}").strip()
        if user_input.lower() == '\\q':
            break
        elif user_input.lower() == '\\learn':
            ingest_knowledge()
            continue
            
        if not user_input:
            continue
            
        # Add prompt to temporary memory and generate
        ai_response = generate_thought(user_input)
        print(f"{GREEN}AI  > {NC}{ai_response}\n")
        
    except KeyboardInterrupt:
        break
