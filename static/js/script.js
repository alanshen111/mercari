let previousListings = [];
const notificationSound = new Audio(notificationSoundUrl);
notificationSound.volume = 0.5;
let soundEnabled = false;

function monitorListings(query) {
    document.getElementById('search-btn').disabled = true;
    document.getElementById("loading-spinner").style.display = "inline";
    fetchListings(query);
    setInterval(() => fetchListings(query), 60000);
}

function fetchListings(query) {
    console.log('Fetching listings for query:', query);
    fetch(`/get_listings?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const listingsContainer = document.getElementById('listings');
            const newListings = data.filter(item => !previousListings.some(prevItem => prevItem.link === item.link));
            previousListings = [...newListings, ...previousListings]; 

            if (newListings.length === 0) {
                console.log('No new listings found for search query: ', query);
                return;
            }

            newListings.forEach(item => {
                // Render the listing using the listing.html template
                fetchListingTemplate(item).then(listingHtml => {
                    const listingDiv = document.createElement('div');
                    listingDiv.innerHTML = listingHtml;
                    listingsContainer.prepend(listingDiv);  // Add new items to the top
                });
                console.log('New listing found:', item.link);
            });

            if (soundEnabled) {
                notificationSound.play();
            }
        })
        .catch(error => console.error('Error fetching listings:', error));
}

function fetchListingTemplate(item) {
    return fetch(`/render_listing?item=${encodeURIComponent(JSON.stringify(item))}`)
        .then(response => response.text());
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    const button = document.getElementById('enable-sound-btn');
    button.textContent = soundEnabled ? "Disable Sound 🔇" : "Enable Sound 🔊";
    if (soundEnabled) {
        console.log('Sound enabled');
        notificationSound.play().catch(error => console.log("Autoplay blocked:", error));
    } else {
        console.log('Sound disabled');
    }
}