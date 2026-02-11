# Database Schema Diagram

## Tables

### auth_user
- id (Primary Key, AutoField)
- password (CharField)
- last_login (DateTimeField, nullable)
- is_superuser (BooleanField)
- username (CharField, unique)
- first_name (CharField)
- last_name (CharField)
- email (CharField)
- is_staff (BooleanField)
- is_active (BooleanField)
- date_joined (DateTimeField)

### auth_group
- id (Primary Key, AutoField)
- name (CharField, unique)

### auth_user_groups (Many-to-Many relationship)
- id (Primary Key, AutoField)
- user_id (ForeignKey to auth_user)
- group_id (ForeignKey to auth_group)

### candidates_candidate
- id (Primary Key, AutoField)
- user_id (OneToOneField to auth_user)
- name (CharField, max_length=100)
- email (EmailField)
- role (CharField, max_length=100)
- resume_text (TextField)
- status (CharField, max_length=20, choices=['APPLIED', 'SCREENING', 'INTERVIEW', 'HIRED', 'REJECTED'])

## Relationships
- candidates_candidate.user_id -> auth_user.id (One-to-One)
- auth_user_groups.user_id -> auth_user.id (Many-to-One)
- auth_user_groups.group_id -> auth_group.id (Many-to-One)

## Groups
- 'Recruiter': Can view all candidates, create, update, delete, move stages
- 'Candidate': Can view own candidate details/status
