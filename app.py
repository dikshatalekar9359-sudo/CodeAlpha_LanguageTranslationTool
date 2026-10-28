
import streamlit as st
import requests
import html
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)

LANGUAGES = {
    "English": "en",
    "Marathi": "mr",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Urdu": "ur"
}

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e8f0ff, #f5eaff);
}
.title {
    text-align: center;
    color: #273c85;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 25px;
}
.stButton button {
    border-radius: 10px;
    font-weight: bold;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🌍 Language Translation Tool</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Translate your text into different languages!</div>',
    unsafe_allow_html=True
)

st.subheader("Enter Your Text")

source = st.selectbox(
    "Select Source Language",
    list(LANGUAGES.keys()),
    index=0
)

target = st.selectbox(
    "Select Target Language",
    list(LANGUAGES.keys()),
    index=1
)

text = st.text_area(
    "Enter text here",
    placeholder="Example: Hello, how are you?",
    height=140,
    max_chars=1000
)

if st.button("🌐 Translate Text", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text first.")

    elif source == target:
        st.warning("Please select two different languages.")

    else:
        try:
            with st.spinner("Translating... Please wait"):
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text,
                        "langpair":
                            f"{LANGUAGES[source]}|{LANGUAGES[target]}"
                    },
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

                if data.get("responseStatus") != 200:
                    st.error(
                        "Translation failed. Please try again later."
                    )
                else:
                    result = html.unescape(
                        data["responseData"]["translatedText"]
                    )
                    st.session_state["result"] = result
                    st.session_state["source"] = source
                    st.session_state["target"] = target

        except requests.exceptions.RequestException:
            st.error(
                "Internet connection or translation service error. "
                "Please try again."
            )
        except (ValueError, KeyError, TypeError):
            st.error("Unexpected response. Please try again.")

if "result" in st.session_state:
    result = st.session_state["result"]

    st.divider()
    st.subheader("✅ Translated Result")
    st.caption(
        f"{st.session_state['source']} → "
        f"{st.session_state['target']}"
    )

    st.text_area(
        "Your translated text",
        value=result,
        height=140
    )

    st.code(result, language=None)

    if st.button("📋 Copy Translation"):
        components.html(
            f"""
            <button id="copyBtn"
            style="padding:10px 18px; cursor:pointer;">
            Copy translated text
            </button>
            <script>
            const textToCopy = {json.dumps(result)};
            document.getElementById("copyBtn").onclick = async () => {{
                try {{
                    await navigator.clipboard.writeText(textToCopy);
                    document.getElementById("copyBtn").innerText =
                        "Copied!";
                }} catch (e) {{
                    document.getElementById("copyBtn").innerText =
                        "Please select and copy the text manually";
                }}
            }};
            </script>
            """,
            height=55
        )

    if st.button("🔊 Speak Translation"):
        language_codes = {
            "English": "en-US",
            "Marathi": "mr-IN",
            "Hindi": "hi-IN",
            "Gujarati": "gu-IN",
            "Bengali": "bn-IN",
            "Tamil": "ta-IN",
            "Telugu": "te-IN",
            "Kannada": "kn-IN",
            "French": "fr-FR",
            "Spanish": "es-ES",
            "German": "de-DE",
            "Italian": "it-IT",
            "Japanese": "ja-JP",
            "Chinese": "zh-CN",
            "Arabic": "ar-SA",
            "Russian": "ru-RU",
            "Portuguese": "pt-PT",
            "Urdu": "ur-PK"
        }

        components.html(
            f"""
            <script>
            const message = {json.dumps(result)};
            const utterance = new SpeechSynthesisUtterance(message);
            utterance.lang = {json.dumps(
                language_codes.get(st.session_state['target'], 'en-US')
            )};
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
            </script>
            """,
            height=0
        )

st.divider()
st.caption("CodeAlpha Internship | Task 1: Language Translation Tool")
