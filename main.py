from flask import Flask, render_template, request
import sqlite3, requests
from xml.etree import ElementTree

app = Flask(__name__)

app.database = "address_book.db"

@app.route('/')
def index():
	connection = connect_db()
	cursor = connection.execute('SELECT * FROM contacts')
	contacts = [dict(name=row[0], address=row[1], city=row[2], state=row[3], zip=row[4]) for row in cursor.fetchall()]
	connection.close()
	
	return render_template("home.html", contacts = contacts)
	
	
@app.route('/zip-lookup')
def zip_lookup():
	address = request.args.get("address")
	city = request.args.get("city")
	state = request.args.get("state")
	
	contact = parse_zip_lookup_response(address, city, state)
	
	return render_template("lookup.html", contact = contact)	

	
@app.route('/city-state-lookup')
def city_state_lookup():
	zip = request.args.get("zip")
	
	contact = parse_city_state_lookup_response(zip);
	return render_template("lookup.html", contact = contact)	


@app.route('/add')
def add():
	name = request.args.get("name")
	address = request.args.get("address")
	city = request.args.get("city")
	state = request.args.get("state")
	zip = request.args.get("zip")
	
	contact = parse_verification_response(address, city, state, zip)
	
	with sqlite3.connect("address_book.db") as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO contacts VALUES(?, ?, ?, ?, ?)", (name, contact.get("address"), contact.get("city"), contact.get("state"), contact.get("zip")))
		cursor.close()
	
	return index()
	
	
@app.route('/delete')
def delete():
	name = request.args.get("name")
	
	with sqlite3.connect("address_book.db") as connection:
		cursor = connection.cursor()
		cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
		cursor.close()
	
	return index()
	
	
def connect_db():
	return sqlite3.connect(app.database)

def parse_zip_lookup_response(address, city, state):
	response = requests.get(build_zip_lookup_url(address, city, state))
	root = ElementTree.fromstring(response.content)
	return {"contactAddress":address, 
			"contactCity":city, 
			"contactState":state, 
			"contactZip":root[0][3].text, 
			"contactZip2":root[0][4].text}

def build_zip_lookup_url(address, city, state):
	return "http://production.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=<ZipCodeLookupRequest USERID=\"176PERSO6838\"><Address ID=\"0\"><Address1></Address1><Address2>"+address+"</Address2><City>"+city+"</City><State>"+state+"</State></Address></ZipCodeLookupRequest>"

def parse_city_state_lookup_response(zip):
	response = requests.get(build_city_state_lookup_url(zip))
	root = ElementTree.fromstring(response.content)
	return {"contactCity":root[0][1].text, 
			"contactState":root[0][2].text, 
			"contactZip":root[0][0].text}
			
def build_city_state_lookup_url(zip):
	return "http://production.shippingapis.com/ShippingAPI.dll?API=CityStateLookup&XML=<CityStateLookupRequest USERID=\"176PERSO6838\"><ZipCode ID=\"0\"><Zip5>"+zip+"</Zip5></ZipCode></CityStateLookupRequest>"

def parse_verification_response(address, city, state, zip):
	response = requests.get(build_address_verification_url(address, city, state, zip))
	root = ElementTree.fromstring(response.content)
	combinedZip = root[0][3].text+"-"+root[0][4].text
	return {"address":root[0][0].text, 
			"city":root[0][1].text, 
			"state":root[0][2].text, 
			"zip":combinedZip}
			
def build_address_verification_url(address, city, state, zip):
	return "http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=<AddressValidateRequest USERID=\"176PERSO6838\"><Address ID=\"0\"><FirmName></FirmName><Address1></Address1><Address2>"+address+"</Address2><City>"+city+"</City><State>"+state+"</State><Zip5>"+zip+"</Zip5><Zip4></Zip4></Address></AddressValidateRequest>"
	
if __name__ == "__main__":
	app.run()
