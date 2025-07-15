# Core Components

Deep dive into the essential building blocks that power the OmniDev Supreme platform and enable seamless integration of 29 specialized AI agents.

## 🎯 Component Overview

The OmniDev Supreme platform is built on five core components that work together to provide a unified AI development experience:

1. **Agent Registry System** - Central agent management
2. **Integration Manager** - Agent coordination and workflow
3. **Memory System** - Unified knowledge storage
4. **Model Orchestration** - AI model routing and optimization
5. **Web Interface** - User interaction and real-time updates

## 🏗️ 1. Agent Registry System

### **Purpose**
The Agent Registry System serves as the central nervous system for all 29 agents, providing registration, metadata management, and lifecycle control.

### **Core Classes**

#### **BaseAgent**
```python
class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, metadata: AgentMetadata, config: Dict[str, Any]):
        self.metadata = metadata
        self.config = config
        self.status = AgentStatus.IDLE
        self.memory_manager = None
        self.orchestrator = None
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task and return the result."""
        pass
    
    @abstractmethod
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if this agent can handle the given task."""
        pass
```

#### **AgentMetadata**
```python
@dataclass
class AgentMetadata:
    """Metadata for agent configuration and capabilities."""
    name: str
    agent_type: AgentType
    capabilities: List[str]
    description: str
    priority: int = 5
    max_concurrent_tasks: int = 1
    timeout_seconds: int = 300
    model_requirements: Optional[List[str]] = None
    tags: List[str] = field(default_factory=list)
```

#### **AgentStatus**
```python
class AgentStatus(Enum):
    """Agent operational status."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    DISABLED = "disabled"
    INITIALIZING = "initializing"
    STOPPING = "stopping"
```

#### **AgentType**
```python
class AgentType(Enum):
    """Agent type categorization."""
    ARCHITECT = "architect"
    CODER = "coder"
    TESTER = "tester"
    REVIEWER = "reviewer"
    FIXER = "fixer"
    DEPLOYER = "deployer"
    ORCHESTRATOR = "orchestrator"
    EXECUTOR = "executor"
    MANAGER = "manager"
    INTEGRATOR = "integrator"
    TRACKER = "tracker"
    GENERATOR = "generator"
    CHECKER = "checker"
    HARNESS = "harness"
    IDEAS = "ideas"
    CREATIVITY = "creativity"
    SCORER = "scorer"
    PROJECT_MANAGER = "project_manager"
    DEVELOPER = "developer"
    QA = "qa"
    DEVOPS = "devops"
    REVIEWER = "reviewer"
    ANALYZER = "analyzer"
    BUILDER = "builder"
    ARTIST = "artist"
    GUARDIAN = "guardian"
    TRAINER = "trainer"
```

### **Registry Operations**
- **Registration**: Register agents with metadata and capabilities
- **Discovery**: Find agents based on type, capabilities, or availability
- **Lifecycle**: Manage agent initialization, status, and shutdown
- **Monitoring**: Track agent performance and health

### **Integration Pattern**
```python
def create_agent_factory(agent_class, default_config):
    """Factory pattern for agent creation."""
    def create_agent(config: Dict[str, Any]):
        merged_config = {**default_config, **config}
        return agent_class(merged_config)
    return create_agent
```

## 🔄 2. Integration Manager

### **Purpose**
The Integration Manager coordinates all agent interactions, manages workflows, and provides intelligent task routing across the 29 agents.

### **Core Class**

#### **AgentIntegrationManager**
```python
class AgentIntegrationManager:
    """Central coordination for all agent systems."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_factories: Dict[str, Callable] = {}
        self.memory_manager = UnifiedMemoryManager(config)
        self.orchestrator = ModelOrchestrator(config)
    
    async def initialize_all_agents(self):
        """Initialize all registered agents."""
        await self._integrate_agency_agents()
        await self._integrate_meistrocraft_agents()
        await self._integrate_obelisk_agents()
        await self._integrate_ai_dev_team_agents()
        await self._integrate_village_agents()
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with the most appropriate agent."""
        agent = self._select_agent(task)
        return await agent.execute(task)
    
    def _select_agent(self, task: Dict[str, Any]) -> BaseAgent:
        """Select the best agent for a given task."""
        # Intelligent routing based on task content and agent capabilities
        pass
```

### **Agent System Integration**

