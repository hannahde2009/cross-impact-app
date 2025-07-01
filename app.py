import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cross-Impact-Matrix", layout="wide")
st.title("Cross-Impact-Matrix – Modellprojekte")

# Lade die vorbereitete Matrix
@st.cache_data
def load_data():
    return pd.read_csv("cross_impact_data_python.csv")

data = load_data()

# Eingabefeld für jede Kombination
options = ["", "0", "1", "10", "100"]
responses = []

st.markdown("Bitte bewerten Sie den Einfluss jedes Faktors auf jede Zielvariable:")

for idx, row in data.iterrows():
    col1, col2 = row["X_Faktor"], row["Y_Ziel"]
    default = row["Wert"] if row["Wert"] in options else ""
    key = f"{col1}_{col2}_{idx}"
    selection = st.selectbox(f"{col1} ➝ {col2}", options, index=options.index(default), key=key)
    responses.append(selection)

# Daten aktualisieren
data["Wert"] = responses

# Download
csv = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download als CSV",
    csv,
    "cross_impact_output.csv",
    "text/csv"
)