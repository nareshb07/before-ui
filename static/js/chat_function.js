const messageInput = document.getElementById('message_input');
const submitButton = document.getElementById('chat-message-submit');



    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            console.log("entered ")
            event.preventDefault(); // Prevent the default form submission

            // Trigger the submit button click event
            submitButton.click();
        }
    });


