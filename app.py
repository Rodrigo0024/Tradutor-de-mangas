import base64
import os
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
import requests
import streamlit as st
from streamlit_paste_button import paste_image_button

# Carrega a chave do arquivo .env
load_dotenv()

st.set_page_config(
    page_title="Tradutor Contextual & Cultural",
    page_icon="🎌",
    layout="wide"
)

INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-large-4-1t-a52b"


def encode_pil_image_to_base64(image: Image.Image) -> str:
    """Converte um objeto PIL.Image (vindo de upload ou Ctrl+V) para Data URL base64."""
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGBA")
        fmt = "PNG"
        mime = "image/png"
    else:
        image = image.convert("RGB")
        fmt = "JPEG"
        mime = "image/jpeg"

    buffer = BytesIO()
    image.save(buffer, format=fmt)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def build_prompt(media_type: str, style: str, extra_context: str) -> str:
    reading_order = {
        "Mangá (Japonês - Direita para Esquerda)": (
            "Siga rigorosamente a ordem de leitura tradicional japonesa: "
            "de cima para baixo e da DIREITA para a ESQUERDA."
        ),
        "HQ / Comic (Ocidental - Esquerda para Direita)": (
            "Siga a ordem de leitura ocidental: de cima para baixo e da ESQUERDA para a DIREITA."
        ),
        "Jogo Retrô (Caixa de Diálogo / Menu)": (
            "Identifique caixas de diálogo, nomes de personagens, menus ou itens na tela do jogo."
        ),
    }[media_type]

    style_instruction = {
        "Adaptação Natural (Localização)": (
            "Faça uma localização fluida para o português brasileiro natural, adaptando gírias, "
            "expressões idiomáticas e o tom de voz à expressão facial e emoção dos personagens na cena."
        ),
        "Fiel ao Original + Notas Culturais": (
            "Mantenha a tradução mais próxima do texto original, preservando honoríficos (-san, -kun, -sama) "
            "se houver, e adicione notas explicando trocadilhos, referências culturais ou termos específicos."
        ),
        "Modo Estudo (Original -> Tradução -> Vocabulário)": (
            "Para cada fala, mostre: 1) O texto original transcrito; 2) A tradução para o português; "
            "3) Explicação de expressões-chave ou gírias usadas na frase."
        ),
    }[style]

    context_note = f"\nContexto adicional fornecido pelo usuário: {extra_context}" if extra_context.strip() else ""

    return f"""Você é um tradutor e localizador especialista em cultura pop, mangás, quadrinhos e jogos clássicos.

Analise a imagem enviada levando em conta não apenas o texto, mas também o **contexto visual** (expressões faciais, postura, clima da cena, interface do jogo).

**Regras de Leitura:**
{reading_order}

**Estilo de Tradução:**
{style_instruction}
{context_note}

**Formato de Resposta:**
1. **Contexto da Cena:** (1 ou 2 linhas resumindo o clima/emoção que você observou na imagem).
2. **Diálogos Traduzidos (em ordem):**
   - **[Personagem ou Posição na tela]:** "Tradução aqui" *(breve nota sobre o tom, ex: irônico, gritando, sussurrando)*
3. **Notas Culturais / Adaptação:** (Explique gírias, referências ou escolhas de tradução relevantes, se houver)."""


def translate_image(data_url: str, prompt_text: str) -> str:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("A variável NVIDIA_API_KEY não foi encontrada no arquivo .env.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        "max_tokens": 4096,
        "stream": False,
        "temperature": 0.4,
        "top_p": 1,
        "reasoning_effort": "medium",
    }

    response = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=180)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


# --- INTERFACE ---
st.title("🎌 Tradutor Cultural & Contextual")
st.caption("Recorte o mangá ou jogo de qualquer aba e cole aqui para traduzir com contexto visual.")

with st.sidebar:
    st.header("⚙️ Configurações")
    media_type = st.selectbox(
        "Tipo de Mídia",
        [
            "Mangá (Japonês - Direita para Esquerda)",
            "Jogo Retrô (Caixa de Diálogo / Menu)",
            "HQ / Comic (Ocidental - Esquerda para Direita)",
        ],
    )

    style = st.selectbox(
        "Estilo da Tradução",
        [
            "Adaptação Natural (Localização)",
            "Fiel ao Original + Notas Culturais",
            "Modo Estudo (Original -> Tradução -> Vocabulário)",
        ],
    )

    extra_context = st.text_area(
        "Contexto Extra (Opcional)",
        placeholder="Ex: Esse personagem é um samurai arrogante falando com um plebeu / Jogo de RPG de PS1.",
        height=100,
    )

# --- ENTRADA DE IMAGEM (COLAR OU UPLOAD) ---
tab_paste, tab_upload = st.tabs(["📋 Colar Recorte (Área de Transferência)", "📁 Enviar Arquivo"])

active_image = None

with tab_paste:
    st.info("💡 **Dica:** Na aba do mangá ou emulador, aperte **`Win + Shift + S`**, selecione apenas os balões/cena que deseja traduzir e clique no botão abaixo.")
    paste_result = paste_image_button(
        label="📋 Colar Imagem Recortada",
        background_color="#FF4B4B",
        hover_background_color="#FF2B2B",
        errors="ignore",
    )
    if paste_result.image_data is not None:
        active_image = paste_result.image_data

with tab_upload:
    uploaded_file = st.file_uploader(
        "Ou selecione uma imagem salva no computador",
        type=["png", "jpg", "jpeg", "webp"],
    )
    if uploaded_file is not None:
        active_image = Image.open(uploaded_file)

# --- EXIBIÇÃO E TRADUÇÃO ---
if active_image is not None:
    st.divider()
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🖼️ Cena Capturada")
        st.image(active_image, use_container_width=True)

    with col2:
        st.subheader("💬 Tradução Contextualizada")
        if st.button("✨ Traduzir Cena", type="primary", use_container_width=True):
            with st.status("Processando a imagem...", expanded=True) as status:
                st.write("🔍 Codificando recorte em Base64...")
                try:
                    data_url = encode_pil_image_to_base64(active_image)
                    st.write("📝 Preparando prompt cultural e regras de leitura...")
                    prompt = build_prompt(media_type, style, extra_context)

                    st.write("🤖 Enviando para a API da NVIDIA (Mistral Large) e aguardando resposta...")
                    status.update(label="A IA está analisando a imagem e traduzindo...", state="running")

                    translation = translate_image(data_url, prompt)

                    status.update(label="Tradução concluída com sucesso!", state="complete", expanded=False)
                    st.markdown(translation)

                except requests.exceptions.HTTPError as e:
                    status.update(label="Erro na API!", state="error")
                    st.error(f"Erro na API da NVIDIA: {e.response.status_code} - {e.response.text}")
                except Exception as e:
                    status.update(label="Erro no processamento!", state="error")
                    st.error(f"Erro ao processar: {str(e)}")