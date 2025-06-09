# 📦 Sistema de Inventário Simples

Este é um sistema simples de controle de inventário desenvolvido com **Python** e **Streamlit**. Ele permite registrar contagens de itens, gerar gráficos, exportar relatórios em Excel e visualizar o histórico de registros.

## 🚀 Funcionalidades

- Registrar itens com código e quantidade  
- Resumo por código  
- Gráfico de pizza com distribuição das quantidades  
- Exportação para Excel (resumo e histórico)  
- Filtro por código  
- Registro automático de data/hora  
- Botão para limpar registros  
- Interface amigável via navegador  

## 🛠 Requisitos

- Python 3.10 ou superior  
- Bibliotecas Python:
  - streamlit  
  - pandas  
  - openpyxl  
  - plotly  
  - reportlab *(opcional para exportação em PDF)*  

## 📦 Instalação

1. Clone este repositório ou baixe o `.zip`:

```bash
git clone https://github.com/SEU_USUARIO/inventario-streamlit.git
cd inventario-streamlit
pip install -r requirements.txt
```

2. Execute o sistema:

```bash
streamlit run inventario.py
```

Ou dê **dois cliques** no arquivo `executar.bat` (Windows).

## 📁 Estrutura do Projeto

```
inventario/
├── inventario.py         # Código principal
├── inventario.csv        # Arquivo com os dados registrados
├── executar.bat          # Atalho para rodar com 1 clique
├── requirements.txt      # Bibliotecas necessárias
└── README.md             # Instruções e informações do sistema
```

---

Desenvolvido por **Breno Rodrigues Bittencourt**.
