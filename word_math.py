import sys
import re

print("========================================")
print(" INTERACTIVE MATH ENGINE (Step-by-Step)")
print("========================================")
print(" Type 'q' to quit.")

while True:
    try:
        expr = input("Math > ")
        if expr.lower() == 'q':
            break
        
        # Clean up the input for evaluation
        clean_expr = expr.replace(' ', '').replace('^', '**').replace('x', '*').replace('{', '(').replace('}', ')')
        
        current_expr = clean_expr
        step_count = 1
        
        # Loop to find and solve innermost parentheses step-by-step
        while '(' in current_expr:
            # Find innermost parentheses using regex
            match = re.search(r'\([^()]+\)', current_expr)
            if match:
                sub_expr = match.group(0)
                try:
                    # Evaluate just the chunk inside the parentheses
                    sub_result = str(eval(sub_expr))
                    current_expr = current_expr.replace(sub_expr, sub_result)
                    
                    # Clean it up for the terminal display
                    display_expr = current_expr.replace('**', '^')
                    print(f" [Step {step_count}]  {display_expr}")
                    step_count += 1
                except:
                    break
            else:
                break
                
        # Final Evaluation of the entire cleaned expression
        final_ans = eval(clean_expr)
        
        # Drop the decimal if it's a perfectly clean whole number
        if isinstance(final_ans, float) and final_ans.is_integer():
            final_ans = int(final_ans)
        
        print(f" [Final]   {final_ans}\n")
        
    except Exception as e:
        print(f" [Error] Invalid syntax. Check your math! ({e})\n")
