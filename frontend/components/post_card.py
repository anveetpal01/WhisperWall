import streamlit as st
from datetime import datetime


def render_post_card(post, api):
    """Render a single post card"""
    with st.container():
        # Post header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            author = post.get('author_alias', 'Anonymous')
            if post.get('is_flagged'):
                st.markdown(f"**👤 {author}** 🚩 *Flagged*")
            else:
                st.markdown(f"**👤 {author}**")
        
        with col2:
            created_at = post.get('created_at')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    time_ago = get_time_ago(dt)
                    st.markdown(f"*{time_ago}*")
                except:
                    st.markdown("*Recently*")
        
        # Post content
        st.markdown(f"<div class='post-card'>{post['content']}</div>", unsafe_allow_html=True)
        
        # Post actions
        action_col1, action_col2, action_col3, action_col4 = st.columns([1, 1, 1, 3])
        
        with action_col1:
            if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                try:
                    api.like_post(post['id'])
                    st.session_state.posts = None  # Refresh posts
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with action_col2:
            if not post.get('is_flagged'):
                if st.button("🚩 Flag", key=f"flag_{post['id']}"):
                    try:
                        api.flag_post(post['id'])
                        st.session_state.posts = None  # Refresh posts
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        st.markdown("---")


def get_time_ago(dt):
    """Convert datetime to human-readable time ago"""
    now = datetime.now(dt.tzinfo)
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}m ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}h ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days}d ago"
    else:
        return dt.strftime("%b %d, %Y")