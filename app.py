from woocommerce import API
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do WooCommerce usando variáveis de ambiente
wcapi = API(
    url=os.getenv("WOOCOMMERCE_URL"),
    consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
    consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
    version="wc/v3"
)

# Buscar produtos (máx. 100 por página)
response = wcapi.get("products", params={"per_page": 100})

# Transformar em DataFrame
produtos = pd.DataFrame(response.json())

# Adicionar campo de etapa com base no nome (classificação simples)
def classificar_etapa(nome):
    nome = nome.lower()
    if any(p in nome for p in ["apc", "desengraxante", "multitec", "citrus"]):
        return "Pré-lavagem"
    elif any(p in nome for p in ["shampoo", "lava", "luva", "balde"]):
        return "Lavagem"
    elif any(p in nome for p in ["clay", "descontaminação", "iron", "descontaminante"]):
        return "Descontaminação"
    elif any(p in nome for p in ["polidor", "composto", "boina", "polimento"]):
        return "Correção"
    elif any(p in nome for p in ["cera", "vitrificador", "selante", "coating", "protection"]):
        return "Proteção"
    elif any(p in nome for p in ["pretinho", "silicone", "microfibra", "toalha", "finalização"]):
        return "Finalização"
    else:
        return "Outros"

# Aplica classificação
produtos["etapa"] = produtos["name"].apply(classificar_etapa)

# Interface Streamlit
st.title("🧼 Gerador de Kits MM Clean")
st.write("Monte kits automáticos baseados em etapas de detalhamento automotivo")

# Seleção de etapas
etapas_disponiveis = produtos["etapa"].unique().tolist()
etapas_selecionadas = st.multiselect("Selecione as etapas para o kit:", etapas_disponiveis)

# Geração do kit
if etapas_selecionadas:
    st.subheader("Kit Gerado")
    kit = []
    for etapa in etapas_selecionadas:
        produtos_na_etapa = produtos[produtos["etapa"] == etapa]
        if not produtos_na_etapa.empty:
            produto_escolhido = produtos_na_etapa.sample(1).iloc[0]
            kit.append(produto_escolhido)

    for item in kit:
        st.markdown(f"- **{item['etapa']}** → {item['name']}")
else:
    st.info("Selecione ao menos uma etapa para gerar o kit.")