import os
import re
import json
import random

# ==========================================
# word@ NEURAL CORE (Hybrid Markov-RNN)
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
last_path = [] # Tracks the exact synapses of the last generated thought
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
    text = re.sub(r'([.?!,])', r' \1 ', text)
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
                brain["weights"][key][target] = min(new_weight, 255) # Cap at 255
    save_brain()
    return True

def generate_thought(prompt, is_loop=False):
    global last_path, context_state
    last_path = []
    words = clean_text(prompt)
    if len(words) < 2 and not is_loop:
        return "I need more context."

    # Update RNN hidden state
    for k in list(context_state.keys()):
        context_state[k] *= 0.5
        if context_state[k] < 0.1:
            del context_state[k]
    for w in words:
        if w not in ['.', ',', '?', '!', 'the', 'a', 'and', 'to', 'of', 'in']:
            context_state[w] = context_state.get(w, 0) + 1.0

    # Determine starting synapse
    if len(words) >= 2:
        w1, w2 = words[-2], words[-1]
    else:
        w1, w2 = random.choice(list(brain["weights"].keys())).split("::")

    response = []
    for _ in range(30):
        key = f"{w1}::{w2}"
        
        # Dead-end Fallback Logic
        if key not in brain["weights"] or not brain["weights"][key]:
            fallbacks = [k for k in brain["weights"] if k.startswith(f"{w2}::")]
            if fallbacks:
                key = random.choice(fallbacks)
            else:
                # Total fallback based on context state
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
        
        # Apply context dopamine
        adj_weights = []
        for i, choice in enumerate(choices):
            weight = base_weights[i]
            if choice in context_state:
                weight += int(context_state[choice] * 5)
            adj_weights.append(weight)
            
        next_word = random.choices(choices, weights=adj_weights, k=1)[0]
        last_path.append((key, next_word))
        
        # Don't let it just output a single period and give up
        if next_word in ['.', '?', '!'] and len(response) < 3:
            w1, w2 = w2, next_word
            continue

        response.append(next_word)
        if next_word in ['.', '?', '!'] and len(response) >= 3:
            break
            
        w1, w2 = w2, next_word

    out = " ".join(response)
    out = re.sub(r'\s+([.?!,])', r'\1', out)
    return out.capitalize()

def run_critic_loop(cycles):
    print(f"\n{CYAN}[System] Initiating Adversarial Critic Loop for {cycles} cycles...{NC}")
    approved, rejected = 0, 0
    prompt = random.choice(list(brain["vocab"].keys()))

    for i in range(cycles):
        thought = generate_thought(prompt, is_loop=True)
        words = thought.split()
        
        # Simple Critic Rules
        score = 1
        if len(words) < 4: score = -1
        if len(set(words)) < len(words) // 2: score = -2 # Repetition penalty
        
        if score > 0:
            approved += 1
            apply_reward(1)
            prompt = words[-1] # Feed the end of the thought into the next prompt
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
print(f"{WHITE} word@ NEURAL CORE (Hybrid Model v2){NC}")
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
