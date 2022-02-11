import scanner3 as scanner

#url = 'http://10.5.5.4/mutillidae/'


url = 'http://10.5.5.4/dvwa/'
links_ignore = ["http://10.5.5.4/dvwa/logout.php"]

datadict = {"username":"admin", "password" : "password","Login":"submit"}
#response = requests.post(url,data=datadict)


v = scanner.Scanner(url,links_ignore)
response = v.session.post("http://10.5.5.4/dvwa/login.php",data=datadict)
v.crawl()


v.run_scanner()



#forms =  v.extract_forms("http://10.5.5.4/dvwa/vulnerabilities/xss_r/")
#response = v.submit_form(forms[0],"test","http://10.5.5.4/dvwa/vulnerabilities/xss_r/")

#print forms
#response = v.xss_form(forms[0],"http://10.5.5.4/dvwa/vulnerabilities/xss_r/")

#response = v.xss_link("http://10.5.5.4/dvwa/vulnerabilities/xss_r/?name=kunal")
#print (response) 
