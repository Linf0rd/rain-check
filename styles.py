import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .weather-card {
            background-color: #fff;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        .weather-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .temp-text {
            font-size: 2rem;
            font-weight: bold;
            color: #1E88E5;
        }
        
        .condition-text {
            font-size: 1.2rem;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .weather-card {
                padding: 1rem;
            }
            
            .weather-icon {
                font-size: 2rem;
            }
            
            .temp-text {
                font-size: 1.5rem;
            }
            
            .condition-text {
                font-size: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def get_weather_icon(condition):
    """Return Font Awesome icon class based on weather condition"""
    icons = {
        'Clear': 'fas fa-sun',
        'Clouds': 'fas fa-cloud',
        'Rain': 'fas fa-cloud-rain',
        'Snow': 'fas fa-snowflake',
        'Thunderstorm': 'fas fa-bolt',
        'Drizzle': 'fas fa-cloud-rain',
        'Mist': 'fas fa-smog'
    }
    return icons.get(condition, 'fas fa-cloud')
