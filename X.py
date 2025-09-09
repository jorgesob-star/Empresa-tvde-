import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Gestão TVDE", layout="wide")
st.title("Sistema de Gestão para Empresas TVDE")

# Menu lateral
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Motoristas", "Veículos", "Financeiro"])

if menu == "Dashboard":
    st.header("Visão Geral da Operação")
    # Carregar dados de exemplo
    dados = pd.DataFrame({"Mês": ["Jan", "Fev", "Mar"], "Faturação": [5000, 7000, 6000]})
    fig = px.line(dados, x="Mês", y="Faturação", title="Faturação Trimestral")
    st.plotly_chart(fig)

elif menu == "Motoristas":
    st.header("Gestão de Motoristas")
    # Formulário para adicionar motorista
    with st.form("novo_motorista"):
        nome = st.text_input("Nome")
        nif = st.number_input("NIF", step=1)
        documento = st.file_uploader("Anexar Licença")
        submitted = st.form_submit_button("Registar")
        if submitted:
            st.success(f"Motorista {nome} registado com sucesso!")

elif menu == "Financeiro":
    st.header("Cálculo de Impostos")
    faturacao = st.number_input("Faturação Trimestral (€)", min_value=0.0)
    iva = faturacao * 0.06  # Cálculo de IVA a 6%
    st.metric("IVA a Pagar", f"{iva:.2f} €")
