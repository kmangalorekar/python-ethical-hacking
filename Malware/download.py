import requests


def download(url):
    gr = requests.get(url)
    #print gr.content
    f_name  = url.split("/")[-1]
    with open(f_name, 'wb') as f:
        f.write(gr.content)


download("https://image.shutterstock.com/image-photo/white-transparent-leaf-on-mirror-600w-1029171697.jpg")
