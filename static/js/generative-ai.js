function generateWithAI(confirmButtonText = "Generate", defaultValue = "Generate a sample markdown content", contentId = "content") {
    Swal.fire({
        title: "Enter your prompt",
        input: "text",
        inputValue: defaultValue,
        inputAttributes: {
            autocapitalize: "off"
        },
        showCancelButton: true,
        confirmButtonText: confirmButtonText,
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
        backdrop: true,
        allowOutsideClick: () => !Swal.isLoading(),
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Success!",
                html: "Announcement generated.<br/>Please proof-read before publishing.",
                icon: "success"
            });

            const textarea = document.getElementById(contentId);
            textarea.value = result.value.response;
        }
    });
}