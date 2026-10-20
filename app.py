import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from popular_banco import popular_banco

# Configura a aba do navegador
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Executa o script que garante que o banco tem dados
popular_banco()

# Credenciais do Banco
db_user = os.environ.get("DB_USER", "usuario")
db_pass = os.environ.get("DB_PASSWORD", "senha123")
db_host = os.environ.get("DB_HOST", "db")
db_name = os.environ.get("DB_NAME", "vendas_db")

# Função com cache para não sobrecarregar o banco de dados a cada clique
@st.cache_data(ttl=60)
def carregar_dados():
    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
    query = "SELECT * FROM vendas ORDER BY data DESC;"
    return pd.read_sql(query, engine)

df = carregar_dados()

# --- INTERFACE DO USUÁRIO ---
st.title("📊 Dashboard Executivo de Vendas")

# Filtro na Barra Lateral
st.sidebar.header("Filtros")
categorias = ["Todas"] + list(df["categoria"].unique())
categoria_selecionada = st.sidebar.selectbox("Filtrar por Categoria", categorias)

# Aplica o filtro de dados conforme a seleção do usuário
if categoria_selecionada != "Todas":
    df_filtrado = df[df["categoria"] == categoria_selecionada]
else:
    df_filtrado = df.copy()

# Cálculo dos Cartões de Métricas (KPIs)
total_faturamento = df_filtrado["valor"].sum()
total_pedidos = len(df_filtrado)
ticket_medio = total_faturamento / total_pedidos if total_pedidos > 0 else 0.0

# Exibição dos KPIs em 3 colunas paralelas
col1, col2, col3 = st.columns(3)
col1.metric("Faturamento Total", f"R$ {total_faturamento:,.2f}")
col2.metric("Total de Pedidos", total_pedidos)
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# Seção de Gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Faturamento por Categoria")
    # Agrupa por categoria e soma os valores
    df_cat = df_filtrado.groupby("categoria")["valor"].sum().reset_index()
    fig_cat = px.bar(df_cat, x="categoria", y="valor", color="categoria", labels={"valor": "Total (R$)", "categoria": "Categoria"})
    st.plotly_chart(fig_cat, use_container_width=True)

with col_graf2:
    st.subheader("Evolução Temporal das Vendas")
    # Agrupa vendas por dia
    df_tempo = df_filtrado.copy()
    df_tempo["data_dia"] = df_tempo["data"].dt.date
    vendas_dia = df_tempo.groupby("data_dia")["valor"].sum().reset_index()
    fig_linha = px.line(vendas_dia, x="data_dia", y="valor", labels={"valor": "Faturamento (R$)", "data_dia": "Data"})
    st.plotly_chart(fig_linha, use_container_width=True)

# Tabela Bruta de Dados
st.subheader("Registros Recentes")
st.dataframe(df_filtrado, use_container_width=True)