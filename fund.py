import requests
import json
import csv

contacts = "https://levelsolar.secure.force.com/api/services/apexrest/contacts"
accounts = "https://levelsolar.secure.force.com/api/services/apexrest/accounts"
cases = "https://levelsolar.secure.force.com/api/services/apexrest/cases"

# permanent values
client_id = "dpww8ee2sog7ttqhdlml7kz2tj6zuc8j"
client_secret = "zot4htJANVmTEBQET7Z2t4bOvq4OUh2d"
ny_customer_folder_id = "1763301834"

def customer_array():
	customers = []
	with open("s.csv") as csvfile:
		csv_r = csv.DictReader(csvfile)
		for row in csv_r:
			cust = {"name": row["name"], "account_id": row["account_id"]}
			customers.append(cust)
	csvfile.close()
	return customers

def api_response(url, parameters):
	response_json = requests.get(url, params=parameters).json()
	return response_json

def get_token():
	token_file = open("token.json", "r")
	token_json = json.load(token_file)
	refresh_token = token_json["refresh_token"]
	token_file.close()
	get_token_url = "https://app.box.com/api/oauth2/token"
	body = {"grant_type": "refresh_token",
			"refresh_token": refresh_token,
			"client_id": client_id,
			"client_secret": client_secret}
	response_object = requests.post(get_token_url, data=body)
	response_body = response_object.json()
	access_token = response_body["access_token"]
	file_object = open("token.json", "w")
	json.dump(response_body, file_object)
	file_object.close()
	return access_token

def get_county_city(account_id):
	account_list = api_response(accounts, {"account_number": account_id})
	county = account_list[0]["municipality"]["county"]["name"]
	address, city, zip_code = account_list[0]["name"].split(" - ")
	info = {"county": county, "city": city}
	return info

def download_ppa_signed(county, city, account_id):
	data = "File"
	access_token = get_token()
	headers = {"Authorization": "Bearer " + access_token}
	folder_items_url = "https://api.box.com/2.0/folders/" + ny_customer_folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == county:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == city:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if account_id in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if "Permits" in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["type"] == "file":
			if "PPA RK" in item["name"] or "ppa RK" in item["name"] or "PPA - RK" in item["name"] or "PPA -RK" in item["name"] or "PPA- RK" in item["name"]:
				file_id = item["id"]
				download_file_url = "https://api.box.com/2.0/files/" + file_id + "/content"
				response_object = requests.get(download_file_url, headers=headers)
				data = response_object.content
				return data
	if data == "File":
		return "Not Found"
	else:
		return data

def download_ppa_unsigned(county, city, account_id):
	data = "File"
	access_token = get_token()
	headers = {"Authorization": "Bearer " + access_token}
	folder_items_url = "https://api.box.com/2.0/folders/" + ny_customer_folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == county:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == city:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if account_id in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if "Permits" in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["type"] == "file":
			if "PPA" in item["name"] or "ppa" in item["name"] or "Ppa" in item["name"]:
				file_id = item["id"]
				download_file_url = "https://api.box.com/2.0/files/" + file_id + "/content"
				response_object = requests.get(download_file_url, headers=headers)
				data = response_object.content
				return data
	if data == "File":
		return "Not Found"
	else:
		return data

def download_building_permit(county, city, account_id):
	data = "File"
	access_token = get_token()
	headers = {"Authorization": "Bearer " + access_token}
	folder_items_url = "https://api.box.com/2.0/folders/" + ny_customer_folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == county:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["name"] == city:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if account_id in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if "Permits" in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if "Fund Documents" in item["name"]:
			folder_id = item["id"]
			folder_items_url = "https://api.box.com/2.0/folders/" + folder_id + "/items"
	folder_items = requests.get(folder_items_url, headers=headers).json()
	for item in folder_items["entries"]:
		if item["type"] == "file":
			if "BP" in item["name"] or "bp" in item["name"] or "Bp" in item["name"] or "Building Permit" in item["name"]:
				file_id = item["id"]
				download_file_url = "https://api.box.com/2.0/files/" + file_id + "/content"
				response_object = requests.get(download_file_url, headers=headers)
				data = response_object.content
	if data == "File":
		return "Not Found"
	else:
		return data

def get_files():
	not_found = []
	customer_list = customer_array()
	for item in customer_list:
		county_city = get_county_city(item["account_id"])
		county = county_city["county"]
		city = county_city["city"]
		ppa_signed = download_ppa_signed(county, city, item["account_id"])
		if ppa_signed == "Not Found":
			ppa_unsigned = download_ppa_unsigned(county, city, item["account_id"])
			if ppa_unsigned == "Not Found":
				not_found.append({"missing_ppa": item["name"]})
			else:
				ppa_unsigned_file = open("Files/%s - Unsigned PPA.pdf" %item["name"], "wb")
				ppa_unsigned_file.write(ppa_unsigned)
				ppa_unsigned_file.close()	
		else:
			ppa_signed_file = open("Files/%s - Signed PPA.pdf" %item["name"], "wb")
			ppa_signed_file.write(ppa_signed)
			ppa_signed_file.close()
		building_permit = download_building_permit(county, city, item["account_id"])
		if building_permit == "Not Found":
			not_found.append({"missing_bp": item["name"]})
		else:
			bp_file = open("Files/%s - Building Permit.pdf" %item["name"], "wb")
			bp_file.write(building_permit)
			bp_file.close()
	missing_file = open("Files/missing.json", "w")
	json.dump(not_found, missing_file)
	missing_file.close()
	print "Done"

get_files()


