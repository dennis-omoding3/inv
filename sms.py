# import package
import africastalking


# Initialize SDK
username = "deni"    # use 'sandbox' for development in the test environment
api_key = "4ec0c2a877eb3d2bee322dad77a4e1b8adcbce79d9a6ac831336c43a611d45cc"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("come home!", ["+254703273154"])
print(response)



