"""
OmniDev Supreme Model Orchestrator
Intelligent routing and management of multiple AI models
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging
from abc import ABC, abstractmethod

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """AI model types"""
    OPENAI_GPT4 = "openai_gpt4"
    OPENAI_GPT4_TURBO = "openai_gpt4_turbo"
    OPENAI_GPT35_TURBO = "openai_gpt35_turbo"
    ANTHROPIC_CLAUDE_OPUS = "anthropic_claude_opus"
    ANTHROPIC_CLAUDE_SONNET = "anthropic_claude_sonnet"
    ANTHROPIC_CLAUDE_HAIKU = "anthropic_claude_haiku"
    OLLAMA_LLAMA3 = "ollama_llama3"
    OLLAMA_CODELLAMA = "ollama_codellama"
    OLLAMA_MISTRAL = "ollama_mistral"
    SPECIALIZED_TTS = "specialized_tts"
    SPECIALIZED_DIALOGUE = "specialized_dialogue"


class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = 1
    MEDIUM = 2
    COMPLEX = 3
    EXPERT = 4


class ModelCapability(Enum):
    """Model capabilities"""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    CREATIVITY = "creativity"
    CONVERSATION = "conversation"
    SPECIALIZED = "specialized"


@dataclass
class ModelConfig:
    """Model configuration"""
    model_type: ModelType
    name: str
    provider: str
    endpoint: Optional[str]
    capabilities: List[ModelCapability]
    max_tokens: int
    cost_per_token: float
    speed_score: int  # 1-10, higher is faster
    quality_score: int  # 1-10, higher is better
    availability: bool = True
    
    def supports_capability(self, capability: ModelCapability) -> bool:
        """Check if model supports a capability"""
        return capability in self.capabilities


@dataclass
class TaskRequest:
    """Task request for model orchestration"""
    id: str
    content: str
    task_type: str
    complexity: TaskComplexity
    required_capabilities: List[ModelCapability]
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    priority: int = 1
    timeout: int = 300
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ModelResponse:
    """Model response"""
    request_id: str
    model_type: ModelType
    content: str
    tokens_used: int
    response_time: float
    cost: float
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseModelProvider(ABC):
    """Base class for model providers"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.stats = {
            "requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "average_response_time": 0.0
        }
    
    @abstractmethod
    async def generate(self, request: TaskRequest) -> ModelResponse:
        """Generate response for task"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if model is available"""
        pass
    
    def update_stats(self, response: ModelResponse):
        """Update provider statistics"""
        self.stats["requests"] += 1
        if response.success:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1
        
        self.stats["total_tokens"] += response.tokens_used
        self.stats["total_cost"] += response.cost
        
        # Update average response time
        total_requests = self.stats["requests"]
        current_avg = self.stats["average_response_time"]
        self.stats["average_response_time"] = (
            (current_avg * (total_requests - 1) + response.response_time) / total_requests
        )


