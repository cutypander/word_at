import os
import re
import json
import random

# ==========================================
# word@ NEURAL CORE (Hybrid Markov-RNN v3)
# ==========================================
BANK_DIR = os.path.expanduser("~/word_at_bank/text")
BRAIN_FILE = os.path.expanduser("~/word_at_bank/brain.json")

ORANGE = '\033[38;5;208m'
WHITE = '\033[1;37m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
NC = '\033[0m'

brain = {"weights": {}, "vocab": {}}
context_state = {}  
last_path = [] 
BASE_REWARD = 10

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
    # Separate punctuation so the engine can map it, but keep structure intact
    text = re.sub(r'([.?!,()\[\]"”’])', r' \1 ', text)
    return text.split()

def ingest_knowledge():
    print(f"\n{CYAN}[System] Ingesting neural data from Bank...{NC}")
    if not os.path.exists(BANK_DIR):
        print(f"{RED}[Error] Text bank not found.{NC}")
        return

    files = [f for f in os.listdir(BANK_DIR) if f.endswith('.txt')]
    word_count = 0
    for file in files:
        with open(os.path.join(BANK_DIR, file), 'r', errors='ignore') as f:
            words = clean_text(f.read())
            word_count += len(words)
            for i in range(len(words) - 2):
                w1, w2, target = words[i], words[i+1], words[i+2]
                brain["vocab"][w1] = brain["vocab"].get(w1, 0) + 1
                key = f"{w1}::{w2}"
                if key not in brain["weights"]:
                    brain["weights"][key] = {}
                brain["weights"][key][target] = brain["weights"][key].get(target, 0) + 1

    save_brain()
    print(f"{GREEN}[System] Synapses forged. Processed {word_count} words.{NC}\n")

def apply_reward(multiplier=1):
    global brain
    if not last_path:
        return False
    for (key, target) in last_path:
        if key in brain["weights"] and target in brain["weights"][key]:
            current = brain["weights"][key][target]
            new_weight = current + (BASE_REWARD * multiplier)
            if new_weight <= 0:
                del brain["weights"][key][target]
            else:
                brain["weights"][key][target] = min(new_weight, 255)
    save_brain()
    return True

def generate_thought(prompt, is_loop=False):
    global last_path, context_state
    last_path = []
    words = clean_text(prompt)
    if len(words) < 2 and not is_loop:
        return "I need more context."

    # Update RNN hidden state (The Neural Context)
    for k in list(context_state.keys()):
        context_state[k] *= 0.5
        if context_state[k] < 0.1:
            del context_state[k]
    for w in words:
        if w not in ['.', ',', '?', '!', 'the', 'a', 'and', 'to', 'of', 'in', '"', '(', ')']:
            context_state[w] = context_state.get(w, 0) + 1.0

    if len(words) >= 2:
        w1, w2 = words[-2], words[-1]
    else:
        w1, w2 = random.choice(list(brain["weights"].keys())).split("::")

    response = []
    for _ in range(40): # Slightly longer max length
        key = f"{w1}::{w2}"
        
        if key not in brain["weights"] or not brain["weights"][key]:
            fallbacks = [k for k in brain["weights"] if k.startswith(f"{w2}::")]
            if fallbacks:
                key = random.choice(fallbacks)
            else:
                if context_state:
                    top_context = max(context_state, key=context_state.get)
                    context_keys = [k for k in brain["weights"] if top_context in k]
                    key = random.choice(context_keys) if context_keys else random.choice(list(brain["weights"].keys()))
                else:
                    key = random.choice(list(brain["weights"].keys()))
            w1, w2 = key.split("::")

        candidates = brain["weights"][key]
        choices = list(candidates.keys())
        base_weights = list(candidates.values())
        
        # Apply contextual dopamine to weight selection
        adj_weights = []
        for i, choice in enumerate(choices):
            weight = base_weights[i]
            if choice in context_state:
                weight += int(context_state[choice] * 10) # Heavily favor context
            adj_weights.append(weight)
            
        next_word = random.choices(choices, weights=adj_weights, k=1)[0]
        last_path.append((key, next_word))
        
        if next_word in ['.', '?', '!'] and len(response) < 5:
            w1, w2 = w2, next_word
            continue

        response.append(next_word)
        if next_word in ['.', '?', '!'] and len(response) >= 5:
            break
            
        w1, w2 = w2, next_word

    out = " ".join(response)
    # Clean up spacing around punctuation
    out = re.sub(r'\s+([.?!,\])])', r'\1', out)
    out = re.sub(r'([\[(])\s+', r'\1', out)
    return out.capitalize()

