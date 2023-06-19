const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let timeoutId;

searchInput.addEventListener('input', function() {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        const searchTerm = searchInput.value;
        if (searchTerm.trim() !== '') {
            fetchSearchResults(searchTerm);
        } else {
            searchResults.innerHTML = '';
        }
    }, 500);
});

function fetchSearchResults(searchTerm) {
    const url = '/search/?search=' + encodeURIComponent(searchTerm);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let searchResultsHTML = '';
            if (data.length > 0) {
                
                data.forEach(result => {
                    const imageUrl = result.image_url;
                    
                    searchResultsHTML += ` 
                                        <div class="py-2 shadow-lg rounded-2xl mt-4">
                                            <a href = "/Creator_profile/${result.id}"> 
                                                <div class="flex  items-start justify-center">
                                                    <div class="flex flex-row items-center">
                                                        <div class = ""><img src = "${imageUrl}" class="h-16 w-16 border-4  rounded-full" /></div>
                                                            <div class="ml-5">
                                                                <h1 class = "text-xl font-bold ">${result.first_name} ${result.last_name}</h1>
                                                                <p class = "-mt-1 text-md text-gray-600 ">@${result.username}</p>
                                                                ${result.profession ? `<h1 class="text-xl font-semibold -mt-1">${result.profession}</h1>` : ''}
                                                            </div>
                                                        </div>
                                                    </div>
                                                 </a>
                                            </div>`;
                                          });
                                  searchResultsHTML += '</ul>';
                                   } else {
                                  searchResultsHTML = '<p>No users found.</p>';
                                  }

                                   searchResults.innerHTML = searchResultsHTML;
                                  })
                                    .catch(error => {
                                  console.error('Error:', error);
                                      });
                                 }

