import { useState, useEffect, useCallback } from 'react';
import apiClient from './services/apiClient';
import Header from './components/Header';
import PostForm from './components/PostForm';
import PostCard from './components/PostCard';
import Pagination from './components/Pagination';
import Footer from './components/Footer';
import Toast from './components/Toast';
import './App.css';

function App() {
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalPosts, setTotalPosts] = useState(0);
  const [hasPrev, setHasPrev] = useState(false);
  const [hasNext, setHasNext] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchPosts = useCallback(async (page = 1) => {
    setIsLoading(true);
    try {
      const data = await apiClient.getPosts(page);
      setPosts(data.posts || []);
      setTotalPages(data.pages || 1);
      setTotalPosts(data.total || 0);
      setHasPrev(data.has_prev || false);
      setHasNext(data.has_next || false);
      setCurrentPage(page);
    } catch (error) {
      console.error('Failed to fetch posts:', error);
      showToast('Failed to load posts. Is the backend running?', 'error');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPosts(1);
  }, [fetchPosts]);

  const handleCreatePost = async (content, authorAlias) => {
    try {
      await apiClient.createPost(content, authorAlias);
      showToast('Your whisper has been shared!', 'success');
      setCurrentPage(1);
      await fetchPosts(1);
    } catch (error) {
      showToast(error.message || 'Failed to create post', 'error');
      throw error;
    }
  };

  const handleLikePost = async (postId) => {
    try {
      await apiClient.likePost(postId);
      // Update the post in the local state
      setPosts(prevPosts =>
        prevPosts.map(post =>
          post.id === postId
            ? { ...post, likes: (post.likes || 0) + 1 }
            : post
        )
      );
    } catch (error) {
      showToast('Failed to like post', 'error');
    }
  };

  const handleFlagPost = async (postId) => {
    try {
      await apiClient.flagPost(postId);
      // Update the post in the local state
      setPosts(prevPosts =>
        prevPosts.map(post =>
          post.id === postId
            ? { ...post, is_flagged: true }
            : post
        )
      );
      showToast('Post has been flagged for review', 'info');
    } catch (error) {
      showToast('Failed to flag post', 'error');
    }
  };

  const handlePageChange = (newPage) => {
    fetchPosts(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleRefresh = () => {
    fetchPosts(currentPage);
    showToast('Feed refreshed!', 'success');
  };

  return (
    <div className="app">
      <Header totalPosts={totalPosts} />

      <main className="main-container">
        <div className="content-grid">
          {/* Posts Feed */}
          <section className="feed-section">
            <div className="section-header">
              <h2 className="section-title">
                <span>📰</span>
                Latest Whispers
              </h2>
              <button className="btn btn-ghost refresh-btn" onClick={handleRefresh}>
                🔄 Refresh
              </button>
            </div>

            {isLoading ? (
              <div className="loading-container">
                <div className="spinner large"></div>
                <p className="loading-text">Loading whispers...</p>
              </div>
            ) : posts.length === 0 ? (
              <div className="empty-state glass-card">
                <div className="empty-state-icon">💬</div>
                <h3>No whispers yet</h3>
                <p>Be the first to share something!</p>
              </div>
            ) : (
              <>
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  hasPrev={hasPrev}
                  hasNext={hasNext}
                  onPageChange={handlePageChange}
                />

                <div className="posts-list">
                  {posts.map((post, index) => (
                    <PostCard
                      key={post.id}
                      post={post}
                      onLike={handleLikePost}
                      onFlag={handleFlagPost}
                      style={{ animationDelay: `${index * 0.05}s` }}
                    />
                  ))}
                </div>

                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  hasPrev={hasPrev}
                  hasNext={hasNext}
                  onPageChange={handlePageChange}
                />
              </>
            )}
          </section>

          {/* Sidebar */}
          <aside className="sidebar">
            <PostForm onPostCreated={handleCreatePost} />
          </aside>
        </div>
      </main>

      <Footer />

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

export default App;
