import pandas as pd 
import plotly.express as px 
import streamlit as st 

# Carregar a tabela do Excel
tabela = pd.read_excel('levantamento DDA.xlsx')

# Remover espaços em branco nas strings
tabela = tabela.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Definir as colunas relevantes
coluna1 = 'Situação'
coluna2 = 'Nome Cedente'
coluna3 = 'Observação do Vínculo'

# Mapa de cores para a coluna 'Situação'
color_map = {
    'Automático': 'green',
    'Manual': 'blue',
    'Pendente': 'yellow',
    'Vinculado - Com diferença': 'red'
}

color_map_vinculo = {
    'Número do documento diferente, Cnpj/Cpf do cedente': 'purple',
    'Número do documento diferente': 'red',
    'Cnpj/Cpf do cedente diferente': 'blue'
}

# Criar gráficos
grafico_situacao = px.pie(tabela, names=coluna1, title='Situação', 
                          color=coluna1, color_discrete_map=color_map)

grafico_situacao.update_traces(
    hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<extra></extra>'
)

tabela_agrupada = tabela.groupby([coluna2, coluna1]).size().reset_index(name='count')
grafico_cruzado = px.bar(tabela_agrupada, x=coluna2, y='count',
                         color=coluna1, title='Distribuição de Situação por Nome Cedente',
                         color_discrete_map=color_map)

# Filtrar e criar gráficos para 'Vinculado - Com Diferença'
tabela_filtrada = tabela[tabela[coluna1] == 'Vinculado - Com diferença']
tabela_filtrada_agrupada = tabela_filtrada.groupby([coluna2, coluna3]).size().reset_index(name='count')

grafico_vinculado = px.bar(tabela_filtrada_agrupada, x=coluna2, y='count', 
                           color=coluna3, title='Vinculado - Com Diferença por Nome Cedente',
                           color_discrete_map=color_map_vinculo)

grafico_pizza = px.pie(tabela_filtrada_agrupada, names=coluna3, values='count',
                       title='Distribuição de Vinculado - Com Diferença por Observação do Vínculo',
                       color=coluna3, color_discrete_map=color_map_vinculo)

# Criar o dropdown para seleção de gráficos
st.title('Levantamento DDA')

opcao = st.selectbox(
    'Seleção de Dash Board',
    ['Situação', 'Distribuição de Situação por Nome Cedente', 'Vinculado - Com Diferença por Nome Cedente', 'Distribuição de Vinculado - Com Diferença por Observação do Vínculo']
)

# Exibir o gráfico com base na opção selecionada
if opcao == 'Situação':
    st.plotly_chart(grafico_situacao, use_container_width=True)
    
    st.subheader("Observações")
    
    # Caixas de texto abaixo do gráfico
    with st.expander("30,8% Vinculado com Diferença"):
        st.markdown(f"""
        <span style="color:{color_map['Vinculado - Com diferença']}">Consegue fazer o vínculo manual e processar a remessa.  
        **Impacto Negativo:** O retrabalho na validação das informações leva o dobro do tempo em comparação ao método atual.</span>
        """, unsafe_allow_html=True)
    
    with st.expander("54% Pendente"):
        st.markdown(f"""
    <span>**Agrupamentos:** Erros com diferença de valor e lançamento posterior ao fechamento (até 7 dias). Requer o mesmo retrabalho do "Vinculado com Diferença", pois é necessário acessar outra tela.  
    Para ajustar a diferença de valor, é preciso realizar um ajuste manual.  
    **Vencimentos Errados:** Manutenção necessária.  
    **Ação Requerida:** Trazer por setor os vencimentos incorretos.</span>
    """, unsafe_allow_html=True)

    
    with st.expander("5,02% Manual"):
        st.markdown(f"""
        <span style="color:{color_map['Manual']}">Não consegue vincular automaticamente, resultando no mesmo retrabalho do "Vinculado com Diferença".  
        **Ação Requerida:** Buscar entendimento, pois a causa não foi identificada. Trazer evidências.</span>
        """, unsafe_allow_html=True)
    
    with st.expander("10,2% Automático"):
        st.markdown(f"""
        <span style="color:{color_map['Automático']}">É vinculado automaticamente, sem necessidade de intervenção manual.</span>
        """, unsafe_allow_html=True)

elif opcao == 'Distribuição de Situação por Nome Cedente':
    # Checkbox para mostrar ou esconder os nomes das empresas
    mostrar_nomes = st.checkbox('Mostrar nomes das empresas')
    
    if not mostrar_nomes:
        grafico_cruzado.update_xaxes(showticklabels=False)
    
    st.plotly_chart(grafico_cruzado)

elif opcao == 'Vinculado - Com Diferença por Nome Cedente':
    # Checkbox para mostrar ou esconder os nomes das empresas
    mostrar_nomes = st.checkbox('Mostrar nomes das empresas')
    
    if not mostrar_nomes:
        grafico_vinculado.update_xaxes(showticklabels=False)
    
    st.plotly_chart(grafico_vinculado)

elif opcao == 'Distribuição de Vinculado - Com Diferença por Observação do Vínculo':
    st.plotly_chart(grafico_pizza)
