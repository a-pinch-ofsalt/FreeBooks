document.getElementById('findButton').addEventListener('click', function() {
    const Title = document.getElementById('book-title').value;
    const AuthorLastName = document.getElementById('book-author').value;

    const data = {
        Title: Title,
        AuthorLastName: AuthorLastName
    };

    fetch('https://freebooks-b7fl.onrender.com/pirate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Success:', data);
        // You can handle the server response here, like showing a message to the user
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});