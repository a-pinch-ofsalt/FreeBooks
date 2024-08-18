import requests

def download_epub(downloadLink, title):
     filepath = 'downloads/' + title + '.epub'
     response = requests.get(downloadLink, allow_redirects=True)
     with open(filepath, 'wb') as epub:
            epub.write(response.content)
     return filepath
