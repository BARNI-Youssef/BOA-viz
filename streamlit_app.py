import streamlit as st
import pandas as pd
import os
import plotly.express as px

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
data_path = os.path.join(script_dir, 'data.csv')

st.set_page_config(layout="wide")

df = pd.read_csv(data_path)


st.markdown('# Evolution de la balance des comptes entre Janvier 2019 et Decembre 2023')


st.dataframe(df)


fig = px.line(df, x="Mois", y=df.columns[1:-1], title='Balance des comptes')
fig.update_layout(xaxis_tickangle=-45,
                  yaxis_title="Montant",
                  xaxis_title='Date',
                  legend_title="Compte")
st.plotly_chart(fig)

df_melted = df.melt(id_vars=['Mois'], value_vars=df.columns[1:-1], var_name='Compte', value_name='Valeur')

fig = px.bar(
    df_melted, x='Mois', y='Valeur', color='Compte',
    title="Balance Totale, par compte",
    labels={'Valeur': 'Compte', 'Mois': 'Temps'},
)
fig.update_layout(
    xaxis=dict(tickangle=-45, tickmode='array', tickvals=df['Mois'][::5]), 
    yaxis_title="Montant",
    barmode='stack',
    hovermode="x unified"
)
st.plotly_chart(fig)

df_long = df[df.columns[:-1]].melt(id_vars=['Mois'], var_name='Compte', value_name='Montant')
fig = px.box(df_long, x='Compte', y='Montant', title="Boite à moustache des comptes")
fig.update_layout(
    xaxis=dict(type='category'),
     xaxis_title='Compte',
)
st.plotly_chart(fig)

df['Année'] = df['Mois'].apply(lambda x: x.split('-')[1])

df_year = df.groupby(['Année']).sum().drop(['Mois'], axis=1)
# st.dataframe(df_year)
accounts = ('121101','121205','251100','251101','251102','251103','251110')

for acc in accounts :
  df[acc] /= df['Total']*100

st.dataframe(df_year)
