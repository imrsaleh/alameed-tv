document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const channelId = urlParams.get('id');
    
    if (channelId) {
        // Fetch channel details from the API with the specific id
        fetch(`https://api.zxx3111.workers.dev/?id=${channelId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === "success" && data.data) {
                    const channel = data.data;
                    if (channel.type === 'mpd') {
                        jwplayer("player").setup({
                            autostart: true,
                            type: "mpd",
                            width: "100%",
                            file: channel.file,
                            drm: { clearkey: { keyId: channel.keyId, key: channel.key } },
                            logo: {
                                file: "JWplayer/logo.png",
                                hide: false,
                                position: "bottom-left"
                            },
                        });
                    } else if (channel.type === 'hls') {
                        jwplayer("player").setup({
                            autostart: true,
                            type: "hls",
                            width: "100%",
                            logo: {
                                file: "JWplayer/logo.png",
                                hide: false,
                                position: "bottom-left"
                            },
                            file: channel.file,
                        });
                    }
                } else {
                    console.error('Channel not found');
                }
            })
            .catch(error => console.error('Error fetching channel details:', error));
    } else {
        console.error('Channel ID not provided');
    }
});

