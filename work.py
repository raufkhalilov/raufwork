import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page style
st.set_page_config(page_title="Hypothesis Testing App", page_icon=":bar_chart:")

# Set custom theme
CUSTOM_THEME = """
    <style>
        /* Custom CSS */
        .stApp {
            font-family: 'Arial', sans-serif;
            font-size: 16px;
            line-height: 1.5;
            color: #333333;
            background-color: #f1f1f1;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .stButton button {
            background-color: #ff6f61;
            border-color: #ff6f61;
            color: #ffffff;
            width: auto;
        }
        .stButton button:hover {
            background-color: #db4b3c;
            border-color: #db4b3c;
            color: #ffffff;
        }
        .stTextInput input {
            border-radius: 3px;
            padding: 8px;
            width: 100%;
            margin-bottom: 10px;
        }
        .stSelectbox select {
            border-radius: 3px;
            padding: 8px;
            width: 100%;
            margin-bottom: 10px;
        }
        .stPlotlyChart {
            width: 100%;
            margin-bottom: 10px;
        }
    </style>
"""
st.markdown(CUSTOM_THEME, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Перетащите файл сюда или кликните для загрузки", key="file_uploader")
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except:
        st.error("Это не csv файл!")
else:
    st.error("Не удалось загрузить файл.")

if uploaded_file is not None:
    col1 = st.selectbox("Первая колонка", df.columns)
    col2 = st.selectbox("Вторая колонка", df.columns)

    st.write(f"Вы выбрали колонки '{col1}' и '{col2}'")

    if df[col1].dtype == "float64" or df[col1].dtype == "int64":
        fig, ax = plt.subplots()
        ax.hist(df[col1], bins=20, color='skyblue')  # Change histogram color to sky blue
        ax.set_xlabel(col1)
        ax.set_ylabel("Частота")
        st.pyplot(fig)

    else:
        pie_data = df[col1].value_counts().to_frame().rename(columns={col1: "Count"})
        fig = px.pie(pie_data, values="Count", names=pie_data.index)
        fig.update_traces(marker=dict(colors=['coral']))  # Change pie chart color to coral
        st.plotly_chart(fig)

    if df[col2].dtype == "float64" or df[col2].dtype == "int64":
        fig, ax = plt.subplots()
        ax.hist(df[col2], bins=20, color='lightgreen')  # Change histogram color to light green
        ax.set_xlabel(col2)
        ax.set_ylabel("Частота")
        st.pyplot(fig)

else:
    pie_data = df[col2].value_counts().to_frame().rename(columns={col2: "Count"})
    fig = px.pie(pie_data, values="Count", names=pie_data.index)
    fig.update_traces(marker=dict(colors=['gold']))  # Change pie chart color to gold
    st.plotly_chart(fig)

test = st.selectbox("Выберите алгоритм теста гипотез", ["Критерий знаковых рангов Уилкоксона", "t-тест"])

if test == "Критерий знаковых рангов Уилкоксона":
    stat, pvalue = stats.wilcoxon(df[col1], df[col2])
    st.write(f"Результат критерия знаковых рангов Уилкоксона: статистика = {stat:.3f}, p-значение = {pvalue:.3f}")
elif test == "t-тест":
    stat, pvalue = stats.ttest_ind(df[col1], df[col2])
    st.write(f"Результат t-теста: статистика = {stat:.3f}, p-значение = {pvalue:.3f}")