const API_BASE_URL = 'https://whisperwall-ultimate-project-backend.onrender.com/';

/**
 * API Client for WhisperWall Backend
 */
class APIClient {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Make HTTP request with error handling
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * Get paginated posts
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Posts per page (default: 20)
   * @returns {Promise<{posts: Array, total: number, pages: number, has_prev: boolean, has_next: boolean}>}
   */
  async getPosts(page = 1, limit = 20) {
    const params = new URLSearchParams({ page, limit });
    return this.request(`/posts?${params}`);
  }

  /**
   * Create a new post
   * @param {string} content - Post content
   * @param {string} authorAlias - Author name (default: "Anonymous")
   * @returns {Promise<Object>} Created post object
   */
  async createPost(content, authorAlias = 'Anonymous') {
    return this.request('/posts', {
      method: 'POST',
      body: JSON.stringify({
        content,
        author_alias: authorAlias,
      }),
    });
  }

  /**
   * Like a post
   * @param {number} postId - ID of the post to like
   * @returns {Promise<Object>} Updated post object
   */
  async likePost(postId) {
    return this.request(`/posts/${postId}/like`, {
      method: 'POST',
    });
  }

  /**
   * Flag a post for moderation
   * @param {number} postId - ID of the post to flag
   * @returns {Promise<Object>} Updated post object
   */
  async flagPost(postId) {
    return this.request(`/posts/${postId}/flag`, {
      method: 'POST',
    });
  }
}

// Export singleton instance
const apiClient = new APIClient();
export default apiClient;
export { APIClient };
