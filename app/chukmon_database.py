#!/usr/bin/env python3
import sys, os, sqlite3, datetime


def chuk_checkdb(DB_FILE):
	print("\033[1;34mChecking db file exists\033[0m")
	try:
		os.path.isfile(DB_FILE)
		print("\033[1;32m[OK] DB File " + DB_FILE + " found.\033[0m")
	except:
		print("\033[0;31m[ERROR] DB File " + DB_FILE + " not found, quiting!\033[0m")
		sys.exit(1)


	print("\033[1;34mChecking DB Read")
	try:
		conn = sqlite3.connect(DB_FILE)
		c = conn.cursor()
		c.execute("select value from config where option = 'last_startup';")
		dbv = c.fetchone()
		print("\033[1;32m[OK] DB READABLE: last_startup:" + dbv[0] + "\033[0m")
	except:
		print("\033[0;31m[ERROR] Unable to read last_startup from: " + DB_FILE + ", possible DB corruption or permision issue!\033[0m")
		sys.exit(1)

	print("\033[1;34mChecking DB Write\033[0m")
	try:
		now = datetime.datetime.now()
		sql = "insert or replace into config values('last_startup','" + str(now) + "');"
		conn = sqlite3.connect(DB_FILE)
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		print("\033[1;32m[OK] Wrote start time:" + str(now) + "\033[0m")
	except:
		print("\033[0;31m[ERROR] Unable to write startup time to: " + DB_FILE + ", possible DB corruption or permision issue!\033[0m")
		sys.exit(1)


def chuk_initdb(DB_FILE):
	print("\033[1;34mChecking if DB exist")
	if (  os.path.isfile(DB_FILE) ):
		print("\033[1;32m[OK] DB Files exists, will not initialise")
	else:
		print("\033[1;35m[WARNING] DB File does not exits, will initialise")
		try:
			conn = sqlite3.connect(DB_FILE)
			c = conn.cursor()
			print("Creating config table")
			sql_file= open("skel/db/create_config.sql")
			c.executescript(sql_file.read())
			print("Creating compaies house table")
			sql_file= open("skel/db/create_companieshouse.sql")
			c.executescript(sql_file.read())
			print("Creating good companies table")
			sql_file= open("skel/db/create_goodcompanies.sql")
			c.executescript(sql_file.read())		
			print("Creating search terms table")
			sql_file= open("skel/db/create_searchterms.sql")
			c.executescript(sql_file.read())	
		except:
			print("\033[0;31m[ERROR] Unable to create DB: " + DB_FILE + "!\033[0m")
			sys.exit(1)