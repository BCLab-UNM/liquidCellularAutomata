import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('./results-lock.csv')

#Constrain the node_degree value to look at node_degree less than 8
df = df.loc[df['node_degree'] < 8]

#fig = px.scatter_3d(df, x = 'agents', y = 'iterations', z = 'node_degree', color = 'iterations', title='90 Agents Iterations and Node Degree')

z_data = []

#The set of all possible values for the number of agents
agents = set(df['agents'])

#The set of all possible values for the node_degree
node_degrees = set(df['node_degree'])


#Fixed radius to use
radius = 30

for agent_val in agents:
    tmp = []
    for node_degree_val in node_degrees:
        fixed_agents = df.loc[df['agents'] == agent_val]
        fixed_node_degree = fixed_agents.loc[df['node_degree'] == node_degree_val]
        fixed_radius = fixed_node_degree.loc[df['radius'] == radius]
        iteration_values = fixed_radius['iterations']
        z_point = iteration_values.mean()
        tmp.append(z_point)

    z_data.append(tmp)

print(z_data)

fig = go.Figure(data=[go.Surface(z=z_data, y=list(agents), x=list(node_degrees))])

fig.update_layout(title='Liquid Cellular Automata consensus landscape', autosize=False,
                  width=1000, height=1000,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.update_xaxes(title="Node Degrees")


fig.show()
