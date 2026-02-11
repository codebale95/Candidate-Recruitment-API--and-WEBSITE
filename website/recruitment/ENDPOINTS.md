# API Endpoints Documentation

## Authentication Endpoints

### POST /accounts/login/
- **Description**: Login user
- **Method**: POST
- **Form Data**:
  - username: string (required)
  - password: string (required)
- **Response**: Redirects to candidate list on success, shows form on failure

### GET /accounts/logout/
- **Description**: Logout user
- **Method**: GET
- **Response**: Redirects to login page

### GET /signup/
- **Description**: Sign up form
- **Method**: GET
- **Response**: Sign up form page

### POST /signup/
- **Description**: Create new user account
- **Method**: POST
- **Form Data**:
  - username: string (required)
  - email: string (required)
  - password1: string (required)
  - password2: string (required)
  - role: 'Candidate' or 'Recruiter' (required)
- **Response**: Redirects to candidate list on success, shows form with errors on failure

## Candidate Management Endpoints

### GET /
- **Description**: List candidates (Recruiter sees all, Candidate sees own)
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter or Candidate
- **Response**: HTML page with candidate list

### GET /<int:pk>/
- **Description**: View candidate details
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter or owner (for Candidates)
- **Parameters**:
  - pk: Candidate ID (integer)
- **Response**: HTML page with candidate details

### GET /create/
- **Description**: Create candidate form
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter or Candidate
- **Response**: HTML form for creating candidate

### POST /create/
- **Description**: Create new candidate
- **Method**: POST
- **Authentication**: Required
- **Permissions**: Recruiter or Candidate
- **Form Data**:
  - name: string (required)
  - email: string (required)
  - role: string (required)
  - resume_text: text (required)
- **Response**: Redirects to candidate detail on success

### GET /<int:pk>/update/
- **Description**: Update candidate form
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter or owner (for Candidates)
- **Parameters**:
  - pk: Candidate ID (integer)
- **Response**: HTML form pre-filled with candidate data

### POST /<int:pk>/update/
- **Description**: Update candidate
- **Method**: POST
- **Authentication**: Required
- **Permissions**: Recruiter or owner (for Candidates)
- **Parameters**:
  - pk: Candidate ID (integer)
- **Form Data**:
  - name: string (required)
  - email: string (required)
  - role: string (required)
  - resume_text: text (required)
- **Response**: Redirects to candidate detail on success

### GET /<int:pk>/delete/
- **Description**: Delete candidate confirmation
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter only
- **Parameters**:
  - pk: Candidate ID (integer)
- **Response**: HTML confirmation page

### POST /<int:pk>/delete/
- **Description**: Delete candidate
- **Method**: POST
- **Authentication**: Required
- **Permissions**: Recruiter only
- **Parameters**:
  - pk: Candidate ID (integer)
- **Response**: Redirects to candidate list on success

### GET /<int:pk>/move/
- **Description**: Move candidate stage form
- **Method**: GET
- **Authentication**: Required
- **Permissions**: Recruiter only
- **Parameters**:
  - pk: Candidate ID (integer)
- **Response**: HTML form for selecting new status

### POST /<int:pk>/move/
- **Description**: Move candidate to new stage
- **Method**: POST
- **Authentication**: Required
- **Permissions**: Recruiter only
- **Parameters**:
  - pk: Candidate ID (integer)
- **Form Data**:
  - status: 'APPLIED' | 'SCREENING' | 'INTERVIEW' | 'HIRED' | 'REJECTED' (required)
- **Response**: Redirects to candidate detail on success

## Pipeline Stages
Candidates move through these sequential stages:
1. APPLIED (default)
2. SCREENING
3. INTERVIEW
4. HIRED or REJECTED

## Role-Based Access Control (RBAC)
- **Candidate**: Can view own candidate details/status, create/update own candidate
- **Recruiter**: Can view all candidates, create/update/delete any candidate, move candidates through stages
