import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
from urllib.request import urlopen
import requests
import gzip
from pathlib import Path
from io import BytesIO

# funcao que gera um grafico de total de casos 
# confirmados + novos casos por dia
def plot1(datafull):
  datagroup = datafull[(datafull.city.isna())].groupby(['date']).sum().reset_index()
  datagroup['date'] = range(len(datagroup['date'].values))

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=datagroup['date'], 
                          y=datagroup['last_available_confirmed'], 
                          mode='lines+markers', 
                          name="Total de casos confirmados"))
  fig.add_trace(go.Bar(x=datagroup['date'], 
                      y=datagroup['new_confirmed'],
                      name="Novos casos confirmados"))
  fig.update_layout(yaxis_type='log')

  return plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)


# funcao para gerar grafico de casos totais, agrupados por estado
# em escala logaritmica
def plot2(datafull):
  colores = ['aliceblue', 'azure', 'beige', 'bisque', 'black', 
           'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 
           'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 
           'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 
           'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 
           'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 
           'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 
           'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 
           'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 
           'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 
           'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 
           'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 
           'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
           'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 
           'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 
           'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 
           'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 
           'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 
           'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 
           'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 
           'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 
           'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 
           'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 
           'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 
           'violet', 'wheat', 'yellow', 'yellowgreen']

  datastates = datafull[(datafull.city.isna())]
  datagroup = datastates.groupby([datastates.date, datastates.state, datastates.last_available_confirmed]).sum().reset_index()

  col = np.random.choice(colores, 28)

  fig = go.Figure()
  values = list(range(27))

  for e, st in enumerate(datagroup.state.unique()):
    datasta = datagroup[datagroup['state'] == st]
    fig.add_trace(go.Scatter(x=datasta['date'], y=datasta['last_available_confirmed'], 
                                  mode='lines+markers', name=st, line_color=col[e])) 
  fig.update_layout(yaxis_type='log')

  return plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)

# funcao para gerar heatmap do brasil de casos confirmados por municipio
# por 100k habitantes
def plot3(datafull, geo_data):
  datacity = datafull[(datafull.city.isna() ==  False) & (datafull.is_last)]

  datagroup = datacity.groupby([datacity.city_ibge_code, datacity.city]).last_available_confirmed_per_100k_inhabitants.max().reset_index()

  datagroup['city_ibge_code'] = datagroup['city_ibge_code'].astype(int)
  datagroup['city_ibge_code'] = datagroup['city_ibge_code'].astype(str)
  datagroup['last_available_confirmed_per_100k_inhabitants'] = \
            datagroup['last_available_confirmed_per_100k_inhabitants'].fillna(0) 

  maxvalue = datagroup[datagroup['last_available_confirmed_per_100k_inhabitants'] != 0]
  maxvalue = maxvalue.quantile(0.95)[0]
  
  fig = px.choropleth_mapbox(datagroup, geojson=geo_data, locations='city_ibge_code', 
                            color='last_available_confirmed_per_100k_inhabitants',
                            color_continuous_scale="Viridis",
                            featureidkey="properties.id",
                            range_color=(0, maxvalue + 1),
                            mapbox_style="carto-positron",
                            opacity=0.5,
                            center={"lat":-12.98, "lon":-50.45},
                            zoom = 3,
                            labels={
                              'last_available_confirmed_per_100k_inhabitants':'Confirmados por 100k'
                            })

  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

  return plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)

# funcao que cria a lista de graficos quie serao inseridos no html
# devido ao custo de gerar os graficos, eles estao sendo pre 
# computados
def plots_list():
  plots = []

  for plot in ['graph1.html', 'graph2.html', 'graph3.html']:
    with open(Path('website/plots').absolute() / plot) as f:
      plots.append(f.read())

  titles = [
    'Evolução de total de casos confirmados no desde primeiro caso confirmado no brasil',
    'Evolução de total de casos confirmados por estado',
    'Total de casos confirmados por 100\'000 habitantes em cada município'
  ]
  return zip(titles, plots)

# driver para gerar os aquivos pre-computados
def main():
  data_link = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'

  data = requests.get(data_link)

  with gzip.GzipFile(fileobj=BytesIO(data.content)) as data_file:
    datafull = pd.read_csv(data_file, encoding='utf-8')

  datafull = pd.DataFrame(data=datafull)

  print(len(datafull))

  sns.set(style="darkgrid")
  with open('geojs-100-mun.json', encoding='latin-1') as fh:
      geo_data = json.load(fh)

  with open('graph1.html', 'w+') as f:
    f.write(plot1(datafull))

  with open('graph2.html', 'w+') as f:
    f.write(plot2(datafull))

  with open('graph3.html', 'w+') as f:
    f.write(plot3(datafull, geo_data))


if __name__ == '__main__':
  main()