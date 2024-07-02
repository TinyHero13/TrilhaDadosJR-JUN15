import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px

def menu_app():
    st.set_page_config(layout="wide")      
    
def reading_df():
    df = pd.read_csv('venda_cursos.csv')
    df_grouped = df.groupby(['Nome do Curso', 'Preço Unitário'])['Quantidade de Vendas'].sum().reset_index()
    df_grouped['Lucro Total'] = df_grouped['Quantidade de Vendas'] * df_grouped['Preço Unitário']
    
    return df, df_grouped
    
def main():
    menu_app()
    df, df_grouped = reading_df()
    
    st.title('Análise das vendas dos curso')
    
    dash_1 = st.container()
    with dash_1:
        st.write("")

    dash_2 = st.container()

    with dash_2:
        total_profit = df_grouped['Lucro Total'].sum()
        total_rows = df.shape[0]
        total_sales = df_grouped['Quantidade de Vendas'].sum()
                
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label='Receita total',value=round(total_profit,2))
        col2.metric(label='Quantidade total de linhas', value=total_rows)
        col3.metric(label='Vendas totais', value=total_sales)
        
        style_metric_cards(border_left_color="#87f7ff", background_color="#003f5c")

    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.line(df, x='Data', y='Quantidade de Vendas', 
                      title='Quantidade de vendas por periodo')
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None
        )
        st.plotly_chart(fig)

    with col2:
        df_vendas = df_grouped[['Quantidade de Vendas', 'Nome do Curso']].sort_values(by='Quantidade de Vendas')
        fig = px.bar(df_vendas, x='Quantidade de Vendas', y='Nome do Curso', 
                     text_auto=True,
                    title='Quantidade de vendas por curso')
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None
        )
        st.plotly_chart(fig)
        
    with col3:
        fig = px.histogram(df_grouped, x='Preço Unitário', y='Quantidade de Vendas', nbins=18,
                           text_auto=True,
                           title='Preço por quantidade de vendas'
                           )
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None
        )
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()