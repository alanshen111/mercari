let previousListings = [];
const notificationSound = new Audio(notificationSoundUrl);
notificationSound.volume = 0.5;
let soundEnabled = false;

function fetchListings() {
    const searchQuery = document.getElementById('search-input').value;
    fetch(`/get_listings?search_query=${searchQuery}`)
        .then(response => response.json())
        .then(data => {
            const listingsContainer = document.getElementById('listings');
            const newListings = data.filter(item => !previousListings.some(prevItem => prevItem.link === item.link));
            previousListings = [...newListings, ...previousListings];  // Add new listings to the top

            if (newListings.length === 0) {
                console.log('No new listings found for search query: ', searchQuery);
                return;
            }

            newListings.forEach(item => {
                const listingDiv = document.createElement('div');
                listingDiv.innerHTML = `
                    <img src="${item.image}" alt="Item Image" width="100">
                    <div>${item.price}</div>
                    <a href="${item.link}" target="_blank">View Listing</a>
                `;
                listingsContainer.prepend(listingDiv);  // Add new items to the top
            });

            if (soundEnabled) {
                notificationSound.play();
            }
        })
        .catch(error => console.error('Error fetching listings:', error));
}

function enableSound() {
    soundEnabled = true;
    document.getElementById('enable-sound-btn').disabled = true;  // Disable the button after enabling sound
    console.log('Sound enabled');
    notificationSound.play();
}

window.onload = function() {
    // Fetch listings immediately on load
    fetchListings();
    // Fetch listings every 60 seconds
    setInterval(fetchListings, 60000);
};
