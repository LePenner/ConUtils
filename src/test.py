from conutils import *

con = Console()

spn = Spinner(parent=con, color="green")

text = StaticText(parent=con, representation=[
                  f"{spn.seq}"], x=1, color=(255, 0, 0))

con.run()
