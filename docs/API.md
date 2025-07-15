# OmniDev Supreme API Documentation

## 🌐 API Overview

OmniDev Supreme provides a comprehensive REST API for interacting with the unified agent system. The API supports real-time communication through WebSocket connections and provides extensive capabilities for development automation.

**Base URL**: `http://localhost:8000` (development) | `https://api.omnidev-supreme.com` (production)

## 🚀 Quick Start

### Authentication
Currently using API key authentication. Include your API key in the header:
```
Authorization: Bearer YOUR_API_KEY
```

### Content Type
All requests should use JSON:
```
Content-Type: application/json
```

## 📡 Core Endpoints

### 1. Health Check
Check system status and availability.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "agents": {
    "total": 6,
    "active": 6,
    "idle": 6
  },
  "memory": {
    "total_items": 1250,
    "vector_index_size": 1024,
    "active_sessions": 3
  }
}
```

### 2. Single Agent Task
Execute a task with a specific agent.

**Endpoint**: `POST /task`

**Request**:
```json
{
  "agent": "architect",
  "content": "Design a REST API for user management",
  "session_id": "user_session_123",
  "language": "python",
  "context": {
    "project_type": "web_api",
    "framework": "fastapi"
  }
}
```

**Response**:
```json
{
  "success": true,
  "task_id": "task_123456",
  "agent": "architect",
  "result": {
    "plan": {
      "title": "User Management REST API",
      "description": "Comprehensive user management system",
      "tasks": [
        {
          "id": "task_1",
          "title": "Database Design",
          "description": "Design user table schema",
          "priority": "high"
        }
      ]
    }
  },
  "tokens_used": 1250,
  "response_time": 2.5,
  "model_used": "gpt-4",
  "memory_ids": ["mem_123", "mem_124"]
}
```

### 3. Multi-Agent Workflow
Execute a complete multi-agent workflow.

**Endpoint**: `POST /workflow`

**Request**:
```json
{
  "content": "Create a web application with user authentication",
  "session_id": "user_session_123",
  "language": "python",
  "framework": "fastapi",
  "deployment": {
    "platform": "docker",
    "environment": "development"
  }
}
```

**Response**:
```json
{
  "success": true,
  "workflow_id": "workflow_123456",
  "stages": [
    {
      "stage": "architecture",
      "agent": "architect",
      "result": {
        "plan": { /* architectural plan */ }
      }
    },
    {
      "stage": "coding",
      "agent": "coder",
      "result": {
        "code_files": [ /* generated code */ ]
      }
    },
    {
      "stage": "testing",
      "agent": "tester",
      "result": {
        "test_files": [ /* generated tests */ ]
      }
    },
    {
      "stage": "review",
      "agent": "reviewer",
      "result": {
        "review_results": { /* code review */ }
      }
    },
    {
      "stage": "deployment",
      "agent": "deployer",
      "result": {
        "deployment_config": { /* deployment files */ }
      }
    }
  ],
  "total_tokens": 8500,
  "total_time": 45.2
}
```

### 4. Memory Search
Search through the unified memory system.

**Endpoint**: `GET /memory/search`

**Parameters**:
- `query` (string, required): Search query
- `memory_type` (string, optional): Type filter (code, task, project, agent)
- `limit` (integer, optional): Number of results (default: 10)
- `use_vector` (boolean, optional): Use vector search (default: true)

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "id": "mem_123",
      "content": "Generated code for user authentication",
      "memory_type": "code",
      "similarity_score": 0.95,
      "metadata": {
        "agent": "coder",
        "language": "python",
        "timestamp": "2024-01-15T10:30:00Z"
      }
    }
  ],
  "total_results": 45,
  "query_time": 0.15
}
```

### 5. Agent Status
Get status and information about all agents.

**Endpoint**: `GET /agents`

**Response**:
```json
{
  "total_agents": 6,
  "agents_by_type": {
    "architect": 1,
    "coder": 1,
    "tester": 1,
    "reviewer": 1,
    "fixer": 1,
    "deployer": 1
  },
  "available_agents": [
    {
      "name": "architect",
      "type": "architect",
      "capabilities": [
        "requirements_analysis",
        "architecture_design",
        "task_breakdown"
      ],
      "status": "idle",
      "can_accept_tasks": true,
      "stats": {
        "tasks_completed": 150,
        "avg_response_time": 2.3,
        "success_rate": 0.97
      }
    }
  ]
}
```

### 6. Session Management
Create and manage user sessions.

**Endpoint**: `POST /session`

**Request**:
```json
{
  "user_id": "user_123",
  "project_context": {
    "project_name": "My Web App",
    "technology_stack": ["python", "fastapi", "react"],
    "requirements": "User authentication and data management"
  }
}
```

**Response**:
```json
{
  "session_id": "session_123456",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-01-15T18:30:00Z",
  "context": {
    "project_name": "My Web App",
    "technology_stack": ["python", "fastapi", "react"]
  }
}
```

## 🔄 WebSocket API

For real-time communication and streaming responses.

**Endpoint**: `ws://localhost:8000/ws/{session_id}`

### Message Types

#### 1. Task Execution
```json
{
  "type": "task",
  "data": {
    "agent": "coder",
    "content": "Create a user model",
    "context": { /* context data */ }
  }
}
```

