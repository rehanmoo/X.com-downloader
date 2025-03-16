// Track processed videos to avoid duplicates
const processedVideos = new Set();

// Function to check for videos
function checkForVideos() {
  const videos = document.querySelectorAll('video');
  
  videos.forEach(video => {
    // Get the tweet URL
    const tweetElement = video.closest('article');
    if (!tweetElement) return;
    
    // Find the time element which contains the link to the tweet
    const timeElement = tweetElement.querySelector('time');
    if (!timeElement || !timeElement.parentElement || !timeElement.parentElement.href) return;
    
    const tweetUrl = timeElement.parentElement.href;
    
    // Check if we've already processed this video
    if (processedVideos.has(tweetUrl)) return;
    
    // Add event listener for when the video starts playing
    video.addEventListener('play', () => {
      if (processedVideos.has(tweetUrl)) return;
      
      // Mark as processed
      processedVideos.add(tweetUrl);
      
      // Send to our backend server
      fetch('http://localhost:8765', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: tweetUrl }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }, { once: true });
  });
}

// Run initially and set up a mutation observer to detect new videos
checkForVideos();

// Create a mutation observer to watch for new videos being added to the DOM
const observer = new MutationObserver((mutations) => {
  checkForVideos();
});

// Start observing the document
observer.observe(document.body, {
  childList: true,
  subtree: true
});
