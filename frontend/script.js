async function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("result");

    if (!fileInput.files.length) {
        resultBox.innerHTML = "Please select an image first.";
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    resultBox.innerHTML = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        resultBox.innerHTML = `
            <h3>Transcription:</h3>
            <p>${data.text}</p>
            <a href="${data.doc_url}" download>Download Word Document</a>
        `;
    } catch (error) {
        resultBox.innerHTML = "Error processing image.";
        console.error(error);
    }
}