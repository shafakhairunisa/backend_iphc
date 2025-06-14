# IPHC Backend API

A FastAPI-based backend for the Intelligent Personal Health Care (IPHC) application that provides medical prediction services using machine learning and medical logic.

## Features

- 🔐 User authentication and management
- 🏥 Medical symptom analysis and disease prediction
- 📊 Health assessment with ML-driven insights
- 💾 Document storage and management
- 🔍 Disease information lookup
- 📋 Allergy management
- 📈 Prediction history tracking

## Technology Stack

- **Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **ML**: Scikit-learn for medical predictions
- **Authentication**: JWT-based authentication
- **CORS**: Enabled for cross-origin requests

## Quick Start

### Prerequisites
- Python 3.8+
- MySQL database
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/shafakhairunisa/backend_iphc.git
cd backend_iphc

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database configuration

# Run the application
python app.py
```

### Environment Variables

Create a `.env` file with the following variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=iphc_db
DB_USER=your_username
DB_PASS=your_password
```

## API Endpoints

### Authentication
- `POST /users/register` - User registration
- `POST /users/login` - User login
- `POST /users/forgot-password` - Request password reset
- `POST /users/verify-otp` - Verify OTP
- `POST /users/reset-password` - Reset password

### User Management
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user profile

### Medical Predictions
- `POST /predict/` - Make disease prediction
- `GET /predict/history/{user_id}` - Get prediction history
- `DELETE /predict/{predict_id}` - Delete prediction
- `GET /predict/symptoms` - Get available symptoms

### Health Information
- `GET /api/disease/{disease_name}` - Get disease information
- `GET /allergies` - Get allergy list

### Document Management
- `POST /documents/upload` - Upload document
- `GET /documents/user/{user_id}` - Get user documents
- `DELETE /documents/{document_id}` - Delete document

## Development

### Running Tests
```bash
python test_medical_logic.py
```

### API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Project Structure
```
backend/
├── app.py                 # Main application entry point
├── config/
│   └── database.py       # Database configuration
├── models/               # SQLAlchemy models
├── routes/               # API route handlers
├── services/             # Business logic
├── controllers/          # Request/response handling
└── requirements.txt      # Python dependencies
```

## Medical Logic

The prediction system combines:
- **Machine Learning**: Scikit-learn models trained on medical data
- **Rule-based Logic**: Medical expertise encoded as business rules
- **Symptom Analysis**: 75+ supported symptoms with intelligent filtering
- **Risk Assessment**: Severity and duration-based scoring

## Database Schema

The application uses MySQL with the following main tables:
- `users` - User profiles and authentication
- `predictions` - Medical prediction history
- `diseases` - Disease information database
- `allergies` - Allergy reference data
- `documents` - User document storage

## Deployment

### Local Development
```bash
python app.py
# Server runs on http://localhost:8000
```

### Production Deployment
Recommended platforms:
- Railway
- Render
- Heroku
- DigitalOcean App Platform
- AWS/Google Cloud/Azure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the GitHub repository.

---

**Note**: This is a medical assistance tool and should not replace professional medical advice. Always consult healthcare providers for medical decisions.
