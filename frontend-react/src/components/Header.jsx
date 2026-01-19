import './Header.css';

function Header({ totalPosts }) {
    return (
        <header className="header">
            <div className="header-content">
                <div className="logo-section">
                    <div className="logo-icon">
                        <span className="whisper-icon">💬</span>
                    </div>
                    <div className="logo-text">
                        <h1 className="app-title">
                            <span className="gradient-text">WhisperWall</span>
                        </h1>
                        <p className="app-tagline">Share your thoughts anonymously</p>
                    </div>
                </div>

                <div className="header-stats">
                    {totalPosts !== undefined && (
                        <div className="stat-badge">
                            <span className="stat-number">{totalPosts}</span>
                            <span className="stat-label">whispers</span>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;
