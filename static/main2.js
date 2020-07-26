//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");
var fileDrag2 = document.getElementById("file-drag2");
var fileSelect2 = document.getElementById("file-upload2");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);



function fileDragHover(e) {
    // prevent default behaviour
    e.preventDefault();
    e.stopPropagation();

    fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
    // handle file selecting
    var files = e.target.files || e.dataTransfer.files;
    fileDragHover(e);
    for (var i = 0, f;
        (f = files[i]); i++) {
        previewFile(f);
    }
}


// Add event listeners
fileDrag2.addEventListener("dragover", fileDragHover2, false);
fileDrag2.addEventListener("dragleave", fileDragHover2, false);
fileDrag2.addEventListener("drop", fileSelectHandler2, false);
fileSelect2.addEventListener("change", fileSelectHandler2, false);

function fileDragHover2(e) {
    // prevent default behaviour
    e.preventDefault();
    e.stopPropagation();
    fileDrag2.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler2(e) {
    // handle file selecting
    var files2 = e.target.files || e.dataTransfer.files;
    fileDragHover2(e);
    for (var ii = 0, f2;
        (f2 = files2[ii]); ii++) {
        previewFile2(f2);
    }
}



//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

var imagePreview2 = document.getElementById("image-preview2");
var imageDisplay2 = document.getElementById("image-display2");
var uploadCaption2 = document.getElementById("upload-caption2");
var predResult2 = document.getElementById("pred-result2");
var loader2 = document.getElementById("loader2");

//========================================================================
// Main button events
//========================================================================

function submitImage() {
    // action for the submit button
    console.log("submit");

    if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
        window.alert("Please select an image before submit.");
        return;
    }
    if (!imageDisplay2.src || !imageDisplay2.src.startsWith("data")) {
        window.alert("Please select an image before submit.");
        return;
    }
    loader2.classList.remove("hidden");
    imageDisplay2.classList.add("loading");

    // call the predict function of the backend

    predictImage(imageDisplay.src, imageDisplay2.src);
}

function clearImage() {
    // reset selected files
    fileSelect.value = "";
    document.getElementById("output").innerHTML = "";
    // remove image sources and hide them
    imagePreview.src = "";
    imageDisplay.src = "";
    predResult.innerHTML = "";

    hide(imagePreview);
    hide(imageDisplay);
    hide(loader);
    hide(predResult);
    show(uploadCaption);

    imageDisplay.classList.remove("loading");
    // reset selected files
    fileSelect2.value = "";

    // remove image sources and hide them
    imagePreview2.src = "";
    imageDisplay2.src = "";
    predResult2.innerHTML = "";

    hide(imagePreview2);
    hide(imageDisplay2);
    hide(loader2);
    hide(predResult2);
    show(uploadCaption2);
    imageDisplay2.classList.remove("loading");
}

function previewFile(file) {
    // show the preview of the image
    console.log(file.name);
    var fileName = encodeURI(file.name);

    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
        imagePreview.src = URL.createObjectURL(file);

        show(imagePreview);
        hide(uploadCaption);

        // reset
        predResult.innerHTML = "";
        imageDisplay.classList.remove("loading");

        displayImage(reader.result, "image-display");
    };
}

function previewFile2(file) {
    // show the preview of the image
    console.log(file.name);
    var fileName2 = encodeURI(file.name);

    var reader2 = new FileReader();
    reader2.readAsDataURL(file);
    reader2.onloadend = () => {
        imagePreview2.src = URL.createObjectURL(file);

        show(imagePreview2);
        hide(uploadCaption2);

        // reset
        predResult2.innerHTML = "";
        imageDisplay2.classList.remove("loading");

        displayImage(reader2.result, "image-display2");
    };
}


//========================================================================
// Helper functions
//========================================================================



function predictImage(image, image2) {
    // console.log(JSON.stringify(image));
    var formData = {
        'avatar': image,
        'avatar2': image2
    }
    fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then((response) => response.json())
        .then(resp => {
            console.log(resp)
            console.log(typeof resp)
            if (resp)
                console.log('g')
            clearImage();
            console.log("geg");
            // document.getElementById("output").innerHTML = `<img src=${resp.image_url}/>`;
            var image = new Image();
            image.src = resp;
            document.getElementById("output").appendChild(image);
        })
        .catch(err => {
            console.log("An error occured", err.message);
            window.alert("Oops! Something went wrong.");
        });
}

function displayImage(image, id) {
    // display image on given id <img> element
    let display = document.getElementById(id);
    display.src = image;
    show(display);
}


function hide(el) {
    // hide an element
    el.classList.add("hidden");
}

function show(el) {
    // show an element
    el.classList.remove("hidden");
}