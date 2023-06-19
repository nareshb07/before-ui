function openImageCropper(event) {
    var input = event.target;
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        // Create a new image element to use with the cropper
        var img = document.createElement('img');
        img.onload = function() {
          // Open the image in the cropper popup window
          openCropper(img);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  function openCropper(image) {
    // Initialize the Cropper.js instance with the image
    var cropper = new Cropper(image, {
      aspectRatio: 1, // Set the aspect ratio for square cropping (you can change it as needed)
      viewMode: 1, // Set the cropping view mode
      autoCropArea: 0.8, // Set the initial size of the cropping area
      cropBoxResizable: false // Disable resizing the cropping area
    });
  
    // Create a popup window for the cropper
    var cropperWindow = window.open('', '_blank', 'width=800,height=600');
    cropperWindow.document.body.innerHTML = `
      <div style="padding: 20px;">
        <h2>Crop Image</h2>
        <div id="cropper-container">
          <div id="cropper-image"></div>
          <button id="apply-crop-btn">Apply</button>
        </div>
      </div>
    `;
  
    // Append the image element to the cropper container
    cropperWindow.document.getElementById('cropper-image').appendChild(image);
  
    // Handle the "Apply" button click
    cropperWindow.document.getElementById('apply-crop-btn').addEventListener('click', function() {
      // Get the cropped canvas
      var canvas = cropper.getCroppedCanvas();
  
      // Convert the canvas to a data URL
      var croppedImage = canvas.toDataURL();
  
      // Set the data URL as the source of the profile picture preview
      document.getElementById('preview').src = croppedImage;
  
      // Set the cropped image data to the hidden input field
      document.getElementById('profile-pic').value = croppedImage;
  
      // Close the cropper popup window
      cropperWindow.close();
    });
  }
  