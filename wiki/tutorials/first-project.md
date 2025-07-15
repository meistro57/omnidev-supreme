# Tutorial 1: Your First Project

Welcome to your first hands-on experience with OmniDev Supreme! This tutorial will guide you through creating a complete project using multiple AI agents, from initial concept to deployment.

## 🎯 Tutorial Overview

In this tutorial, you'll learn how to:
- Create a new project in OmniDev Supreme
- Work with multiple AI agents in sequence
- Use the Monaco Editor for development
- Navigate the agent collaboration workflow
- Deploy your first application

### **What We'll Build**
A simple **Task Manager Application** with:
- React frontend with TypeScript
- FastAPI backend with Python
- SQLite database
- Basic authentication
- Responsive design

### **Time Required**
⏱️ **45-60 minutes** (depending on your experience level)

### **Prerequisites**
- OmniDev Supreme installed and running
- Basic understanding of web development
- API keys configured (OpenAI recommended)

## 🚀 Step 1: Create Your Project

### **1.1 Navigate to Projects**
1. Open OmniDev Supreme in your browser: `http://localhost:3000`
2. Click **Projects** in the navigation menu
3. Click the **New Project** button

### **1.2 Configure Project Settings**
Fill in the project details:
```json
{
  "name": "My Task Manager",
  "description": "A simple task management application with React and FastAPI",
  "language": "javascript",
  "framework": "react",
  "settings": {
    "auto_deploy": true,
    "code_review": true,
    "testing": "comprehensive"
  }
}
```

### **1.3 Project Structure**
After creation, you'll see your project structure:
```
my-task-manager/
├── frontend/          # React TypeScript app
├── backend/           # FastAPI Python app
├── database/          # SQLite database
├── tests/             # Test files
├── docs/              # Documentation
└── deployment/        # Deployment configurations
```

## 📝 Step 2: Define Requirements with Architect Agent

### **2.1 Open the Editor**
1. Click **Editor** in the navigation
2. Create a new file: `requirements.md`
3. Write your requirements in natural language

### **2.2 Write Requirements**
```markdown
# Task Manager Requirements

## Overview
Create a task management application for personal productivity.

## Features
- User authentication (login/register)
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Filter tasks by status
- Search tasks by title
- Responsive design for mobile and desktop

## Technical Requirements
- Frontend: React with TypeScript
- Backend: FastAPI with Python
- Database: SQLite
- Authentication: JWT tokens
- Styling: Tailwind CSS
- Testing: Jest for frontend, pytest for backend

## User Stories
1. As a user, I want to register an account
2. As a user, I want to login to my account
3. As a user, I want to create new tasks
4. As a user, I want to view my tasks
5. As a user, I want to edit existing tasks
6. As a user, I want to delete tasks
7. As a user, I want to mark tasks as complete
8. As a user, I want to filter tasks by status
9. As a user, I want to search for specific tasks
```

### **2.3 Invoke the Architect Agent**
1. Select all the requirements text
2. Right-click and choose **Ask Architect Agent**
3. Or type a comment: `// Architect: Design system architecture for this task manager`

### **2.4 Review Architecture Output**
The Architect Agent will provide:
```json
{
  "system_architecture": {
    "frontend": {
      "framework": "React 18 with TypeScript",
      "state_management": "Redux Toolkit",
      "styling": "Tailwind CSS",
      "routing": "React Router",
      "http_client": "Axios"
    },
    "backend": {
      "framework": "FastAPI",
      "database": "SQLite with SQLAlchemy",
      "authentication": "JWT with passlib",
      "validation": "Pydantic models",
      "testing": "pytest with httpx"
    },
    "database_schema": {
      "users": ["id", "email", "password_hash", "created_at"],
      "tasks": ["id", "title", "description", "completed", "user_id", "created_at", "updated_at"]
    },
    "api_endpoints": [
      "POST /auth/register",
      "POST /auth/login",
      "GET /tasks",
      "POST /tasks",
      "PUT /tasks/{id}",
      "DELETE /tasks/{id}"
    ]
  },
  "recommendations": [
    "Use React Query for server state management",
    "Implement proper error handling on both frontend and backend",
    "Add input validation and sanitization",
    "Use environment variables for configuration",
    "Implement proper logging and monitoring"
  ]
}
```

## 💻 Step 3: Generate Backend Code with Coder Agent

### **3.1 Create Backend Structure**
1. Create a new file: `backend/main.py`
2. Type a comment: `// Coder: Generate FastAPI backend for task manager based on the architecture`

### **3.2 Backend Code Generation**
The Coder Agent will generate:

