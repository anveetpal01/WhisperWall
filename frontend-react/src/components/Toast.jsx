import './Toast.css';

function Toast({ message, type = 'info', onClose }) {
    return (
        <div className={`toast ${type}`}>
            <span className="toast-icon">
                {type === 'success' && '✅'}
                {type === 'error' && '❌'}
                {type === 'info' && 'ℹ️'}
            </span>
            <span className="toast-message">{message}</span>
            <button className="toast-close" onClick={onClose}>
                ✕
            </button>
        </div>
    );
}

export default Toast;
