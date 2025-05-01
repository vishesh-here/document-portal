# Document Portal

A Flask-based web application for managing and selling documents with user authentication.

## Features

- User authentication (regular users and admin)
- Document management system
- Document preview and purchase functionality
- Skeuomorphic UI design
- SQLite database for data storage

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## Login Credentials

Regular User:
- Email: user@example.com
- Password: password123

Admin User:
- Email: admin@example.com
- Password: admin123

Document Access Password: 1234

## Deployment

This application is ready to be deployed on Render.com. Follow these steps:

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Configure the environment variables:
   - SECRET_KEY
   - PYTHON_VERSION: 3.9.0

## License

MIT License