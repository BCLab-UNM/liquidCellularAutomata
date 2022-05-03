import pandas as pd
import plotly.express as px

df = pd.read_csv('./agents_fixed_90.csv')

fig = px.scatter_3d(df, x = 'agents', y = 'iterations', z = 'node_degree', color = 'seed', title='90 Agents Iterations and Node Degree')
fig.show()
