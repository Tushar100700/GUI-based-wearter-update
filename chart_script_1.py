import plotly.graph_objects as go
import pandas as pd

# Create the data with shortened names (15 char limit)
data = [
  {"Step": 1, "Task": "Setup Env", "Time": 30},
  {"Step": 2, "Task": "Get API Key", "Time": 15},
  {"Step": 3, "Task": "Design GUI", "Time": 60},
  {"Step": 4, "Task": "API Connect", "Time": 45},
  {"Step": 5, "Task": "Show Weather", "Time": 45},
  {"Step": 6, "Task": "Handle Errors", "Time": 30},
  {"Step": 7, "Task": "Test & Debug", "Time": 60},
  {"Step": 8, "Task": "Add Features", "Time": 120}
]

df = pd.DataFrame(data)

# Create vertical flowchart layout
x_pos = [2] * 8  # All centered on x=2
y_pos = [8, 7, 6, 5, 4, 3, 2, 1]  # Vertical descending flow

fig = go.Figure()

# Colors for each step
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454']

# Add flowchart boxes as scatter points with text
for i, (task, time) in enumerate(zip(df['Task'], df['Time'])):
    fig.add_trace(go.Scatter(
        x=[x_pos[i]],
        y=[y_pos[i]],
        mode='markers+text',
        marker=dict(
            size=80,
            color=colors[i],
            symbol='square',
            line=dict(width=2, color='white')
        ),
        text=f"{i+1}. {task}<br>{time}min",
        textposition="middle center",
        textfont=dict(size=11, color='white', family="Arial Black"),
        showlegend=False,
        hovertemplate=f'Step {i+1}: {task}<br>Time: {time} min<extra></extra>'
    ))

# Add connecting arrows between steps
for i in range(len(y_pos)-1):
    # Add arrow line
    fig.add_annotation(
        x=x_pos[i], y=y_pos[i]-0.25,
        ax=x_pos[i+1], ay=y_pos[i+1]+0.25,
        arrowhead=2, arrowsize=1.5, arrowwidth=3, 
        arrowcolor='#666666',
        showarrow=True,
        text=""
    )

fig.update_layout(
    title='Weather App Dev Process',
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[1, 3]),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0.5, 8.5])
)

fig.update_traces(cliponaxis=False)

# Save the chart as both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")