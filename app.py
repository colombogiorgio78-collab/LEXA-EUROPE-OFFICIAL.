import streamlit as st
import fitz
from groq import Groq
import streamlit.components.v1 as components

# Configurazione Pagina
st.set_page_config(page_title="LEXA EUROPE - Groq Edition", layout="wide")

st.title("⚖️ LEXA EUROPE: Intelligenza Legale (Llama 3)")

# Sidebar
with st.sidebar:
    st.header("Configurazione")
    api_input = st.text_input("Inserisci GROQ API Key (gsk_...)", type="password")
    giurisdizione = st.selectbox("Giurisdizione", ["Italia", "Unione Europea", "International"])
    st.info("Prendi la chiave gratis su: console.groq.com")

# Area Input
col1, col2 = st.columns(2)
testo_input = ""

with col1:
    st.subheader("📂 Input Contratto")
    scelta = st.radio("Modalità:", ["Incolla Testo", "Carica PDF"])
    if scelta == "Incolla Testo":
        testo_input = st.text_area("Incolla qui il contratto o la clausola...", height=350)
    else:
        file_pdf = st.file_uploader("Scegli un file PDF", type="pdf")
        if file_pdf:
            doc = fitz.open(stream=file_pdf.read(), filetype="pdf")
            testo_input = "".join([p.get_text() for p in doc])

# Analisi con Groq
with col2:
    st.subheader("📊 Report LEXA")
    if st.button("🚀 AVVIA ANALISI PROFESSIONALE"):
        if not api_input:
            st.error("Inserisci la chiave API di Groq nella barra laterale!")
        elif not testo_input:
            st.warning("Incolla del testo o carica un PDF.")
        else:
            try:
                # Inizializza Groq
                client = Groq(api_key=api_input.strip())
                
                with st.spinner("LEXA (Llama 3) sta analizzando..."):
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": f"Sei LEXA, un avvocato esperto in diritto di {giurisdizione}. Analizza il contratto per rischi IP, recesso e penali. Sii schematico e professionale."
                            },
                            {
                                "role": "user",
                                "content": testo_input[:20000],
                            }
                        ],
                        model="llama3-8b-8192", # Il modello super veloce
                    )
                    
                    risposta = chat_completion.choices[0].message.content
                    st.success("Analisi completata!")
                    st.markdown(risposta)
                    
                    # Funzione Audio
                    testo_audio = risposta.replace("'", " ").replace("\n", " ").replace("`", "")
                    tts = f"""<script>function speak() {{ window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{testo_audio[:3000]}'); m.lang = 'it-IT'; window.speechSynthesis.speak(m); }}</script>
                    <button onclick="speak()" style="width:100%;height:50px;background:#FFD700;border-radius:10px;font-weight:bold;cursor:pointer;border:none;">🔊 ASCOLTA REPORT</button>"""
                    components.html(tts, height=70)

            except Exception as e:
                st.error(f"ERRORE TECNICO: {str(e)}")

st.divider()
st.caption("LEXA Europe v3.0 - Powered by Groq & Llama 3")
