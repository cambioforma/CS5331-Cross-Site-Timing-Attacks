import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

def getImages(url):
    page = requests.get(url, headers=headers, verify=False)
    
    soup = BeautifulSoup(page.text, 'lxml')
    images = []
    for img in soup.findAll('img'):
        src = img.get('src')
        if 'http' not in src:
            continue
        images.append(src)
        
    return images
    print(images)

    #print(page.text)

#if __name__ == '__main__':
#    getImages("https://www.youtube.com")

