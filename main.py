import math
tosiffer="{:>02}"
tid=float( input("Skriv inn antall timer:  "))
print(tid)
timer=math.floor(tid)
minutter=((tid-math.floor(tid))*60)
sekunder=((minutter-math.floor(minutter))*60)
print(tosiffer.format(str(int(timer)))+":"+tosiffer.format(str(int(minutter)))+":"+tosiffer.format(str(int(sekunder))))