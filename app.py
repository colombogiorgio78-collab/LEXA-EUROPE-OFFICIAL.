 import streamlit as st
import fitz
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="LEXA EUROPE AI", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1E3A8A; color: white; font-weight: bold; }
    .report-card { padding: 20px; border-radius: 12px; background-color: white; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚖️ LEXA PANEL")
    api_key = st.text_input("Inserisci Gemini API Key", type="password")
    jurisdiction = st.selectbox("Seleziona Giurisdizione", ["Italia", "Unione Europea", "International"])

st.title("⚖️ LEXA EUROPE: Intelligenza Legale")
col_in, col_out = st.columns([1, 1], gap="large")

testo_da_analizzare = ""

with col_in:
    st.subheader("📂 Input Documento")
    tab1, tab2 = st.tabs(["📄 PDF", "✍️ Testo"])
    with tab1:
        file = st.file_uploader("Upload Contratto", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            testo_da_analizzare = "".join([p.get_text() for p in doc])
    with tab2:
        testo_manuale = st.text_area("Incolla clausole qui...", height=350)
        if testo_manuale:
            testo_da_analizzare = testo_manuale

with col_out:
    st.subheader("📊 Report LEXA")
    if st.button("🚀 AVVIA ANALISI PROFESSIONALE"):
        if not api_key or not testo_da_analizzare:
            st.error("Inserisci la chiave API e il testo!")
        else:
            # .strip() elimina spazi invisibili prima o dopo la chiave
            clean_key = api_key.strip()
            try:
                genai.configure(api_key=clean_key)
                modelli = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                res_text = ""
                errore_reale = ""
                
                for m in modelli:
                    try:
                        model = genai.GenerativeModel(m)
                        prompt = f"Sei un avvocato esperto in {jurisdiction}. Analizza questo contratto per rischi IP e clausole critiche: \n\n {testo_da_analizzare}"
                        response = model.generate_content(prompt)
                        res_text = response.text
                        break
                    except Exception as e:
                        errore_reale = str(e)
                        continue
                
                if res_text:
                    st.markdown(f"<div class='report-card'>{res_text}</div>", unsafe_allow_html=True)
                    clean_text = res_text.replace("'", " ").replace("\n", " ").replace("`", "")
                    tts = f"""<script>function speak() {{ window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance(); m.text='{clean_text[:3000]}'; m.lang='it-IT'; window.speechSynthesis.speak(m); }}</script>
                    <button onclick="speak()" style="width:100%;height:50px;background:#FFD700;border-radius:10px;font-weight:bold;cursor:pointer;border:none;">🔊 ASCOLTA L'ANALISI</button>"""
                    components.html(tts, height=70)
                else:
                    # MOSTRA L'ERRORE VERO DI GOOGLE
                    st.error(f"ERRORE DI GOOGLE: {errore_reale}")
            except Exception as e:
                st.error(f"Errore Generale: {e}")
