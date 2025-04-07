import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

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
accounts = ('121101','121205','251100','251101','251102','251103','251110')

for acc in accounts :
  df_year[acc] /= df_year['Total']/100

fig2 = go.Figure()
for acc in accounts:
  fig2.add_trace(go.Bar(
      x = df_year[acc],
      y = df_year.index,
      orientation='h',
      name = acc
    )
  )
fig2.update_layout(barmode='stack', title='Contribution au total par année.',legend_title="Compte")
st.plotly_chart(fig2)

year = st.selectbox('Année', df_year.index)
df_pie = df[df['Année'] == year].groupby(['Année']).sum().drop(['Mois', 'Total'], axis=1)

pie = go.Figure(data=[go.Pie(
  labels = accounts,
  values = [df_pie[acc].iloc[0] for acc in accounts]
)])
pie.update_layout(
    
  title = f'Contribution au total (en pourcentage) des différents comptes pour l\'année {year}',
  legend_title="Compte"
)
st.plotly_chart(pie)

st.markdown("## Analyse 2022 - 2023")

''''''
