import requests
from bs4 import BeautifulSoup
import urlparse

def request(url):
	try:
		return requests.get(url)
	except Exception as e:
		pass

url = "http://10.5.5.4/mutillidae/index.php?page=dns-lookup.php"
response = request(url)
#print response.content

parsed_html = BeautifulSoup(response.content,features="lxml")

forms_list = parsed_html.findAll("form")
for form in forms_list:
	action = form.get("action")
	post_url = urlparse.urljoin(url,action)
	method = form.get("method")
	#print post_url


	inputs_list = form.findAll("input")
	post_data = {}
	for i in inputs_list:
		iname = i.get("name")
		itype = i.get("type")
		ivalue = i.get("value")
		if itype == 'text':
			ivalue = "test"
		post_data[iname] = ivalue
	result = requests.post(post_url,post_data)
	print result.content

#print forms_list