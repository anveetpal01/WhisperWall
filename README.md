(In development phase)

# Anonymous Blog Platform - Complete Project Structure

## Project Structure
```
WhisperWall/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── post.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── post.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── posts.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── post_service.py
│   ├── alembic/
│   │   └── versions/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_posts.py
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── streamlit_app.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── post_card.py
│   │   └── post_form.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── api_client.py
│   ├── config.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

### Key Features
1. **Clean Architecture**: Separation of concerns (models, schemas, services, routers)
2. **Database Migrations**: Alembic for version-controlled schema changes
3. **Environment Variables**: Secure configuration management
4. **API Versioning**: Structured endpoint versioning
5. **Error Handling**: Comprehensive exception handling
6. **Input Validation**: Pydantic schemas for data validation
7. **CORS Configuration**: Proper frontend-backend communication
8. **Logging**: Application logging for debugging and monitoring
9. **Testing**: Unit and integration tests
10. **Docker Support**: Containerization for easy deployment
11. **Rate Limiting**: Protection against abuse
12. **Pagination**: Efficient data loading for large datasets

### Application Features:
- Anonymous post creation
- Post listing with pagination
- Like functionality
- Real-time updates
- Content moderation flags
- Character limits and validation
- Responsive UI
- Error feedback


## Modules

1. Backend API (FastAPI)
2. Database models and migrations
3. Frontend application (react)
4. Configuration files
5. Docker setup
6. Testing suite


next upgrade - 
add soft delete in delete api