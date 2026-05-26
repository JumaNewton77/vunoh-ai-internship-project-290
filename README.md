# Vunoh Diaspora AI Assistant

An AI-powered web application built for the Vunoh Global AI Internship Practical Test that helps Kenyans living abroad initiate and track important services back home.

The platform uses Artificial Intelligence to understand natural language requests, extract structured information, assess risk, generate fulfillment steps, assign tasks to relevant teams, and communicate updates through multiple channels.

---

# Problem Statement

Kenyans living abroad often struggle to manage important tasks back home such as:

- Sending money to family members
- Hiring local services
- Verifying important documents
- Requesting airport transfer services
- Tracking existing requests

Most people currently rely on WhatsApp, phone calls, or relatives, which can be slow, unreliable, and difficult to track.

This project aims to solve that problem through an AI-powered assistant.

---

# Features

### 1. Natural Language Input

Users can type requests in plain English:

Examples:

```text
I need to send KES 15,000 to my mother in Kisumu urgently

Please verify my land title deed for my Karen property

Can someone clean my apartment in Westlands on Friday?
```

---

### 2. AI Intent Extraction

The AI extracts:

#### Intent

Supported intents:

- send_money
- hire_service
- verify_document
- airport_transfer
- check_status

#### Entities

Examples of extracted entities:

- Amount
- Recipient
- Location
- Urgency
- Service Type
- Document Type

Example output:

```json
{
    "intent":"send_money",
    "entities":{
        "amount":2000,
        "recipient":"mother",
        "location":"Kitale",
        "urgency":"high"
    }
}
```

---

### 3. Risk Scoring System

Each request receives a calculated risk score based on real-world diaspora considerations.

Risk factors include:

| Rule | Score |
|--------|--------|
| Money transfer > KES 100,000 | +35 |
| Urgent request | +15 |
| Land title verification | +25 |
| Unknown recipient | +20 |
| Trusted customer history | -10 |

Risk levels:

| Score | Level |
|---------|-------|
| 0–30 | Low |
| 31–60 | Medium |
| 61–100 | High |

Example:

```text
Risk Score: 75
Level: High

Reasons:
- Large transfer amount
- Urgent request
- Document verification
```

---

### 4. Task Creation

Every request generates a task record containing:

- Unique task code
- Extracted intent
- Entities
- Risk score
- Status
- Employee assignment
- Creation timestamp

Example:

```text
Task Code: VNH-2026-001
```

---

### 5. AI Workflow Step Generation

The AI creates task-specific fulfillment steps.

Example:

Money transfer:

1. Verify sender identity
2. Confirm recipient details
3. Review risk indicators
4. Initiate transfer
5. Send confirmation

Document verification:

1. Receive document
2. Verify ownership records
3. Legal review
4. Approve verification
5. Notify customer

---

### 6. Three Communication Formats

For each task, the AI generates:

### WhatsApp Style

```text
Hi Newton 👋

We've received your money transfer request.

Task Code: VNH-2026-001

We'll keep you updated.
```

### Email Style

```text
Subject: Vunoh Task Confirmation

Dear Customer,

Your request has been received successfully.

Task Code: VNH-2026-001
Risk Score: Medium
Status: Pending

Regards,
Vunoh Team
```

### SMS Style

```text
VNH-2026-001: Request received. Status pending.
```

---

### 7. Employee Assignment

Tasks are automatically assigned:

| Intent | Team |
|----------|------|
| send_money | Finance |
| hire_service | Operations |
| verify_document | Legal |
| airport_transfer | Logistics |
| check_status | Customer Support |

---

### 8. Dashboard

Dashboard features:

- View all tasks
- View risk scores
- Status tracking
- Employee assignment
- Task creation dates
- Analytics cards
- Search functionality
- Task detail view

---

### 9. Database Persistence

Stored data:

- Tasks
- Extracted entities
- Workflow steps
- Generated messages
- Risk scores
- Employee assignments
- Status history

---

# Technology Stack

## Backend

- Python
- Django

## Frontend

- HTML
- CSS
- Vanilla JavaScript

## Database

- SQLite

## AI Services

- Groq API
- Llama 3.3 70B

## OCR

- Tesseract OCR

---

# System Architecture

```text
User Request
      ↓
Frontend Form
      ↓
Django Backend
      ↓
AI Processing Layer
      ↓
Intent + Entity Extraction
      ↓
Risk Scoring Engine
      ↓
Task Generation
      ↓
Workflow Generation
      ↓
Employee Assignment
      ↓
Database Storage
      ↓
Dashboard Display
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/JumaNewton77/vunoh-ai-internship-project-290.git
```

Move into project:

```bash
cd vunoh-ai-internship-project-290
```

---

## Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Create environment variables

Create:

```text
.env
```

Add:

```env
SECRET_KEY=your_secret_key

GROQ_API_KEY=your_groq_api_key
```

---

## Run migrations

```bash
python manage.py migrate
```

---

## Run server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

---

# SQL Dump

SQL dump file included:

```text
database/database_dump.sql
```

Contains:

- Full schema
- Sample tasks
- Messages
- Risk scores
- Employee assignments

---

# Sample Tasks

Included sample records:

1. Send KES 15,00 to Kitale
2. Verify Kitale land title
3. Apartment cleaning request
4. Airport transfer request
5. Status check request

---

# Decisions I Made and Why

## AI tools used

### ChatGPT

Used for:

- Prompt refinement
- Architecture discussions
- README creation
- Debugging

### GitHub Copilot

Used for:

- Route generation
- Boilerplate code assistance

### Groq LLM

Used for:

- Intent extraction
- Step generation
- Message generation

---

## Prompt Design

The prompt was designed to:

- Force JSON output
- Avoid markdown responses
- Restrict possible intents
- Ensure consistent formatting
- Separate entities from free text

I intentionally excluded conversational responses because they make parsing difficult.

---

## One AI suggestion I changed

AI initially suggested storing workflow steps as comma-separated text.

I changed this to JSON storage because:

- Easier retrieval
- Better scalability
- Supports future editing
- Cleaner database structure

---

## One thing that did not work as expected

Groq occasionally returned malformed JSON responses.

Example:

```text
```json
{
"intent":"send_money"
}
```
```

This caused parsing errors.

Solution:

I added response cleanup and validation before processing:

python 
content=content.replace("```json","")
content=content.replace("```","")
content=content.strip()
```

---

# Future Improvements

Potential improvements:

- Real authentication system
- User accounts
- Email integration
- WhatsApp API integration
- Real payment integration
- Analytics dashboard charts
- Notification system
- Deployment with Docker
- PostgreSQL database
- Role-based employee access

---

# Evaluation Alignment

| Requirement | Implemented |
|-------------|-------------|
| Natural language input | ✅ |
| AI intent extraction | ✅ |
| Risk scoring | ✅ |
| Task creation | ✅ |
| Step generation | ✅ |
| Three message formats | ✅ |
| Employee assignment | ✅ |
| Dashboard | ✅ |
| Database persistence | ✅ |
| SQL dump | ✅ |

---

# Author

Newton Juma

BSc Computer Science  
Meru University of Science and Technology

GitHub:

https://github.com/JumaNewton77

---

# License
