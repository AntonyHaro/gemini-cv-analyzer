from flask import Flask, request, jsonify, render_template
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)


# Função para upload de arquivos no Gemini
def upload_to_gemini(path, mime_type=None):
    """Envia o arquivo para o Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Arquivo enviado: '{file.display_name}' como: {file.uri}")
    return file


# Função para esperar que os arquivos estejam ativos
def wait_for_files_active(files):
    """Aguarda o processamento dos arquivos enviados para o Gemini."""
    print("Aguardando processamento dos arquivos...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"O arquivo {file.name} falhou no processamento.")
    print("...todos os arquivos estão prontos.")


# Configuração do modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Página HTML para upload do PDF


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Somente arquivos PDF são suportados."}), 400

    # Salvar o arquivo localmente
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    try:
        # Enviar para o Gemini
        gemini_file = upload_to_gemini(file_path, mime_type="application/pdf")

        # Esperar que o arquivo esteja ativo
        wait_for_files_active([gemini_file])

        # Iniciar a sessão de chat com o arquivo
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        gemini_file,
                    ],
                },
            ]
        )

        # Enviar uma mensagem ao modelo
        response = chat_session.send_message(
            "Faça um resumo detalhado sobre este currículo. Devolva sua resposta no formato markdown."
        )

        return jsonify({"response": response.text})
        # aqui pode ser reaproveitado diretamente como api, não se fazendo necessário renderizar nenhum template
        # apenas será necessário conectar isso ao javascript para consumir o endpoint
        # dentro do frontend, colocar alguma biblioteca que renderize a resposta do gemini para formato markdown

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
    # em prod, o app.run deve receber o host e a porta (pesquisar como fazer isso em um servidor ubuntu)