#### **main.py**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, UserCreate, UserResponse
from auth import create_access_token, verify_token, get_password_hash, verify_password
import uvicorn

app = FastAPI(title="Task Manager API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user = verify_token(credentials.credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

# Authentication routes
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(id=db_user.id, email=db_user.email, created_at=db_user.created_at)

@app.post("/auth/login")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    # Verify user credentials
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Task routes
@app.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    completed: bool = None,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if search:
        query = query.filter(Task.title.contains(search))
    
    tasks = query.all()
    return tasks

@app.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id, 
        Task.user_id == current_user.id
    ).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The Coder Agent will also generate:
- Database models (`models.py`)
- Pydantic schemas (`schemas.py`)
- Authentication utilities (`auth.py`)
- Database configuration (`database.py`)

## 🎨 Step 4: Generate Frontend Code

### **4.1 Create Frontend Structure**
1. Create a new file: `frontend/src/App.tsx`
2. Type: `// Coder: Generate React frontend for task manager with TypeScript and Tailwind`

### **4.2 Frontend Code Generation**
The Coder Agent will generate a complete React application:

#### **App.tsx**
```typescript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store/store';
import { AuthProvider } from './context/AuthContext';
import { Header } from './components/Header';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { TasksPage } from './pages/TasksPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import './App.css';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Header />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <TasksPage />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </main>
          </div>
        </Router>
      </AuthProvider>
    </Provider>
  );
};

export default App;
```

The agent will also generate:
- Component library (Header, TaskList, TaskForm, etc.)
- Redux store and slices
- API service layer
- Authentication context
- Custom hooks
- TypeScript type definitions

## 🧪 Step 5: Generate Tests with Tester Agent

### **5.1 Request Test Generation**
1. Select your backend code
2. Type: `// Tester: Generate comprehensive tests for this FastAPI backend`

### **5.2 Backend Tests**
The Tester Agent will create:

#### **test_main.py**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from main import app

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_user():
    """Create a test user."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return user_data

@pytest.fixture
def auth_token(test_user):
    """Get authentication token."""
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Get authentication headers."""
    return {"Authorization": f"Bearer {auth_token}"}

class TestAuthentication:
    def test_register_success(self):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "password": "password123"
        }
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["email"] == user_data["email"]

    def test_register_duplicate_email(self, test_user):
        """Test registration with duplicate email."""
        response = client.post("/auth/register", json=test_user)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_success(self, test_user):
        """Test successful login."""
        response = client.post("/auth/login", json=test_user)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        user_data = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=user_data)
        assert response.status_code == 401