class OpenAIProvider(BaseModelProvider):
    """OpenAI model provider"""
    
    def __init__(self, config: ModelConfig, api_key: str):
        super().__init__(config)
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model_mapping = {
            ModelType.OPENAI_GPT4: "gpt-4",
            ModelType.OPENAI_GPT4_TURBO: "gpt-4-turbo",
            ModelType.OPENAI_GPT35_TURBO: "gpt-3.5-turbo"
        }
    
    async def generate(self, request: TaskRequest) -> ModelResponse:
        """Generate response using OpenAI"""
        start_time = time.time()
        
        try:
            model_name = self.model_mapping[self.config.model_type]
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": request.content}],
                max_tokens=request.max_tokens or self.config.max_tokens,
                temperature=request.temperature,
                timeout=request.timeout
            )
            
            response_time = time.time() - start_time
            tokens_used = response.usage.total_tokens
            cost = tokens_used * self.config.cost_per_token
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content=response.choices[0].message.content,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=cost,
                success=True
            )
            
            self.update_stats(model_response)
            return model_response
            
        except Exception as e:
            logger.error(f"❌ OpenAI generation failed: {e}")
            response_time = time.time() - start_time
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content="",
                tokens_used=0,
                response_time=response_time,
                cost=0.0,
                success=False,
                error=str(e)
            )
            
            self.update_stats(model_response)
            return model_response
    
    async def health_check(self) -> bool:
        """Check OpenAI API health"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False


class AnthropicProvider(BaseModelProvider):
    """Anthropic Claude model provider"""
    
    def __init__(self, config: ModelConfig, api_key: str):
        super().__init__(config)
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic library not available")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_mapping = {
            ModelType.ANTHROPIC_CLAUDE_OPUS: "claude-3-opus-20240229",
            ModelType.ANTHROPIC_CLAUDE_SONNET: "claude-3-5-sonnet-20241022",
            ModelType.ANTHROPIC_CLAUDE_HAIKU: "claude-3-haiku-20240307"
        }
    
    async def generate(self, request: TaskRequest) -> ModelResponse:
        """Generate response using Anthropic"""
        start_time = time.time()
        
        try:
            model_name = self.model_mapping[self.config.model_type]
            
            response = self.client.messages.create(
                model=model_name,
                max_tokens=request.max_tokens or self.config.max_tokens,
                temperature=request.temperature,
                messages=[{"role": "user", "content": request.content}]
            )
            
            response_time = time.time() - start_time
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = tokens_used * self.config.cost_per_token
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content=response.content[0].text,
                tokens_used=tokens_used,
                response_time=response_time,
                cost=cost,
                success=True
            )
            
            self.update_stats(model_response)
            return model_response
            
        except Exception as e:
            logger.error(f"❌ Anthropic generation failed: {e}")
            response_time = time.time() - start_time
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content="",
                tokens_used=0,
                response_time=response_time,
                cost=0.0,
                success=False,
                error=str(e)
            )
            
            self.update_stats(model_response)
            return model_response
    
    async def health_check(self) -> bool:
        """Check Anthropic API health"""
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception:
            return False


class OllamaProvider(BaseModelProvider):
    """Ollama local model provider"""
    
    def __init__(self, config: ModelConfig, base_url: str = "http://localhost:11434"):
        super().__init__(config)
        if not OLLAMA_AVAILABLE:
            raise ImportError("Requests library not available")
        
        self.base_url = base_url
        self.model_mapping = {
            ModelType.OLLAMA_LLAMA3: "llama3.1",
            ModelType.OLLAMA_CODELLAMA: "codellama",
            ModelType.OLLAMA_MISTRAL: "mistral"
        }
    
    async def generate(self, request: TaskRequest) -> ModelResponse:
        """Generate response using Ollama"""
        start_time = time.time()
        
        try:
            model_name = self.model_mapping[self.config.model_type]
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": request.content,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens or self.config.max_tokens
                    }
                },
                timeout=request.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            response_time = time.time() - start_time
            # Ollama doesn't provide token counts, estimate based on content
            tokens_used = len(result["response"].split()) * 1.3  # Rough estimate
            cost = 0.0  # Local models are free
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content=result["response"],
                tokens_used=int(tokens_used),
                response_time=response_time,
                cost=cost,
                success=True
            )
            
            self.update_stats(model_response)
            return model_response
            
        except Exception as e:
            logger.error(f"❌ Ollama generation failed: {e}")
            response_time = time.time() - start_time
            
            model_response = ModelResponse(
                request_id=request.id,
                model_type=self.config.model_type,
                content="",
                tokens_used=0,
                response_time=response_time,
                cost=0.0,
                success=False,
                error=str(e)
            )
            
            self.update_stats(model_response)
            return model_response
    
    async def health_check(self) -> bool:
        """Check Ollama health"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


