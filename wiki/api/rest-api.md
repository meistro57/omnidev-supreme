# REST API Reference

Complete documentation for the OmniDev Supreme REST API. This API provides programmatic access to all 29 agents, memory systems, and platform features.

## 🌐 Base URL

```
Production: https://api.omnidev-supreme.com
Development: http://localhost:8000
```

## 🔐 Authentication

All API requests require authentication using Bearer tokens.

### **Get Authentication Token**
```http
POST /auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### **Using the Token**
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 🏥 Health & Status

### **System Health**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.6.0",
  "timestamp": "2024-12-15T10:30:00Z",
  "agents": {
    "total": 29,
    "active": 29,
    "idle": 25,
    "busy": 4,
    "error": 0,
    "disabled": 0
  },
  "memory": {
    "vector_entries": 15420,
    "relational_entries": 8934,
    "session_entries": 156
  },
  "performance": {
    "avg_response_time": 1.2,
    "requests_per_second": 45.6,
    "error_rate": 0.002
  }
}
```

### **Detailed System Status**
```http
GET /status
```

**Response:**
```json
{
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "vector_store": "healthy",
    "ai_models": "healthy"
  },
  "resources": {
    "memory_usage": {
      "used": 2.1,
      "total": 8.0,
      "unit": "GB"
    },
    "cpu_usage": 34.5,
    "disk_usage": {
      "used": 45.2,
      "total": 100.0,
      "unit": "GB"
    }
  },
  "uptime": 86400,
  "active_connections": 23
}
```

## 🤖 Agents API

### **List All Agents**
```http
GET /agents
```

