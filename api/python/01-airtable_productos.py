import http.client

conn = http.client.HTTPSConnection("api.airtable.com")
payload = ''
headers = {
  'Authorization': 'Bearer patdbap8raFBNlNhA.7aa8f22f86ce7658d1cc316867bef146214327d637ebcb7c7f3bccd6b697c586',
  'Cookie': 'brw=brwMS7Lemd31YKJa0; brwConsent=opt-in; AWSALBTG=Ydp1eJo1egLdKha824QwydEj8ZsCOEVy2O2BEMKgicWD/laeWlrSukqDmKcDspw/44Df/Mtz15i6UuDZ6fxtjBzdnD6EF/tI2SQ5RX82MsVu2NWjnjvAPnRqHLXY7r5x8YoBQiupHUKCRVLKHjnf1vdeCOtdwePAgKFfowx9PNBWjiwDs4Y=; AWSALBTGCORS=Ydp1eJo1egLdKha824QwydEj8ZsCOEVy2O2BEMKgicWD/laeWlrSukqDmKcDspw/44Df/Mtz15i6UuDZ6fxtjBzdnD6EF/tI2SQ5RX82MsVu2NWjnjvAPnRqHLXY7r5x8YoBQiupHUKCRVLKHjnf1vdeCOtdwePAgKFfowx9PNBWjiwDs4Y='
}
conn.request("GET", "/v0/appLLNRwDQ9NC4BOj/Productos", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))