import sqlite3

with sqlite3.connect("address_book.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS contacts")
	c.execute("""CREATE TABLE contacts(name TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)""")
	c.execute("""INSERT INTO contacts VALUES("Charlie Winnard", "3936 WYANDOT ST", "DENVER", "CO", "80211-2139")""")
	c.close()