import requests
# domain - The domain of the URL
# requestPath - The url that is requesting
# headers - The headers of the request
# method - The request method

def getResponse(url, headers, method, body):
	# Note that this method deviate from the original source where instead of Async Promise to handle API calls
	# this uses a Sync request method.
	requestOptions = {
		"method": method,
		"url": url,
		"headers": headers
	}

	print("requestOptions: ",requestOptions)

	result = {
		"success": False
	}
	response = requests.request(method,headers=headers,url=url,data=body)

	if response.status_code >= 400:
		result['data'] = response.text
	else:
		result['success'] = True
		result['data'] = response.text

	return result