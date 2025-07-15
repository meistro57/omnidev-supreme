# OmniDev Supreme Testing Guide

## Quick Start Testing

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/meistro57/omnidev-supreme.git
cd omnidev-supreme

# Copy and edit the setup script with your API keys
cp setup_env.sh.example setup_env.sh
# Edit setup_env.sh and add your actual API keys

# Run the quick start script
./start.sh
```

### 2. Test API Endpoints

Once the server is running at `http://localhost:8000`, you can test:

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Get Available Agents
```bash
curl http://localhost:8000/agents
```

#### Execute Single Task
```bash
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Create a simple calculator function in Python",
    "task_type": "coding",
    "language": "python",
    "session_id": "test-session-1"
  }'
```

#### Execute Multi-Agent Workflow
```bash
curl -X POST http://localhost:8000/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Create a web API for a todo list application",
    "workflow_type": "full_development",
    "language": "python",
    "session_id": "test-session-2"
  }'
```

#### Search Memory
```bash
curl -X POST http://localhost:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "calculator function",
    "limit": 5
  }'
```

### 3. Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation where you can:
- Try all endpoints
- See request/response schemas
- Test with different parameters

### 4. Example Workflows

#### Simple Code Generation
```python
import requests

response = requests.post('http://localhost:8000/task', json={
    "content": "Create a Python function to calculate fibonacci numbers",
    "task_type": "coding",
    "language": "python"
})

print(response.json())
```

#### Full Development Workflow
```python
import requests

response = requests.post('http://localhost:8000/workflow', json={
    "content": "Create a REST API for managing books with CRUD operations",
    "workflow_type": "full_development",
    "language": "python"
})

print(response.json())
```

### 5. Testing Different Languages

```bash
# JavaScript
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Create a React component for user authentication",
    "task_type": "coding",
    "language": "javascript"
  }'

# Java
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Create a Spring Boot controller for user management",
    "task_type": "coding",
    "language": "java"
  }'
```

### 6. Monitoring and Statistics

```bash
# Memory statistics
curl http://localhost:8000/memory/stats

# Orchestrator statistics
curl http://localhost:8000/orchestrator/stats

# Integration statistics
curl http://localhost:8000/integration/stats
```

## Expected Results

### Successful Task Execution
```json
{
  "success": true,
  "code_files": [
    {
      "filename": "calculator.py",
      "content": "def calculate(a, b, operation):\n    # Generated code here",
      "language": "python",
      "validated": true
    }
  ],
  "agent": "coder",
  "tokens_used": 150,
  "response_time": 2.5
}
```

### Successful Workflow Execution
```json
{
  "workflow_id": "workflow_test-session-2_123456",
  "stages": [
    {
      "stage": "architecture",
      "agent": "architect",
      "result": {
        "success": true,
        "plan": {
          "overview": "Todo list API with CRUD operations",
          "tasks": [...]
        }
      }
    },
    {
      "stage": "coding",
      "agent": "coder",
      "result": {
        "success": true,
        "code_files": [...]
      }
    }
  ],
  "success": true
}
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Make sure you've set real API keys in `setup_env.sh`
   - Check that the keys are exported: `echo $OPENAI_API_KEY`

2. **Import Errors**
   - Make sure you're in the correct directory
   - Check that PYTHONPATH is set correctly

3. **Memory Issues**
   - Vector memory requires additional dependencies
   - Install with: `pip install sentence-transformers faiss-cpu`

4. **Model Timeouts**
   - Increase timeout in configuration
   - Check network connectivity to AI providers

### Debug Mode

Run with debug logging:
```bash
LOG_LEVEL=DEBUG python -m backend.main
```

### Testing Without API Keys

The system will work in limited mode without API keys, but you'll need at least one provider configured for full functionality.

## Next Steps

- Add your own test cases
- Integrate with your existing projects
- Extend with additional agents
- Set up production deployment

## Security Note

⚠️ **Important**: The `setup_env.sh` script is for testing only. Never commit real API keys to version control. Use proper environment management for production deployments.