
import os
import datetime
import glob
import schedule
import time


def job():
   
path = 'c:\\1\\'

folders = [f for f in glob.glob(path + "**/", recursive=True)]

for f in folders:
    print("Modified")
    print(datetime.datetime.fromtimestamp(os.path.getmtime(f)))

    print("Created")
    print(datetime.datetime.fromtimestamp(os.path.getctime(f)))


schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
