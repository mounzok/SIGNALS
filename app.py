import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(layout="wide")
st.title("📊 Dashboard Vanilla Options – Marchés Volatility")

FICHIER_CSV = "signaux_vanilla.csv"

try:
    df = pd.read_csv(FICHIER_CSV)

    # Filtrer uniquement les marchés Volatility
    df = df[df["Marché"].str.startswith("Volatility")]
    marches_dispo = df["Marché"].unique().tolist()
    choix = st.selectbox("🎯 Choisir un marché VIX", ["Tous"] + marches_dispo)

    if choix != "Tous":
        df = df[df["Marché"] == choix]

    # Afficher le tableau complet
    st.subheader("📄 Données disponibles")
    st.dataframe(df)

    # Filtrer les signaux valides (CALL ou PUT)
    signaux_valides = df[
        (df["RSI > 50"] == "✅") &
        (df["Bollinger Signal"].isin(["Rebond", "Rejet"])) &
        (df["MACD Signal"] == "✅") &
        (df["SMA Position"].isin(["> SMA", "< SMA"]))
    ]

    st.markdown("---")
    st.subheader("📢 Signaux Valides (CALL ou PUT)")

    if signaux_valides.empty:
        st.info("Aucun signal valide pour l’instant.")
    else:
        for i, row in signaux_valides.iterrows():
            st.write(f"🕒 {row['Date']} – 📈 {row['Marché']}")
            st.write(f"🔹 RSI: {row['RSI > 50']} | Bollinger: {row['Bollinger Signal']} | MACD: {row['MACD Signal']} | SMA: {row['SMA Position']}")
            st.markdown("---")

    # Graphiques d’indicateurs
    st.subheader("📉 Graphiques d’indicateurs")

    col1, col2, col3 = st.columns(3)

    with col1:
        rsi_data = df["RSI > 50"].value_counts().reset_index()
        rsi_data.columns = ["RSI", "Count"]
        fig_rsi = px.pie(rsi_data, names="RSI", values="Count", title="RSI > 50")
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col2:
        boll_data = df["Bollinger Signal"].value_counts().reset_index()
        boll_data.columns = ["Signal", "Count"]
        fig_boll = px.bar(boll_data, x="Signal", y="Count", title="Bollinger Signal")
        st.plotly_chart(fig_boll, use_container_width=True)

    with col3:
        macd_data = df["MACD Signal"].value_counts().reset_index()
        macd_data.columns = ["MACD", "Count"]
        fig_macd = px.pie(macd_data, names="MACD", values="Count", title="MACD Signal")
        st.plotly_chart(fig_macd, use_container_width=True)

    # Résumé des marchés actifs
    st.markdown("---")
    st.subheader("📌 Marchés les plus actifs (RSI > 50)")

    resume = df[df["RSI > 50"] == "✅"].groupby("Marché").size().reset_index(name="Nombre de signaux")
    resume = resume.sort_values("Nombre de signaux", ascending=False)

    st.dataframe(resume)

    fig_resume = px.bar(
        resume,
        x="Marché",
        y="Nombre de signaux",
        text="Nombre de signaux",
        title="Top marchés par fréquence de signaux RSI > 50"
    )
    fig_resume.update_traces(textposition="outside")
    fig_resume.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_resume, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️ Le fichier 'signaux_vanilla.csv' est introuvable.")
except Exception as e:
    st.error(f"❌ Erreur : {e}")
