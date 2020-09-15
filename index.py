import sys

import config
from lib import api

# Testing data - START
# NOTE
# venueId is the unique id of the SafeEntry QR venue used to checkin/checkout
# Staging - Example for Venue with no destination configured
data = {
    "subType": "uinfin",
    "actionType": "checkin",
    "sub": "S9960846C",
    "venueId": "STG-180000001W-83338-SEQRSELFTESTSINGLE-SE",
    "mobileno": "92376345"
}

# Staging - Example for Venue with multiple destinations (e.g. Lobby, Swimming Pool, Restaurant)
# data = {
# 	"subType": "uinfin",
# 	"actionType": "checkin",
# 	"sub": "S9960846C",
# 	"venueId": "STG-180000001W-409531-SEQRSELFTESTMULTIPLE-SE",
# 	"mobileno": "92376345",
# 	"tenantId": "VENUE1"
# };

# Testing data - END

if __name__ == '__main__':
	apiType = str(sys.argv[2])
	if apiType == "entry":
		# Call SE Entry API
		result = api.callEntry(data, config)
		if result['success']:
			print("Success! \nBody:")
		else:
			print("Error! \nBody: ",result['data'])