import './Pagination.css';

function Pagination({ currentPage, totalPages, hasPrev, hasNext, onPageChange }) {
    return (
        <div className="pagination">
            <button
                className="btn btn-ghost pagination-btn"
                disabled={!hasPrev}
                onClick={() => onPageChange(currentPage - 1)}
            >
                <span className="pagination-arrow">←</span>
                <span className="pagination-text">Previous</span>
            </button>

            <div className="pagination-info">
                <span className="current-page">{currentPage}</span>
                <span className="page-separator">/</span>
                <span className="total-pages">{totalPages || 1}</span>
            </div>

            <button
                className="btn btn-ghost pagination-btn"
                disabled={!hasNext}
                onClick={() => onPageChange(currentPage + 1)}
            >
                <span className="pagination-text">Next</span>
                <span className="pagination-arrow">→</span>
            </button>
        </div>
    );
}

export default Pagination;
