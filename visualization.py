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
    """Create daily temperature chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Day Temperature',
        x=df['day'],
        y=df['temp_day'],
        marker_color='#1E88E5'
    ))
    
    fig.add_trace(go.Bar(
        name='Night Temperature',
        x=df['day'],
        y=df['temp_night'],
        marker_color='#90CAF9'
    ))
    
    fig.update_layout(
        title='7-Day Temperature Forecast',
        xaxis_title='Day',
        yaxis_title='Temperature (°C)',
        barmode='group',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig
