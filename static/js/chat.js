const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/' + id + '/'
);

socket.onopen = function() {
    console.log("CONNECTION ESTABLISHED");
};

socket.onclose = function() {
    console.log("CONNECTION LOST");
};

socket.onerror = function() {
    console.log("ERROR OCCURRED");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.file_url) {
        const isSender = data.username === message_username;
        const align = isSender ? 'float-right' : 'float-left';
        let content;

        if (data.file_name.toLowerCase().match(/\.(jpg|jpeg|png)$/i)) {
            content = `<img src="${data.file_url}" alt="Image" class="w-36 h-36" />`;
        } else if (data.file_name.toLowerCase().match(/\.(mp4|avi|mov)$/i)) {
            content = `<video class="h-40 w-36" controls>
                          <source src="${data.file_url}" type="${data.content_type}">
                          Your browser does not support the video tag.
                      </video>`;
        } else if (data.file_name.toLowerCase().match(/\.(pdf|doc|docx)$/i)) {
            content = `<a href="${data.file_url}" target="_blank">${data.file_name}</a>`;
        } else {
            content = `<a href="${data.file_url}" download>${data.file_name}</a>`;
        }

        const chatBody = document.querySelector('#chat-body');
        const messageClass = isSender ? 'bg-success' : 'bg-primary';
        const messageFloat = isSender ? 'float-right' : 'float-left';
        const messageHTML = `<tr>
                                <td>
                                    <div class="${messageClass} p-2 mt-2 mr-5 shadow-sm text-white ${messageFloat} rounded">
                                        ${content}
                                    </div>
                                </td>
                            </tr>`;
        
        chatBody.innerHTML += messageHTML;
    } else {
        const chatBody = document.querySelector('#chat-body');
        const messageClass = (data.username === message_username) ? 'bg-success' : 'bg-primary';
        const messageFloat = (data.username === message_username) ? 'float-right' : 'float-left';
        const messageHTML = `<tr>
                                <td>
                                    <p class="${messageClass} p-2 mt-2 mr-5 shadow-sm text-white ${messageFloat} rounded">
                                        ${data.message}
                                    </p>
                                </td>
                            </tr>`;
        
        chatBody.innerHTML += messageHTML;
    }
};

document.querySelector('#chat-message-submit').onclick = function() {
  const messageInput = document.querySelector('#message_input');
  const message = messageInput.value;

  // Check if message input is not empty
  if (message.trim() !== '') {
      socket.send(JSON.stringify({
          'message': message,
          'username': message_username,
          'receiver': receiver
      }));

      messageInput.value = '';
  }
};
document.querySelector('#file-upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.querySelector('#fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('fileInput', file);

        fetch(`/chat/${id}/`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                socket.send(JSON.stringify({
                    'file_url': data.file_url,
                    'file_name': data.file_name,
                    'username': message_username,
                    'receiver': receiver,
                   
                }));
                fileInput.value = '';
                console.log("File uploaded successfully:", data.file_url);
            } else {
                fileInput.value = '';
                console.log("File upload failed:", data.message);
            }
        })
        .catch(error => {
            console.log("An error occurred during file upload:", error);
        });
    }
});
