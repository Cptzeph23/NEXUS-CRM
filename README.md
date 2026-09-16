# NexusCRM

NexusCRM is a professional, role-based Customer Relationship Management
(CRM) system built with Django, HTML, CSS, JavaScript, and Bootstrap.

The system is designed to centralize customer and sales information,
manage leads and deals, track activities and tasks, organize notes and
calendar events, provide notifications and user preferences, maintain
audit history, expose protected REST API endpoints, and provide a
foundation for production deployment and future integrations.

> **Project status:** Active development\
> **Current development stage:** Automated testing and
> production-readiness work\
> **Primary framework:** Django\
> **Primary application:** `crmApp`

------------------------------------------------------------------------

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Project Goals](#project-goals)
3.  [Technology Stack](#technology-stack)
4.  [Core Features](#core-features)
5.  [User Roles and Permissions](#user-roles-and-permissions)
6.  [CRM Modules](#crm-modules)
7.  [System Architecture](#system-architecture)
8.  [Project Structure](#project-structure)
9.  [Database and Data Model](#database-and-data-model)
10. [Authentication and User
    Profiles](#authentication-and-user-profiles)
11. [Leads and Lead Conversion](#leads-and-lead-conversion)
12. [Deals and Sales Pipeline](#deals-and-sales-pipeline)
13. [Activities and Tasks](#activities-and-tasks)
14. [Notes](#notes)
15. [Calendar](#calendar)
16. [Notifications](#notifications)
17. [User Preferences](#user-preferences)
18. [Audit Logging](#audit-logging)
19. [Global Search](#global-search)
20. [REST API](#rest-api)
21. [Security](#security)
22. [Automated Testing](#automated-testing)
23. [Development Environment](#development-environment)
24. [Installation and Setup](#installation-and-setup)
25. [Database Migrations](#database-migrations)
26. [Running the Application](#running-the-application)
27. [Testing the Application](#testing-the-application)
28. [API Authentication](#api-authentication)
29. [Development Workflow](#development-workflow)
30. [Development Phases](#development-phases)
31. [Production Roadmap](#production-roadmap)
32. [Deployment Considerations](#deployment-considerations)
33. [Troubleshooting](#troubleshooting)
34. [Development Conventions](#development-conventions)
35. [Future Enhancements](#future-enhancements)
36. [Project Principles](#project-principles)
37. [License](#license)

------------------------------------------------------------------------

# Project Overview

NexusCRM is a web-based CRM intended to provide organizations with a
centralized platform for managing relationships with customers,
prospects, leads, and sales opportunities.

The application combines operational CRM functionality with role-based
access control, activity tracking, auditability, search, notifications,
and API access.

The project has been developed incrementally through defined phases.
Each phase adds a functional part of the system and is tested before
moving to the next stage.

The system is intended to be:

-   Professional enough for client demonstrations.
-   Modular and maintainable.
-   Secure and role-aware.
-   Extensible for future integrations.
-   Suitable for deployment beyond the local development environment.
-   Structured around actual business workflows rather than isolated
    CRUD pages.

------------------------------------------------------------------------

# Project Goals

The primary goals of NexusCRM are to provide:

### Customer management

A centralized location for companies and contacts.

### Lead management

A structured process for capturing, assigning, qualifying, updating, and
converting leads.

### Sales management

Pipeline, stages, deals, amounts, expected close dates, ownership, and
sales tracking.

### Productivity management

Tasks, activities, notes, and calendar events associated with CRM
records.

### User management

Authentication, profiles, roles, and role-aware functionality.

### Operational visibility

Dashboard statistics, pipeline information, lead information, search,
notifications, and reporting foundations.

### Accountability

Audit logs that record important system actions.

### Integration readiness

Protected REST API endpoints and serializers for core CRM resources.

------------------------------------------------------------------------

# Technology Stack

## Backend

-   Python
-   Django
-   Django ORM
-   Django authentication
-   Django migrations

## Frontend

-   HTML5
-   CSS3
-   JavaScript
-   Bootstrap
-   Bootstrap Icons

## API

-   Django REST Framework
-   API serializers
-   Protected API endpoints
-   Authentication-controlled API access

## Database

The application uses Django's database abstraction layer and migrations.
The development environment is configured around Django's standard
database workflow, while production deployment can use a production
database configuration appropriate to the hosting environment.

## Development Tools

The project is developed using a Python virtual environment named:

``` text
crm
```

The project is maintained from:

``` text
~/Desktop/Programs/python/Nexus-CRM/NexusCRM
```

------------------------------------------------------------------------

# Core Features

NexusCRM currently includes the following major functionality:

-   User authentication
-   User profiles
-   Role-based access control
-   Dashboard
-   Companies
-   Contacts
-   Leads
-   Lead ownership
-   Lead status management
-   Lead conversion
-   Deals
-   Sales pipelines
-   Pipeline stages
-   Activities
-   Tasks
-   Notes
-   Calendar
-   Notifications
-   User preferences
-   Global search
-   Audit logs
-   REST API
-   API serializers
-   API authentication protection
-   Database migrations
-   Automated testing foundation

------------------------------------------------------------------------

# User Roles and Permissions

NexusCRM uses role-based access control.

The defined roles are:

  Role        Display Name           General Responsibility
  ----------- ---------------------- --------------------------------------
  `admin`     Administrator          Full system administration
  `manager`   Manager                Management and operational oversight
  `sales`     Sales Representative   Sales and assigned CRM records
  `support`   Support                Customer/support-oriented access
  `viewer`    Viewer                 Read-only access

## Administrator

Administrators have the broadest access to the system.

Typical responsibilities include:

-   Managing users.
-   Managing roles.
-   Managing CRM records.
-   Managing system settings.
-   Reviewing audit logs.
-   Performing administrative operations.

## Manager

Managers have broad operational access and can manage CRM data within
the permissions implemented by the application.

## Sales Representative

Sales users are primarily responsible for sales-related CRM activity.

Depending on the module, access may be restricted to records they own or
create.

For example, note permissions currently allow sales users to:

-   View notes.
-   Create notes.
-   Edit notes they created.

## Support

Support users have access appropriate to support operations and are
restricted from administrative modifications where applicable.

## Viewer

Viewers are intended for read-only access.

They should not be able to perform protected modification operations
such as creating or editing notes where role restrictions apply.

------------------------------------------------------------------------

# CRM Modules

## Dashboard

The dashboard provides an operational overview of CRM activity.

It includes CRM statistics such as:

-   Lead statistics.
-   Qualified lead information.
-   Pipeline value.
-   Other system-level CRM indicators implemented in the dashboard.

The dashboard is designed to give users an immediate view of important
CRM information after authentication.

------------------------------------------------------------------------

## Companies

Companies represent organizations stored within the CRM.

Company information includes fields such as:

-   Name
-   Industry
-   Website
-   Email
-   Phone
-   Address
-   City
-   Country
-   Description
-   Owner
-   Creation timestamp
-   Last update timestamp

Companies can be associated with contacts, leads, deals, activities,
tasks, and notes.

------------------------------------------------------------------------

## Contacts

Contacts represent individual people associated with CRM organizations.

Contact information includes:

-   First name
-   Last name
-   Company
-   Owner
-   Job title
-   Email
-   Phone
-   Mobile
-   Status
-   Address
-   City
-   Country
-   Notes
-   Creation timestamp
-   Last update timestamp

Contact statuses include:

-   Lead
-   Prospect
-   Customer
-   Inactive

------------------------------------------------------------------------

## Leads

Leads represent potential customers or sales opportunities before they
become established CRM relationships.

Lead information includes:

-   First name
-   Last name
-   Company name
-   Email
-   Phone
-   Job title
-   Source
-   Status
-   Estimated value
-   Owner
-   Description
-   Tags
-   Converted company
-   Converted contact
-   Creation timestamp
-   Last update timestamp

The lead workflow includes:

-   Lead creation
-   Ownership
-   Search/filtering
-   Pagination
-   Lead details
-   Lead editing
-   Lead deletion
-   Status transitions
-   Conversion into CRM records
-   Dashboard statistics

The application also contains duplicate-detection and controlled
lead-status transition logic.

------------------------------------------------------------------------

# Lead Conversion

Lead conversion allows a lead to become an established CRM relationship.

A converted lead can be associated with:

-   A company
-   A contact

The `Lead` model contains:

``` text
converted_company
converted_contact
```

This provides a connection between the original lead and the resulting
CRM records.

------------------------------------------------------------------------

# Deals and Sales Pipeline

NexusCRM includes sales pipeline management.

## Pipeline

A pipeline represents a sales workflow.

## Pipeline Stage

A pipeline stage represents a step within a pipeline.

## Deal

A deal represents a sales opportunity moving through a pipeline.

Deal information includes:

-   Deal name
-   Company
-   Contact
-   Pipeline
-   Stage
-   Amount
-   Expected close date
-   Owner
-   Description
-   Tags
-   Creation timestamp
-   Last update timestamp

The application enforces pipeline/stage integrity so that a deal's
selected stage belongs to its selected pipeline.

This validation is implemented in the `Deal.clean()` model logic.

------------------------------------------------------------------------

# Activities and Tasks

## Activities

Activities record interactions or events associated with CRM records.

Supported activity types include:

-   Call
-   Email
-   Meeting
-   SMS
-   Other

An activity can be associated with:

-   Company
-   Contact
-   Lead
-   Deal

Additional activity information includes:

-   Subject
-   Description
-   Assigned user
-   Activity date
-   Creator
-   Creation timestamp

------------------------------------------------------------------------

## Tasks

Tasks represent actionable work.

Task information includes:

-   Title
-   Description
-   Company
-   Contact
-   Lead
-   Deal
-   Assigned user
-   Due date
-   Priority
-   Status
-   Creator
-   Creation timestamp
-   Last update timestamp

Task priorities include:

-   Low
-   Normal
-   High
-   Urgent

Task statuses include:

-   Pending
-   In progress
-   Completed
-   Cancelled

Tasks can therefore be attached directly to CRM records while
maintaining ownership and accountability.

------------------------------------------------------------------------

# Notes

Notes provide a way to store additional CRM information that does not
fit into structured fields.

A note contains:

-   Title
-   Content
-   Company
-   Contact
-   Lead
-   Deal
-   Creator
-   Creation timestamp
-   Last update timestamp

Notes are ordered with the newest records first.

## Note permissions

The current permission design includes:

  Action     Admin   Manager   Sales   Support   Viewer
  -------- ------- --------- ------- --------- --------
  View         Yes       Yes     Yes       Yes      Yes
  Create       Yes       Yes     Yes        No       No
  Edit         Yes       Yes     Own        No       No
  Delete       Yes       Yes      No        No       No

The exact enforcement is implemented in the application's permission
functions and views.

------------------------------------------------------------------------

# Calendar

The calendar module provides CRM scheduling functionality.

Calendar functionality has been implemented as a working module rather
than a placeholder.

It supports the calendar workflow implemented in the application,
including:

-   Calendar views
-   Event creation
-   Event forms
-   Event listing
-   Event details
-   Event deletion
-   Calendar actions

Calendar functionality is integrated into the primary CRM navigation.

------------------------------------------------------------------------

# Notifications

NexusCRM includes a notification system for communicating relevant
system events to users.

The main interface includes a notification control in the primary
application layout.

Notifications can be surfaced through the application's notification
workflow and UI.

The notification system is designed to be extensible for additional CRM
events.

------------------------------------------------------------------------

# User Preferences

Users can maintain configurable preferences within the application.

Preferences are stored independently from the main authentication record
and allow user-specific application settings to be managed.

Preference changes are also integrated with the audit logging system
where applicable.

------------------------------------------------------------------------

# Audit Logging

NexusCRM includes an `AuditLog` model for tracking important system
actions.

Audit logging provides accountability by recording events such as:

-   Record creation
-   Record updates
-   Other tracked system actions

The audit log contains information associated with the user and action
being performed.

Audit logs are useful for:

-   Troubleshooting
-   Accountability
-   Security review
-   Administrative monitoring
-   Understanding changes made to CRM data

The audit logging module has been migrated into the active database
schema.

------------------------------------------------------------------------

# Global Search

NexusCRM provides global search functionality across the application.

The search feature is designed to allow users to locate CRM information
without navigating manually through every module.

Search coverage includes the core CRM entities implemented by the
application.

Global search is already integrated into the system and should be
extended rather than duplicated when new searchable modules are
introduced.

------------------------------------------------------------------------

# REST API

NexusCRM provides protected REST API functionality through Django REST
Framework.

The API exposes serializers and protected endpoints for core CRM
resources.

Current serializer coverage includes:

``` text
CompanySerializer
ContactSerializer
LeadSerializer
DealSerializer
ActivitySerializer
TaskSerializer
NoteSerializer
```

The API is protected against unauthenticated access.

For example, accessing the API without authentication returns an
authentication error rather than exposing CRM data.

## API structure

The primary API namespace is:

``` text
/api/v1/
```

The API is intended to provide a foundation for:

-   External integrations
-   Mobile applications
-   Third-party systems
-   Future automation
-   Internal frontend/API separation
-   Reporting integrations

------------------------------------------------------------------------

# System Architecture

The project follows a Django application architecture centered around
the `crmApp` application.

The system can broadly be divided into:

``` text
Browser
   |
   v
Django URLs
   |
   v
Views
   |
   +------ Forms
   |
   +------ Permissions
   |
   +------ Models / ORM
   |
   v
Database

API clients
   |
   v
/api/v1/
   |
   v
DRF Views / Endpoints
   |
   v
Serializers
   |
   v
Models / ORM
   |
   v
Database
```

The frontend uses Django templates together with Bootstrap, CSS, and
JavaScript.

The primary application base template is:

``` text
templates/crmApp/base.html
```

This template is the main layout foundation for the CRM interface.

------------------------------------------------------------------------

# Project Structure

The project structure should be treated as the existing source of truth.

A simplified representation is:

``` text
Nexus-CRM/
└── NexusCRM/
    ├── manage.py
    ├── README.md
    ├── crmApp/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── permissions.py
    │   ├── signals.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── api/
    │   │   └── serializers.py
    │   ├── migrations/
    │   └── tests/
    ├── NexusCRM/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── templates/
    │   └── crmApp/
    │       ├── base.html
    │       └── ...
    └── static/
        └── ...
```

> The exact directory contents may evolve as the project progresses.
> Existing files should be inspected before adding new files to avoid
> duplicate templates, static directories, URL modules, views,
> applications, or other components.

------------------------------------------------------------------------

# Database and Data Model

The core CRM data model includes the following entities.

## Profile

Extends the Django user with CRM-specific information.

Important fields include:

-   User
-   Role
-   Phone
-   Job title
-   Avatar
-   Created timestamp
-   Updated timestamp

Profiles are automatically created and maintained using Django signals.

------------------------------------------------------------------------

## Company

Stores organization-level customer information.

------------------------------------------------------------------------

## Contact

Stores individual customer/contact information.

------------------------------------------------------------------------

## Lead

Stores prospective customer information before or during qualification.

------------------------------------------------------------------------

## Pipeline

Defines a sales workflow.

------------------------------------------------------------------------

## PipelineStage

Defines stages belonging to a pipeline.

------------------------------------------------------------------------

## Deal

Represents a sales opportunity within a pipeline.

------------------------------------------------------------------------

## Activity

Records customer or sales interactions.

------------------------------------------------------------------------

## Task

Tracks actionable work.

------------------------------------------------------------------------

## Note

Stores free-form CRM information.

------------------------------------------------------------------------

## Tag

Provides categorization for CRM records that support tagging.

------------------------------------------------------------------------

## AuditLog

Records tracked system actions for accountability.

------------------------------------------------------------------------

## UserPreference

Stores user-specific application preferences.

------------------------------------------------------------------------

# Authentication and User Profiles

NexusCRM uses Django's authentication system.

The general authentication workflow is:

``` text
Login
  |
  v
Authenticated session
  |
  v
Dashboard / CRM
  |
  v
Logout
  |
  v
Login
```

The application uses session-based authentication for its normal web
interface.

Unauthenticated users are redirected to the appropriate authentication
flow instead of being allowed to access protected CRM pages.

------------------------------------------------------------------------

# User Profile Creation

The application uses Django signals to create a `Profile` automatically
when a user is created.

The relevant architecture is:

``` text
User created
    |
    v
post_save signal
    |
    v
Profile created
```

The profile contains the user's CRM role.

Role assignment is integrated with the user administration workflow.

------------------------------------------------------------------------

# Security

Security is an ongoing development area and is addressed progressively.

Current security-related functionality includes:

-   Django authentication
-   Session-based protected web views
-   Role-based access control
-   Protected API endpoints
-   Permission functions
-   CSRF protection through Django forms/templates
-   Password handling through Django authentication
-   Audit logging
-   Ownership-aware permissions
-   Database-level model validation where appropriate

Production hardening is scheduled as a dedicated development phase.

------------------------------------------------------------------------

# Automated Testing

Automated testing is part of the project's development process.

The testing structure is intended to cover:

``` text
crmApp/tests/
├── __init__.py
├── test_models.py
├── test_permissions.py
├── test_views.py
└── test_api.py
```

## Model tests

Model tests verify important behavior for entities such as:

-   Company
-   Contact
-   Lead
-   Deal
-   Activity
-   Task
-   Note
-   Tag

## Permission tests

Permission tests verify role-specific access.

For example:

-   Admin access
-   Manager access
-   Sales access
-   Support restrictions
-   Viewer restrictions
-   Ownership-based permissions

## View tests

View tests verify that important application pages respond correctly and
enforce authentication.

## API tests

API tests verify:

-   API authentication
-   Endpoint behavior
-   Serialization
-   Protected access
-   CRUD behavior where implemented

------------------------------------------------------------------------

# Development Environment

The project is developed inside a Python virtual environment named:

``` text
crm
```

The project directory is:

``` text
~/Desktop/Programs/python/Nexus-CRM/NexusCRM
```

Activate the environment before running Django commands.

Example:

``` bash
cd ~/Desktop/Programs/python/Nexus-CRM/NexusCRM
source ../crm/bin/activate
```

If the environment is already active, the terminal prompt should show:

``` text
(crm)
```

------------------------------------------------------------------------

# Installation and Setup

## 1. Navigate to the project

``` bash
cd ~/Desktop/Programs/python/Nexus-CRM/NexusCRM
```

## 2. Activate the virtual environment

``` bash
source ../crm/bin/activate
```

## 3. Install dependencies

If a requirements file is available:

``` bash
pip install -r requirements.txt
```

## 4. Check the Django project

``` bash
python3 manage.py check
```

A healthy project should return:

``` text
System check identified no issues (0 silenced).
```

------------------------------------------------------------------------

# Database Migrations

Whenever model changes are made, generate migrations:

``` bash
python3 manage.py makemigrations crmApp
```

Then apply them:

``` bash
python3 manage.py migrate
```

To inspect migration status:

``` bash
python3 manage.py showmigrations
```

Migrations are part of the project's source-controlled database
evolution.

Do not manually recreate existing migrations unless there is a specific
migration-repair requirement.

------------------------------------------------------------------------

# Running the Application

Start the development server with:

``` bash
python3 manage.py runserver
```

If a specific port is required:

``` bash
python3 manage.py runserver 8003
```

The development server will normally be available at:

``` text
http://127.0.0.1:8003/
```

The exact port can be changed as required.

------------------------------------------------------------------------

# Testing the Application

## Django system check

``` bash
python3 manage.py check
```

## Model and permission tests

``` bash
python3 manage.py test crmApp.tests.test_models crmApp.tests.test_permissions
```

## View tests

``` bash
python3 manage.py test crmApp.tests.test_views
```

## API tests

``` bash
python3 manage.py test crmApp.tests.test_api
```

## Full test suite

``` bash
python3 manage.py test
```

A normal development checkpoint should include:

``` bash
python3 manage.py check
python3 manage.py test
```

------------------------------------------------------------------------

# API Authentication

The API is protected.

An unauthenticated request to:

``` text
/api/v1/
```

should not expose protected CRM information.

Example:

``` bash
curl http://127.0.0.1:8003/api/v1/
```

Expected behavior is an authentication response similar to:

``` json
{
    "detail": "Authentication credentials were not provided."
}
```

The exact authentication mechanism used by the project's current Django
REST Framework configuration should be treated as authoritative. API
clients must use the configured authentication method rather than
assuming a different authentication backend.

------------------------------------------------------------------------

# Development Workflow

NexusCRM is developed incrementally.

The recommended workflow for future changes is:

``` text
1. Inspect the existing implementation
2. Identify the exact module being changed
3. Reuse existing architecture
4. Make the smallest required change
5. Create migrations if models changed
6. Run Django system checks
7. Run targeted tests
8. Run the full test suite
9. Manually verify the affected UI/API
10. Proceed to the next phase
```

This prevents accidental duplication and protects previously completed
functionality.

------------------------------------------------------------------------

# Important Architecture Rule

The existing project structure is the source of truth.

Before creating a new:

-   Template
-   Static directory
-   CSS file
-   JavaScript file
-   URL file
-   View
-   Form
-   Model
-   Application
-   API module
-   Test module

inspect the existing implementation first.

Do not assume the project has a fresh Django structure.

Do not duplicate functionality that has already been implemented.

The primary CRM template is:

``` text
templates/crmApp/base.html
```

Changes to the global interface should normally build on this existing
template.

------------------------------------------------------------------------

# Development Phases

The project has been developed through a phased roadmap.

## Phase 0 --- Project Foundation

Established the initial Django CRM project and development architecture.

------------------------------------------------------------------------

## Phase 1--5 --- Core CRM Foundation

Established the initial CRM structure and core modules.

These phases form the architectural foundation on which later phases
were built.

------------------------------------------------------------------------

## Phase 6 --- CRM Expansion

Expanded the CRM functionality beyond the initial foundation.

------------------------------------------------------------------------

## Phase 7 --- Leads and Related CRM Workflows

Implemented and refined lead management, ownership, permissions, status
transitions, conversion, dashboard statistics, and lead UI workflows.

------------------------------------------------------------------------

## Phase 13 --- Calendar

Implemented the working calendar module, including:

-   Views
-   Forms
-   Lists
-   Details
-   Creation
-   Deletion
-   Calendar actions

------------------------------------------------------------------------

## Phase 14 --- Notifications

Implemented the notification system and associated UI.

------------------------------------------------------------------------

## Phase 15 --- Editable Preferences

Implemented user-editable preferences.

------------------------------------------------------------------------

## Phase 19 --- Global Search

Implemented global CRM search across the application's major modules.

------------------------------------------------------------------------

## Phase 20 --- Audit Logs

Implemented audit logging.

The audit log migration was created and applied successfully.

The system has demonstrated recorded audit events for actions such as:

-   Lead creation
-   Lead updates
-   Task creation
-   Preference updates
-   System events

------------------------------------------------------------------------

## Phase 21 --- API and Integrations

Implemented the REST API foundation.

Serializer coverage includes:

``` text
CompanySerializer
ContactSerializer
LeadSerializer
DealSerializer
ActivitySerializer
TaskSerializer
NoteSerializer
```

API authentication protection was verified.

------------------------------------------------------------------------

## Phase 22 --- Automated Testing

The next development focus is comprehensive automated testing.

Testing areas include:

-   Models
-   Permissions
-   Views
-   APIs
-   Full application regression testing

------------------------------------------------------------------------

## Phase 23 --- Security Hardening

Planned security work includes:

-   Production security settings
-   Secure cookies
-   HTTPS enforcement
-   Security headers
-   Secret management
-   Allowed hosts
-   CSRF configuration
-   Authentication review
-   Authorization review
-   API security review
-   File upload security
-   Input validation
-   Error handling
-   Dependency security

------------------------------------------------------------------------

## Phase 24 --- Performance Optimization

Planned performance work includes:

-   Query optimization
-   `select_related`
-   `prefetch_related`
-   Database indexing
-   Pagination review
-   Caching where appropriate
-   Static asset optimization
-   API optimization
-   Dashboard query optimization
-   Search optimization

------------------------------------------------------------------------

## Phase 25 --- Production Deployment

Planned deployment work includes:

-   Production settings
-   Environment variables
-   Production database
-   Static files
-   Media files
-   WSGI/ASGI configuration
-   HTTPS
-   Domain configuration
-   Logging
-   Monitoring
-   Backups
-   Deployment documentation

------------------------------------------------------------------------

## Phase 26 --- Final Client Acceptance Testing

The final phase is intended to validate the complete system from a
client's perspective.

Testing should cover:

-   Authentication
-   User roles
-   Dashboard
-   Companies
-   Contacts
-   Leads
-   Lead conversion
-   Deals
-   Pipelines
-   Activities
-   Tasks
-   Notes
-   Calendar
-   Notifications
-   Preferences
-   Search
-   Audit logs
-   API
-   Security
-   Performance
-   Production deployment

------------------------------------------------------------------------

# Production Roadmap

The intended path to production is:

``` text
Phase 22
Automated Testing
        |
        v
Phase 23
Security Hardening
        |
        v
Phase 24
Performance Optimization
        |
        v
Phase 25
Production Deployment
        |
        v
Phase 26
Client Acceptance Testing
```

A feature should not be considered production-ready merely because its
UI works locally.

Production readiness requires:

-   Functional correctness
-   Permission correctness
-   Security
-   Testing
-   Performance
-   Error handling
-   Deployment configuration
-   Data protection
-   Operational monitoring

------------------------------------------------------------------------

# Deployment Considerations

Production deployment should use environment-specific configuration.

Sensitive values should not be hardcoded into source code.

Examples of values that should be environment-controlled include:

``` text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
Database credentials
Email credentials
API credentials
Third-party integration credentials
```

Production deployment should also use:

-   HTTPS
-   Secure cookies
-   Production database
-   Proper static-file serving
-   Proper media-file storage
-   Application logging
-   Database backups
-   Error monitoring
-   Restricted administrative access

------------------------------------------------------------------------

# Troubleshooting

## Django reports configuration errors

Run:

``` bash
python3 manage.py check
```

Resolve configuration errors before continuing.

------------------------------------------------------------------------

## Migration problems

Check:

``` bash
python3 manage.py showmigrations
```

Then:

``` bash
python3 manage.py makemigrations crmApp
python3 manage.py migrate
```

Avoid deleting migration history as a first response to a migration
problem.

------------------------------------------------------------------------

## Authentication appears to behave unexpectedly

First verify:

1.  The correct browser session is being used.
2.  The user has logged out and logged back in.
3.  The correct account is being tested.
4.  The user's Profile role is correct.
5.  Django authentication configuration is unchanged.

Browser cookies/session state can sometimes make an old login state
appear to be an application bug.

------------------------------------------------------------------------

## Role appears incorrect

Inspect the user's profile from the Django shell:

``` bash
python3 manage.py shell
```

Then inspect the relevant user/profile.

The application uses the `Profile.role` value for CRM role behavior.

------------------------------------------------------------------------

## API returns authentication errors

This is expected for protected endpoints when no valid credentials are
supplied.

Check the current Django REST Framework configuration in settings before
changing API authentication code.

------------------------------------------------------------------------

## Template errors

When a template raises an attribute error, verify the actual model
fields/properties.

For example, the `Contact` model uses:

``` text
first_name
last_name
```

and its string representation is available through:

``` python
str(contact)
```

Do not assume a field such as `full_name` exists unless it is actually
defined.

------------------------------------------------------------------------

## NoReverseMatch errors

Check:

``` text
crmApp/urls.py
```

and verify that:

-   The URL name exists.
-   The template uses the correct URL name.
-   Required parameters are supplied.
-   The corresponding view exists.

Do not create a duplicate URL when the correct existing endpoint already
exists under a different name.

------------------------------------------------------------------------

# Development Conventions

## Reuse existing functionality

Before implementing something new, inspect the existing code.

If functionality already exists, extend it rather than creating a second
implementation.

------------------------------------------------------------------------

## Preserve the primary template

Use:

``` text
templates/crmApp/base.html
```

as the primary CRM layout.

Do not introduce another base template unless the architecture genuinely
requires one.

------------------------------------------------------------------------

## Preserve URL architecture

Existing URL names are part of the application's internal contract.

Changing URL names can break:

-   Templates
-   Redirects
-   Tests
-   Navigation
-   JavaScript
-   API consumers

------------------------------------------------------------------------

## Keep permissions centralized

Role logic should use the application's permission architecture rather
than scattering role checks unnecessarily throughout templates and
views.

------------------------------------------------------------------------

## Use Django forms

Form validation should remain centralized in Django forms and model
validation where appropriate.

------------------------------------------------------------------------

## Use migrations for schema changes

Never rely on manual database edits for normal development model
changes.

------------------------------------------------------------------------

## Test after changes

At minimum:

``` bash
python3 manage.py check
python3 manage.py test
```

For a targeted change, run the relevant test module first.

------------------------------------------------------------------------

# Future Enhancements

Potential future functionality includes:

## Advanced reporting

-   Sales reports
-   Revenue reports
-   Lead conversion reports
-   Activity reports
-   User performance reports
-   Pipeline analytics
-   Date-based reporting
-   Exportable reports

## Communication integrations

Potential integrations include:

-   Email
-   SMS
-   WhatsApp
-   Calendar providers

## Payment and billing integrations

Where required by a deployment, the system could be integrated with
relevant payment services.

## Advanced API integrations

The REST API can be extended for:

-   Mobile applications
-   External business applications
-   Data synchronization
-   Automation services

## Advanced search

Future search improvements could include:

-   Full-text search
-   Search ranking
-   Advanced filters
-   Saved searches
-   Search suggestions

## Reporting dashboards

Future dashboards could include:

-   Sales funnels
-   Revenue trends
-   Pipeline charts
-   Lead source analysis
-   Activity trends
-   Team performance

## File and document management

CRM records can be extended with more comprehensive document handling,
storage, permissions, and attachment workflows.

------------------------------------------------------------------------

# Project Principles

NexusCRM follows several core principles.

## 1. Build incrementally

Each major capability is developed as a phase.

## 2. Do not duplicate working functionality

Existing code is reused whenever possible.

## 3. Protect data

Authentication and authorization are fundamental parts of the CRM.

## 4. Make permissions explicit

Users should only be able to perform actions appropriate to their role.

## 5. Keep business logic maintainable

Business rules should be implemented in appropriate Django models,
forms, permissions, and services rather than duplicated across
templates.

## 6. Test before progressing

A completed feature should be verified before depending on it in later
phases.

## 7. Preserve the existing architecture

The project should evolve from its established structure instead of
repeatedly recreating the Django application.

## 8. Design for production

Even during prototype development, the application should be structured
so that it can progress toward a production deployment.

------------------------------------------------------------------------

# Current Project Verification

The project has successfully passed Django's system check at the current
development stage:

``` bash
python3 manage.py check
```

Expected result:

``` text
System check identified no issues (0 silenced).
```

The API serializer layer has also been verified for the current core
serializers.

Audit logging has been migrated and has recorded system events.

The API root has been verified as protected against unauthenticated
access.

------------------------------------------------------------------------

# Useful Django Commands

## Start server

``` bash
python3 manage.py runserver
```

## Start on port 8003

``` bash
python3 manage.py runserver 8003
```

## System check

``` bash
python3 manage.py check
```

## Make migrations

``` bash
python3 manage.py makemigrations crmApp
```

## Apply migrations

``` bash
python3 manage.py migrate
```

## Show migrations

``` bash
python3 manage.py showmigrations
```

## Open Django shell

``` bash
python3 manage.py shell
```

## Create superuser

``` bash
python3 manage.py createsuperuser
```

## Run all tests

``` bash
python3 manage.py test
```

------------------------------------------------------------------------

# Project Maintenance Checklist

Before declaring a development phase complete:

-   [ ] Existing architecture inspected
-   [ ] No duplicate files created
-   [ ] Models validated
-   [ ] Forms validated
-   [ ] URLs validated
-   [ ] Views validated
-   [ ] Permissions validated
-   [ ] Templates validated
-   [ ] JavaScript validated where applicable
-   [ ] Migrations created where required
-   [ ] Migrations applied
-   [ ] `manage.py check` passes
-   [ ] Targeted tests pass
-   [ ] Full test suite passes
-   [ ] Manual UI testing completed
-   [ ] API testing completed where applicable
-   [ ] Existing functionality regression-tested

------------------------------------------------------------------------

# Client Acceptance Checklist

Before final delivery, verify the following end-to-end workflows.

## Authentication

-   [ ] Login works
-   [ ] Logout works
-   [ ] Protected pages require authentication
-   [ ] User roles are correctly applied

## Companies

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Permissions

## Contacts

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Permissions

## Leads

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Search
-   [ ] Filtering
-   [ ] Pagination
-   [ ] Ownership
-   [ ] Status transitions
-   [ ] Conversion

## Deals

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Pipeline assignment
-   [ ] Stage integrity
-   [ ] Ownership

## Activities

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Record associations

## Tasks

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Assignment
-   [ ] Priority
-   [ ] Status
-   [ ] Due dates

## Notes

-   [ ] Create
-   [ ] View
-   [ ] Edit
-   [ ] Delete
-   [ ] Role permissions
-   [ ] Ownership restrictions

## Calendar

-   [ ] Create events
-   [ ] View events
-   [ ] Edit where supported
-   [ ] Delete
-   [ ] Calendar navigation

## Notifications

-   [ ] Notification display
-   [ ] Notification state
-   [ ] User-specific behavior

## Preferences

-   [ ] View preferences
-   [ ] Edit preferences
-   [ ] Persist changes

## Search

-   [ ] Global search
-   [ ] Results
-   [ ] Links to records
-   [ ] Permission-aware results

## Audit Logs

-   [ ] Actions are logged
-   [ ] User attribution works
-   [ ] Audit history can be reviewed

## API

-   [ ] Authentication
-   [ ] Serialization
-   [ ] Endpoint access
-   [ ] CRUD operations where implemented
-   [ ] Unauthorized access blocked

------------------------------------------------------------------------

# License

No final open-source license has been specified for NexusCRM at this
stage.

Until a license is explicitly selected, the project should be treated as
proprietary project code.

A production/client release should define the applicable:

-   Ownership
-   Usage rights
-   Distribution rights
-   Modification rights
-   Third-party dependency licenses
-   Client licensing terms

------------------------------------------------------------------------

# Conclusion

NexusCRM is being developed as a complete CRM platform rather than a
collection of isolated CRUD pages.

Its current architecture combines:

``` text
Authentication
      +
Role-Based Access
      +
Companies & Contacts
      +
Leads & Conversion
      +
Deals & Pipelines
      +
Activities & Tasks
      +
Notes & Calendar
      +
Notifications & Preferences
      +
Global Search
      +
Audit Logging
      +
REST API
      +
Automated Testing
      +
Security & Performance Hardening
      +
Production Deployment
```

The immediate development path is to complete automated testing, then
proceed through security hardening, performance optimization, production
deployment, and final client acceptance testing.

The existing implementation should remain the source of truth throughout
the remaining phases. Future development should extend the established
architecture without duplicating already-completed modules or
restructuring the project unnecessarily.
