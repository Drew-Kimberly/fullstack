from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC9957f335b24e2ab7a69bd7addad04b49"
auth_token  = "935c1d6974af3a7f8e2366b16b170089"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(
    body="write anything here",
    to="+12038953853",    # Replace with your phone number
    from_="+12035905135") # Replace with your Twilio number

