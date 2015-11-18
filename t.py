import json
import requests

client_id = "dpww8ee2sog7ttqhdlml7kz2tj6zuc8j"
client_secret = "zot4htJANVmTEBQET7Z2t4bOvq4OUh2d"

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

print get_token()