#### **The-Agency Integration**
```python
async def _integrate_agency_agents(self):
    """Integrate The-Agency's 6 core development agents."""
    from .agency import (
        create_architect_agent,
        create_coder_agent,
        create_tester_agent,
        create_reviewer_agent,
        create_fixer_agent,
        create_deployer_agent
    )
    
    agents = [
        ("architect_agent", create_architect_agent),
        ("coder_agent", create_coder_agent),
        ("tester_agent", create_tester_agent),
        ("reviewer_agent", create_reviewer_agent),
        ("fixer_agent", create_fixer_agent),
        ("deployer_agent", create_deployer_agent)
    ]
    
    for name, factory in agents:
        agent = factory(self.config)
        agent.memory_manager = self.memory_manager
        agent.orchestrator = self.orchestrator
        self.agents[name] = agent
```

#### **Multi-Agent Workflow**
```python
async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a multi-agent workflow."""
    results = {}
    
    for step in workflow['steps']:
        if step['type'] == 'sequential':
            for agent_name in step['agents']:
                agent = self.agents[agent_name]
                result = await agent.execute(step['task'])
                results[agent_name] = result
        
        elif step['type'] == 'parallel':
            tasks = [
                self.agents[agent_name].execute(step['task'])
                for agent_name in step['agents']
            ]
            parallel_results = await asyncio.gather(*tasks)
            for i, agent_name in enumerate(step['agents']):
                results[agent_name] = parallel_results[i]
    
    return results
```

### **Task Routing Logic**
- **Content Analysis**: Analyze task description for keywords
- **Capability Matching**: Match task requirements to agent capabilities
- **Load Balancing**: Consider agent current load and availability
- **Performance History**: Use historical performance data
- **Fallback Strategy**: Provide alternative agents if primary is unavailable

## 🧠 3. Memory System

### **Purpose**
The Memory System provides unified knowledge storage and retrieval across all agents, enabling context sharing and continuous learning.

### **Core Architecture**

#### **UnifiedMemoryManager**
```python
class UnifiedMemoryManager:
    """Unified interface for all memory systems."""
    
    def __init__(self, config: Dict[str, Any]):
        self.vector_memory = VectorMemory(config)
        self.relational_memory = RelationalMemory(config)
        self.session_memory = SessionMemory(config)
    
    async def store_memory(
        self,
        content: str,
        memory_type: MemoryType,
        priority: MemoryPriority = MemoryPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> str:
        """Store memory across all relevant systems."""
        memory_id = str(uuid.uuid4())
        
        # Store in vector memory for semantic search
        await self.vector_memory.store(
            memory_id, content, metadata or {}, tags or []
        )
        
        # Store in relational memory for structured queries
        await self.relational_memory.store(
            memory_id, content, memory_type, priority, metadata, tags
        )
        
        # Store in session memory if session_id provided
        if session_id:
            await self.session_memory.store(
                session_id, memory_id, content, metadata
            )
        
        return memory_id
    
    async def search_memory(
        self,
        query: str,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search across all memory systems."""
        # Combine vector and relational search results
        vector_results = await self.vector_memory.search(
            query, limit, similarity_threshold
        )
        
        relational_results = await self.relational_memory.search(
            query, memory_type, limit
        )
        
        # Merge and rank results
        return self._merge_search_results(vector_results, relational_results)
```

#### **Memory Types**
```python
class MemoryType(Enum):
    """Memory categorization for different content types."""
    CODE = "code"
    TASK = "task"
    AGENT = "agent"
    KNOWLEDGE = "knowledge"
    SESSION = "session"
    PROJECT = "project"
    ERROR = "error"
    WORKFLOW = "workflow"
    INSIGHT = "insight"
    FEEDBACK = "feedback"
```

#### **Memory Priority**
```python
class MemoryPriority(Enum):
    """Memory priority levels for retention and retrieval."""
    LOW = 1
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 10
```

### **Memory Storage Systems**

#### **1. Vector Memory**
- **Technology**: FAISS (Facebook AI Similarity Search)
- **Purpose**: Semantic similarity search
- **Use Cases**: Code similarity, concept matching, context retrieval
- **Features**: Embeddings, similarity scoring, clustering

#### **2. Relational Memory**
- **Technology**: SQLite with SQLAlchemy
- **Purpose**: Structured data storage
- **Use Cases**: Task history, agent performance, project metadata
- **Features**: Complex queries, relationships, transactions

#### **3. Session Memory**
- **Technology**: Redis with TTL
- **Purpose**: Temporary context storage
- **Use Cases**: Conversation state, workflow context, user preferences
- **Features**: Fast access, automatic expiration, pub/sub

## 🚀 4. Model Orchestration

### **Purpose**
The Model Orchestration component intelligently routes tasks to the most appropriate AI model based on complexity, cost, and performance requirements.

### **Core Class**

