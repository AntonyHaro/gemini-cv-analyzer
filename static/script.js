function isLoading(loading) {
    loader.style.display = loading ? "inline-block" : "none";
}

async function uploadAndSummarizePDF(file) {
    if (!file) {
        alert("Nenhum arquivo selecionado.");
        return;
    }

    // adicionar verificação extra para documentos word ou .txt
    if (!file.name.endsWith(".pdf")) {
        alert("Somente arquivos PDF são suportados.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        isLoading(true);

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

        // Renderizar resposta no frontend
        if (data.response) {
            renderMarkdown(data.response);
        } else {
            console.error("Nenhuma resposta válida recebida do servidor.");
        }
    } catch (error) {
        console.error("Erro ao enviar o arquivo:", error);
        alert("Erro ao processar a requisição. Tente novamente mais tarde.");
    } finally {
        isLoading(false);
    }
}

function renderMarkdown(markdownText) {
    const outputDiv = document.getElementById("output");

    // Usar Showdown para converter o Markdown em HTML
    const converter = new showdown.Converter();
    const htmlOutput = converter.makeHtml(markdownText);

    outputDiv.innerHTML = htmlOutput;
}

// Configurar os eventos do formulário
const loader = document.getElementById("loader");
const fileInput = document.getElementById("file-input");
const uploadForm = document.getElementById("upload-form");

uploadForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Impedir recarregamento da página
    const file = fileInput.files[0];
    uploadAndSummarizePDF(file);
});
