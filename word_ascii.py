import os, time, sys, signal
try:
    import cv2
except ImportError:
    print("\033[0;31m[ERROR] Python cv2 (OpenCV) missing. Run 'word@ ?inst'\033[0m")
    sys.exit(1)

chars = [' ', '░', '▒', '▓', '█']
vid_path = sys.argv[1]
sub_path = sys.argv[2] if len(sys.argv) > 2 else ""

print("\n\033[38;5;208m--- TERMINAL ASCII CONFIGURATION ---\033[0m")
use_color = input(" Color Mode [1] Pure White [2] Phosphor Green [3] True Color: ") == '3'
use_green = input(" Color Mode [1] Pure White [2] Phosphor Green [3] True Color: ") == '2' if not use_color else False
res_mode = input(" Resolution [1] 80-col [2] 120-col [3] MAX: ")
if res_mode not in ['1', '2', '3']: res_mode = '1'

cap = cv2.VideoCapture(vid_path)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 0: fps = 30
target_delay = 1.0 / fps

subs = []
if os.path.exists(sub_path):
    with open(sub_path, 'r') as f:
        subs = [line.strip() for line in f if line.strip()]

sys.stdout.write('\033[48;2;0;0;0m\033[2J\033[?25l') 
frame_count = 0

try:
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try: term_width = os.get_terminal_size().columns
        except OSError: term_width = 80
            
        if res_mode == '1': width = min(80, term_width)
        elif res_mode == '2': width = min(120, term_width)
        else: width = term_width
            
        aspect = gray.shape[0] / gray.shape[1]
        height = int(width * aspect * 0.45) 
        
        resized_gray = cv2.resize(gray, (width, height))
        if use_color: resized_color = cv2.resize(frame, (width, height))
            
        ascii_lines = []
        for y in range(height):
            line_chars = []
            for x in range(width):
                char_idx = int((resized_gray[y, x] / 255.0) * 4.99)
                char = chars[char_idx]
                if use_color:
                    b, g, r = resized_color[y, x]
                    line_chars.append(f'\033[38;2;{r};{g};{b}m{char}')
                elif use_green:
                    line_chars.append(f'\033[38;2;0;255;0m{char}')
                else:
                    line_chars.append(f'\033[1;37m{char}')
            ascii_lines.append(''.join(line_chars) + '\033[0m\033[K')
            
        ascii_frame = '\n'.join(ascii_lines)
            
        if subs:
            sub_idx = int((frame_count / fps) // 3) % len(subs)
            current_sub = subs[sub_idx]
            pad = max(0, (width - len(current_sub)) // 2)
            sub_line = (' ' * pad) + '\033[1;37m' + current_sub + '\033[48;2;0;0;0m\033[K'
            lines = ascii_frame.split('\n')
            if len(lines) > 3: lines[-4] = sub_line
            ascii_frame = '\n'.join(lines)
            
        sys.stdout.write('\033[H' + ascii_frame + '\033[J')
        sys.stdout.flush()
        
        elapsed = time.time() - start_time
        sleep_time = target_delay - elapsed
        if sleep_time > 0: time.sleep(sleep_time)
        frame_count += 1
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    sys.stdout.write('\033[0m\033[2J\033[H\033[?25h')
    sys.stdout.flush()
