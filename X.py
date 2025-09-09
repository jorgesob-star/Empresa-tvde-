import streamlit as st import pandas as pd

st.set_page_config(page_title="Simulador TVDE", layout="wide")

st.title("Simulador financeiro para empresa TVDE — Streamlit") st.markdown( "Use esta app para simular faturação, despesas e encargos (Seg. Social, IRC) e ver o lucro mensal e anual.\n" "Os valores por defeito correspondem aos exemplos que discutimos: faturação 3.000€ ou 4.000€." )

with st.sidebar: st.header("Parâmetros") faturacao = st.number_input("Faturação bruta mensal (€)", min_value=0.0, value=3000.0, step=100.0, format="%.2f") comissao_pct = st.slider("Comissão plataforma (%)", min_value=0.0, max_value=60.0, value=25.0, step=1.0) combustivel = st.number_input("Combustível mensal (€)", min_value=0.0, value=450.0, step=10.0, format="%.2f") manutencao = st.number_input("Manutenção mensal (€)", min_value=0.0, value=75.0, step=5.0, format="%.2f") seguro = st.number_input("Seguro mensal (€)", min_value=0.0, value=180.0, step=5.0, format="%.2f") outros = st.number_input("Outros custos operacionais (€)", min_value=0.0, value=0.0, step=5.0, format="%.2f")

seg_social_pct = st.number_input("Taxa Segurança Social (%)", min_value=0.0, value=21.4, step=0.1, format="%.2f")
irc_pct = st.number_input("Taxa IRC/IRS aproximada (%)", min_value=0.0, value=17.0, step=0.1, format="%.2f")

periodo = st.selectbox("Período de visualização", ["Mensal", "Anual (12 meses)"])

st.markdown("---")

Cálculos

comissao = faturacao * (comissao_pct / 100.0) custos_operacionais = combustivel + manutencao + seguro + outros lucro_bruto = faturacao - comissao - custos_operacionais

Evita valores negativos para encargos

seg_social = max(lucro_bruto * (seg_social_pct / 100.0), 0.0) irc = max(lucro_bruto * (irc_pct / 100.0), 0.0) lucro_liquido = lucro_bruto - seg_social - irc

Valores anuais

faturacao_ano = faturacao * 12 comissao_ano = comissao * 12 custos_operacionais_ano = custos_operacionais * 12 lucro_bruto_ano = lucro_bruto * 12 seg_social_ano = seg_social * 12 irc_ano = irc * 12 lucro_liquido_ano = lucro_liquido * 12

DataFrames

df_mensal = pd.DataFrame({ "Descrição": ["Faturação bruta", "Comissão plataforma", "Combustíveis", "Manutenção", "Seguro", "Outros custos", "Total custos operacionais", "Lucro bruto (antes impostos)", "Segurança Social", "IRC", "Lucro líquido"], "€ (mensal)": [faturacao, comissao, combustivel, manutencao, seguro, outros, custos_operacionais, lucro_bruto, seg_social, irc, lucro_liquido] })

df_anual = pd.DataFrame({ "Descrição": df_mensal['Descrição'], "€ (anual)": [faturacao_ano, comissao_ano, combustivel12, manutencao12, seguro12, outros12, custos_operacionais_ano, lucro_bruto_ano, seg_social_ano, irc_ano, lucro_liquido_ano] })

Mostrar resultados

if periodo == "Mensal": st.header("Resumo mensal") st.table(df_mensal.style.format({"€ (mensal)": "{:.2f} €"})) st.metric("Lucro líquido (mensal)", f"{lucro_liquido:.2f} €") else: st.header("Resumo anual") st.table(df_anual.style.format({"€ (anual)": "{:.2f} €"})) st.metric("Lucro líquido (anual)", f"{lucro_liquido_ano:.2f} €")

Gráfico

st.subheader("Gráfico: Distribuição dos custos") plot_df = pd.DataFrame({ "Categorias": ["Comissão", "Custos operacionais", "Seg. Social", "IRC", "Lucro líquido"], "€": [comissao, custos_operacionais, seg_social, irc, lucro_liquido] }) plot_df = plot_df.set_index('Categorias') st.bar_chart(plot_df)

Exportação CSV

st.subheader("Exportar resultados") result_df = pd.concat([df_mensal.set_index('Descrição'), df_anual.set_index('Descrição')], axis=1) result_df.columns = ["Mensal (€)", "Anual (€)"]

csv = result_df.to_csv(sep=';')

st.download_button(label="Descarregar CSV", data=csv, file_name="simulacao_tvde.csv", mime="text/csv")

st.markdown("---") st.caption("Simulação simplificada: não substitui aconselhamento contabilístico. Ajuste taxas e custos conforme necessário.")

