# NexusCRM

NexusCRM is a professional, web-based Customer Relationship Management (CRM) system built with Django. It is designed to centralize customer and sales information, manage leads and deals, coordinate activities and tasks, provide role-based access control, maintain audit trails, and expose selected CRM functionality through a REST API.

The project is being developed as a production-oriented CRM rather than a simple CRUD demonstration. Development is organized into phases, with functionality tested and validated before moving to the next phase.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Goals](#project-goals)
3. [Core Capabilities](#core-capabilities)
4. [Technology Stack](#technology-stack)
5. [System Architecture](#system-architecture)
6. [Application Structure](#application-structure)
7. [Authentication and Authorization](#authentication-and-authorization)
8. [CRM Modules](#crm-modules)
9. [Dashboard and Search](#dashboard-and-search)
10. [Notifications and Preferences](#notifications-and-preferences)
11. [Audit Logging](#audit-logging)
12. [REST API](#rest-api)
13. [Data Model](#data-model)
14. [Role and Permission Model](#role-and-permission-model)
15. [Testing](#testing)
16. [Development Phases](#development-phases)
17. [Local Development Setup](#local-development-setup)
18. [Environment Configuration](#environment-configuration)
19. [Database and Migrations](#database-and-migrations)
20. [Running the Application](#running-the-application)
21. [API Development](#api-development)
22. [Security](#security)
23. [Performance](#performance)
24. [Production Deployment](#production-deployment)
25. [Troubleshooting](#troubleshooting)
26. [Development Guidelines](#development-guidelines)
27. [Future Roadmap](#future-roadmap)
28. [Project Status](#project-status)
29. [License](#license)

---

# Project Overview

**Project Name:** NexusCRM

**Project Type:** Customer Relationship Management System

**Primary Framework:** Django

**Primary Language:** Python

**Frontend:** HTML5, CSS3, JavaScript, Bootstrap

**Backend API:** Django REST Framework

**Database:** Django-supported relational database; SQLite is used during local development unless another database is configured.

NexusCRM provides a centralized workspace where an organization can manage its customer lifecycle from initial lead capture through sales opportunities, customer relationships, activities, follow-ups, notes, tasks, and reporting.

The application also includes user roles, permissions, notifications, preferences, audit logs, global search, and a REST API foundation for integrations.

---

# Project Goals

NexusCRM is intended to provide:

- Centralized customer information
- Structured lead management
- Sales pipeline management
- Deal/opportunity tracking
- Company and contact management
- Activity and task management
- Internal notes
- Calendar-based planning
- Notifications
- User preferences
- Role-based access control
- Auditability of important actions
- Global CRM search
- REST API access
- Automated regression testing
- A foundation suitable for production deployment
- An extensible architecture for future integrations

The long-term goal is to evolve NexusCRM from a functional CRM application into a complete, secure, maintainable business platform.

---

# Core Capabilities

## Customer Management

NexusCRM supports management of:

- Companies
- Contacts
- Leads
- Deals
- Sales pipelines
- Pipeline stages
- Activities
- Tasks
- Notes
- Tags

## Sales Management

The sales workflow supports:

- Lead creation
- Lead ownership
- Lead status management
- Lead search and filtering
- Lead estimated values
- Lead conversion
- Company/contact association
- Deal management
- Pipeline management
- Pipeline stage management
- Deal ownership
- Deal amounts
- Expected close dates
- Tags

## Productivity

The system includes:

- Activities
- Tasks
- Calendar
- Notes
- Notifications
- User preferences
- Dashboard information
- Global search

## Administration

Administrative functionality includes:

- User management
- User profiles
- Role assignment
- Role-specific permissions
- Audit logs
- System configuration foundations
- API access controls

---

# Technology Stack

NexusCRM deliberately uses a straightforward and maintainable web stack.

## Backend

### Python

Python is the primary programming language used for server-side application logic.

Responsibilities include:

- Business logic
- Database interaction
- Form processing
- Authentication
- Authorization
- Validation
- API processing
- Automated tests
- Application configuration

### Django

Django is the primary web framework.

Django provides:

- URL routing
- Views
- Templates
- ORM
- Forms
- Authentication
- Sessions
- Middleware
- CSRF protection
- Administration
- Migrations
- Testing infrastructure

The project has been developed against the Django 5.x generation, with the current development environment using Django 5.2.8.

### Django ORM

The Django ORM is used for database abstraction and relational data management.

It provides the application models for entities such as:

- Users
- Profiles
- Companies
- Contacts
- Leads
- Pipelines
- Pipeline stages
- Deals
- Activities
- Tasks
- Notes
- Tags
- Audit logs
- Notifications
- User preferences

---

# Frontend Stack

## HTML5

HTML5 provides the semantic structure of the application.

It is used for:

- Pages
- Forms
- Tables
- Navigation
- Dashboard components
- Detail pages
- Modal interfaces
- Search interfaces

## CSS3

CSS3 is used for:

- Application layout
- Dashboard styling
- Sidebar styling
- Responsive design
- Tables
- Forms
- Cards
- Navigation
- UI states
- Custom CRM styling

The application maintains custom styling on top of the Bootstrap component system.

## JavaScript

JavaScript provides client-side interaction and dynamic behavior.

It is used for functionality such as:

- Interactive UI elements
- Dynamic page behavior
- Notifications
- Search interactions
- Form-related behavior
- Dashboard/UI enhancements

## Bootstrap

Bootstrap provides the primary frontend component framework.

It is used for:

- Responsive layouts
- Grid system
- Cards
- Buttons
- Forms
- Tables
- Navigation
- Badges
- Modals
- Responsive utilities

## Bootstrap Icons

Bootstrap Icons are used throughout the application for interface elements such as:

- Dashboard
- Companies
- Contacts
- Leads
- Deals
- Tasks
- Calendar
- Notifications
- Settings
- Search

---

# API Stack

## Django REST Framework

Django REST Framework (DRF) provides the REST API layer.

It is used for:

- Serializers
- API endpoints
- Request/response handling
- API authentication
- API permissions
- JSON responses
- Integration-ready backend services

The API is organized under the `/api/v1/` namespace.

---

# Development and Testing Stack

The project uses Django's built-in testing framework together with Django REST Framework's testing facilities.

The automated test suite is organized around:

- Model tests
- Permission tests
- View tests
- API tests

Development also relies on:

- Django management commands
- Django migrations
- Django system checks
- Python virtual environments
- Git-based source control

---

# System Architecture

NexusCRM follows a conventional Django architecture.

```text
Browser
   |
   v
HTML / CSS / JavaScript / Bootstrap
   |
   v
Django URL Routing
   |
   v
Django Views
   |
   +--------------------+
   |                    |
   v                    v
Django Forms       Django REST Framework
   |                    |
   +----------+---------+
              |
              v
          Django ORM
              |
              v
        Relational Database
```

The application is organized around the `crmApp` Django application.

The main application responsibilities are separated into:

- Models
- Forms
- Views
- URLs
- Templates
- Static assets
- Permissions
- API serializers/endpoints
- Tests
- Signals
- Application configuration

---

# Application Structure

The project intentionally maintains the existing architecture rather than creating duplicate applications, template directories, static directories, URL configurations, or view modules.

The important structure is conceptually:

```text
NexusCRM/
├── manage.py
├── NexusCRM/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── crmApp/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── signals.py
│   ├── urls.py
│   ├── views.py
│   ├── api/
│   │   ├── serializers.py
│   │   └── ...
│   ├── migrations/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_permissions.py
│   │   ├── test_views.py
│   │   └── test_api.py
│   └── ...
│
├── templates/
│   └── crmApp/
│       ├── base.html
│       └── ...
│
├── static/
│   └── ...
│
└── ...
```

> The exact contents may grow as development continues. Existing project structure should always be inspected before adding new files.

## Primary Base Template

The main application base template is:

```text
templates/crmApp/base.html
```

This is the primary template used for the CRM interface.

The project should not introduce another competing base template when extending existing functionality.

---

# Authentication and Authorization

NexusCRM uses Django's authentication system for user accounts and sessions.

Users are associated with a `Profile` containing additional CRM-specific information.

## User Profile

The profile contains information including:

- User
- Role
- Phone
- Job title
- Avatar
- Created timestamp
- Updated timestamp

The profile is linked to Django's built-in `User` model through a one-to-one relationship.

The application uses a signal-based profile creation mechanism so that profiles are automatically created when appropriate users are created.

---

# User Roles

NexusCRM currently supports the following roles:

| Internal Role | Display Name |
|---|---|
| `admin` | Administrator |
| `manager` | Manager |
| `sales` | Sales Representative |
| `support` | Support |
| `viewer` | Viewer |

The default role for newly created profiles is Viewer unless explicitly assigned otherwise.

---

# Role Responsibilities

## Administrator

Designed for complete system administration.

Typical capabilities include:

- User administration
- Full CRM management
- Configuration
- Audit access
- Full record management
- Administrative operations

## Manager

Designed for management-level CRM operations.

Typical capabilities include:

- Managing CRM records
- Supervising sales activity
- Managing notes
- Reviewing customer information
- Managing deals and pipeline information
- Reviewing operational information

## Sales Representative

Designed for sales staff.

Typical capabilities include:

- Managing assigned sales records
- Creating and updating leads
- Managing appropriate customer records
- Creating notes
- Managing personal/owned records
- Working with deals and sales activities

## Support

Designed for support-oriented access.

Access is controlled according to the specific module and permission rules.

## Viewer

Designed for read-only access.

Viewers can inspect permitted information but are restricted from destructive or management operations.

---

# CRM Modules

## Dashboard

The dashboard provides an overview of CRM activity.

Current dashboard information includes areas such as:

- Lead statistics
- New leads
- Qualified leads
- Pipeline value
- CRM activity information

The dashboard is designed to provide an immediate overview of the state of the CRM.

---

# Companies

Companies represent organizations/customers in the CRM.

Company information includes fields such as:

- Name
- Industry
- Website
- Email
- Phone
- Address
- City
- Country
- Description
- Owner
- Created timestamp
- Updated timestamp

Supported operations include:

- List
- Search
- View
- Create
- Edit
- Delete
- Ownership management

---

# Contacts

Contacts represent individuals associated with companies or CRM relationships.

Contact information includes:

- First name
- Last name
- Company
- Owner
- Job title
- Email
- Phone
- Mobile
- Status
- Address
- City
- Country
- Notes
- Created timestamp
- Updated timestamp

Supported operations include:

- List
- Search
- View
- Create
- Edit
- Delete

Contact statuses include:

- Lead
- Prospect
- Customer
- Inactive

---

# Leads

Leads represent potential customers entering the sales process.

Lead fields include:

- First name
- Last name
- Company name
- Email
- Phone
- Job title
- Source
- Status
- Estimated value
- Owner
- Description
- Tags
- Converted company
- Converted contact
- Created timestamp
- Updated timestamp

Lead functionality includes:

- Lead creation
- Lead listing
- Lead detail pages
- Search
- Filtering
- Pagination
- Editing
- Deletion
- Ownership
- Status transitions
- Duplicate detection
- Lead conversion
- Company/contact conversion relationships
- Dashboard statistics

The application uses controlled lead status transitions to prevent invalid workflow changes.

---

# Deals

Deals represent sales opportunities.

Deal information includes:

- Deal name
- Company
- Contact
- Pipeline
- Pipeline stage
- Amount
- Expected close date
- Owner
- Description
- Tags
- Created timestamp
- Updated timestamp

The `Deal.clean()` validation ensures that a selected stage belongs to the selected pipeline.

This protects the integrity of pipeline data.

---

# Pipelines

Pipelines represent sales processes.

A pipeline contains stages representing progression through the sales cycle.

The system supports:

- Pipeline creation
- Pipeline editing
- Pipeline deletion
- Stage creation
- Stage editing
- Stage deletion
- Pipeline-stage relationships
- Deal-stage validation

---

# Activities

Activities provide a history of customer and sales interactions.

Supported activity types include:

- Call
- Email
- Meeting
- SMS
- Other

Activities can be associated with:

- Company
- Contact
- Lead
- Deal

Activity information also includes:

- Subject
- Description
- Assigned user
- Activity date
- Created by
- Created timestamp

---

# Tasks

Tasks provide follow-up and work management.

A task may be associated with:

- Company
- Contact
- Lead
- Deal

Task fields include:

- Title
- Description
- Assigned user
- Due date
- Priority
- Status
- Created by
- Created timestamp
- Updated timestamp

## Task Priorities

- Low
- Normal
- High
- Urgent

## Task Statuses

- Pending
- In progress
- Completed
- Cancelled

---

# Notes

Notes provide internal CRM documentation.

A note can be associated with:

- Company
- Contact
- Lead
- Deal

Note fields include:

- Title
- Content
- Created by
- Created timestamp
- Updated timestamp

Notes support:

- Creation
- Listing
- Detail viewing
- Editing
- Deletion
- Role-based permissions

Current note permissions include:

- Administrators and Managers can manage notes broadly.
- Sales Representatives can create notes and edit notes they created.
- Support and Viewer roles are restricted from note management operations according to the permission layer.
- Authorized users can view permitted notes.

---

# Calendar

The Calendar module provides a centralized view for scheduled CRM events and activities.

It is intended to help users coordinate:

- Meetings
- Calls
- Follow-ups
- Activities
- Scheduled work

The Calendar functionality is already implemented and integrated into the primary CRM navigation.

---

# Notifications

NexusCRM includes a notification system integrated into the main application interface.

The main navigation contains a notification control and notification indicator.

The notification system provides the foundation for informing users about relevant CRM events.

---

# User Preferences

Users can manage application preferences through the Settings area.

Preferences are stored per user and are separate from core CRM records.

This provides a foundation for user-specific UI and notification configuration.

---

# Global Search

NexusCRM provides global search functionality.

The purpose is to allow users to search across multiple CRM entities without having to manually navigate to each module.

Search functionality is already integrated into the application and should be extended rather than replaced as new modules are added.

---

# Audit Logging

NexusCRM includes an audit logging system for tracking important system actions.

The `AuditLog` model records events such as:

- Record creation
- Record updates
- User preference changes
- Other important application actions

Audit information can include:

- User
- Action
- Object/type
- Object identifier
- Description/details
- Timestamp

Audit logging is important for:

- Accountability
- Troubleshooting
- Security monitoring
- Administrative review
- Change tracking

The audit system is already migrated and operational.

---

# REST API

NexusCRM includes a REST API under:

```text
/api/v1/
```

The API is designed to provide structured access to CRM resources and serve as the integration layer for future applications and services.

## Current API Serializer Coverage

Serializers currently exist for:

- Companies
- Contacts
- Leads
- Deals
- Activities
- Tasks
- Notes

Examples:

```text
CompanySerializer
ContactSerializer
LeadSerializer
DealSerializer
ActivitySerializer
TaskSerializer
NoteSerializer
```

## API Security

Unauthenticated requests to the protected API are rejected.

Example:

```bash
curl http://127.0.0.1:8003/api/v1/
```

Expected response:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

This confirms that the API is protected rather than publicly exposing CRM data.

---

# Data Model

The major CRM models include:

```text
User
  |
  +--- Profile
  |
  +--- Company
  |
  +--- Contact
  |
  +--- Lead
  |
  +--- Deal
  |
  +--- Activity
  |
  +--- Task
  |
  +--- Note
  |
  +--- AuditLog
  |
  +--- UserPreference
```

Supporting models include:

```text
Pipeline
PipelineStage
Tag
Notification-related models
```

## Important Relationships

### Company

A company can have multiple contacts and CRM relationships.

### Contact

A contact can belong to a company and can be associated with CRM activities and deals.

### Lead

A lead can have an owner, tags, and eventual converted company/contact records.

### Deal

A deal belongs to a pipeline and stage and may be associated with a company/contact.

### Pipeline

A pipeline contains pipeline stages.

### Activity

An activity can connect multiple CRM entities through optional relationships.

### Task

A task can be assigned to a user and associated with CRM records.

### Note

A note belongs to its creator and can optionally reference a company, contact, lead, or deal.

---

# Role and Permission Model

Permissions are implemented centrally through the CRM permission layer.

Important permission concepts include:

- Can view
- Can create
- Can edit
- Can delete
- Ownership-based access
- Role-based access
- Administrative access

The application should use the existing permission functions instead of duplicating permission logic inside individual templates or views.

This makes authorization easier to maintain and test.

---

# Testing

Automated testing is a core part of NexusCRM development.

The testing structure is:

```text
crmApp/tests/
├── __init__.py
├── test_models.py
├── test_permissions.py
├── test_views.py
└── test_api.py
```

## Model Tests

Model tests verify important behavior of CRM models including:

- Companies
- Contacts
- Leads
- Deals
- Activities
- Tasks
- Notes
- Tags

## Permission Tests

Permission tests verify role-specific behavior.

Examples include:

- Administrator access
- Manager access
- Sales access
- Support access
- Viewer access
- Note permissions
- Ownership restrictions

## View Tests

View tests verify:

- Authentication requirements
- Page accessibility
- CRUD behavior
- Redirects
- Permissions
- Important view responses

## API Tests

API tests verify:

- Authentication
- API access
- Serializer behavior
- Endpoint responses
- Protected resources

---

# Running Tests

Run the complete test suite with:

```bash
python3 manage.py test
```

Run specific test groups:

```bash
python3 manage.py test crmApp.tests.test_models
```

```bash
python3 manage.py test crmApp.tests.test_permissions
```

```bash
python3 manage.py test crmApp.tests.test_views
```

```bash
python3 manage.py test crmApp.tests.test_api
```

Run multiple groups:

```bash
python3 manage.py test crmApp.tests.test_models crmApp.tests.test_permissions
```

Always run:

```bash
python3 manage.py check
```

before major commits or phase completion.

---

# Development Phases

NexusCRM has been developed through structured phases.

## Completed Areas

The project currently includes completed implementations covering:

### Phase 0–5

Initial project foundation and core CRM functionality.

### Phase 6

Extended CRM functionality built on the established architecture.

### Phase 7

Lead and CRM workflow expansion, including:

- Lead functionality
- Lead statistics
- Lead permissions
- Lead editing
- Lead deletion
- Lead workflow behavior

### Phase 13 — Calendar

Calendar functionality completed.

### Phase 14 — Notifications

Notification functionality completed.

### Phase 15 — Editable Preferences

User preferences completed.

### Phase 19 — Global Search

Global search across CRM functionality completed.

### Phase 20 — Audit Logs

Audit logging completed and migrated.

### Phase 21 — API and Integrations

REST API foundation completed, including serializers and protected API access.

---

# Current Development Roadmap

## Phase 22 — Automated Testing

Focus:

- Comprehensive model tests
- Permission tests
- View tests
- API tests
- Regression testing
- Full-suite validation

---

## Phase 23 — Security Hardening

Planned focus:

- Authentication security
- Authorization review
- CSRF protection review
- Session security
- Secure headers
- Production settings
- Secret management
- File upload security
- API security
- Permission audit
- Input validation

---

## Phase 24 — Performance Optimization

Planned focus:

- Database query optimization
- `select_related`
- `prefetch_related`
- Query-count analysis
- Pagination
- Static asset optimization
- Caching where appropriate
- API performance
- Dashboard optimization
- Search optimization

---

## Phase 25 — Production Deployment

Planned focus:

- Production settings
- Environment variables
- Production database
- Static files
- Media files
- WSGI/ASGI configuration
- HTTPS
- Domain configuration
- Logging
- Error handling
- Backups
- Deployment verification

---

## Phase 26 — Final Client Acceptance Testing

Final validation will cover:

- Authentication
- User roles
- Permissions
- Dashboard
- Companies
- Contacts
- Leads
- Deals
- Pipelines
- Activities
- Tasks
- Notes
- Calendar
- Notifications
- Preferences
- Global search
- Audit logs
- API
- Security
- Responsive UI
- Production deployment
- Regression testing

---

# Local Development Setup

## Requirements

Recommended development environment:

- Python 3.12+
- pip
- Git
- Virtual environment
- SQLite for local development
- Modern web browser

The project is currently developed in a Python virtual environment named:

```text
crm
```

---

# Project Location

The established project location is:

```text
~/Desktop/Programs/python/Nexus-CRM/NexusCRM
```

The virtual environment is maintained separately from the Django project source.

---

# Activate the Virtual Environment

From the project environment:

```bash
source ../crm/bin/activate
```

Verify Python:

```bash
python3 --version
```

Verify Django:

```bash
python3 -m django --version
```

---

# Install Dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

For a new environment, the project should maintain all production and development dependencies in the dependency file rather than relying on undocumented global packages.

---

# Database Setup

Apply migrations:

```bash
python3 manage.py migrate
```

Create migrations after model changes:

```bash
python3 manage.py makemigrations
```

Apply them:

```bash
python3 manage.py migrate
```

Check migration status:

```bash
python3 manage.py showmigrations
```

---

# Create a Superuser

Create an administrative account with:

```bash
python3 manage.py createsuperuser
```

Follow the prompts.

The resulting user can be used for administrative access and development testing.

---

# Run the Development Server

Start the application with:

```bash
python3 manage.py runserver
```

If a different port is required:

```bash
python3 manage.py runserver 8003
```

The development server can then be accessed at:

```text
http://127.0.0.1:8003/
```

---

# Django System Check

Run:

```bash
python3 manage.py check
```

A healthy project should return:

```text
System check identified no issues (0 silenced).
```

---

# Environment Configuration

Production secrets and environment-specific settings should not be hard-coded into source code.

Important configuration areas include:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Database credentials
- Email configuration
- API credentials
- Storage credentials
- External service credentials

Use environment variables for secrets in production.

Example concept:

```text
SECRET_KEY=<secret>
DEBUG=False
ALLOWED_HOSTS=<production-domain>
```

Never commit real passwords, API keys, tokens, or secret credentials to Git.

---

# Database and Migrations

Django migrations are the source-controlled mechanism for evolving the database schema.

Current migrations include the project's incremental CRM schema changes.

For example, the audit log implementation introduced a migration similar to:

```text
crmApp/migrations/0008_auditlog.py
```

Migration workflow:

```bash
python3 manage.py makemigrations
```

then:

```bash
python3 manage.py migrate
```

Never manually modify an already-applied migration unless there is a deliberate migration-repair procedure.

---

# API Development

The API namespace is:

```text
/api/v1/
```

API development should follow these principles:

1. Keep serializers focused on representation and validation.
2. Keep authorization enforced server-side.
3. Never trust frontend permissions as security.
4. Require authentication for protected CRM resources.
5. Use consistent JSON responses.
6. Preserve backwards compatibility for existing API consumers where possible.
7. Version future breaking API changes.

---

# Security

Security is a continuing development requirement.

Important security areas include:

## Authentication

All protected CRM functionality must require authentication.

## Authorization

Users must only access operations permitted by their role and ownership rules.

## CSRF

Django's CSRF protection should remain enabled for browser-based form operations.

## Passwords

Passwords should always be handled by Django's secure password hashing system.

Plain-text passwords must never be stored.

## Secrets

Secrets must be stored outside source code in production.

## Input Validation

All user input should be validated through Django forms, serializers, model validation, or appropriate application-level validation.

## API Protection

CRM API endpoints must enforce authentication and permissions.

## Auditability

Important state-changing actions should be logged where appropriate.

---

# Performance

The application is designed to support future optimization as data volume grows.

Potential performance strategies include:

- Database indexes
- `select_related`
- `prefetch_related`
- Query optimization
- Pagination
- Caching
- Efficient search queries
- Static file optimization
- API response optimization
- Dashboard query optimization

Performance work should be measured rather than based only on assumptions.

---

# Production Deployment

Before production deployment:

```bash
python3 manage.py check --deploy
```

Production deployment should include:

- `DEBUG=False`
- Secure `SECRET_KEY`
- Correct `ALLOWED_HOSTS`
- Production database
- HTTPS
- Secure cookies
- CSRF configuration
- Static file collection
- Media storage configuration
- Error logging
- Backup strategy
- Database backup
- Monitoring
- Appropriate WSGI/ASGI server
- Reverse proxy configuration where applicable

Collect static files with:

```bash
python3 manage.py collectstatic
```

The exact production infrastructure may be selected during Phase 25.

---

# Troubleshooting

## Check Django Configuration

```bash
python3 manage.py check
```

## Check Migrations

```bash
python3 manage.py showmigrations
```

## Create Missing Migrations

```bash
python3 manage.py makemigrations
```

## Apply Migrations

```bash
python3 manage.py migrate
```

## Run Tests

```bash
python3 manage.py test
```

## Inspect Database from Django Shell

```bash
python3 manage.py shell
```

Example:

```python
from crmApp.models import AuditLog
AuditLog.objects.count()
```

---

# Common Development Rules

## Do Not Duplicate Existing Components

Before creating a new:

- Template
- Static directory
- URL file
- View
- Form
- Model
- App
- Base template
- Permission helper
- API module

inspect the existing project first.

The existing Phase 0–21 architecture is the source of truth.

## Preserve Existing Functionality

New phases should extend the current application rather than replacing working modules.

## Reuse Existing Base Template

The primary base template is:

```text
templates/crmApp/base.html
```

Do not introduce a second competing base layout.

## Reuse Existing Permissions

Use the central permission system in:

```text
crmApp/permissions.py
```

instead of creating inconsistent role checks throughout the project.

## Test Every Change

After significant changes:

```bash
python3 manage.py check
```

Then run the relevant tests.

Finally:

```bash
python3 manage.py test
```

---

# Development Workflow

Recommended workflow:

```text
1. Inspect existing implementation
        |
        v
2. Identify the exact feature/change
        |
        v
3. Reuse existing architecture
        |
        v
4. Implement backend logic
        |
        v
5. Implement/update frontend
        |
        v
6. Add/update tests
        |
        v
7. Run Django checks
        |
        v
8. Run relevant tests
        |
        v
9. Run full test suite
        |
        v
10. Manually verify UI
        |
        v
11. Commit changes
```

---

# Git and Source Control

The project should be maintained using Git.

Recommended workflow:

```bash
git status
```

Review changes:

```bash
git diff
```

Stage changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Describe the change"
```

Push:

```bash
git push
```

Do not commit:

- Virtual environments
- `.env` files
- Database secrets
- API tokens
- Passwords
- Generated cache files
- Unnecessary IDE metadata
- Local-only files

A suitable `.gitignore` should cover these items.

---

# Project Quality Standards

NexusCRM should maintain the following qualities:

- Clear architecture
- Consistent naming
- Reusable components
- Server-side authorization
- Input validation
- Automated tests
- Responsive UI
- Maintainable code
- Minimal duplication
- Secure configuration
- Documented APIs
- Reliable database migrations
- Production-ready configuration

---

# Extensibility

The current architecture is intended to support future expansion.

Potential extensions include:

- Email integration
- SMS integration
- WhatsApp integration
- M-Pesa/payment integration
- Calendar synchronization
- Google/Microsoft integrations
- Advanced reporting
- Sales forecasting
- Customer support/ticketing
- Document management
- Workflow automation
- Marketing automation
- Webhooks
- Third-party APIs
- Mobile applications
- Advanced analytics
- AI-assisted CRM functionality

These should be introduced incrementally without compromising the existing architecture.

---

# Future Roadmap

Beyond the current Phase 26 acceptance milestone, possible product evolution includes:

## Advanced Sales Automation

- Automated lead assignment
- Follow-up reminders
- Sales sequences
- Automated deal progression
- Workflow rules

## Communication

- Email integration
- SMS
- WhatsApp
- Communication history
- Message templates

## Reporting

- Custom reports
- Exportable reports
- Sales forecasting
- Team performance reports
- Conversion analytics

## Customer Support

- Support tickets
- Ticket assignment
- SLA tracking
- Customer communication history

## Integrations

- Payment providers
- Accounting systems
- Calendar providers
- Email providers
- Messaging providers
- External business systems

## Mobile

A future mobile client can consume the existing REST API rather than duplicating backend business logic.

---

# Project Status

## Current Status

NexusCRM has progressed through the core CRM implementation and integration stages.

Completed areas include:

- Core CRM foundation
- Authentication
- User profiles
- Role-based permissions
- Companies
- Contacts
- Leads
- Lead workflows
- Deals
- Pipelines
- Pipeline stages
- Activities
- Tasks
- Notes
- Calendar
- Notifications
- User preferences
- Global search
- Audit logging
- REST API foundation

The API layer has protected endpoints and serializers for major CRM resources.

Automated testing is being expanded as part of the Phase 22 quality stage.

---

# Verification Commands

The following commands provide a quick health check:

```bash
python3 manage.py check
```

```bash
python3 manage.py test
```

```bash
python3 manage.py showmigrations
```

```bash
python3 manage.py makemigrations --check
```

A clean project should pass the Django system check and the automated test suite.

---

# Documentation Philosophy

This README documents the NexusCRM project as an evolving system.

When new phases are completed, this document should be updated to reflect:

- New modules
- New technologies
- New dependencies
- New API endpoints
- New permissions
- New models
- New integrations
- New deployment requirements
- New testing requirements

Documentation should describe the actual implementation rather than an intended future architecture.

---

# License

This project is currently developed as a proprietary CRM project.

Unless a separate license is added to the repository, the source code should not be assumed to be freely licensed for redistribution, modification, or commercial use.

---

# NexusCRM

**A centralized CRM platform for managing customers, sales, activities, tasks, relationships, and business operations.**

Built with:

```text
Python
Django
Django REST Framework
HTML5
CSS3
JavaScript
Bootstrap
Bootstrap Icons
Django ORM
SQLite (local development)
Git
```