#### **ModelOrchestrator**
```python
class ModelOrchestrator:
    """Intelligent routing for AI model selection."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers = {
            ModelType.OPENAI: OpenAIProvider(config.get('openai', {})),
            ModelType.ANTHROPIC: AnthropicProvider(config.get('anthropic', {})),
            ModelType.OLLAMA: OllamaProvider(config.get('ollama', {}))
        }
        self.performance_tracker = PerformanceTracker()
    
    async def generate_response(
        self,
        prompt: str,
        task_type: str,
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
        model_preference: Optional[ModelType] = None
    ) -> Dict[str, Any]:
        """Generate AI response with optimal model selection."""
        
        # Select model based on task complexity and performance
        model_type = model_preference or self._select_optimal_model(
            task_type, complexity
        )
        
        provider = self.providers[model_type]
        
        # Execute request with performance tracking
        start_time = time.time()
        response = await provider.generate(prompt, task_type)
        execution_time = time.time() - start_time
        
        # Track performance metrics
        self.performance_tracker.record_execution(
            model_type, task_type, execution_time, response.get('token_count', 0)
        )
        
        return {
            'model_type': model_type.value,
            'response': response,
            'execution_time': execution_time,
            'performance_score': self._calculate_performance_score(response)
        }
    
    def _select_optimal_model(
        self, task_type: str, complexity: TaskComplexity
    ) -> ModelType:
        """Select the optimal model based on task requirements."""
        # Complex routing logic based on:
        # - Task complexity
        # - Historical performance
        # - Cost considerations
        # - Model availability
        # - Specific capabilities
        
        if complexity == TaskComplexity.SIMPLE:
            return ModelType.OPENAI  # GPT-3.5 for simple tasks
        elif complexity == TaskComplexity.COMPLEX:
            return ModelType.ANTHROPIC  # Claude for complex reasoning
        else:
            return ModelType.OPENAI  # GPT-4 for medium complexity
```

### **Model Providers**

#### **OpenAI Provider**
```python
class OpenAIProvider:
    """OpenAI GPT model integration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.client = OpenAI(api_key=self.api_key)
        self.model_mapping = {
            TaskComplexity.SIMPLE: "gpt-3.5-turbo",
            TaskComplexity.MEDIUM: "gpt-4",
            TaskComplexity.COMPLEX: "gpt-4"
        }
    
    async def generate(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Generate response using OpenAI models."""
        # Implementation details
        pass
```

#### **Anthropic Provider**
```python
class AnthropicProvider:
    """Anthropic Claude model integration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.client = Anthropic(api_key=self.api_key)
        self.model_mapping = {
            TaskComplexity.SIMPLE: "claude-3-haiku-20240307",
            TaskComplexity.MEDIUM: "claude-3-sonnet-20240229",
            TaskComplexity.COMPLEX: "claude-3-opus-20240229"
        }
    
    async def generate(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Generate response using Anthropic models."""
        # Implementation details
        pass
```

#### **Ollama Provider**
```python
class OllamaProvider:
    """Ollama local model integration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.host = config.get('host', 'http://localhost:11434')
        self.enabled = config.get('enabled', False)
        self.client = OllamaClient(self.host) if self.enabled else None
    
    async def generate(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Generate response using local Ollama models."""
        # Implementation details
        pass
```

## 🌐 5. Web Interface

### **Purpose**
The Web Interface provides a unified, real-time interface for interacting with all 29 agents through a Monaco Editor-based development environment.

### **Core Architecture**

#### **React Application Structure**
```
frontend/
├── src/
│   ├── components/
│   │   ├── Editor/
│   │   │   ├── MonacoEditor.tsx
│   │   │   ├── EditorToolbar.tsx
│   │   │   └── EditorSidebar.tsx
│   │   ├── Dashboard/
│   │   │   ├── AgentDashboard.tsx
│   │   │   ├── SystemHealth.tsx
│   │   │   └── TaskQueue.tsx
│   │   ├── Projects/
│   │   │   ├── ProjectList.tsx
│   │   │   ├── ProjectEditor.tsx
│   │   │   └── ProjectSettings.tsx
│   │   └── Memory/
│   │       ├── MemoryExplorer.tsx
│   │       ├── KnowledgeGraph.tsx
│   │       └── SearchInterface.tsx
│   ├── store/
│   │   ├── slices/
│   │   │   ├── agentsSlice.ts
│   │   │   ├── tasksSlice.ts
│   │   │   ├── projectsSlice.ts
│   │   │   └── memorySlice.ts
│   │   └── store.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   └── agents.ts
│   └── utils/
│       ├── monaco.ts
│       └── helpers.ts
```

