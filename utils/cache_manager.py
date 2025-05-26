import streamlit as st
import json
from datetime import datetime
from typing import List, Dict

class CacheManager:
    def __init__(self):
        self.search_history_key = "search_history"
        self.max_history = 10
        
    def add_to_search_history(self, symbol: str):
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []
        
        history = st.session_state.search_history
        symbol = symbol.upper()
        
        if symbol in history:
            history.remove(symbol)
        
        history.insert(0, symbol)
        
        if len(history) > self.max_history:
            history = history[:self.max_history]
        
        st.session_state.search_history = history
    
    def get_search_history(self) -> List[str]:
        return st.session_state.get('search_history', [])
    
    def clear_search_history(self):
        st.session_state.search_history = []
    
    def save_user_preferences(self, preferences: Dict):
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        
        st.session_state.user_preferences.update(preferences)
    
    def get_user_preferences(self) -> Dict:
        return st.session_state.get('user_preferences', {
            'theme': 'light',
            'default_period': '1y',
            'auto_refresh': False,
            'show_technical_indicators': True
        })