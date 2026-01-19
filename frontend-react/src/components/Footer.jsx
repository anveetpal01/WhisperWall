import './Footer.css';

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p className="footer-text">
                    <span className="footer-brand">WhisperWall</span>
                    <span className="footer-separator">•</span>
                    <span>All posts are anonymous</span>
                    <span className="footer-separator">•</span>
                    <span>Be respectful 💙</span>
                </p>
                <p className="footer-copyright">
                    Built with ❤️ using React + FastAPI
                </p>
            </div>
        </footer>
    );
}

export default Footer;
