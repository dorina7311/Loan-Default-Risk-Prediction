import plotly.graph_objects as go
import plotly.express as px
from ui.config.settings import COLORS

def create_default_gauge(probability: float) -> go.Figure:
    """
    Create gauge chart for default probability visualization.
    
    Args:
        probability: Probability value between 0 and 1
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Default Probability (%)", 'font': {'color': '#000000', 'size': 18, 'family': 'Arial, sans-serif'}},
        number={'font': {'size': 32, 'color': '#000000', 'family': 'Arial, sans-serif'}},
        delta={'reference': 50, 'font': {'size': 16, 'color': '#DC143C'}},
        gauge={
            'axis': {'range': [None, 100], 'tickfont': {'size': 12, 'color': '#000000'}},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': COLORS['success']},
                {'range': [30, 50], 'color': COLORS['warning']},
                {'range': [50, 70], 'color': COLORS['danger']},
                {'range': [70, 100], 'color': COLORS['dark_danger']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    )])
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=60, b=15),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#000000')
    )
    return fig

def create_probability_stacked_bar(prob_default: float, prob_no_default: float) -> go.Figure:
    """
    Create stacked bar chart for probability comparison.
    
    Args:
        prob_default: Probability of default
        prob_no_default: Probability of no default
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(data=[
        go.Bar(name='No Default', x=['Probability'], y=[prob_no_default * 100], marker_color=COLORS['success'], marker_line_color='#000', marker_line_width=1.5),
        go.Bar(name='Default', x=['Probability'], y=[prob_default * 100], marker_color=COLORS['danger'], marker_line_color='#000', marker_line_width=1.5)
    ])
    fig.update_layout(
        barmode='stack',
        height=320,
        yaxis_title="Probability (%)",
        yaxis=dict(title_font=dict(size=14, color='#000000'), tickfont=dict(size=12, color='#000000')),
        xaxis=dict(tickfont=dict(size=12, color='#000000')),
        title={'text': 'Probability Breakdown', 'font': {'color': '#000000', 'size': 16, 'family': 'Arial, sans-serif'}},
        showlegend=True,
        legend=dict(font=dict(size=12, color='#000000'), bgcolor='rgba(255,255,255,0.7)'),
        margin=dict(l=15, r=15, t=50, b=15),
        paper_bgcolor='white',
        plot_bgcolor='rgba(240, 240, 240, 0.3)',
        font=dict(family='Arial, sans-serif', size=12, color='#000000')
    )
    return fig

def create_risk_distribution_pie(no_default_count: int, default_count: int) -> go.Figure:
    """
    Create pie chart for portfolio risk distribution.
    
    Args:
        no_default_count: Number of non-default loans
        default_count: Number of default loans
        
    Returns:
        Plotly Figure object
    """
    fig = px.pie(
        values=[no_default_count, default_count],
        names=['No Default', 'Default'],
        color_discrete_map={'No Default': COLORS['success'], 'Default': COLORS['danger']},
        title="Portfolio Risk Distribution"
    )
    fig.update_layout(
        height=400,
        title={'font': {'color': '#000000', 'size': 16, 'family': 'Arial, sans-serif'}},
        margin=dict(l=15, r=15, t=50, b=15),
        paper_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#000000'),
        showlegend=True,
        legend=dict(font=dict(size=12, color='#000000'))
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(size=12, color='white', family='Arial, sans-serif'))
    return fig

def create_risk_heatmap(categories: list, values: list) -> go.Figure:
    """
    Create heatmap for risk category visualization.
    
    Args:
        categories: List of category names
        values: List of risk values
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(data=go.Heatmap(
        z=[values],
        x=categories,
        colorscale=[[0, COLORS['success']], [0.5, COLORS['warning']], [1, COLORS['danger']]],
        showscale=True,
        colorbar=dict(title="Risk Level", tickfont=dict(size=11, color='#000000')),
        text=[[f'{v:.2f}' for v in values]],
        texttemplate='%{text}',
        textfont=dict(size=14, color='white', family='Arial, sans-serif'),
        hovertemplate='%{x}: %{z:.2f}<extra></extra>'
    ))
    fig.update_layout(
        height=300,
        title={'text': 'Risk Category Analysis', 'font': {'color': '#000000', 'size': 16, 'family': 'Arial, sans-serif'}},
        xaxis_title="Risk Category",
        xaxis=dict(title_font=dict(size=14, color='#000000'), tickfont=dict(size=12, color='#000000')),
        yaxis=dict(tickfont=dict(size=12, color='#000000')),
        margin=dict(l=15, r=15, t=50, b=15),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='#000000')
    )
    return fig