class TestTasks:
    def test_create_task(self, auth_headers):
        """Test creating a new task."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        response = client.post("/tasks", json=task_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == task_data["title"]

    def test_get_tasks(self, auth_headers):
        """Test retrieving tasks."""
        # Create a task first
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        client.post("/tasks", json=task_data, headers=auth_headers)
        
        # Get tasks
        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_update_task(self, auth_headers):
        """Test updating a task."""
        # Create a task first
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        create_response = client.post("/tasks", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"
        assert response.json()["completed"] == True

    def test_delete_task(self, auth_headers):
        """Test deleting a task."""
        # Create a task first
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        create_response = client.post("/tasks", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_filter_tasks_by_completion(self, auth_headers):
        """Test filtering tasks by completion status."""
        # Create completed and incomplete tasks
        completed_task = {
            "title": "Completed Task",
            "description": "This task is completed",
            "completed": True
        }
        incomplete_task = {
            "title": "Incomplete Task",
            "description": "This task is not completed",
            "completed": False
        }
        
        client.post("/tasks", json=completed_task, headers=auth_headers)
        client.post("/tasks", json=incomplete_task, headers=auth_headers)
        
        # Filter for completed tasks
        response = client.get("/tasks?completed=true", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert all(task["completed"] for task in tasks)
        
        # Filter for incomplete tasks
        response = client.get("/tasks?completed=false", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert all(not task["completed"] for task in tasks)

    def test_search_tasks(self, auth_headers):
        """Test searching tasks by title."""
        # Create tasks with different titles
        task1 = {
            "title": "Important Meeting",
            "description": "Quarterly review meeting",
            "completed": False
        }
        task2 = {
            "title": "Buy Groceries",
            "description": "Weekly grocery shopping",
            "completed": False
        }
        
        client.post("/tasks", json=task1, headers=auth_headers)
        client.post("/tasks", json=task2, headers=auth_headers)
        
        # Search for tasks containing "Meeting"
        response = client.get("/tasks?search=Meeting", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert "Meeting" in tasks[0]["title"]

    def test_unauthorized_access(self):
        """Test accessing protected endpoints without authentication."""
        response = client.get("/tasks")
        assert response.status_code == 401
```

### **5.3 Frontend Tests**
The Tester Agent will also create React component tests:

#### **TaskList.test.tsx**
```typescript
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { TaskList } from '../components/TaskList';
import { tasksSlice } from '../store/tasksSlice';
import { Task } from '../types/Task';

const mockTasks: Task[] = [
  {
    id: 1,
    title: 'Test Task 1',
    description: 'This is a test task',
    completed: false,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  },
  {
    id: 2,
    title: 'Test Task 2',
    description: 'This is another test task',
    completed: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  }
];

const mockStore = configureStore({
  reducer: {
    tasks: tasksSlice.reducer
  },
  preloadedState: {
    tasks: {
      items: mockTasks,
      loading: false,
      error: null
    }
  }
});

const renderWithProvider = (component: React.ReactElement) => {
  return render(
    <Provider store={mockStore}>
      {component}
    </Provider>
  );
};

describe('TaskList', () => {
  test('renders task list with tasks', () => {
    renderWithProvider(<TaskList />);
    
    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    expect(screen.getByText('Test Task 2')).toBeInTheDocument();
  });

  test('filters tasks by completion status', async () => {
    renderWithProvider(<TaskList />);
    
    // Click on "Completed" filter
    fireEvent.click(screen.getByText('Completed'));
    
    await waitFor(() => {
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
      expect(screen.queryByText('Test Task 1')).not.toBeInTheDocument();
    });
  });

  test('searches tasks by title', async () => {
    renderWithProvider(<TaskList />);
    
    const searchInput = screen.getByPlaceholderText('Search tasks...');
    fireEvent.change(searchInput, { target: { value: 'Task 1' } });
    
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument();
    });
  });

  test('toggles task completion', async () => {
    renderWithProvider(<TaskList />);
    
    const checkbox = screen.getAllByRole('checkbox')[0];
    fireEvent.click(checkbox);
    
    await waitFor(() => {
      expect(checkbox).toBeChecked();
    });
  });

  test('deletes task', async () => {
    renderWithProvider(<TaskList />);
    
    const deleteButton = screen.getAllByText('Delete')[0];
    fireEvent.click(deleteButton);
    
    await waitFor(() => {
      expect(screen.queryByText('Test Task 1')).not.toBeInTheDocument();
    });
  });
});
```

## 🔍 Step 6: Code Review with Reviewer Agent

### **6.1 Request Code Review**
1. Select all your backend code
2. Type: `// Reviewer: Please review this FastAPI backend code for quality and security`

### **6.2 Review Results**
The Reviewer Agent will provide:

```json
{
  "quality_score": 8.5,
  "security_score": 9.0,
  "performance_score": 7.8,
  "issues": {
    "critical": [],
    "high": [
      {
        "type": "security",
        "description": "Password hashing algorithm could be stronger",
        "file": "auth.py",
        "line": 15,
        "suggestion": "Use bcrypt with higher cost factor"
      }
    ],
    "medium": [
      {
        "type": "performance",
        "description": "Database queries could be optimized",
        "file": "main.py",
        "line": 87,
        "suggestion": "Add database indexes for frequently queried fields"
      }
    ],
    "low": [
      {
        "type": "style",
        "description": "Missing docstrings for some functions",
        "file": "main.py",
        "line": 45,
        "suggestion": "Add comprehensive docstrings"
      }
    ]
  },
  "recommendations": [
    "Add input validation for all endpoints",
    "Implement rate limiting for authentication endpoints",
    "Add logging for security events",
    "Consider using environment variables for sensitive configuration"
  ],
  "approved": true
}
```

## 🔧 Step 7: Fix Issues with Fixer Agent

### **7.1 Request Fixes**
1. Copy the review results
2. Type: `// Fixer: Please fix the security and performance issues identified in the review`

### **7.2 Applied Fixes**
The Fixer Agent will automatically apply fixes:

#### **Enhanced Authentication (auth.py)**
```python
import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from models import User

# Use bcrypt with higher cost factor
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

SECRET_KEY = "your-secret-key-here"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash with bcrypt."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session) -> User:
    """Verify JWT token and return user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except JWTError:
        return None
```

#### **Database Optimization (models.py)**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False, index=True)  # Index for filtering
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Index for sorting
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="tasks")
    
    # Composite index for user_id and completed (common query pattern)
    __table_args__ = (Index('ix_user_completed', 'user_id', 'completed'),)
```

## 🚀 Step 8: Deploy with Deployer Agent

### **8.1 Request Deployment**
1. Type: `// Deployer: Create deployment configuration for this task manager application`

