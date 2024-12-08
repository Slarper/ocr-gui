document.getElementById('imageUpload').addEventListener('change', async function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        const read_image = () => {
            return new Promise(res => {
                reader.onload = async function (e) {
                    res(e);
                };
            })
        }

        let e = await read_image();
        document.getElementById('preview').style.display = 'block';
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('svg').style.display = 'none';

    }
});

ocrImage = async (base64Image) => {
    // console.log(base64Image);

    // get string from id: ocr_language, which is a input node
    let lang = document.getElementById('ocr_language').value;
    // 
    if (!lang) {
        lang = 'ch'
    }
    console.log(lang);
    let lang_set = ['ch', 'en', 'korean', 'japan', 'chinese_cht', 'ta', 'te', 'ka', 'latin', 'arabic', 'cyrillic', 'devanagari'];
    if (!lang_set.includes(lang)) {
        alert('Please select a valid language.');
        return;
    }

    const response = await fetch('/ocr/full', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image: base64Image,
            lang: lang
        }),
    });
    const data = await response.json();
    console.log(data);

    const l = data.l;
    // if l is empty [], alert no text found
    if (l.length == 0) {
        alert('No text found in the image.');
        return
    }
    const l1 = l[0];
    console.log(l1.x);
    console.log(l1.y);
    console.log(l1.w);
    console.log(l1.h);
    console.log(l1.text);

    // hide preview
    document.getElementById('preview').style.display = 'none';
    let svg = document.getElementById('svg');
    svg.style.display = 'block';
    // remove all children
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }



    // Create a new Image object
    const img = new Image();

    // Set the src of the image to the base64 string
    const loadImage = () => {
        return new Promise((resolve, reject) => {
            img.onload = () => resolve(img);
            img.onerror = reject; // handle errors
            img.src = base64Image;
        });
    };
    // Wait for the image to load
    const loadedImage = await loadImage();

    // Once the image is loaded, get the dimensions
    let width = loadedImage.width;
    let height = loadedImage.height;

    console.log(`Image width: ${width}, Image height: ${height}`);


    // get width and height of ImagePreview
    // const previewImage = document.getElementById('previewImage');
    // get width and height from base64Image

    const aspect_ratio = width / height;

    // re-adjust width and height
    width = 1000;
    height = width / aspect_ratio;

    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    // add this image as background
    let image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
    image.setAttribute('x', 0);
    image.setAttribute('y', 0);
    image.setAttribute('width', "100%");
    image.setAttribute('height', "100%");
    image.setAttribute('href', base64Image);
    svg.appendChild(image);

    l.forEach((l1) => {
        let x = l1.x;
        let y = l1.y;
        let w = l1.w;
        let h = l1.h;
        let text = l1.text;
        let rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x * width);
        rect.setAttribute('y', height - y * height - h * height);
        rect.setAttribute('width', w * width);
        rect.setAttribute('height', h * height);
        rect.setAttribute('fill', 'none');
        rect.setAttribute('stroke', 'red');
        rect.setAttribute('stroke-width', '2');
        svg.appendChild(rect);
        let textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textElement.setAttribute('x', x * width);
        textElement.setAttribute('y', height - y * height);
        textElement.setAttribute('font-size', 1);
        textElement.setAttribute('fill', 'transparent');
        textElement.setAttribute('dominant-baseline', `middle`)
        textElement.setAttribute('id', `ocr_text`)
        // put text inside
        textElement.innerHTML = text;

        svg.appendChild(textElement);

        // adjust text fit into box
        let bb = textElement.getBBox();
        console.log(bb);
        let widthTransform = w * width / bb.width;
        console.log(widthTransform);
        let scaling = widthTransform;
        textElement.setAttribute('font-size', scaling);

        // align text with rect horizontally
        // bb = textElement.getBBox();
        // console.log(bb);
        let middle = (height - y * height - h * height) + h * height / 2;
        let text_y = middle;
        textElement.setAttribute('y', text_y);

        textElement.addEventListener('dblclick', function () {
            const text = this.textContent;
            copyTextToClipboard(text);
        });

    })



}
function copyTextToClipboard(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    // alert("Text copied to clipboard!");
}



