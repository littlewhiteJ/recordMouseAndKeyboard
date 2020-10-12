from Replaying import Replaying
import pyperclip
import time
import random

replay = Replaying()

def getEndDay(year, month):
    if month == 2:
        if year % 4 == 0:
            return '29'
        else:
            return '28'
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        return '31'
    else:
        return '30'

for year in range(2000, 2010):
    for month in range(1, 13):
        if year == 2000 and month < 6:
            continue

        startDate = str(year) + '-' + str(month).zfill(2) + '-' + '01'
        endDate = str(year) + '-' + str(month).zfill(2) + '-' + getEndDay(year, month)

        replay.startReplay('steps/pointStartDate.json')
        pyperclip.copy(startDate)
        replay.startReplay('steps/Ctrl_V.json')

        replay.startReplay('steps/pointEndDate.json')
        pyperclip.copy(endDate)
        replay.startReplay('steps/Ctrl_V.json')

        replay.startReplay('steps/apply.json')
        time.sleep(random.randint(5, 7))

        replay.startReplay('steps/copyAndPaste.json')
        pyperclip.copy(startDate)
        replay.startReplay('steps/Ctrl_V.json')
        
