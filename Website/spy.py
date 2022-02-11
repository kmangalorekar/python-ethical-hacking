import requests
import re
import urlparse

url = "http://10.5.5.4/mutillidae/"
links = []

def extract_links(url):
	response = requests.get(url)
	return re.findall('(?:href=")(.*?)"',response.content)


def crawl(url):
	hlinks = extract_links(url)

	for link in hlinks:
		link = urlparse.urljoin(url,link)
		

		if "#" in link:
			link = link.split("#")[0]


		if url in link and link not in links:
			links.append(link)
			print link
			crawl(link)


crawl(url)
