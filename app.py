from dotenv import load_dotenv
import os
import google.generativeai as genai

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a chave de API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuração do modelo (você pode ajustar conforme necessário)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Inicializar o modelo com a configuração
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Nome do modelo
    generation_config=generation_config,
)

response = model.generate_content(
    "Olá! Eu consigo te mandar arquivos por aqui? estou utilizando a api gemini-1.5-flash"
)
resposta = response.text

print(resposta)
