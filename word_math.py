import sys
from math import *

print("\033[38;5;208m========================================\033[0m")
print("\033[1;37m INTERACTIVE MATH ENGINE\033[0m")
print("\033[38;5;208m========================================\033[0m")
print(" Type 'q' to quit.")

while True:
    try:
        math_input = input(" Math > ")
        if math_input.lower() in ['q', 'quit', 'exit']:
            break
        if not math_input.strip():
            continue
            
        clean_expr = math_input.replace('{','(').replace('}',')').replace('[','(').replace(']',')').replace('x','*').replace('^','**')
        result = eval(clean_expr)
        
        if isinstance(result, float) and result.is_integer(): 
            result = int(result)
            
        print(f"\033[0;32m [Final]\033[0m    {result}\n")
    except KeyboardInterrupt:
        break
    except Exception:
        print("\033[0;31m Invalid Syntax\033[0m\n")

