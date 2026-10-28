import sys, time, random
from core.config import R, R2, R3, B, B2, B3, W, W2, Y, O, G, D, D2, N, BOLD

CHARS = "─☸❖♡★ᏦᎥᏁᎶ⏤01"

ART = r"""
           /$$                  /$$$$$$            /$$                 /$$ /$$
          | $$                 /$$__  $$          | $$                | $$| $$
  /$$$$$$ | $$$$$$$   /$$$$$$ |__/  \ $$  /$$$$$$$| $$$$$$$   /$$$$$$ | $$| $$
 /$$__  $$| $$__  $$ /$$__  $$  /$$$$$$/ /$$_____/| $$__  $$ /$$__  $$| $$| $$
| $$  \ $$| $$  \ $$| $$  \ $$ /$$____/ |  $$$$$$ | $$  \ $$| $$$$$$$$| $$| $$
| $$  | $$| $$  | $$| $$  | $$| $$       \____  $$| $$  | $$| $$_____/| $$| $$
| $$$$$$$/| $$  | $$| $$$$$$$/| $$$$$$$$ /$$$$$$$/| $$  | $$|  $$$$$$$| $$| $$
| $$____/ |__/  |__/| $$____/ |________/|_______/ |__/  |__/ \_______/|__/|__/
| $$                | $$                                                      
| $$                | $$                                                      
|__/                |__/                                                      
"""

def matrix_rain(duration=1.2):
    cols = 74
    end = time.time() + duration
    while time.time() < end:
        line = ""
        for _ in range(cols):
            r = random.random()
            if r < 0.12:
                line += f"{R}{random.choice(CHARS)}{N}"
            elif r < 0.25:
                line += f"{B2}{random.choice(CHARS)}{N}"
            elif r < 0.35:
                line += f"{R3}{random.choice(CHARS)}{N}"
            elif r < 0.42:
                line += f"{D}{random.choice(CHARS)}{N}"
            else:
                line += " "
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        time.sleep(0.025)

def show_banner():
    lines = ART.strip("\n").split("\n")
    colors = [R, R, R2, R2, R3, B, B2, B2]

    print()
    for i, line in enumerate(lines):
        c = colors[i] if i < len(colors) else B2
        print(f"  {c}{line}{N}")

    print(f"""
  {D}┌{'─'*66}┐{N}
  {D}│{N}                                                                {D}│{N}
  {D}│{N}  {R}{BOLD}PHP{N}{R2}{BOLD}2{N}{B}{BOLD}SHELL{N}  {W2}Advanced PHP Vulnerability Scanner{N}              {D}│{N}
  {D}│{N}                                                                {D}│{N}
  {D}│{N}  {D2}Version  :{W} 1.0{N}                                                {D}│{N}
  {D}│{N}  {D2}Author   :{W} maxod{N}                                              {D}│{N}
  {D}│{N}  {D2}Platform :{W} Kali Linux {R2}+{W} Termux{N}                               {D}│{N}
  {D}│{N}  {D2}Engine   :{W} Pure Python {D2}(zero dependencies){N}                    {D}│{N}
  {D}│{N}                                                                {D}│{N}
  {D}│{N}  {R}Config{D2} ▸ {R2}Upload{D2} ▸ {O}Inject{D2} ▸ {B}LFI{D2} ▸ {B2}Shell{D2} ▸ {G}CVE{D2} ▸ {Y}Deser{N}      {D}│{N}
  {D}│{N}                                                                {D}│{N}
  {D}│{N}  {D2}Authorized testing only. Use responsibly.{N}                     {D}│{N}
  {D}│{N}                                                                {D}│{N}
  {D}└{'─'*66}┘{N}
""")

