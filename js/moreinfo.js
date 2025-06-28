document.addEventListener("DOMContentLoaded", function() {
    // Modal functionality
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");
    var currentChannelId = null;

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('slider-item-img')) {
            modal.style.display = "flex"; // تغيير إلى flex لتحسين العرض
            modalImg.src = event.target.src;
            modalImg.alt = event.target.alt; // للحفاظ على accessibility
            captionText.innerHTML = event.target.alt;
            currentChannelId = event.target.dataset.channelId;
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
    playButton.style.cssText = `
        position: relative;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        padding: 12px 24px;
        border-radius: 5px;
        cursor: pointer;
        margin: 20px auto;
        width: auto;
        max-width: 280px;
        font-weight: bold;
        transition: background-color 0.3s;
    `;
    
    playButton.addEventListener('mouseenter', function() {
        this.style.backgroundColor = '#45a049';
    });
    
    playButton.addEventListener('mouseleave', function() {
        this.style.backgroundColor = '#4CAF50';
    });

    document.querySelector('.image-wrapper').appendChild(playButton);

    playButton.addEventListener('click', function() {
        if (currentChannelId) {
            window.location.href = `player.html?id=${currentChannelId}`;
        }
    });

    // إغلاق المودال عند النقر خارج الصورة
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});