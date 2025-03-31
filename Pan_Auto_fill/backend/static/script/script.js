async function uploadImage() {
    let fileInput = document.getElementById("imageInput");
    if (!fileInput.files[0]) {
        alert("Please upload an image");
        return;
    }

    let formData = new FormData();
    formData.append("image", fileInput.files[0]);

    let response = await fetch("http://127.0.0.1:5000/extract", {
        method: "POST",
        body: formData,
    });

    let data = await response.json();

    if (data.error) {
        alert("Error: " + data.error);
        return;
    }

    document.getElementById("Name").value = data.name || "";
    document.getElementById("Fathers Name").value = data.fathers_name || "";
    document.getElementById("dob").value = data.dob || "";
    document.getElementById("pan number").value = data.pan_number || "";
}
