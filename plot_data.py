import pandas as pd
import plotly.express as px

df = pd.read_csv('./results-lock.csv')

fig = px.scatter_3d(df, x = 'agents', y = 'iterations', z = 'radius', title='Agents Iterations and Radius')
fig.show()
