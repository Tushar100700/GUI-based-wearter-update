import plotly.graph_objects as go
import pandas as pd

# Data for the chart
data = [
    {"Framework": "Tkinter", "Ease of Use": 9, "Performance": 7, "Modern UI": 5, "Cross-platform": 8, "Learning Curve": 9},
    {"Framework": "PyQt5/6", "Ease of Use": 6, "Performance": 9, "Modern UI": 9, "Cross-platform": 9, "Learning Curve": 5},
    {"Framework": "Kivy", "Ease of Use": 7, "Performance": 8, "Modern UI": 8, "Cross-platform": 9, "Learning Curve": 6},
    {"Framework": "wxPython", "Ease of Use": 7, "Performance": 8, "Modern UI": 7, "Cross-platform": 8, "Learning Curve": 6}
]

df = pd.DataFrame(data)

# Define colors in order
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Features to plot
features = ['Ease of Use', 'Performance', 'Modern UI', 'Cross-platform', 'Learning Curve']

# Create the figure
fig = go.Figure()

# Add bars for each feature
for i, feature in enumerate(features):
    fig.add_trace(go.Bar(
        name=feature,
        y=df['Framework'],
        x=df[feature],
        orientation='h',
        marker_color=colors[i]
    ))

# Update layout
fig.update_layout(
    title='Python GUI Framework Comparison',
    xaxis_title='Score',
    yaxis_title='Framework',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes
fig.update_xaxes(range=[0, 10])
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()