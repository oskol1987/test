import os
import datetime
import glob
import schedule
import time
import mysql.connector as mysql

def job():
   
	path = 'c:\\1\\'
	showDbsSql = "show databases"
	createDbSql = "create database fileops"
	createTableFilesHistorySql = "create table if NOT exists fileshistory(fileName varchar(100) NOT NULL, createdAt datetime NOT NULL, modifitedAt datetime NOT NULL, fileStatus varchar(50) NOT NULL, deletedAt datetime)"
	selectFilesHistorySql = "select * from fileshistory where fileName = %s"
	insertFilesHistorySql = "insert into fileshistory values(%s, %s, %s, 'created', NULL)"
	updateFilesHistorySql = "update fileshistory set modifitedAt = %s, fileStatus = 'updated' where fileName = %s AND modifitedAt <> %s"
	updateFilesHistoryDeletedSql = "update fileshistory set fileStatus = 'deleted', deletedAt = %s where fileName NOT IN(%s)"
	
	mysqlServer = mysql.connect(
		host = "localhost",
		user = "root",
		passwd = "pass"
	)
	
	mysqlServerCursor = mysqlServer.cursor()
	mysqlServerCursor.execute(showDbsSql)
    	mysqlServerDatabases = mysqlServerCursor.fethall()
	databaseExist = False 
	for dbName in mysqlServerDatabases:
		if dbName == "fileshistory": 
			databaseExist = True
	if not databaseExist:
		mysqlServerCursor.execute(createDbSql)
	
	mysqlServer.commit()
	
	mysqlFileOps = mysql.connect(
		host = "localhost",
		user = "root",
		passwd = "pass",
		database = "fileops"
	)

	mysqlFileOpsCursor = mysqlFileOps.cursor()
	mysqlFileOpsCursor.execute(createTableFilesHistorySql)
	
	files = [file for file in glob.glob(path + "*.*", recursive=False)]

	for file in files: 
		modifitedAt = (datetime.datetime.fromtimestamp(os.path.getmtime(file)))
		createdAt = (datetime.datetime.fromtimestamp(os.path.getctime(file)))
		mysqlFileOpsCursor.execute(selectFilesHistorySql, file)
		
		if mysqlFileOpsCursor.rowcount == 0:
			mysqlFileOpsCursor.execute(insertFilesHistorySql, (file, createdAt, modifitedAt))
		else: 
			mysqlFileOpsCursor.execute(updateFilesHistorySql, (modifitedAt, file, modifitedAt))
	
	mysqlFileOpsCursor.execute(updateFilesHistoryDeletedSql, (datetime.datetime.now(), files))
					
	mysqlFileOps.commit()
	
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
