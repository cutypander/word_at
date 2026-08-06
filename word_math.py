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
print(f"  Functions : {WHITE}sqrt(9), sin(pi), log(100){NC}")
print(f"  Constants : {WHITE}pi, e, tau{NC}")
print(f"{ORANGE}========================================{NC}")
print(" Type 'q' to quit.\n")

# Build a safe mathematical environment using Python's math library
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
        # Replace 'x' with '*' if it's surrounded by numbers
        clean_expr = re.sub(r'(?<=\d)\s*x\s*(?=\d)', '*', expr)
        # Replace ^ with ** for exponents
        clean_expr = clean_expr.replace('^', '**').replace('{', '(').replace('}', ')')
        # Translate factorials: 100! -> factorial(100)
        clean_expr = re.sub(r'(\d+)!', r'factorial(\1)', clean_expr)

        current_expr = clean_expr
        step_count = 1

        # 2. Step-by-Step Breakdown (For arithmetic)
        while True:
            # Find innermost parentheses NOT preceded by a letter (protects functions like 'factorial(')
            match = re.search(r'(?<![a-zA-Z])\(([^()]+)\)', current_expr)
            if match:
                sub_expr = match.group(0)
                inner = match.group(1)
                try:
                    sub_result = str(eval(inner, safe_env))
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
        
        # Format integers cleanly to drop the .0 if it's a whole number
        if isinstance(final_ans, float) and final_ans.is_integer():
            final_ans = int(final_ans)
            
        print(f" {GREEN}[Final]{NC}   {final_ans}\n")

    except Exception as e:
        # Provide a clean error message
        print(f" {RED}[Error] Invalid syntax or mathematical impossibility.{NC}\n")
