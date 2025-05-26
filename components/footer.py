import streamlit as st

def render_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; font-size: 12px; color: #666;'>", unsafe_allow_html=True)
        st.markdown("**FinanceHub**")
        
        # Social links in one line
        st.markdown("[GitHub](https://github.com/archbaer)")
        
        st.caption("© 2025 FinanceHub • Data by Yahoo Finance • [Privacy](#) | [Terms](#)")
        st.markdown("</div>", unsafe_allow_html=True)