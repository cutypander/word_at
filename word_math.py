import sys
import re
import math

# ANSI Terminal Colors
ORANGE = '\033[38;5;208m'
WHITE = '\033[1;37m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
NC = '\033[0m'

print(f"{ORANGE}========================================{NC}")
print(f"{WHITE} INTERACTIVE MATH ENGINE (Advanced){NC}")
print(f"{ORANGE}========================================{NC}")
print(f"{CYAN} [ SYNTAX GUIDE ]{NC}")
print(f"  Fractions : {WHITE}1/2{NC} (Standard division)")
print(f"  Exponents : {WHITE}2^3{NC} or {WHITE}2**3{NC}")
print(f"  Factorial : {WHITE}5!{NC}")
print(f"  Modulo    : {WHITE}10 % 3{NC} (Remainder)")
print(f"  Functions : {WHITE}sqrt(9), sin(pi), log(100){NC}")
print(f"  Constants : {WHITE}pi, e, tau{NC}")
print(f"{ORANGE}========================================{NC}")
print(" Type 'q' to quit.\n")

safe_env = {"__builtins__": None}
for name in dir(math):
    if not name.startswith('_'):
        safe_env[name] = getattr(math, name)
safe_env['abs'] = abs
safe_env['round'] = round

while True:
    try:
        expr = input(f"{WHITE}Math > {NC}")
        if expr.lower() == 'q':
            break
        if not expr.strip():
            continue

        # 1. Translate Human Math to Python Logic
        clean_expr = re.sub(r'(?<=\d)\s*x\s*(?=\d)', '*', expr)
        clean_expr = clean_expr.replace('^', '**').replace('{', '(').replace('}', ')')
        clean_expr = re.sub(r'(\d+)!', r'factorial(\1)', clean_expr)

        current_expr = clean_expr
        step_count = 1
        last_expr = ""

        # 2. Step-by-Step Breakdown
        while current_expr != last_expr:
            last_expr = current_expr
            # Match innermost parentheses and their preceding function names (e.g., 'factorial(100)')
            match = re.search(r'([a-zA-Z_]+)?\(([^()]+)\)', current_expr)
            if match:
                sub_expr = match.group(0)
                try:
                    sub_result = str(eval(sub_expr, safe_env))
                    current_expr = current_expr.replace(sub_expr, sub_result, 1)
                    display_expr = current_expr.replace('**', '^')
                    print(f" {CYAN}[Step {step_count}]{NC}  {display_expr}")
                    step_count += 1
                except:
                    break
            else:
                break

        # 3. Final Evaluation
        final_ans = eval(clean_expr, safe_env)
        
        if isinstance(final_ans, float) and final_ans.is_integer():
            final_ans = int(final_ans)
            
        print(f" {GREEN}[Final]{NC}   {final_ans}\n")

    except Exception as e:
        print(f" {RED}[Error] Invalid syntax or mathematical impossibility.{NC}\n")
