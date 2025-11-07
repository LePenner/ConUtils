import random
from conutils import *  # type: ignore

con = Console(overlap=True, fps=30)

DVD = ["DDDD  VV   VV DDDD",
       "D  DD  VV VV  D  DD",
       "D  DD   VVV   D  DD",
       "DDDD     V    DDDD"]

BETTERDVD = """⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡀
⠀⢠⣿⣿⡿⠀⠀⠈⢹⣿⣿⡿⣿⣿⣇⠀⣠⣿⣿⠟⣽⣿⣿⠇⠀⠀⢹⣿⣿⣿
⠀⢸⣿⣿⡇⠀⢀⣠⣾⣿⡿⠃⢹⣿⣿⣶⣿⡿⠋⢰⣿⣿⡿⠀⠀⣠⣼⣿⣿⠏
⠀⣿⣿⣿⣿⣿⣿⠿⠟⠋⠁⠀⠀⢿⣿⣿⠏⠀⠀⢸⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣸⣟⣁⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣠⣴⣶⣾⣿⣿⣻⡟⣻⣿⢻⣿⡟⣛⢻⣿⡟⣛⣿⡿⣛⣛⢻⣿⣿⣶⣦⣄⡀⠀
⠉⠛⠻⠿⠿⠿⠷⣼⣿⣿⣼⣿⣧⣭⣼⣿⣧⣭⣿⣿⣬⡭⠾⠿⠿⠿⠛⠉⠀"""

seg = 50

Spinner().reg_spn_type("wideee", "\\" *
                       seg + "|"*seg + "/"*seg + "-"*seg, seg)

pong: Text = Text(parent=con, representation=BETTERDVD)

vec = [-2, -1]
c = 0


def update():

    global c
    c += 1
    x = pong.x
    y = pong.y

    if x+vec[0] >= con.width-pong.width or x <= 0:
        vec[0] *= -1
        pong.color = (random.randint(1, 255), random.randint(
            1, 255), random.randint(1, 255))

    if y+vec[1] >= con.height-pong.height or y <= 0:
        vec[1] *= -1
        rand = random. randint(1, 255)
        pong.color = (rand, 255-rand, random.randint(1, 255))

    pong.x += vec[0]
    pong.y += vec[1]


con.run()
