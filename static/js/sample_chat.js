const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);


function uploadFile(id) {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];

  // Create a new FormData instance
  const formData = new FormData();
  formData.append('file', file);


  // Send the file to the backend for saving
  
  fetch(`/upload/${id}` , {
    method: 'POST',
    body: formData,
    
  })
  
    .then(response => response.json())
    .then(data => {
      // Use the file URL returned by the server
      const fileUrl = data.file_url;
      console.log("these file",fileUrl)
      console.log("starting to send")

      // Send the file URL to the chat consumer via WebSocket
      // Replace 'your_room_name' with the actual room name


      
      const message = {
        type: 'file_url',
        file_url: fileUrl,
      };
      console.log(file_url)
      const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/'
        + id
        + '/'
    );
    
      socket.addEventListener('open', () => {
        socket.send(JSON.stringify(message));
      });
    })
    
    .catch(error => {
      console.error('Error uploading file:', error);
      console.error('Error details:', error.message);
    });
}




const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function(e){
    
    console.log("CONNECTION ESTABLISHED");
    
}

socket.onmessage = function(e){
    console.log("message_sent")

}
socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }else{
        document.querySelector('#chat-body').innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver
        
    }));

    message_input.value = '';
}


