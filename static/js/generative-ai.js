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
                html: "Content generated.<br/>Please proof-read before publishing.",
                icon: "success"
            });

            const textarea = document.getElementById(contentId);
            textarea.value = result.value.response;
        }
    });
}

function generateTLDR(type, id) {
    const url = `/api/generate_tldr?type=${type}&id=${id}`;
    
    Swal.fire({
        title: 'Loading...',
        text: 'Please wait while we generate the TL;DR',
        icon: 'info',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'TL;DR',
                    html: data.tldr,
                    icon: 'info',
                    confirmButtonText: 'Got it!'
                });
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Failed to generate TL;DR',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            Swal.fire({
                title: 'Error',
                text: 'There was a problem with the request',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        });
}