uploadImage2 = async () => {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image.');
        return;
    }
    // read file as image and post it into /ocr/full
    const reader = new FileReader();
    reader.readAsDataURL(file);

    const read_image = () => {
        return new Promise(res => {
            reader.onload = async function (e) {
                res(e);
            };
        })
    }

    let e = await read_image();
    const base64Image = e.target.result;
    ocrImage(base64Image);
}
// Function to read image from clipboard and convert to Base64
async function getClipboardImageAsBase64() {
    // let status = await navigator.permissions.query({ name: "clipboard-read" });
    // console.log(status)
    // Wait for clipboard data
    const clipboardItems = await navigator.clipboard.read();

    for (const item of clipboardItems) {
        console.log(item)
        for (const type of item.types) {
            console.log(type)
            if (type.startsWith('image/')) {
                // Extract the image as a Blob
                const imageBlob = await item.getType(type);

                // Convert Blob to Base64 using FileReader
                const reader = new FileReader();
                reader.readAsDataURL(imageBlob);
                const read_image = () => {
                    return new Promise(res => {
                        reader.onload = async function (e) {
                            res(e);
                        };
                    })
                }

                let e = await read_image();
                const base64Image = e.target.result;
                // console.log(base64Image);
                return base64Image;

            }
        }
    }
}



clipImage = async () => {

    const base64Image = await getClipboardImageAsBase64();
    if (!base64Image) {
        alert('No image found in clipboard.');
        return;
    }
    // console.log(base64Image);
    ocrImage(base64Image);
}

// uploadImage = async () => {
//     const fileInput = document.getElementById('imageUpload');
//     const file = fileInput.files[0];
//     if (!file) {
//         alert('Please select an image.');
//         return;
//     }
//     // read file as image and post it into /ocr/full
//     const reader = new FileReader();
//     reader.readAsDataURL(file);
//     reader.onloadend = async function (e) {
//         const base64Image = e.target.result;
//         const response = await fetch('/ocr/full', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 image: base64Image,
//             }),
//         });
//         const data = await response.json();
//         console.log(data);

//         const l = data.l;
//         const l1 = l[1];
//         console.log(l1.x);
//         console.log(l1.y);
//         console.log(l1.w);
//         console.log(l1.h);
//         console.log(l1.text);

//         // hide preview
//         document.getElementById('preview').style.display = 'none';
//         let svg = document.getElementById('svg');
//         svg.style.display = 'block';
//         // remove all children
//         while (svg.firstChild) {
//             svg.removeChild(svg.firstChild);
//         }



//         // Create a new Image object
//         const img = new Image();

//         // Set the src of the image to the base64 string
//         const loadImage = () => {
//             return new Promise((resolve, reject) => {
//                 img.onload = () => resolve(img);
//                 img.onerror = reject; // handle errors
//                 img.src = base64Image;
//             });
//         };
//         // Wait for the image to load
//         const loadedImage = await loadImage();

//         // Once the image is loaded, get the dimensions
//         let width = loadedImage.width;
//         let height = loadedImage.height;

//         console.log(`Image width: ${width}, Image height: ${height}`);


//         // get width and height of ImagePreview
//         // const previewImage = document.getElementById('previewImage');
//         // get width and height from base64Image

//         const aspect_ratio = width / height;

//         // re-adjust width and height
//         width = 1000;
//         height = width / aspect_ratio;

//         svg.setAttribute('width', width);
//         svg.setAttribute('height', height);
//         // add this image as background
//         let image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
//         image.setAttribute('x', 0);
//         image.setAttribute('y', 0);
//         image.setAttribute('width', "100%");
//         // image.setAttribute('height', "100%");
//         image.setAttribute('href', base64Image);
//         svg.appendChild(image);

//         l.forEach((l1) => {
//             let x = l1.x;
//             let y = l1.y;
//             let w = l1.w;
//             let h = l1.h;
//             let text = l1.text;
//             let rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
//             rect.setAttribute('x', x * width);
//             rect.setAttribute('y', height - y * height - h * height);
//             rect.setAttribute('width', w * width);
//             rect.setAttribute('height', h * height);
//             rect.setAttribute('fill', 'none');
//             rect.setAttribute('stroke', 'red');
//             rect.setAttribute('stroke-width', '2');
//             svg.appendChild(rect);
//             let textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
//             textElement.setAttribute('x', x * width);
//             textElement.setAttribute('y', height - y * height - 20);
//             textElement.setAttribute('font-size', 1);
//             textElement.setAttribute('fill', 'transparent');
//             // put text inside
//             textElement.innerHTML = text;

//             svg.appendChild(textElement);

//             // adjust text fit into box
//             let bb = textElement.getBBox();
//             console.log(bb);
//             let widthTransform = w * width / bb.width;
//             console.log(widthTransform);
//             // // var heightTransform = h / bb.height;
//             // // var scaling = widthTransform < heightTransform ? widthTransform : heightTransform;
//             let scaling = widthTransform;
//             textElement.setAttribute('font-size', scaling);
//             // textElement.setAttribute("transform", "matrix(" + scaling + ", 0, 0, " + scaling + ", 0,0)");
//             // svg.appendChild(textElement);
//         })


//     }
// }
