async function uploadAndSummarizePDF(file) {
    if (!file) {
        alert("Nenhum arquivo selecionado.");
        return;
    }

    if (!file.name.endsWith(".pdf")) {
        alert("Somente arquivos PDF são suportados.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error(
                "Erro do servidor:",
                errorData.error || response.statusText
            );
            alert(`Erro: ${errorData.error || "Algo deu errado."}`);
            return;
        }

        const data = await response.json();
        console.log("Resposta do servidor:", data);

        // Exibir a resposta no frontend
        if (data.response) {
            // renderMarkdown(data.response);
        } else {
            console.error("Nenhuma resposta válida recebida do servidor.");
        }
    } catch (error) {
        // Capturar erros na requisição ou processamento
        console.error("Erro ao enviar o arquivo:", error);
        alert("Erro ao processar a requisição. Tente novamente mais tarde.");
    }
}

// Exemplo de função para exibir a resposta Markdown (usando uma biblioteca como marked.js)
function renderMarkdown(markdownText) {
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = marked.parse(markdownText); // Requer a biblioteca marked.js
}

// Exemplo de uso com um input file HTML
const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-button");

uploadButton.addEventListener("click", () => {
    console.log("click")
    const file = fileInput.files[0];
    uploadAndSummarizePDF(file);
});
