import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Gestão TVDE Portugal",
    page_icon="🚗",
    layout="wide"
)

# Título principal
st.title("🚗 Sistema de Gestão para Empresas TVDE - Portugal")
st.markdown("---")

# Menu lateral
st.sidebar.header("Menu de Navegação")
menu = st.sidebar.selectbox(
    "Selecione a Secção",
    ["Dashboard", "Motoristas", "Veículos", "Financeiro", "Documentos", "Ajuda"]
)

# Dados de exemplo
@st.cache_data
def carregar_dados_exemplo():
    motoristas = pd.DataFrame({
        'Nome': ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Costa'],
        'NIF': [123456789, 987654321, 456789123, 789123456],
        'Telefone': ['912345678', '934567890', '967890123', '923456789'],
        'Estado': ['Ativo', 'Ativo', 'Inativo', 'Ativo'],
        'Data_Registo': ['2024-01-15', '2024-02-20', '2024-01-10', '2024-03-01'],
        'Viagens_Mês': [45, 38, 12, 28]
    })
    
    viagens = pd.DataFrame({
        'Data': pd.date_range('2024-03-01', periods=30),
        'Motorista': np.random.choice(['João Silva', 'Maria Santos', 'Ana Costa'], 30),
        'Valor': np.random.uniform(5, 50, 30),
        'Distancia_km': np.random.uniform(2, 25, 30)
    })
    
    return motoristas, viagens

# Carregar dados
motoristas_df, viagens_df = carregar_dados_exemplo()

if menu == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_motoristas = len(motoristas_df)
        ativos = len(motoristas_df[motoristas_df['Estado'] == 'Ativo'])
        st.metric("Total Motoristas", f"{ativos}/{total_motoristas}")
    
    with col2:
        total_viagens = len(viagens_df)
        st.metric("Viagens este Mês", total_viagens)
    
    with col3:
        total_faturacao = viagens_df['Valor'].sum()
        st.metric("Faturação Mensal", f"{total_faturacao:.2f} €")
    
    with col4:
        media_viagem = viagens_df['Valor'].mean()
        st.metric("Média por Viagem", f"{media_viagem:.2f} €")
    
    st.markdown("---")
    
    # Tabela de performance por motorista
    st.subheader("📈 Performance por Motorista")
    performance = viagens_df.groupby('Motorista').agg({
        'Valor': ['count', 'sum', 'mean']
    }).round(2)
    performance.columns = ['Nº Viagens', 'Total Faturado', 'Média por Viagem']
    st.dataframe(performance, use_container_width=True)

elif menu == "Motoristas":
    st.header("👥 Gestão de Motoristas")
    
    # Lista de motoristas
    st.subheader("Lista de Motoristas Registados")
    st.dataframe(motoristas_df, use_container_width=True)
    
    # Adicionar novo motorista
    st.subheader("➕ Registar Novo Motorista")
    with st.form("form_motorista", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo*")
            nif = st.number_input("NIF*", min_value=100000000, max_value=999999999, step=1)
        
        with col2:
            telefone = st.text_input("Telefone*")
            estado = st.selectbox("Estado*", ["Ativo", "Inativo"])
        
        submitted = st.form_submit_button("📋 Registar Motorista")
        if submitted:
            if nome and nif and telefone:
                st.success(f"✅ Motorista {nome} registado com sucesso!")
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

elif menu == "Veículos":
    st.header("🚙 Gestão de Frota")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registo de Veículos")
        with st.form("form_veiculo"):
            matricula = st.text_input("Matrícula*")
            marca = st.text_input("Marca*")
            modelo = st.text_input("Modelo*")
            ano = st.number_input("Ano", min_value=2000, max_value=2024)
            
            submitted = st.form_submit_button("🚗 Registar Veículo")
            if submitted and matricula and marca and modelo:
                st.success(f"Veículo {matricula} registado!")
    
    with col2:
        st.subheader("Documentos do Veículo")
        docs = st.multiselect(
            "Documentos em Dia:",
            ["Inspeção", "Seguro", "Licença TVDE", "DUA"]
        )
        if st.button("💾 Guardar Estado"):
            st.info("Estado dos documentos atualizado")

elif menu == "Financeiro":
    st.header("💰 Gestão Financeira")
    
    st.subheader("📋 Cálculo de Impostos TVDE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### IVA (6%)")
        faturacao_trimestral = st.number_input(
            "Faturação Trimestral (€)", 
            min_value=0.0, 
            value=15000.0,
            step=500.0
        )
        iva = faturacao_trimestral * 0.06
        st.info(f"**IVA a Pagar:** {iva:.2f} €")
    
    with col2:
        st.markdown("#### IRC/IRS")
        despesas = st.number_input(
            "Despesas Dedutíveis (€)",
            min_value=0.0,
            value=5000.0,
            step=500.0
        )
        lucro_tributavel = max(0, faturacao_trimestral - despesas)
        st.info(f"**Lucro Tributável:** {lucro_tributavel:.2f} €")
    
    st.markdown("---")
    st.subheader("📊 Extrato Financeiro")
    st.dataframe(viagens_df, use_container_width=True)

elif menu == "Documentos":
    st.header("📋 Gestão Documental")
    
    st.subheader("📄 Documentos Obrigatórios TVDE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Para a Empresa:**")
        for doc in ["Licença Exploração", "Registo Comercial", "Seguro RC", "Certificado AT"]:
            status = st.checkbox(f"✅ {doc}", value=True)
        
        st.markdown("**Para Motoristas:**")
        for doc in ["Carta Condução", "Certificado Motorista", "Seguro Acidentes"]:
            status = st.checkbox(f"👤 {doc}", value=True)
    
    with col2:
        st.subheader("📤 Upload de Documentos")
        uploaded_file = st.file_uploader(
            "Selecionar ficheiro", 
            type=['pdf', 'jpg', 'png', 'docx'],
            help="Formatos aceites: PDF, JPG, PNG, DOCX"
        )
        if uploaded_file:
            st.success(f"✅ Ficheiro '{uploaded_file.name}' carregado!")
            if st.button("🗂️ Guardar na Base de Dados"):
                st.info("Documento arquivado com sucesso")

elif menu == "Ajuda":
    st.header("❓ Ajuda e Suporte")
    
    st.info("""
    **📞 Contactos Úteis:**
    - Autoridade Tributária: 217 206 707
    - IMT - Instituto da Mobilidade: 808 202 039
    - Segurança Social: 300 502 502
    
    **📅 Próximas Obrigações:**
    - IVA Trimestral: até dia 20 do mês seguinte ao trimestre
    - IRC Anual: até 31 de Julho
    - Seguros: Renovação anual obrigatória
    """)
    
    st.subheader("🛠️ Suporte Técnico")
    if st.button("📧 Contactar Suporte"):
        st.write("**Email:** suporte@empresatvde.pt")
        st.write("**Telefone:** +351 910 000 000")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**⚠️ Informação Importante:**
Esta aplicação é uma demonstração. 
Para gestão profissional, consulte sempre um contabilista especializado em TVDE.
""")

# Informação de sistema
st.sidebar.markdown("---")
st.sidebar.caption(f"🔄 Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
