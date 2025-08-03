# Mini Event Management System

A lightweight FastAPI-based backend system for managing events and attendee registrations.

## Features
- Create and list events
- Register attendees
- Handle event capacity
- SQLite in-memory DB for testing
- Clean architecture with SQLAlchemy ORM

## 🏗️ Project Structure
```
EventManagement/
├── db/
│   └── database.py
├── models/
│   └── event.py
├── routes/
│   └── event.py
├── schemas/
│   └── event_schema.py
├── services/
│   └── event_service.py
├── main.py
├── test/
│   └── test_event_service.py
├── requirements.txt
├── README.md
└── .gitignore
```
## 🔌 API Endpoints

### ➕ Create Event  
**POST** `/events`  
Create a new event.  
**Request Body:**
```json
{
  "name": "Python Conference",
  "location": "Online",
  "start_time": "2025-08-02T10:00:00Z",
  "end_time": "2025-08-02T12:00:00Z",
  "max_capacity": 100
}
```

### 📋 List Events  
**GET** `/events`  
Returns all upcoming events.

### 🧾 Register Attendee  
**POST** `/events/{event_id}/register`  
Register a new attendee for the event.  
**Request Body:**
```json
{
  "name": "Undertaker",
  "email": "undertaker@example.com"
}
```

### 📜 List Attendees  
**GET** `/events/{event_id}/attendees`  
Get all registered attendees for the given event.

---

## 🗃️ Database Schema

### 📌 `Event` Table
| Column        | Type     | Description               |
|---------------|----------|---------------------------|
| id            | String   | Primary Key (UUID)        |
| name          | String   | Event name                |
| location      | String   | Event location            |
| start_time    | DateTime | Start datetime (UTC)      |
| end_time      | DateTime | End datetime (UTC)        |
| max_capacity  | Integer  | Max number of attendees   |

### 📌 `Attendee` Table
| Column   | Type     | Description                        |
|----------|----------|------------------------------------|
| id       | String   | Primary Key (UUID)                 |
| name     | String   | Attendee name                      |
| email    | String   | Attendee email (unique per event) |
| event_id | String   | Foreign key → Event.id             |

---


## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Mini-Event-Management-System
```

### 2. Create and activate a virtual environment
#### 💻 macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate  # 🔄 Activate virtual environment
```

#### 🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate  # 🔄 Activate virtual environment
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Run the FastAPI App
```bash
uvicorn app.main:app --reload
```
Visit for OpenAPI documentation and testing the APIs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Run Unit Tests
```bash
python3 -m unittest discover tests
```

## 🧼 Ignore Cache Files
Make sure you add this to your `.gitignore` to prevent pushing `__pycache__`:
```bash
__pycache__/
*.py[cod]
venv/
```

## 📬 Contact
For any queries or suggestions, please contact Prem Kumar R.
