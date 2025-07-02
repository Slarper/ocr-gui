


document.addEventListener('paste', async function (event) {
    // Check if clipboard contains image data
    const clipboardItems = event.clipboardData.items;
    for (let i = 0; i < clipboardItems.length; i++) {
        const item = clipboardItems[i];

        // Check for image MIME type
        if (item.type.indexOf('image') === 0) {
            const file = item.getAsFile();
            const reader = new FileReader();

            const read_image = () => {
                return new Promise(res => {
                    reader.onload = async function (e) {
                        res(e);
                    };
                })
            }
            reader.readAsDataURL(file);

            let e = await read_image();

            // Read the image file as a data URL
            let base64Image = e.target.result;

            // show preview
            document.getElementById('preview').style.display = 'block';
            document.getElementById('previewImage').src = base64Image;


            ocrImage(base64Image);


        }
    }
});
