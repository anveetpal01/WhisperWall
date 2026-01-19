import { useState } from 'react';
import './PostForm.css';

function PostForm({ onPostCreated }) {
    const [content, setContent] = useState('');
    const [authorAlias, setAuthorAlias] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const maxChars = 5000;
    const charCount = content.length;
    const isOverLimit = charCount > maxChars;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!content.trim()) {
            setError('Please write something to share!');
            return;
        }

        if (isOverLimit) {
            setError('Your post is too long!');
            return;
        }

        setIsSubmitting(true);

        try {
            await onPostCreated(content.trim(), authorAlias.trim() || 'Anonymous');
            setContent('');
            setAuthorAlias('');
        } catch (err) {
            setError(err.message || 'Failed to create post. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="post-form-container glass-card">
            <h2 className="form-title">
                <span className="form-icon">✍️</span>
                Share Your Thoughts
            </h2>

            <form onSubmit={handleSubmit} className="post-form">
                <div className="form-group">
                    <textarea
                        className="textarea"
                        placeholder="What's on your mind? Share anonymously..."
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        disabled={isSubmitting}
                    />
                    <div className={`char-counter ${isOverLimit ? 'over-limit' : ''}`}>
                        {charCount.toLocaleString()} / {maxChars.toLocaleString()}
                    </div>
                </div>

                <div className="form-group">
                    <input
                        type="text"
                        className="input"
                        placeholder="Your name (optional - defaults to Anonymous)"
                        value={authorAlias}
                        onChange={(e) => setAuthorAlias(e.target.value)}
                        maxLength={50}
                        disabled={isSubmitting}
                    />
                </div>

                {error && (
                    <div className="form-error">
                        <span className="error-icon">⚠️</span>
                        {error}
                    </div>
                )}

                <button
                    type="submit"
                    className="btn btn-primary submit-btn"
                    disabled={isSubmitting || !content.trim()}
                >
                    {isSubmitting ? (
                        <>
                            <span className="spinner"></span>
                            Posting...
                        </>
                    ) : (
                        <>
                            <span>📤</span>
                            Post Anonymously
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}

export default PostForm;
