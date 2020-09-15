import json
import sys
from urllib.parse import urlparse

from lib import security, jwe, requestHandler

env = sys.argv[1]
STAGE_PREFIX = ""
if env == "production":
	STAGE_PREFIX = "api"
elif env == "test":
	STAGE_PREFIX = "test.api"
elif env == "sandbox":
	STAGE_PREFIX = "sandbox.api"

seEntryUrl = "https://" + STAGE_PREFIX + ".safeentry-qr.gov.sg/partner/v1/entry";

def callEntry(data, config):
	url = seEntryUrl
	urlObj = urlparse(url)

	method = "POST"
	params = {}

	body = None

	header = None
	if (getattr(config, env)['security']):
		# if using security, Content - Type must be "application/jose"
		header = {
			"Content-Type": "application/jose"
		}
		encrypted = jwe.encryptCompactJWE(getattr(config, env)['publicCertPath'],json.dumps(data))
		if encrypted['success']:
			params['jose'] = encrypted['data']
			header['Authorization'] = security.generateSHA256withRSAHeader(urlObj.scheme + '://' + urlObj.netloc + urlObj.path, params, method, getattr(config, env)['appId'], getattr(config, env)['privateKeyPath'], None);
		body = params['jose']
	else:
		header = {
			"Content-Type": "application/json"
		}
		body = json.dumps(data)
	return requestHandler.getResponse(url, header, method, body)