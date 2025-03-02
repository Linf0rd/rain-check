import plotly.graph_objects as go
import plotly.express as px

def create_hourly_temp_chart(df):
    """Create hourly temperature chart"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['hour'],
        y=df['temp'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#1E88E5', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title='Hourly Temperature Forecast',
        xaxis_title='Hour',
        yaxis_title='Temperature (°C)',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def create_daily_temp_chart(df):
    """Create daily temperature chart with min/max range"""
    fig = go.Figure()

    # Add range area for temperature
    fig.add_trace(go.Bar(
        name='Temperature Range',
        x=df['day'],
        y=df['temp_day'],
        base=df['temp_night'],
        marker_color='rgba(30, 136, 229, 0.3)',
        hovertemplate='High: %{y}°C<br>Low: %{base}°C<extra></extra>'
    ))

    # Add lines for max and min temperatures
    fig.add_trace(go.Scatter(
        name='Max Temperature',
        x=df['day'],
        y=df['temp_day'],
        mode='lines+markers',
        line=dict(color='#FF4B4B', width=2),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        name='Min Temperature',
        x=df['day'],
        y=df['temp_night'],
        mode='lines+markers',
        line=dict(color='#4B9FFF', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title='7-Day Temperature Forecast',
        xaxis_title='Day',
        yaxis_title='Temperature (°C)',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig