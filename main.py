from downloadLinkRetriever import search_libgen
from bookDownloader import download_epub
from googleDriveUploader import upload_book_to_google_drive
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/pirate-book', methods=['POST'])
def upload_epub():
    data = request.json
    book_title = data.get('title')
    book_author_last_name = data.get('authorLastName')
    status = pirateBook(book_title, book_author_last_name)
    return jsonify({"message": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

def pirateBook(title, authorLastName):
    downloadLink = search_libgen(title, authorLastName)
    if downloadLink == 504:
        return "Timed out"
    else:
        if downloadLink == None:
            return "Failed"
    filepath = download_epub(downloadLink)
    upload_book_to_google_drive(title, filepath)
    return "Success"








