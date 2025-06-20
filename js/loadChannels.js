document.addEventListener("DOMContentLoaded", function() {
    const mainContainer = document.querySelector('.cannels.main');
    if (!mainContainer) {
        console.error('Main container not found');
        return;
    }

    fetch('https://alameed-api.alameedtv.workers.dev/') // Ensure the correct endpoint is used
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data || !data.data) {
                throw new Error('Invalid data format');
            }
            const groupedChannels = groupBy(data.data, 'group');
            createSliders(groupedChannels, mainContainer);
            initializeSliders();
        })
        .catch(error => console.error('Error fetching channels:', error));
});

function groupBy(array, key) {
    return array.reduce((result, currentValue) => {
        (result[currentValue[key]] = result[currentValue[key]] || []).push(currentValue);
        return result;
    }, {});
}

function createSliders(groupedChannels, mainContainer) {
    for (const group in groupedChannels) {
        if (groupedChannels.hasOwnProperty(group)) {
            const sectionTitle = document.createElement('div');
            sectionTitle.className = 'section-title';
            sectionTitle.textContent = group;
            mainContainer.appendChild(sectionTitle);

            const slider = document.createElement('div');
            slider.className = 'slider';

            groupedChannels[group].forEach(channel => {
                const sliderItem = document.createElement('div');
                sliderItem.className = 'slider-item';

                // Create wrapper for image and caption
                const imageWrapper = document.createElement('div');
                imageWrapper.className = 'image-caption-wrapper';

                const img = document.createElement('img');
                img.src = channel.logo;
                img.alt = channel.name;
                img.className = 'slider-item-img';
                img.dataset.channelId = channel.id;

                // Create caption
                const caption = document.createElement('div');
                caption.className = 'channel-caption';
                caption.textContent = channel.name;

                // Add image and caption to wrapper
                imageWrapper.appendChild(img);
                imageWrapper.appendChild(caption);
                sliderItem.appendChild(imageWrapper);

                slider.appendChild(sliderItem);
            });

            mainContainer.appendChild(slider);
        }
    }
    // إخفاء شاشة الانتظار بعد الانتهاء من إنشاء السلايدرز
    document.body.classList.add('loaded');

}
