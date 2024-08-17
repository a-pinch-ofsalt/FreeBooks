import requests

def downloadBook(downloadLink, desiredFilename):
    desiredFilename
    response = requests.get(downloadLink, allow_redirects=True)
    filepath = 'books/' + desiredFilename + '.epub'
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath
