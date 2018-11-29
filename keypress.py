from msvcrt import getch
import serial

ser = serial.Serial('COM5', 9600, timeout=0)

while True:
    key = getch()
    okey = ord(key)
    if okey == 27:  # 27 is escape
        break
    # Special keys (arrows, f keys, ins, del, etc.) generate two codes:
    # first = 224, second = call getch() again to read it
    # only print printable characters
    if okey >= 32 and okey <=126:
        print(key, okey)
        ser.write(key)
    
    