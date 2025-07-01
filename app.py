import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cross-Impact-Matrix", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("cross_impact_data_final.csv")

try:
    if "data" not in st.session_state:
        st.session_state.data = load_data()
        st.session_state.page = 0

    data = st.session_state.data
    x_factors = []

    if not x_factors:
        st.error("❌ Keine gültigen X-Faktoren gefunden.")
        st.stop()

    # Seite resetten, falls zu hoch
    if st.session_state.page >= len(x_factors):
        st.session_state.page = 0

    current_x = x_factors[st.session_state.page]
    page_data = data[data["X_Faktor"] == current_x].reset_index(drop=True)

    st.title("Cross-Impact-Matrix – Modellprojekte")

    # 📋 Erklärung oben
    with st.expander("ℹ️ Hinweis zur Bewertung", expanded=True):
        st.markdown("""
        Für jede Kombination:  
        **Wie stark beeinflusst die Veränderung des Faktors (links)**  
        **die Veränderung des Ziels (oben)?**

        **Wähle einen Wert:**
        - `0` = kein Einfluss  
        - `1` = geringer Einfluss  
        - `10` = moderater Einfluss  
        - `100` = starker Einfluss
        """)

    # Fortschrittsanzeige
    st.subheader(f"Seite {st.session_state.page + 1} von {len(x_factors)} – Faktor: {current_x}")
    progress = int(((st.session_state.page + 1) / len(x_factors)) * 100)
    st.progress(progress)

    options = ["", "0", "1", "10", "100"]
    new_values = []

    for idx, row in page_data.iterrows():
        frage = row["Beschreibung"]
        default = row["Wert"] if row["Wert"] in options else ""
        antwort = st.selectbox(frage, options, index=options.index(default), key=f"frage_{current_x}_{idx}")
        new_values.append(antwort)

    data.loc[data["X_Faktor"] == current_x, "Wert"] = new_values

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.page > 0:
            if st.button("⬅️ Zurück"):
                st.session_state.page -= 1
    with col3:
        if st.session_state.page < len(x_factors) - 1:
            if st.button("Weiter ➡️"):
                st.session_state.page += 1
        else:
            st.markdown("### ✅ Du hast alle Seiten ausgefüllt!")
            csv_ready = data.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Gesamte Matrix herunterladen", csv_ready, "cross_impact_output.csv", "text/csv")

    # Speicheroptionen
    st.divider()
    st.markdown("💾 **Optionen zur Zwischenspeicherung:**")
    save_csv = data.to_csv(index=False).encode("utf-8")
    st.download_button("📝 Zwischenstand speichern", save_csv, "cross_impact_zwischenstand.csv", "text/csv")

    uploaded_file = st.file_uploader("📤 Vorherige Datei laden", type="csv")
    if uploaded_file:
        uploaded_data = pd.read_csv(uploaded_file)
        if {"X_Faktor", "Y_Ziel", "Wert", "Beschreibung"}.issubset(uploaded_data.columns):
            st.session_state.data = uploaded_data
            st.success("✅ Zwischenstand geladen!")
        else:
            st.error("⚠️ Diese Datei ist kein gültiger Zwischenstand.")

except Exception as e:
    st.error("❌ Ein unerwarteter Fehler ist aufgetreten.")
    st.exception(e)