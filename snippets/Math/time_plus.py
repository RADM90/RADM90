from datetime import datetime, timedelta

y2k = datetime(2000, 1, 1)

while True:
    try:
        m, s = map(int, input("Insert mm:ss to add\n>> ").split(":"))
    except:
        continue
    y2k += timedelta(minutes=m, seconds=s)
    print(f"{y2k.hour:02d}:{y2k.minute:02d}:{y2k.second:02d}\n")
