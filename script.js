document.getElementById('findButton').addEventListener('click', function() {
    const field1Value = document.getElementById('field1').value;
    const field2Value = document.getElementById('field2').value;

    const data = {
        field1: field1Value,
        field2: field2Value
    };

    fetch('https://freebooks-b7fl.onrender.com/pirate-book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // You can handle the server response here, like showing a message to the user
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