#### 2. Workflow Execution
```json
{
  "type": "workflow",
  "data": {
    "content": "Build a complete web application",
    "language": "python"
  }
}
```

#### 3. Status Updates
```json
{
  "type": "status",
  "data": {
    "stage": "coding",
    "agent": "coder",
    "progress": 0.6,
    "estimated_time_remaining": 30
  }
}
```

#### 4. Real-time Results
```json
{
  "type": "result",
  "data": {
    "task_id": "task_123",
    "stage": "architecture",
    "result": { /* stage result */ }
  }
}
```

## 🎯 Agent-Specific Endpoints

### Architect Agent
**Endpoint**: `POST /agents/architect`

**Capabilities**:
- Requirements analysis
- Architecture design
- Technology stack selection
- Task breakdown

### Coder Agent
**Endpoint**: `POST /agents/coder`

**Capabilities**:
- Multi-language code generation
- Framework integration
- Code optimization
- Documentation generation

**Supported Languages**: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala, R, SQL, HTML, CSS

### Tester Agent
**Endpoint**: `POST /agents/tester`

**Capabilities**:
- Unit test generation
- Integration test creation
- Performance testing
- Test automation setup

### Reviewer Agent
**Endpoint**: `POST /agents/reviewer`

**Capabilities**:
- Code quality analysis
- Security review
- Performance analysis
- Best practices validation

### Fixer Agent
**Endpoint**: `POST /agents/fixer`

**Capabilities**:
- Bug fixing
- Error resolution
- Performance optimization
- Security vulnerability patching

### Deployer Agent
**Endpoint**: `POST /agents/deployer`

**Capabilities**:
- Containerization (Docker, Kubernetes)
- CI/CD pipeline setup
- Cloud deployment (AWS, Heroku, Vercel)
- Infrastructure as code

## 📊 Analytics and Monitoring

### System Metrics
**Endpoint**: `GET /metrics`

**Response**:
```json
{
  "system": {
    "uptime": 86400,
    "cpu_usage": 0.45,
    "memory_usage": 0.67,
    "disk_usage": 0.23
  },
  "agents": {
    "total_tasks": 1250,
    "successful_tasks": 1203,
    "failed_tasks": 47,
    "avg_response_time": 2.8
  },
  "models": {
    "openai": {
      "requests": 850,
      "tokens_used": 125000,
      "avg_response_time": 1.2
    },
    "anthropic": {
      "requests": 400,
      "tokens_used": 85000,
      "avg_response_time": 1.8
    }
  }
}
```

### Agent Statistics
**Endpoint**: `GET /agents/{agent_name}/stats`

**Response**:
```json
{
  "agent": "coder",
  "stats": {
    "tasks_completed": 450,
    "avg_response_time": 3.2,
    "success_rate": 0.96,
    "languages_used": {
      "python": 180,
      "javascript": 120,
      "typescript": 85,
      "java": 65
    },
    "tokens_used": 95000,
    "memory_items_created": 180
  }
}
```

## 🔒 Security and Rate Limiting

### Rate Limits
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise**: Unlimited

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1642259400
```

### Error Responses
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "details": {
      "limit": 100,
      "window": 3600,
      "retry_after": 1800
    }
  }
}
```

## 📝 Error Handling

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error
- `503`: Service Unavailable

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "content",
      "reason": "Content cannot be empty"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456"
  }
}
```

## 🧪 Testing and Development

### Testing Endpoints
All endpoints support a `test` parameter for development:

```json
{
  "content": "Test request",
  "test": true
}
```

### Mock Responses
In test mode, agents return mock responses for faster development.

### Development Tools
- **OpenAPI/Swagger**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **Health Dashboard**: Available at `/health/dashboard`

## 📚 SDK and Libraries

### Python SDK
```python
from omnidev_supreme import OmniDevClient

client = OmniDevClient(api_key="your_api_key")
result = await client.agents.architect.execute("Design a web API")
```

### JavaScript SDK
```javascript
import { OmniDevClient } from '@omnidev-supreme/sdk';

const client = new OmniDevClient({ apiKey: 'your_api_key' });
const result = await client.agents.coder.execute('Create a user model');
```

## 🚀 Examples

### Complete Development Workflow
```python
import asyncio
from omnidev_supreme import OmniDevClient

async def main():
    client = OmniDevClient(api_key="your_api_key")
    
    # Create session
    session = await client.sessions.create({
        "user_id": "user_123",
        "project_context": {
            "project_name": "E-commerce API",
            "technology_stack": ["python", "fastapi", "postgresql"]
        }
    })
    
    # Execute workflow
    workflow = await client.workflows.execute({
        "content": "Create an e-commerce API with user authentication",
        "session_id": session.id,
        "language": "python",
        "framework": "fastapi"
    })
    
    print(f"Workflow completed: {workflow.success}")
    print(f"Stages: {len(workflow.stages)}")
    
    # Deploy
    if workflow.success:
        deployment = await client.agents.deployer.execute({
            "content": "Deploy to AWS ECS",
            "session_id": session.id,
            "platform": "aws",
            "environment": "production"
        })
        print(f"Deployment: {deployment.success}")

asyncio.run(main())
```

---

*This API documentation is automatically generated and updated. For the latest version, visit the interactive documentation at `/docs`.*