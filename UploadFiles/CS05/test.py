import plotly.graph_objs as go
import plotly.offline as pyo

# Define the data for the pie chart
pie_labels = ['Category A', 'Category B', 'Category C']
pie_values = [20, 35, 50]

# Create the trace for the pie chart
pie_trace = go.Pie(
        labels=pie_labels,
        values=pie_values,
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
    )

# Create the layout for the pie chart
pie_layout = go.Layout(
title='My Pie Chart'
)

# Create the figure for the pie chart
pie_fig = go.Figure(data=[pie_trace], layout=pie_layout)
div = pyo.plot(pie_fig ,output_type='div')
html = '<div>{}</div>'.format(div)
