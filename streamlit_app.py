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

'''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas congue mauris et purus vehicula, ut rhoncus nisl rhoncus. 
Donec tristique, leo vitae convallis dictum, libero velit molestie lorem, non maximus ante metus id augue. Etiam in efficitur lorem. 
Vivamus mattis elit et tincidunt dignissim. Praesent sed nisi nec mauris condimentum suscipit id in nisi. Donec euismod dui eleifend, 
finibus sem ut, sodales massa. Quisque purus risus, sollicitudin ac mattis quis, facilisis lacinia diam. Pellentesque at enim non magna 
venenatis ultrices quis non erat. Vivamus ultricies pretium turpis ac laoreet. Maecenas id volutpat ante. Praesent vel congue sem.

Proin felis ante, pulvinar id sem nec, molestie auctor magna. Cras ornare velit mi, quis aliquam sem lacinia quis. Ut ultrices turpis 
ac massa lobortis elementum. Vestibulum vel mauris maximus mi dignissim blandit. Donec quis mi sit amet nulla tempor interdum id sit amet 
enim. Donec dictum vehicula mollis. Sed varius egestas velit ac luctus. Nulla facilisi. Mauris malesuada nisl ut dolor faucibus, ultrices 
bibendum purus tincidunt. Suspendisse hendrerit sollicitudin enim et euismod. Nunc vel turpis non felis tempus condimentum in auctor 
dolor. Etiam placerat finibus mauris, sit amet tincidunt lorem. Curabitur id nisi sed augue tincidunt tempus. Nam et elementum tellus. 
Cras pretium augue lacus, vel pretium purus tempor vel. Curabitur congue neque porta purus sodales vehicula.

Aenean lacinia, tortor sed tincidunt sollicitudin, nunc eros convallis ligula, eu imperdiet eros est ut urna. Maecenas convallis sed 
nunc eu vulputate. Integer ut cursus risus. Curabitur id maximus arcu. Etiam tortor enim, mattis eget mauris vitae, mattis tristique 
elit. Maecenas nec tortor sit amet enim mattis gravida. Ut metus ligula, dignissim non lorem vitae, rhoncus facilisis mauris. Morbi 
tortor sapien, congue sit amet iaculis at, suscipit eget orci. Nullam eget lectus nec erat venenatis venenatis et in massa. Phasellus 
nec tincidunt erat, sit amet consequat neque. Sed at egestas tellus, et pretium nunc. Etiam sed purus ac magna tristique egestas. 
Curabitur posuere commodo libero ac condimentum. In commodo tellus velit, a elementum urna condimentum in. Nunc commodo lectus purus, 
eget luctus velit vulputate sed.'''
