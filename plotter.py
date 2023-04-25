import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc


df = pd.read_csv('data.csv')

app = Dash(__name__)
fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=df["time"], y=df["speed"], mode="lines", name="speed"))
fig1.add_trace(go.Scatter(x=df["time"], y=df["target_speed"], mode="lines", name="target_speed"))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["time"], y=df["force"], mode="lines", name="Force"))
fig2.add_trace(go.Scatter(x=df["time"], y=df["target_force"], mode="lines", name="Target Force"))

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["time"], y=df["error"], mode="lines", name="Error"))
fig3.add_trace(go.Scatter(x=df["time"], y=df["error_int"], mode="lines", name="Error Int"))


app.layout = html.Div(children=[
    html.Div([
        html.H1(children='PID results', style={'textAlign':'center'}),
        dcc.Graph(figure=fig1)
    ]),
    html.Div([
        html.H1(children='Force', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig2)
    ]),
    html.Div([
        html.H1(children='Error', style={'textAlign': 'center'}),
        dcc.Graph(figure=fig3)
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)