### **8.2 Deployment Configuration**
The Deployer Agent will create:

#### **docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend:/app
      - sqlite_data:/app/data
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
    depends_on:
      - backend

  db:
    image: sqlite:latest
    volumes:
      - sqlite_data:/data

volumes:
  sqlite_data:
```

#### **Dockerfile (Backend)**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Dockerfile (Frontend)**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### **8.3 Deploy Application**
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or deploy to cloud provider
# The Deployer Agent will provide specific instructions for AWS, GCP, or Azure
```

## 🎉 Step 9: Test Your Application

### **9.1 Run the Application**
1. Open `http://localhost:3000` in your browser
2. Register a new account
3. Login with your credentials
4. Create your first task

### **9.2 Test All Features**
- ✅ User registration
- ✅ User login
- ✅ Create tasks
- ✅ View tasks
- ✅ Edit tasks
- ✅ Delete tasks
- ✅ Mark tasks as complete
- ✅ Filter tasks by status
- ✅ Search tasks

### **9.3 Run Automated Tests**
```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test

# Integration tests
pytest tests/integration/ -v
```

## 📊 Step 10: Monitor and Optimize

### **10.1 Performance Monitoring**
The platform provides built-in monitoring:
- API response times
- Database query performance
- Memory usage
- Error rates

### **10.2 Agent Performance**
Monitor how each agent performed:
- **Architect Agent**: 45 seconds (architecture design)
- **Coder Agent**: 120 seconds (full-stack generation)
- **Reviewer Agent**: 30 seconds (code review)
- **Fixer Agent**: 60 seconds (issue resolution)
- **Tester Agent**: 90 seconds (comprehensive tests)
- **Deployer Agent**: 180 seconds (deployment setup)

### **10.3 Code Quality Metrics**
- **Overall Quality Score**: 8.7/10
- **Security Score**: 9.2/10
- **Performance Score**: 8.1/10
- **Test Coverage**: 94%
- **Documentation**: 89%

## 🎯 What You've Learned

Congratulations! You've successfully:

### **Technical Skills**
- ✅ Created a full-stack application with AI assistance
- ✅ Worked with multiple AI agents in collaboration
- ✅ Used the Monaco Editor for development
- ✅ Implemented authentication and CRUD operations
- ✅ Set up automated testing and deployment

### **OmniDev Supreme Skills**
- ✅ Project creation and management
- ✅ Agent collaboration workflows
- ✅ Code generation and review processes
- ✅ Quality assurance and testing
- ✅ Deployment and monitoring

### **Best Practices**
- ✅ Requirements-driven development
- ✅ Security-first approach
- ✅ Comprehensive testing
- ✅ Code review and optimization
- ✅ Automated deployment

## 🚀 Next Steps

### **Extend Your Application**
1. Add user profiles and settings
2. Implement task categories and tags
3. Add due dates and reminders
4. Create task sharing and collaboration
5. Add file attachments to tasks

### **Explore Advanced Features**
1. **Multi-Agent Workflows**: Complex workflows with multiple agents
2. **Custom Agents**: Create your own specialized agents
3. **Memory System**: Leverage the knowledge graph
4. **Real-time Collaboration**: Multi-user editing
5. **Production Deployment**: Deploy to cloud platforms

### **Continue Learning**
- **[Tutorial 2: Agent Interaction](agent-interaction.md)** - Deep dive into agent collaboration
- **[Tutorial 3: Memory System](memory-system.md)** - Leverage the knowledge base
- **[Tutorial 4: Multi-Agent Workflows](multi-agent-workflows.md)** - Complex orchestration
- **[Tutorial 5: Custom Extensions](custom-extensions.md)** - Extend the platform

## 🛟 Troubleshooting

### **Common Issues**
1. **Agent Not Responding**: Check API keys and network connection
2. **Build Failures**: Ensure all dependencies are installed
3. **Authentication Issues**: Verify JWT configuration
4. **Database Errors**: Check database connection and migrations
5. **Frontend Issues**: Verify backend API is running

### **Getting Help**
- **Discord**: Real-time community support
- **GitHub Issues**: Report bugs and get help
- **Documentation**: Check the troubleshooting guide
- **Stack Overflow**: Use tags `omnidev-supreme`, `ai-agents`

---

<div align="center">
  <p><strong>🎉 Congratulations on completing your first OmniDev Supreme project!</strong></p>
  <p>You've just experienced the power of AI-assisted development with 29 specialized agents.</p>
  
  <a href="agent-interaction.md">
    <strong>Continue to Tutorial 2 →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/tutorials/first-project.md)*