import streamlit as st
from datetime import datetime
import time

from utils.api_client import APIClient
from components.post_card import render_post_card
from components.post_form import render_post_form

# Page configuration
st.set_page_config(
    page_title="Anonymous Blog",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .post-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .post-meta {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .like-button {
        color: #dc3545;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient()

api = get_api_client()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'posts' not in st.session_state:
    st.session_state.posts = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

def main():
    # Header
    st.markdown('<h1 class="main-header">📝 Anonymous Blog</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("✍️ Share Your Thoughts")
        render_post_form(api)
        
        # Refresh button
        st.markdown("---")
        if st.button("🔄 Refresh Feed", use_container_width=True):
            st.session_state.posts = None
            st.rerun()
        
        # Stats
        if st.session_state.posts:
            st.markdown("---")
            st.metric("Total Posts", st.session_state.posts['total'])
    
    with col1:
        st.subheader("📰 Latest Posts")
        
        # Pagination controls at top
        pagination_col1, pagination_col2, pagination_col3 = st.columns([1, 2, 1])
        
        with pagination_col1:
            if st.button("⬅️ Previous", disabled=not (st.session_state.posts and st.session_state.posts['has_prev'])):
                st.session_state.page -= 1
                st.session_state.posts = None
                st.rerun()
        
        with pagination_col2:
            if st.session_state.posts:
                st.write(f"Page {st.session_state.page} of {st.session_state.posts['pages']}")
        
        with pagination_col3:
            if st.button("Next ➡️", disabled=not (st.session_state.posts and st.session_state.posts['has_next'])):
                st.session_state.page += 1
                st.session_state.posts = None
                st.rerun()
        
        st.markdown("---")
        
        # Fetch and display posts
        if st.session_state.posts is None or time.time() - st.session_state.last_refresh > 60:
            with st.spinner("Loading posts..."):
                st.session_state.posts = api.get_posts(page=st.session_state.page)
                st.session_state.last_refresh = time.time()
        
        if st.session_state.posts and st.session_state.posts['posts']:
            for post in st.session_state.posts['posts']:
                render_post_card(post, api)
        else:
            st.info("No posts yet. Be the first to share something!")
        
        # Pagination controls at bottom
        st.markdown("---")
        pagination_col1, pagination_col2, pagination_col3 = st.columns([1, 2, 1])
        
        with pagination_col1:
            if st.button("⬅️ Prev", disabled=not (st.session_state.posts and st.session_state.posts['has_prev']), key="prev_bottom"):
                st.session_state.page -= 1
                st.session_state.posts = None
                st.rerun()
        
        with pagination_col3:
            if st.button("Next ➡️", disabled=not (st.session_state.posts and st.session_state.posts['has_next']), key="next_bottom"):
                st.session_state.page += 1
                st.session_state.posts = None
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6c757d; padding: 2rem;'>
            <p>Anonymous Blog Platform | All posts are anonymous | Be respectful 💙</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()