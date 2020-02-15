import os
import datetime
import glob
import schedule
import time
import mysql.connector as mysql

def job():
   
path = 'c:\\1\\'

folders = [f for f in glob.glob(path + "**/", recursive=True)]

for f in folders:
  
m = (datetime.datetime.fromtimestamp(os.path.getmtime(f)))
  
c= (datetime.datetime.fromtimestamp(os.path.getctime(f)))

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "pass",
    database = "file"
)

cursor = db.cursor()

query = "INSERT INTO files (modified, created) VALUES (%s, %s)"

values = ("m", "c")

cursor.execute(query, values)

db.commit()
		
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
