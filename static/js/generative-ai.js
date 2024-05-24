function generateWithAI() {
    Swal.fire({
        title: "Enter your prompt",
        input: "text",
        inputValue: "I'm a Prof. Help me write an annoucement for Quiz 2 for module Computing Science with weightage of 30%.",
        inputAttributes: {
            autocapitalize: "off"
        },
        showCancelButton: true,
        confirmButtonText: "Generate Announcement",
        showLoaderOnConfirm: true,
        preConfirm: async (prompt) => {
            try {
                const requestBody = JSON.stringify({ prompt: prompt });
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const requestOptions = {
                    method: "POST",
                    body: requestBody,
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    }
                };
                const response = await fetch("/api/generative", requestOptions)
    
                if (!response.ok) {
                    return Swal.showValidationMessage(`${JSON.stringify(await response.json())}`);
                }
    
                return response.json();
            } catch (error) {
                Swal.showValidationMessage(`Request failed: ${error}`);
            }
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Success!",
                html: "Announcement generated.<br/>Please proof-read before publishing.",
                icon: "success"
            });

            const textarea = document.getElementById("content");
            textarea.value = result.value.response;
        }
    });
}