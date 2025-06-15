const video = document.getElementById("video");
const detectBtn = document.getElementById("detect-btn");
const emotionResult = document.getElementById("emotion-result");
const songsContainer = document.getElementById("songs");

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alert("Camera access denied or unavailable.");
    console.error(err);
  });

detectBtn.onclick = async () => {
  emotionResult.innerText = "Detecting emotion...";
  songsContainer.innerHTML = "";

  // Capture image from webcam
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth || 320;
  canvas.height = video.videoHeight || 240;
  canvas.getContext("2d").drawImage(video, 0, 0);

  const imageData = canvas.toDataURL("image/jpeg");

  const response = await fetch('/detect', {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ image: imageData })
  });

  const data = await response.json();

  if (data.error) {
    emotionResult.innerText = "Error: " + data.error;
    return;
  }

  emotionResult.innerText = `Detected Emotion: ${data.emotion}`;

  data.tracks.forEach(track => {
    const card = document.createElement("div");
    card.className = "song-card";
    card.innerHTML = `
      <img src="${track.image}" alt="album cover">
      <strong>${track.name}</strong><br>
      <small>${track.artist}</small><br>
      ${track.preview_url
        ? `<audio controls src="${track.preview_url}"></audio>`
        : `<p><em>No preview available</em></p>`}
      <a href="${track.external_url}" target="_blank">Open in Spotify</a>
    `;
    songsContainer.appendChild(card);
  });
};
