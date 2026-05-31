document
    .getElementById("askButton")
    .addEventListener("click", async function () {

        const question = document.getElementById("questionInput").value;

        const answerBox = document.getElementById("answerBox");

        answerBox.innerHTML = "Generating answer...";

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/qa/ask/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );

            const data = await response.json();

            answerBox.innerHTML = data.answer;

        } catch (error) {

            answerBox.innerHTML = "An error occurred.";

            console.error(error);
        }

    });



document
    .getElementById("uploadButton")
    .addEventListener("click", async function () {

        const title = document.getElementById("titleInput").value;
        const file = document.getElementById("fileInput").files[0];
        const status = document.getElementById("uploadStatus");

        if (!title || !file) {
            status.innerHTML = "Please provide title and file.";
            return;
        }

        const formData = new FormData();

        formData.append("title", title);
        formData.append("file", file);

        status.innerHTML = "Uploading...";

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/documents/upload/",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            status.innerHTML = "Upload successful ✔";

            console.log(data);

        } catch (error) {

            status.innerHTML = "Upload failed ❌";

            console.error(error);
        }

    });