import webbrowser
import time

totalBreaks = 3
breakCount = 0

print("This program started on " + time.ctime())
while breakCount < totalBreaks:
    time.sleep(10)
    webbrowser.open("https://www.youtube.com/watch?v=ligGguhHu5U")
    breakCount += 1

