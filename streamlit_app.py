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

st.write('''L'analyse de l'évolution de ces comptes entre 2022 et 2023 montre des tendances qui varient d'un mois à l'autre, 
avec des différences significatives selon les comptes.

En observant l’évolution des totaux mensuels, on remarque que les chiffres en 2022 varient entre 70 millions et 128 millions, avec 
des hausses significatives en juin (128 millions) et en décembre (101 millions). Cette année-là, il y a une certaine irrégularité dans 
les valeurs, avec des pics, notamment en juin, suivi d'une baisse en novembre. En 2023, les totaux sont plus réguliers. Par exemple, 
le total de janvier 2023 est de 78 millions, tandis que celui de décembre est de 79,97 millions, montrant une stabilité avec une légère 
baisse en fin d’année.

Lorsqu’on se concentre sur les comptes plus spécifiquement, le compte 121101, qui représente une part importante des totaux, 
connaît une tendance 
générale à la baisse de 2022 à 2023. En janvier 2022, le montant est de 34,77 millions, en janvier 2023, il tombe à 26,75 millions.
Cependant, en juillet 2023, il atteint un pic à 46,65 millions, suggérant un ajustement exceptionnel en cours d'année. 
Le compte 121205, quant à lui, montre des valeurs élevées en 2022, atteignant 89 millions en juin et 43 millions en décembre. En 
2023, il semble plus stable, avec une légère tendance haussière.

Les comptes 251100 et 251101, montrent des tendances similaires, à savoir une hausse continue tout au long des deux années. 
Alors que les comptes 251102 et 251103 ont connu une année 2022 très stable avec des valeurs fluctuant autour de 7M et 300K 
respectivement tandis que l'année 2023 à été synonyme de de grande évolution pour les deux comptes. 

Une analyse plus détaillée montre également qu’il y a des mois où une diminution globale est observée, notamment en mars 2023, avec un 
total plus bas de 46 millions. En revanche, des pics notables se 
produisent durant l'été 2023, en juillet et août, avec des chiffres supérieurs à 100 millions.

En résumé, l’année 2022 présente des fluctuations notables dans les totaux mensuels, avec des pics en milieu et fin d’année. En 2023, 
les chiffres sont plus homogènes et stables, bien qu'il y ait des hausses importantes en juillet et août, suivies d’une diminution en 
septembre.
''')
