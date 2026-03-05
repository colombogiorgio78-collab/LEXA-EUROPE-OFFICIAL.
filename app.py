import streamlit as st
import fitz
import google.generativeai as genai
import streamlit.components.v1 as components

# Configurazione base
st.set_page_config(page_title="LEXA EUROPE", layout="wide")

st.title("⚖️ LEXA EUROPE: Analisi Legale AI")

# Sidebar
with st.sidebar:
    st.header("Configurazione")
    api_input = st.text_input("Inserisci Gemini API Key", type="password")
    giurisdizione = st.selectbox("Giurisdizione", ["Italia", "Unione Europea", "International"])

# Area Input
col1, col2 = st.columns(2)
testo_input = ""

with col1:
    st.subheader("Carica o Incolla")
    scelta = st.radio("Modalità:", ["Incolla Testo", "Carica PDF"])
    if scelta == "Incolla Testo":
        testo_input = st.text_area("Incolla qui il contratto:", height=300)
    else:
        file_pdf = st.file_uploader("Scegli PDF", type="pdf")
        if file_pdf:
            doc = fitz.open(stream=file_pdf.read(), filetype="pdf")
            testo_input = "".join([p.get_text() for p in doc])

# Analisi
with col2:
    st.subheader("Report LEXA")
    if st.button("🚀 AVVIA ANALISI"):
        if not api_input:
            st.error("ERRORE: Devi inserire la API Key nella barra a sinistra!")
        elif not testo_input:
            st.warning("ERRORE: Incolla del testo prima di premere il tasto.")
        else:
            try:
                # Pulizia chiave da spazi invisibili
                chiave_pulita = api_input.strip()
                genai.configure(api_key=chiave_pulita)
                
                # Prova il modello flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner("LEXA sta analizzando..."):
                    prompt = f"Sei un avvocato in {giurisdizione}. Analizza rischi IP e clausole critiche: \n\n {testo_input[:10000]}"
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.success("Analisi Completata!")
                        st.markdown(response.text)
                        
                        # Tasto Audio
                        testo_audio = response.text.replace("'", " ").replace("\n", " ")
                        codice_audio = f"""
                        <script>
                        function parla() {{
                            window.speechSynthesis.cancel();
                            var m = new SpeechSynthesisUtterance('{testo_audio[:2000]}');
                            m.lang = 'it-IT';
                            window.speechSynthesis.speak(m);
                        }}
                        </script>
                        <button onclick="parla()" style="width:100%;height:50px;background:#FFD700;border-radius:10px;font-weight:bold;cursor:pointer;border:none;">🔊 ASCOLTA REPORT</button>
                        """
                        components.html(codice_audio, height=70)
            except Exception as e:
                # Questo ci dirà l'errore vero!
                st.error(f"ERRORE TECNICO: {str(e)}")
