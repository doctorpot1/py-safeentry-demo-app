# This file provides functions to encrypt/decrypt data
import json

from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode
#  Function to decrypt JWE compact serialization Format
#  - pemPrivateKey : Private Key string, PEM format
#  - compactJWE : data in compact serialization format - header.encryptedKey.iv.ciphertext.tag

def decryptCompactJWE(pemPrivateKey, compactJWE):
	result = {
		"success": False
	}
	try:
		with open(pemPrivateKey, "rb") as pemfile:
			key = jwk.JWK.from_pem(pemfile.read())
			jwetoken = jwe.JWE()
			jwetoken.deserialize(compactJWE)
			jwetoken.decrypt(key)
			result['data'] = jwetoken.payload
	except Exception as e:
		result['data'] = str(e)
	return result

#  Function to Encrypt data into JWE compact serialization Format
#  - pemPublicCert : Public Cert string, PEM format
#  - data : data to be encrypted
#  - return : Promise that resolve to encrypted content in JWE compact serialization format

def encryptCompactJWE(pemPublicCert, data):
	result = {
		"success": False
	}
	try:
		with open(pemPublicCert, "rb") as pemfile:
			key = jwk.JWK.from_pem(pemfile.read())
			jwetoken = jwe.JWE(data.encode('utf-8'), json_encode({"alg": "RSA-OAEP", "enc": "A256GCM"}))
			jwetoken.add_recipient(key)
			result['data'] = jwetoken.serialize(True)
			result['success'] = True
	except Exception as e:
		result['data'] = str(e)
	return result