class ModelOrchestrator:
    """Central orchestrator for multiple AI models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.providers: Dict[ModelType, BaseModelProvider] = {}
        self.fallback_chain: List[ModelType] = []
        self.load_balancing: Dict[str, List[ModelType]] = {}
        self.config = config
        
        # Initialize providers
        self._initialize_providers()
        
        # Set up routing rules
        self._setup_routing_rules()
        
        logger.info("🎯 Model Orchestrator initialized")
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        # OpenAI providers
        if OPENAI_AVAILABLE and self.config.get("openai_api_key"):
            openai_models = [
                (ModelType.OPENAI_GPT4, "gpt-4", 8192, 0.03, 6, 9),
                (ModelType.OPENAI_GPT4_TURBO, "gpt-4-turbo", 4096, 0.01, 8, 9),
                (ModelType.OPENAI_GPT35_TURBO, "gpt-3.5-turbo", 4096, 0.002, 9, 7)
            ]
            
            for model_type, name, max_tokens, cost, speed, quality in openai_models:
                config = ModelConfig(
                    model_type=model_type,
                    name=name,
                    provider="openai",
                    endpoint=None,
                    capabilities=[
                        ModelCapability.TEXT_GENERATION,
                        ModelCapability.CODE_GENERATION,
                        ModelCapability.ANALYSIS,
                        ModelCapability.REASONING
                    ],
                    max_tokens=max_tokens,
                    cost_per_token=cost,
                    speed_score=speed,
                    quality_score=quality
                )
                
                self.providers[model_type] = OpenAIProvider(
                    config, self.config["openai_api_key"]
                )
        
        # Anthropic providers
        if ANTHROPIC_AVAILABLE and self.config.get("anthropic_api_key"):
            anthropic_models = [
                (ModelType.ANTHROPIC_CLAUDE_OPUS, "claude-3-opus", 4096, 0.075, 5, 10),
                (ModelType.ANTHROPIC_CLAUDE_SONNET, "claude-3.5-sonnet", 4096, 0.015, 7, 9),
                (ModelType.ANTHROPIC_CLAUDE_HAIKU, "claude-3-haiku", 4096, 0.00025, 9, 7)
            ]
            
            for model_type, name, max_tokens, cost, speed, quality in anthropic_models:
                config = ModelConfig(
                    model_type=model_type,
                    name=name,
                    provider="anthropic",
                    endpoint=None,
                    capabilities=[
                        ModelCapability.TEXT_GENERATION,
                        ModelCapability.CODE_GENERATION,
                        ModelCapability.ANALYSIS,
                        ModelCapability.REASONING,
                        ModelCapability.CREATIVITY
                    ],
                    max_tokens=max_tokens,
                    cost_per_token=cost,
                    speed_score=speed,
                    quality_score=quality
                )
                
                self.providers[model_type] = AnthropicProvider(
                    config, self.config["anthropic_api_key"]
                )
        
        # Ollama providers
        if OLLAMA_AVAILABLE and self.config.get("ollama_enabled"):
            ollama_models = [
                (ModelType.OLLAMA_LLAMA3, "llama3.1", 8192, 0.0, 7, 8),
                (ModelType.OLLAMA_CODELLAMA, "codellama", 4096, 0.0, 6, 8),
                (ModelType.OLLAMA_MISTRAL, "mistral", 4096, 0.0, 8, 7)
            ]
            
            for model_type, name, max_tokens, cost, speed, quality in ollama_models:
                config = ModelConfig(
                    model_type=model_type,
                    name=name,
                    provider="ollama",
                    endpoint=self.config.get("ollama_url", "http://localhost:11434"),
                    capabilities=[
                        ModelCapability.TEXT_GENERATION,
                        ModelCapability.CODE_GENERATION,
                        ModelCapability.CONVERSATION
                    ],
                    max_tokens=max_tokens,
                    cost_per_token=cost,
                    speed_score=speed,
                    quality_score=quality
                )
                
                self.providers[model_type] = OllamaProvider(
                    config, self.config.get("ollama_url", "http://localhost:11434")
                )
    
    def _setup_routing_rules(self):
        """Set up intelligent routing rules"""
        # Fallback chain: best quality to fastest
        self.fallback_chain = [
            ModelType.ANTHROPIC_CLAUDE_OPUS,
            ModelType.OPENAI_GPT4,
            ModelType.ANTHROPIC_CLAUDE_SONNET,
            ModelType.OPENAI_GPT4_TURBO,
            ModelType.OLLAMA_LLAMA3,
            ModelType.ANTHROPIC_CLAUDE_HAIKU,
            ModelType.OPENAI_GPT35_TURBO,
            ModelType.OLLAMA_CODELLAMA,
            ModelType.OLLAMA_MISTRAL
        ]
        
        # Task-specific routing
        self.load_balancing = {
            "code_generation": [
                ModelType.ANTHROPIC_CLAUDE_SONNET,
                ModelType.OLLAMA_CODELLAMA,
                ModelType.OPENAI_GPT4,
                ModelType.OPENAI_GPT4_TURBO
            ],
            "analysis": [
                ModelType.ANTHROPIC_CLAUDE_OPUS,
                ModelType.OPENAI_GPT4,
                ModelType.ANTHROPIC_CLAUDE_SONNET
            ],
            "creative": [
                ModelType.ANTHROPIC_CLAUDE_OPUS,
                ModelType.ANTHROPIC_CLAUDE_SONNET,
                ModelType.OPENAI_GPT4
            ],
            "conversation": [
                ModelType.ANTHROPIC_CLAUDE_HAIKU,
                ModelType.OPENAI_GPT35_TURBO,
                ModelType.OLLAMA_LLAMA3
            ]
        }
    
    def find_best_model(self, request: TaskRequest) -> Optional[ModelType]:
        """Find the best model for a task"""
        # Get candidates based on task type
        candidates = self.load_balancing.get(request.task_type, self.fallback_chain)
        
        # Filter by capabilities
        filtered_candidates = []
        for model_type in candidates:
            if model_type in self.providers:
                provider = self.providers[model_type]
                if all(provider.config.supports_capability(cap) for cap in request.required_capabilities):
                    filtered_candidates.append(model_type)
        
        # Filter by availability
        available_candidates = []
        for model_type in filtered_candidates:
            if self.providers[model_type].config.availability:
                available_candidates.append(model_type)
        
        if not available_candidates:
            return None
        
        # Select based on complexity and priority
        if request.complexity == TaskComplexity.EXPERT:
            # Use highest quality model
            for model_type in available_candidates:
                if self.providers[model_type].config.quality_score >= 9:
                    return model_type
        elif request.priority > 5:
            # Use fastest model
            for model_type in available_candidates:
                if self.providers[model_type].config.speed_score >= 8:
                    return model_type
        
        # Default to first available
        return available_candidates[0]
    
    async def execute_task(self, request: TaskRequest) -> ModelResponse:
        """Execute task with intelligent model selection"""
        # Find best model
        model_type = self.find_best_model(request)
        if not model_type:
            return ModelResponse(
                request_id=request.id,
                model_type=ModelType.OPENAI_GPT35_TURBO,  # Default
                content="",
                tokens_used=0,
                response_time=0.0,
                cost=0.0,
                success=False,
                error="No suitable model available"
            )
        
        # Try primary model
        provider = self.providers[model_type]
        response = await provider.generate(request)
        
        # If failed, try fallback
        if not response.success:
            logger.warning(f"⚠️  Primary model {model_type} failed, trying fallback")
            for fallback_type in self.fallback_chain:
                if fallback_type != model_type and fallback_type in self.providers:
                    fallback_provider = self.providers[fallback_type]
                    response = await fallback_provider.generate(request)
                    if response.success:
                        break
        
        return response
    
    async def health_check_all(self) -> Dict[ModelType, bool]:
        """Check health of all providers"""
        results = {}
        for model_type, provider in self.providers.items():
            try:
                results[model_type] = await provider.health_check()
            except Exception as e:
                logger.error(f"❌ Health check failed for {model_type}: {e}")
                results[model_type] = False
        
        return results
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_providers": len(self.providers),
            "available_providers": len([p for p in self.providers.values() if p.config.availability]),
            "provider_stats": {
                model_type.value: provider.stats
                for model_type, provider in self.providers.items()
            },
            "routing_rules": {
                "fallback_chain": [mt.value for mt in self.fallback_chain],
                "load_balancing": {
                    task_type: [mt.value for mt in models]
                    for task_type, models in self.load_balancing.items()
                }
            }
        }


# Global orchestrator instance
model_orchestrator = None

def create_orchestrator(config: Dict[str, Any]) -> ModelOrchestrator:
    """Create and configure model orchestrator"""
    global model_orchestrator
    model_orchestrator = ModelOrchestrator(config)
    return model_orchestrator