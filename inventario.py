import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ARQUIVO = "inventario.csv"

# Inicializa o arquivo se não existir
if not os.path.exists(ARQUIVO):
    df_vazio = pd.DataFrame(columns=["Data", "Código", "Quantidade"])
    df_vazio.to_csv(ARQUIVO, index=False)

# Carrega o inventário do CSV
def carregar_dados():
    return pd.read_csv(ARQUIVO)

# Salva nova contagem
def salvar_contagem(codigo, quantidade):
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nova_linha = pd.DataFrame([[data, codigo, quantidade]], columns=["Data", "Código", "Quantidade"])
    df = carregar_dados()
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

# Limpa o inventário
def limpar_dados():
    df_vazio = pd.DataFrame(columns=["Data", "Código", "Quantidade"])
    df_vazio.to_csv(ARQUIVO, index=False)

# Início da interface
st.set_page_config(page_title="Inventário", layout="centered")
st.title("📦 Inventário Simples com Gráfico e Exportação")
df = carregar_dados()

# --- BARRA LATERAL ---
st.sidebar.title("🔧 Navegação")
pagina = st.sidebar.radio("Ir para", ["Registrar", "Visualizar", "Exportar", "⚠️ Limpar Dados"])

# --- Página: Registrar ---
if pagina == "Registrar":
    st.subheader("Registrar contagem")
    codigo = st.text_input("Código do item")
    quantidade = st.number_input("Quantidade contada", min_value=0, step=1)

    # Prevenção de código inválido
    if st.button("Registrar"):
        if not codigo.strip():
            st.warning("Informe o código.")
        elif not codigo.isdigit() or len(codigo.strip()) < 8:
            st.error("O código deve conter pelo menos 8 números.")
        elif quantidade <= 0:
            st.warning("Quantidade deve ser maior que zero.")
        else:
            # Verifica duplicação opcional
            if not df.empty and df.iloc[-1]["Código"] == codigo and int(df.iloc[-1]["Quantidade"]) == quantidade:
                st.warning("Esse item já foi registrado anteriormente com mesma quantidade.")
            else:
                salvar_contagem(codigo, quantidade)
                st.success(f"Item '{codigo}' com {quantidade} unidades registrado.")

# --- Página: Visualizar ---
elif pagina == "Visualizar":
    st.subheader("📑 Relatório de Contagens")
    filtro = st.text_input("Filtrar por código (opcional)")
    df_filtrado = df.copy()
    if filtro:
        df_filtrado = df[df["Código"].str.contains(filtro, case=False)]
    if not df_filtrado.empty:
        df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"]).dt.strftime("%d/%m/%Y %H:%M")
        df_filtrado = df_filtrado.iloc[::-1]  # Mais recentes primeiro
    st.dataframe(df_filtrado)

# --- Página: Exportar ---
elif pagina == "Exportar":
    st.subheader("📊 Resumo por Código")
    resumo = df.groupby("Código")["Quantidade"].sum().reset_index()
    resumo["Quantidade"] = resumo["Quantidade"].astype(int)
    resumo["Rótulo"] = resumo["Código"].astype(str) + " – " + resumo["Quantidade"].astype(str) + " un."
    resumo = resumo.sort_values(by="Quantidade", ascending=False)

    # Gráfico de pizza
    fig = px.pie(
        resumo,
        names="Rótulo",
        values="Quantidade",
        title="📈 Distribuição das Quantidades por Item",
        hole=0.3
    )
    fig.update_traces(textinfo='label+percent', hoverinfo='label+value+percent')
    st.plotly_chart(fig)

    st.subheader("⬇️ Exportar dados")

    # Exportar Excel resumo
    buffer_resumo = BytesIO()
    with pd.ExcelWriter(buffer_resumo, engine='openpyxl') as writer:
        resumo.to_excel(writer, index=False, sheet_name="Resumo")
    buffer_resumo.seek(0)
    st.download_button("📥 Baixar resumo (Excel)", buffer_resumo, f"resumo_inventario_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Exportar histórico
    buffer_hist = BytesIO()
    with pd.ExcelWriter(buffer_hist, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Histórico")
    buffer_hist.seek(0)
    st.download_button("📥 Baixar histórico completo (Excel)", buffer_hist, f"historico_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Gerar PDF
    def gerar_pdf(resumo_df):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 800, "Resumo do Inventário")
        pdf.setFont("Helvetica", 12)
        y = 770
        for i, row in resumo_df.iterrows():
            linha = f"{row['Código']}: {row['Quantidade']} unidades"
            pdf.drawString(50, y, linha)
            y -= 20
            if y < 50:
                pdf.showPage()
                y = 800
        pdf.save()
        buffer.seek(0)
        return buffer

    pdf_bytes = gerar_pdf(resumo)
    st.download_button("📄 Baixar resumo (PDF)", pdf_bytes, f"resumo_inventario_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf")

# --- Página: Limpar dados ---
elif pagina == "⚠️ Limpar Dados":
    st.subheader("⚠️ Limpar todos os registros")
    st.warning("Essa ação não pode ser desfeita.")
    if st.button("Apagar tudo"):
        limpar_dados()
        st.success("Todos os registros foram apagados.")

