document.addEventListener("DOMContentLoaded", function() {
    // Modal functionality
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    var currentChannelId = null; // to store the current channel id

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('slider-item-img')) {
            modal.style.display = "block";
            modalImg.src = event.target.src;
            captionText.innerHTML = event.target.alt;
            currentChannelId = event.target.dataset.channelId; // get the channel id
        }
    });

    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() { 
        modal.style.display = "none";
    }

    // Add the "Watch | PLAY" button
    var playButton = document.createElement('div');
    playButton.id = 'playButton';
    playButton.textContent = 'مشاهدة | PLAY';
    playButton.style.cssText = 'background-color: green; color: white; text-align: center; padding: 10px;border-radius: 5px; cursor: pointer; margin-top: 10px; width: 280px; margin-left: auto; margin-right: auto;';
    document.querySelector('.image-wrapper').appendChild(playButton);

    playButton.addEventListener('click', function() {
        if (currentChannelId) {
            window.location.href = `player.html?id=${currentChannelId}`;
        }
    });
});
