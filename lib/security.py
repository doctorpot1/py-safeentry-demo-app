import json
import uuid
import time
from urllib.parse import urlencode
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

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
	key = RSA.import_key(open(keyCertContent).read())
	signer = PKCS1_v1_5.new(key)
	digest = SHA256.new()
	# It's being assumed the data is base64 encoded, so it's decoded before updating the digest
	digest.update(baseString.encode('utf-8'))
	signature = b64encode(signer.sign(digest)).decode('utf-8')

	print("Digital Signature:")
	print(signature)

	# D) Assembling the Header
	strApexHeader = "PKI_SIGN timestamp=\"" + str(timestamp) +\
					"\",nonce=\"" + str(nonceValue) +\
					"\",app_id=\"" + appId +\
					"\",signature_method=\"RS256\"" +\
					",signature=\"" + signature +\
					"\""
	return strApexHeader