#### **Monaco Editor Integration**
```typescript
const MonacoEditor: React.FC<EditorProps> = ({ 
  value, 
  onChange, 
  language = 'typescript',
  theme = 'vs-dark' 
}) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const { agents, isConnected } = useSelector((state: RootState) => state.agents);
  
  const handleEditorDidMount = (
    editor: monaco.editor.IStandaloneCodeEditor,
    monaco: typeof import('monaco-editor')
  ) => {
    editorRef.current = editor;
    
    // Register agent completion provider
    monaco.languages.registerCompletionItemProvider(language, {
      provideCompletionItems: (model, position) => {
        return createAgentCompletions(agents, model, position);
      }
    });
    
    // Register agent hover provider
    monaco.languages.registerHoverProvider(language, {
      provideHover: (model, position) => {
        return createAgentHover(agents, model, position);
      }
    });
  };
  
  return (
    <Editor
      height="100vh"
      language={language}
      theme={theme}
      value={value}
      onChange={onChange}
      onMount={handleEditorDidMount}
      options={{
        minimap: { enabled: true },
        fontSize: 14,
        wordWrap: 'on',
        automaticLayout: true,
        suggestOnTriggerCharacters: true,
        quickSuggestions: true,
        tabCompletion: 'on'
      }}
    />
  );
};
```

#### **Redux State Management**
```typescript
// Agent slice
const agentsSlice = createSlice({
  name: 'agents',
  initialState: {
    agents: {} as Record<string, Agent>,
    isConnected: false,
    activeAgent: null,
    taskQueue: [] as Task[],
    systemHealth: null
  },
  reducers: {
    setAgents: (state, action) => {
      state.agents = action.payload;
    },
    updateAgentStatus: (state, action) => {
      const { agentId, status } = action.payload;
      if (state.agents[agentId]) {
        state.agents[agentId].status = status;
      }
    },
    addTask: (state, action) => {
      state.taskQueue.push(action.payload);
    },
    updateTask: (state, action) => {
      const { taskId, updates } = action.payload;
      const task = state.taskQueue.find(t => t.id === taskId);
      if (task) {
        Object.assign(task, updates);
      }
    }
  }
});
```

#### **WebSocket Integration**
```typescript
class WebSocketManager {
  private socket: Socket | null = null;
  private dispatch: AppDispatch;
  
  constructor(dispatch: AppDispatch) {
    this.dispatch = dispatch;
  }
  
  connect(): void {
    this.socket = io('http://localhost:8000', {
      transports: ['websocket']
    });
    
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket');
      this.dispatch(setConnectionStatus(true));
    });
    
    this.socket.on('agent_status_update', (data) => {
      this.dispatch(updateAgentStatus(data));
    });
    
    this.socket.on('task_update', (data) => {
      this.dispatch(updateTask(data));
    });
    
    this.socket.on('system_health', (data) => {
      this.dispatch(updateSystemHealth(data));
    });
  }
  
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}
```

### **Real-time Features**
- **Live Agent Status**: Real-time updates of all 29 agents
- **Task Progress**: Live progress tracking for long-running tasks
- **System Health**: Continuous monitoring of system components
- **Collaborative Editing**: Multi-user editing capabilities
- **Instant Feedback**: Immediate responses to user interactions

## 🔧 Component Integration

### **Initialization Flow**
1. **System Startup**: Core components initialize in dependency order
2. **Agent Registration**: All 29 agents register with the registry
3. **Memory System**: Vector, relational, and session stores initialize
4. **Model Orchestration**: AI provider connections established
5. **Web Interface**: Frontend connects via WebSocket
6. **Health Checks**: System health monitoring begins

### **Request Processing Flow**
1. **User Input**: User interacts with Monaco Editor
2. **Task Creation**: Frontend creates task object
3. **Agent Selection**: Integration Manager selects appropriate agent
4. **Model Routing**: Model Orchestrator selects optimal AI model
5. **Execution**: Agent executes task with AI model
6. **Memory Storage**: Results stored in memory system
7. **Response**: Real-time response sent to frontend

### **Error Handling**
- **Circuit Breakers**: Prevent cascading failures
- **Graceful Degradation**: Fallback mechanisms for component failures
- **Retry Logic**: Automatic retries with exponential backoff
- **Error Propagation**: Structured error information across layers

---

<div align="center">
  <p><strong>🔧 Five core components working in perfect harmony</strong></p>
  <p>Each component is designed for reliability, scalability, and extensibility.</p>
  
  <a href="agent-systems.md">
    <strong>Explore Agent Systems →</strong>
  </a>
</div>

---

*Last updated: December 2024 | [Edit this page](https://github.com/meistro57/omnidev-supreme/edit/main/wiki/architecture/core-components.md)*