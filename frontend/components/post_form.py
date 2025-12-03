import streamlit as st


def render_post_form(api):
    """Render the form to create a new post"""
    with st.form("new_post_form", clear_on_submit=True):
        content = st.text_area(
            "What's on your mind?",
            placeholder="Share your thoughts anonymously...",
            max_chars=5000,
            height=150,
            help="Write anything you'd like to share (max 5000 characters)"
        )
        
        author_alias = st.text_input(
            "Name (optional)",
            placeholder="Anonymous",
            max_chars=50,
            help="Leave blank to post as 'Anonymous'"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            submitted = st.form_submit_button("📤 Post", use_container_width=True)
        
        with col1:
            if content:
                st.caption(f"{len(content)}/5000 characters")
        
        if submitted:
            if not content or not content.strip():
                st.error("⚠️ Post content cannot be empty!")
            elif len(content) > 5000:
                st.error("⚠️ Post is too long! Maximum 5000 characters.")
            else:
                try:
                    with st.spinner("Posting..."):
                        api.create_post(
                            content=content.strip(),
                            author_alias=author_alias.strip() if author_alias else "Anonymous"
                        )
                    st.success("✅ Post created successfully!")
                    st.session_state.posts = None  # Clear cache to refresh
                    st.session_state.page = 1  # Go back to first page
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")