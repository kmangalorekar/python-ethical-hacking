import requests
import re
import urlparse
from bs4 import BeautifulSoup

class Scanner:
	def __init__(self,url,ignore_links):
		self.session = requests.Session()
		self.target_url = url
		self.links = []
		self.ignore_links = ignore_links

	def extract_links(self,url):
		response = self.session.get(url)
		return re.findall('(?:href=")(.*?)"',response.content)


	def crawl(self,url = None):
		if url==None:
			url = self.target_url
		hlinks = self.extract_links(url)

		for link in hlinks:
			link = urlparse.urljoin(url,link)
			

			if "#" in link:
				link = link.split("#")[0]

			if self.target_url in link and link not in self.links and link not in self.ignore_links:
				self.links.append(link)
				print link
				self.crawl(link)

	def extract_forms(self,url):
		response = self.session.get(url)
		parsed_html = BeautifulSoup(response.content,features="lxml")
		return parsed_html.findAll("form")

	def submit_form(self,form,value,url):
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
				ivalue = value
			post_data[iname] = ivalue
		if method == "post":
			return self.session.post(post_url,post_data)
		return self.session.get(post_url,params=post_data)

	def run_scanner(self):
		for link in self.links:
			print link
			forms = self.extract_forms(link)
			for i in forms:
				print("\nTesting form in : ", link)
				if self.xss_form(i,link):
					print "\n\nXss in link " + link + " in form "
					print i

			if "=" in link:
				print("\nTesting link: ", link)
				if self.xss_link(link):
					print "\n\nXss in link " + link
	
	def xss_link(self,url):
		test = "<sCript>alert('helllo')</scriPt>"
		url = url.replace("=","="+test)
		response = self.session.get(url)
		return (test in response.content)			

	def xss_form(self,form,url):
		test = "<sCript>alert('helllo')</scriPt>"
		response = self.submit_form(form,test,url)
		return (test in response.content)
