# Candidate Management API

A Django REST API with frontend for managing candidate journey from application to hiring.

## Features

- **Candidate Management**: CRUD operations for candidates (Name, Email, Role, Resume text)
- **Fixed Pipeline**: Sequential stages - APPLIED → SCREENING → INTERVIEW → HIRED/REJECTED
- **Role-Based Access Control**:
  - **Candidate**: View own application status
  - **Recruiter**: View all candidates, move to next stage, reject candidates
- **REST API**: Full CRUD with proper authentication and permissions
- **Web Frontend**: Basic UI for login, candidate management, and stage progression

## Tech Stack

- **Backend**: Django 5.2.11, Django REST Framework
- **Database**: SQLite (switched from MySQL due to setup issues)
- **Frontend**: Django Templates, Bootstrap 5
- **Authentication**: Session-based with custom User model

## API Endpoints

### Authentication
- `POST /api/login/` - Login (web view)
- `POST /api/logout/` - Logout (web view)

### Candidates API
- `GET /api/candidates/` - List candidates (filtered by role)
- `POST /api/candidates/` - Create candidate (recruiters only)
- `GET /api/candidates/{id}/` - Get candidate details
- `PUT /api/candidates/{id}/` - Update candidate (recruiters only)
- `DELETE /api/candidates/{id}/` - Delete candidate (recruiters only)
- `POST /api/candidates/{id}/move_to_next_stage/` - Move to next stage (recruiters only)
- `POST /api/candidates/{id}/reject/` - Reject candidate (recruiters only)

### Web Views
- `GET /api/candidates/` - Candidate list dashboard
- `GET /api/candidates/create/` - Create candidate form
- `GET /api/candidates/{id}/update/` - Update candidate form
- `POST /api/candidates/{id}/move/` - Move to next stage (web)
- `POST /api/candidates/{id}/reject/` - Reject candidate (web)

## Database Schema

```
User (Custom Model)
├── id (AutoField, Primary Key)
├── username (CharField, unique)
├── email (EmailField)
├── role (CharField: 'candidate' or 'recruiter')
├── password (CharField, hashed)
├── is_active (BooleanField)
├── is_staff (BooleanField)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)

Candidate
├── id (AutoField, Primary Key)
├── name (CharField)
├── email (EmailField)
├── role (CharField, e.g., 'Software Engineer')
├── resume (TextField)
├── stage (CharField: 'applied', 'screening', 'interview', 'hired', 'rejected')
├── created_at (DateTimeField, auto_now_add)
└── updated_at (DateTimeField, auto_now)
```

## Setup Instructions

1. **Clone and Install Dependencies**:
   ```bash
   cd candidate_management
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Create Test Users**:
   ```bash
   python manage.py shell -c "
   from candidates.models import User
   User.objects.create_user('recruiter', 'recruiter@example.com', 'pass123', role='recruiter')
   User.objects.create_user('candidate', 'candidate@example.com', 'pass123', role='candidate')
   "
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access Application**:
   - Web Interface: http://127.0.0.1:8000/api/candidates/
   - API: http://127.0.0.1:8000/api/candidates/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

### As a Recruiter
1. Login with recruiter credentials
2. View all candidates in the pipeline
3. Create new candidates
4. Move candidates through stages (Applied → Screening → Interview → Hired)
5. Reject candidates at any stage

### As a Candidate
1. Login with candidate credentials
2. View only your own application status
3. Cannot modify or view other candidates

## API Testing

Use tools like Postman or curl to test the API:

```bash
# Get candidates (authenticated)
curl -H "Authorization: Basic <base64-encoded-credentials>" http://127.0.0.1:8000/api/candidates/

# Create candidate
curl -X POST -H "Authorization: Basic <base64-encoded-credentials>" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","role":"Developer","resume":"Experienced developer"}' \
  http://127.0.0.1:8000/api/candidates/
```

## Security Features

- Session-based authentication
- Role-based permissions
- CSRF protection on web forms
- Password hashing
- Input validation through serializers

## Future Enhancements

- Email notifications for stage changes
- File upload for resumes
- Advanced filtering and search
- Audit logging
- API rate limiting
- JWT authentication option
