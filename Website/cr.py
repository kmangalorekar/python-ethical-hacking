import requests



def request(url):
	try:
		return requests.get("http://" + url)
	except Exception as e:
		pass

url = "zsecurity.org"
with open('/root/Downloads/common.txt','r') as f:
	for line in f:
		test_url =  url + "/" + line.strip()
		response =  request(test_url)
		if response:
			print "Discovered!", test_url


