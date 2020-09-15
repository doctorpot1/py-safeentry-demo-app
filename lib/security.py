import json
import uuid
import time
from urllib.parse import urlencode
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode
import base64

security = {}

# Sorts a JSON object based on the key value in alphabetical order
def sortJSON(json):
	if json is None:
		return json

	newJSON = {}
	keys = sorted(json.keys(), key=lambda x: x.lower())
	for key in keys:
		newJSON[key] = json[key]
	return newJSON

#  @param url Full API URL
#  @param params JSON object of params sent, key/value pair.
#  @param method
#  @param appId ClientId
#  @param keyCertContent Private Key Certificate content
#  @param keyCertPassphrase Private Key Certificate Passphrase
#  @returns {string}

def generateSHA256withRSAHeader(url, params, method, appId, keyCertContent, keyCertPassphrase):
	nonceValue = uuid.uuid4()
	timestamp = int(time.time()*1000)

	# A) Construct the Authorisation Token
	defaultApexHeaders = {
		"app_id": appId, #// App ID assigned to your application
		"nonce": nonceValue, #// secure random number
		"signature_method": "RS256",
		"timestamp": timestamp #// Unix epoch time
	}

	# B) Forming the Signature Base String

	# i) Normalize request parameters
	baseParams = sortJSON({**defaultApexHeaders, **params})
	print("baseParams:",baseParams)
	baseParamsStr = urlencode(baseParams)
	print(baseParamsStr)

	# ii) construct request URL ---> url is passed in to this function

	# iii) concatenate request elements
	baseString = method.upper() + "&" + url + "&" + baseParamsStr

	print("Formulated Base String:")
	print(baseString)

	# C) Signing Base String to get Digital Signature
	with open(keyCertContent, "rb") as pemfile:
		key = jwk.JWK.from_pem(pemfile.read())
		jwstoken = jws.JWS(baseString)
		if keyCertPassphrase is not None and keyCertPassphrase is not None:
			#to decrypt the key first
			pass
		jwstoken.add_signature(key, None, json_encode({"alg": "RS256"}))
		signature = json.loads(jwstoken.serialize())

	print("Digital Signature:")
	print(signature)

	print("\n\n")


	# D) Assembling the Header
	strApexHeader = "PKI_SIGN timestamp=\"" + str(timestamp) +\
					"\",nonce=\"" + str(nonceValue) +\
					"\",app_id=\"" + appId +\
					"\",signature_method=\"RS256\"" +\
					",signature=\"" + signature['signature'] +\
					"\""
	print(strApexHeader)
	return strApexHeader