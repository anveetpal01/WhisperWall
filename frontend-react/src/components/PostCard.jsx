import { useState } from 'react';
import './PostCard.css';

function PostCard({ post, onLike, onFlag }) {
    const [isLiking, setIsLiking] = useState(false);
    const [isFlagging, setIsFlagging] = useState(false);

    const handleLike = async () => {
        if (isLiking) return;
        setIsLiking(true);
        try {
            await onLike(post.id);
        } finally {
            setIsLiking(false);
        }
    };

    const handleFlag = async () => {
        if (isFlagging || post.is_flagged) return;
        setIsFlagging(true);
        try {
            await onFlag(post.id);
        } finally {
            setIsFlagging(false);
        }
    };

    const getTimeAgo = (dateString) => {
        if (!dateString) return 'Recently';

        try {
            const date = new Date(dateString);
            const now = new Date();
            const seconds = Math.floor((now - date) / 1000);

            if (seconds < 60) return 'just now';
            if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
            if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
            if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;

            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
            });
        } catch {
            return 'Recently';
        }
    };

    const getAvatarGradient = (name) => {
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        ];
        const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
        return colors[hash % colors.length];
    };

    const getInitials = (name) => {
        if (!name || name === 'Anonymous') return '?';
        return name.charAt(0).toUpperCase();
    };

    return (
        <article className={`post-card glass-card fade-in ${post.is_flagged ? 'flagged' : ''}`}>
            <div className="post-header">
                <div className="author-section">
                    <div
                        className="author-avatar"
                        style={{ background: getAvatarGradient(post.author_alias || 'Anonymous') }}
                    >
                        {getInitials(post.author_alias)}
                    </div>
                    <div className="author-info">
                        <span className="author-name">
                            {post.author_alias || 'Anonymous'}
                            {post.is_flagged && <span className="flagged-badge">🚩 Flagged</span>}
                        </span>
                        <span className="post-time">{getTimeAgo(post.created_at)}</span>
                    </div>
                </div>
            </div>

            <div className="post-content">
                <p>{post.content}</p>
            </div>

            <div className="post-actions">
                <button
                    className={`btn-action btn-like ${isLiking ? 'loading' : ''}`}
                    onClick={handleLike}
                    disabled={isLiking}
                    title="Like this post"
                >
                    <span className="action-icon">❤️</span>
                    <span className="action-count">{post.likes || 0}</span>
                </button>

                {!post.is_flagged && (
                    <button
                        className={`btn-action btn-flag ${isFlagging ? 'loading' : ''}`}
                        onClick={handleFlag}
                        disabled={isFlagging}
                        title="Flag for moderation"
                    >
                        <span className="action-icon">🚩</span>
                        <span className="action-label">Flag</span>
                    </button>
                )}
            </div>
        </article>
    );
}

export default PostCard;