**Query Parameters:**
- `type`: Filter by agent type (`architect`, `coder`, `tester`, etc.)
- `status`: Filter by status (`idle`, `busy`, `error`, `disabled`)
- `system`: Filter by system (`agency`, `meistrocraft`, `obelisk`, etc.)
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_001",
      "name": "architect_agent",
      "type": "architect",
      "system": "agency",
      "status": "idle",
      "description": "Project planning and system design",
      "capabilities": [
        "system_architecture",
        "project_planning",
        "technology_selection",
        "database_design"
      ],
      "model_requirements": ["gpt-4", "claude-3-opus"],
      "priority": 10,
      "max_concurrent_tasks": 2,
      "stats": {
        "tasks_completed": 1247,
        "tasks_failed": 12,
        "average_response_time": 2.3,
        "total_tokens_used": 2456789
      },
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-12-15T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 29,
    "limit": 50,
    "offset": 0,
    "has_next": false,
    "has_prev": false
  }
}
```

### **Get Agent Details**
```http
GET /agents/{agent_id}
```

**Response:**
```json
{
  "id": "agent_001",
  "name": "architect_agent",
  "type": "architect",
  "system": "agency",
  "status": "idle",
  "description": "Project planning and system design",
  "capabilities": [
    "system_architecture",
    "project_planning",
    "technology_selection",
    "database_design"
  ],
  "model_requirements": ["gpt-4", "claude-3-opus"],
  "priority": 10,
  "max_concurrent_tasks": 2,
  "timeout_seconds": 300,
  "retry_count": 3,
  "current_tasks": [],
  "stats": {
    "tasks_completed": 1247,
    "tasks_failed": 12,
    "average_response_time": 2.3,
    "total_tokens_used": 2456789,
    "success_rate": 99.04,
    "last_24h": {
      "tasks": 45,
      "success_rate": 100.0,
      "avg_response_time": 2.1
    }
  },
  "configuration": {
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_p": 0.9
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-12-15T10:30:00Z"
}
```

### **Execute Agent Task**
```http
POST /agents/{agent_id}/execute
Content-Type: application/json

{
  "content": "Create a system architecture for a React e-commerce application",
  "type": "architecture_design",
  "complexity": "medium",
  "priority": 8,
  "context": {
    "project_id": "proj_123",
    "user_id": "user_456"
  },
  "constraints": {
    "budget": "medium",
    "timeline": "4 weeks",
    "technology_stack": ["React", "Node.js", "PostgreSQL"]
  }
}
```

**Response:**
```json
{
  "task_id": "task_789",
  "agent_id": "agent_001",
  "status": "completed",
  "result": {
    "success": true,
    "output": {
      "architecture": {
        "frontend": {
          "framework": "React 18",
          "state_management": "Redux Toolkit",
          "styling": "Tailwind CSS"
        },
        "backend": {
          "framework": "Express.js",
          "authentication": "JWT",
          "database": "PostgreSQL"
        },
        "infrastructure": {
          "hosting": "AWS",
          "cdn": "CloudFront",
          "monitoring": "DataDog"
        }
      },
      "recommendations": [
        "Use React 18 with concurrent features",
        "Implement server-side rendering with Next.js",
        "Use PostgreSQL with proper indexing"
      ],
      "estimated_timeline": "3-4 weeks",
      "resource_requirements": {
        "developers": 3,
        "devops": 1,
        "designer": 1
      }
    },
    "metadata": {
      "model_used": "gpt-4",
      "tokens_used": 2456,
      "processing_time": 2.3,
      "confidence_score": 0.92
    }
  },
  "created_at": "2024-12-15T10:30:00Z",
  "completed_at": "2024-12-15T10:30:02Z"
}
```

### **Get Agent Tasks**
```http
GET /agents/{agent_id}/tasks
```

**Query Parameters:**
- `status`: Filter by task status
- `limit`: Number of results (default: 20)
- `offset`: Pagination offset

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_789",
      "agent_id": "agent_001",
      "content": "Create a system architecture...",
      "type": "architecture_design",
      "status": "completed",
      "priority": 8,
      "created_at": "2024-12-15T10:30:00Z",
      "completed_at": "2024-12-15T10:30:02Z",
      "processing_time": 2.3,
      "tokens_used": 2456
    }
  ],
  "pagination": {
    "total": 1247,
    "limit": 20,
    "offset": 0,
    "has_next": true,
    "has_prev": false
  }
}
```

### **Update Agent Configuration**
```http
PUT /agents/{agent_id}/config
Content-Type: application/json

{
  "priority": 9,
  "max_concurrent_tasks": 3,
  "timeout_seconds": 600,
  "configuration": {
    "temperature": 0.8,
    "max_tokens": 6000
  }
}
```

## 📋 Tasks API

### **Create Task**
```http
POST /tasks
Content-Type: application/json

{
  "content": "Generate a React component for user authentication",
  "type": "code_generation",
  "complexity": "medium",
  "priority": 7,
  "agent_id": "agent_002",
  "context": {
    "project_id": "proj_123",
    "language": "javascript",
    "framework": "react"
  }
}
```

**Response:**
```json
{
  "id": "task_890",
  "content": "Generate a React component for user authentication",
  "type": "code_generation",
  "complexity": "medium",
  "priority": 7,
  "status": "pending",
  "agent_id": "agent_002",
  "context": {
    "project_id": "proj_123",
    "language": "javascript",
    "framework": "react"
  },
  "created_at": "2024-12-15T10:35:00Z",
  "estimated_completion": "2024-12-15T10:35:30Z"
}
```

### **Get Task Status**
```http
GET /tasks/{task_id}
```

**Response:**
```json
{
  "id": "task_890",
  "content": "Generate a React component for user authentication",
  "type": "code_generation",
  "complexity": "medium",
  "priority": 7,
  "status": "in_progress",
  "agent_id": "agent_002",
  "progress": 65,
  "context": {
    "project_id": "proj_123",
    "language": "javascript",
    "framework": "react"
  },
  "created_at": "2024-12-15T10:35:00Z",
  "started_at": "2024-12-15T10:35:02Z",
  "estimated_completion": "2024-12-15T10:35:30Z"
}
```

### **List Tasks**
```http
GET /tasks
```

**Query Parameters:**
- `status`: Filter by status
- `agent_id`: Filter by agent
- `project_id`: Filter by project
- `priority`: Filter by priority
- `limit`: Number of results
- `offset`: Pagination offset

## 📁 Projects API

### **Create Project**
```http
POST /projects
Content-Type: application/json

{
  "name": "E-commerce Platform",
  "description": "A modern e-commerce platform with React and Node.js",
  "language": "javascript",
  "framework": "react",
  "settings": {
    "auto_deploy": true,
    "code_review": true,
    "testing": "comprehensive"
  }
}
```

**Response:**
```json
{
  "id": "proj_123",
  "name": "E-commerce Platform",
  "description": "A modern e-commerce platform with React and Node.js",
  "language": "javascript",
  "framework": "react",
  "status": "active",
  "settings": {
    "auto_deploy": true,
    "code_review": true,
    "testing": "comprehensive"
  },
  "stats": {
    "files": 0,
    "lines_of_code": 0,
    "tasks_completed": 0,
    "agents_used": 0
  },
  "created_at": "2024-12-15T10:40:00Z",
  "updated_at": "2024-12-15T10:40:00Z"
}
```

### **Get Project Details**
```http
GET /projects/{project_id}
```

### **List Projects**
```http
GET /projects
```

### **Update Project**
```http
PUT /projects/{project_id}
Content-Type: application/json

{
  "name": "Updated E-commerce Platform",
  "description": "Updated description",
  "settings": {
    "auto_deploy": false,
    "code_review": true,
    "testing": "basic"
  }
}
```

### **Delete Project**
```http
DELETE /projects/{project_id}
```

## 🧠 Memory API

### **Search Memory**
```http
GET /memory/search
```

**Query Parameters:**
- `q`: Search query
- `type`: Memory type (`code`, `task`, `agent`, `knowledge`, `session`)
- `priority`: Memory priority (`low`, `medium`, `high`, `critical`)
- `limit`: Number of results
- `offset`: Pagination offset

**Response:**
```json
{
  "results": [
    {
      "id": "mem_001",
      "content": "React component for user authentication with JWT",
      "type": "code",
      "priority": "high",
      "metadata": {
        "agent": "coder_agent",
        "project_id": "proj_123",
        "language": "javascript"
      },
      "tags": ["react", "authentication", "jwt"],
      "similarity_score": 0.95,
      "created_at": "2024-12-15T10:20:00Z"
    }
  ],
  "pagination": {
    "total": 156,
    "limit": 20,
    "offset": 0,
    "has_next": true,
    "has_prev": false
  }
}
```

### **Store Memory**
```http
POST /memory
Content-Type: application/json

{
  "content": "React component for user authentication with JWT",
  "type": "code",
  "priority": "high",
  "metadata": {
    "agent": "coder_agent",
    "project_id": "proj_123",
    "language": "javascript"
  },
  "tags": ["react", "authentication", "jwt"],
  "session_id": "session_456"
}
```

### **Get Memory Entry**
```http
GET /memory/{memory_id}
```

### **Delete Memory Entry**
```http
DELETE /memory/{memory_id}
```

## 📊 Analytics API

### **System Analytics**
```http
GET /analytics/system
```

**Query Parameters:**
- `period`: Time period (`1h`, `24h`, `7d`, `30d`)
- `metrics`: Comma-separated metrics list

**Response:**
```json
{
  "period": "24h",
  "metrics": {
    "total_requests": 12456,
    "total_tasks": 2890,
    "avg_response_time": 1.3,
    "success_rate": 98.7,
    "error_rate": 1.3,
    "most_active_agents": [
      {
        "agent_id": "agent_002",
        "name": "coder_agent",
        "task_count": 567
      }
    ],
    "peak_usage": {
      "timestamp": "2024-12-15T14:30:00Z",
      "requests_per_second": 89.2
    }
  }
}
```

### **Agent Analytics**
```http
GET /analytics/agents/{agent_id}
```

**Response:**
```json
{
  "agent_id": "agent_002",
  "name": "coder_agent",
  "period": "24h",
  "metrics": {
    "tasks_completed": 567,
    "tasks_failed": 8,
    "success_rate": 98.6,
    "avg_response_time": 1.8,
    "total_tokens_used": 145678,
    "avg_tokens_per_task": 257,
    "peak_usage": "2024-12-15T14:30:00Z",
    "task_types": {
      "code_generation": 345,
      "code_review": 123,
      "debugging": 99
    }
  }
}
```

## 🔧 Configuration API

### **Get System Configuration**
```http
GET /config
```

**Response:**
```json
{
  "system": {
    "max_concurrent_tasks": 100,
    "default_timeout": 300,
    "retry_count": 3
  },
  "models": {
    "openai": {
      "default_model": "gpt-4",
      "max_tokens": 4000,
      "temperature": 0.7
    },
    "anthropic": {
      "default_model": "claude-3-opus",
      "max_tokens": 4000,
      "temperature": 0.7
    }
  },
  "memory": {
    "max_vector_entries": 100000,
    "max_relational_entries": 50000,
    "session_timeout": 3600
  }
}
```

### **Update System Configuration**
```http
PUT /config
Content-Type: application/json

{
  "system": {
    "max_concurrent_tasks": 150,
    "default_timeout": 600
  }
}
```

## 🔒 Error Handling

### **Error Response Format**
```json
{
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agent with ID 'agent_999' not found",
    "details": {
      "agent_id": "agent_999",
      "suggested_action": "Check available agents using GET /agents"
    },
    "timestamp": "2024-12-15T10:45:00Z",
    "request_id": "req_abc123"
  }
}
```

### **HTTP Status Codes**
- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `502 Bad Gateway`: Upstream service error
- `503 Service Unavailable`: Service temporarily unavailable

### **Common Error Codes**
- `AGENT_NOT_FOUND`: Agent does not exist
- `AGENT_BUSY`: Agent is currently busy
- `TASK_FAILED`: Task execution failed
- `INVALID_INPUT`: Invalid input parameters
- `RATE_LIMIT_EXCEEDED`: API rate limit exceeded
- `INSUFFICIENT_PERMISSIONS`: Insufficient permissions
- `MODEL_ERROR`: AI model error
- `MEMORY_FULL`: Memory storage full

## 🚀 Rate Limiting

### **Rate Limits**
- **Standard**: 1000 requests per hour
- **Premium**: 5000 requests per hour
- **Enterprise**: 20000 requests per hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### **Rate Limit Exceeded Response**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 3600 seconds.",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "reset": 1640995200
    }
  }
}
```

## 🔍 Pagination

### **Pagination Parameters**
- `limit`: Number of results per page (default: 20, max: 100)
- `offset`: Number of results to skip (default: 0)

### **Pagination Response**
```json
{
  "pagination": {
    "total": 1247,
    "limit": 20,
    "offset": 40,
    "has_next": true,
    "has_prev": true,
    "next_url": "/agents?limit=20&offset=60",
    "prev_url": "/agents?limit=20&offset=20"
  }
}
```

## 🧪 Testing

### **Interactive API Explorer**
Visit `http://localhost:8000/docs` for an interactive API explorer with:
- **Live Testing**: Test endpoints directly
- **Request/Response Examples**: See real examples
- **Authentication**: Built-in auth testing
- **Schema Validation**: Request/response validation

### **API Client Libraries**
- **Python**: `pip install omnidev-supreme-client`
- **JavaScript**: `npm install omnidev-supreme-client`
- **Go**: `go get github.com/omnidev-supreme/go-client`
- **Java**: Maven/Gradle packages available

### **Postman Collection**
Download our [Postman collection](https://github.com/meistro57/omnidev-supreme/blob/main/api/postman_collection.json) for easy testing.

---

<div align="center">
  <p><strong>🚀 Ready to integrate with the OmniDev Supreme API?</strong></p>
  <p>Start building powerful AI-driven applications today!</p>
  
  <a href="websocket-api.md">
    <strong>Explore WebSocket API →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/api/rest-api.md)*