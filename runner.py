from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload_epub', methods=['POST'])
def upload_epub():
    pirateBook()
    return jsonify({"message": "EPUB uploaded successfully!"})

if __name__ == '__main__':
    app.run(debug=True)










def pirateBook():


    print('\n\nCheck your browser to allow FreeBooks to upload books to Google Drive.\n\n'.upper())

    from link_retriever import search_libgen
    from googledrive_uploader import uploadBookToGoogleDrive
    from file_downloader import downloadBook

    print('\nGoogle account authentication successful!\n')
    bookTitle = input("What's the title of the book you want to read?\n").title()
    bookAuthor = input("\nWhat's the author's last name? (If there is more than one author, pick only one.)\n")
    print('\n\nSearching...\n\n')

    downloadLink = search_libgen(bookTitle, bookAuthor)

    if downloadLink == None:
        print("Sorry! We couldn't find the book. \
                \n Make sure you spelled the title and author's name correctly. \
                \n If that doesn't work, try to find it yourself at https://libgen.li!")
    else:
        print(f'Downloading {bookTitle}...')

        bookFilepath = downloadBook(downloadLink, bookTitle)

        print(f'{bookTitle} was successfully downloaded!\nUploading {bookTitle} to your Google Drive...')

        uploadBookToGoogleDrive(bookTitle=bookTitle, bookFilepath=bookFilepath)

        print(f'{bookTitle} was successfully uploaded to your google drive! \
                \nHow to access: \
                \n1. Sign in at https://play.google.com/books. \
                \n2. Press \'Upload files\'. \
                \n3. Press \'Google Drive\'. \
                \n4. In the search bar, type your desired book.\
                \n5. Double press the book and wait for it to process.')