def judge_thought(thought):
    """The Neural Critic: Evaluates grammar, structure, and context."""
    words = thought.split()
    score = 5 # Base score
    
    # 1. Structural Length & Repetition
    if len(words) < 6: 
        score -= 3
    if len(set(words)) < len(words) * 0.6: 
        score -= 4 # Severe penalty for repeating words
        
    # 2. Syntax & Punctuation Integrity
    for punct in ['"', '”', '’', '(', ')', '[', ']']:
        if thought.count(punct) % 2 != 0:
            score -= 5 # Massive penalty for orphaned brackets/quotes
            
    # 3. Contextual Coherence (Does it stay on topic?)
    if context_state:
        context_matches = sum(1 for w in words if w in context_state)
        if context_matches == 0:
            score -= 3 # Penalty for completely ignoring the hidden state
            
    return score

def run_critic_loop(cycles):
    print(f"\n{CYAN}[System] Initiating Adversarial Critic Loop for {cycles} cycles...{NC}")
    approved, rejected = 0, 0
    prompt = random.choice(list(brain["vocab"].keys()))

    for i in range(cycles):
        thought = generate_thought(prompt, is_loop=True)
        
        # Pass to the new ruthless Critic
        score = judge_thought(thought)
        
        if score > 0:
            approved += 1
            apply_reward(1)
            prompt = thought.split()[-1] # Feed end of thought into next prompt
            print(f" Cycle {i+1}: {GREEN}[APPROVED]{NC} {thought}")
        else:
            rejected += 1
            apply_reward(-1)
            print(f" Cycle {i+1}: {RED}[REJECTED]{NC} {thought}")
            
    print(f"\n{WHITE}Loop Complete. Approved: {approved} | Rejected: {rejected}{NC}\n")

# ==========================================
# TERMINAL UI
# ==========================================
load_brain()
print(f"{ORANGE}========================================{NC}")
print(f"{WHITE} word@ NEURAL CORE (Hybrid Model v3){NC}")
print(f"{ORANGE}========================================{NC}")
print(f" Commands:")
print(f"  {WHITE}\\learn{NC}     : Train network on text files.")
print(f"  {WHITE}\\good{NC}      : Manually reward the AI's last sentence (+10).")
print(f"  {WHITE}\\bad{NC}       : Manually punish the AI's last sentence (-10).")
print(f"  {WHITE}\\loop [n]{NC}  : Run the unsupervised Discriminator.")
print(f"  {WHITE}\\q{NC}         : Exit to OS.")
print(f"{ORANGE}========================================{NC}")

while True:
    try:
        user_input = input(f"{CYAN}You > {NC}").strip()
        if user_input.lower() == '\\q':
            break
        elif user_input.lower() == '\\learn':
            ingest_knowledge()
            continue
        elif user_input.lower() == '\\good':
            if apply_reward(1): print(f"{GREEN}[System] Pathway reinforced.{NC}\n")
            continue
        elif user_input.lower() == '\\bad':
            if apply_reward(-1): print(f"{RED}[System] Pathway degraded.{NC}\n")
            continue
        elif user_input.lower().startswith('\\loop'):
            try:
                cycles = int(user_input.split()[1])
                run_critic_loop(cycles)
            except:
                print(f"{RED}[Error] Syntax: \\loop [number]{NC}\n")
            continue
            
        if not user_input:
            continue
            
        ai_response = generate_thought(user_input)
        print(f"{GREEN}AI  > {NC}{ai_response}\n")
        
    except KeyboardInterrupt:
        break
