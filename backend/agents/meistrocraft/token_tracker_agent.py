"""
MeistroCraft Token Tracker Agent Integration
Migrated from MeistroCraft's token_tracker.py
"""

import asyncio
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


@dataclass
class TokenUsage:
    """Token usage data structure"""
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    timestamp: str
    session_id: str
    task_id: str


@dataclass
class UsageLimits:
    """Usage limits configuration"""
    daily_token_limit: int = 50000
    daily_cost_limit: float = 10.0
    hourly_token_limit: int = 10000
    hourly_cost_limit: float = 2.0
    session_token_limit: int = 5000
    session_cost_limit: float = 1.0


class TokenTrackerAgent(BaseAgent):
    """
    Token Tracker Agent - Monitors and manages AI token usage and costs
    Integrated from MeistroCraft system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="token_tracker",
            agent_type=AgentType.ANALYZER,
            description="Monitors and manages AI token usage and costs",
            capabilities=[
                "token_tracking",
                "cost_analysis",
                "usage_monitoring",
                "limit_enforcement",
                "usage_analytics",
                "cost_optimization",
                "budget_management",
                "usage_reporting"
            ],
            model_requirements=["analysis", "monitoring"],
            priority=5,  # Medium priority for monitoring
            max_concurrent_tasks=10,  # Can handle many tracking tasks
            timeout_seconds=60  # Quick tracking operations
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Token tracking configuration
        self.tracking_config = {
            "track_all_models": True,
            "store_usage_history": True,
            "enforce_limits": True,
            "alert_thresholds": {
                "token_warning": 0.8,  # 80% of limit
                "cost_warning": 0.8,   # 80% of cost limit
                "critical_threshold": 0.95  # 95% of limit
            }
        }
        
        # Model pricing (per 1K tokens)
        self.model_pricing = {
            "gpt-4": {"prompt": 0.03, "completion": 0.06},
            "gpt-4-32k": {"prompt": 0.06, "completion": 0.12},
            "gpt-4o": {"prompt": 0.005, "completion": 0.015},
            "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
            "gpt-3.5-turbo": {"prompt": 0.001, "completion": 0.002},
            "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
            "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
            "claude-3-haiku": {"prompt": 0.00025, "completion": 0.00125},
            "claude-3.5-sonnet": {"prompt": 0.003, "completion": 0.015}
        }
        
        # Usage limits
        self.usage_limits = UsageLimits()
        
        # In-memory usage tracking
        self.usage_history = []
        self.session_usage = {}
        self.daily_usage = {}
        self.hourly_usage = {}
        
        logger.info("📊 Token Tracker Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for token tracker agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires token tracking
        tracking_keywords = [
            "token", "usage", "cost", "track", "monitor", "analyze",
            "limit", "budget", "spending", "analytics", "report"
        ]
        
        return any(keyword in content for keyword in tracking_keywords) or task_type == "token_tracking"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute token tracking task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            operation = task.get("operation", "track")
            session_id = task.get("session_id")
            user_request = task.get("content", "")
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Token tracking task: {operation} - {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.MEDIUM,
                metadata={
                    "agent": "token_tracker",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "session_id": session_id
                },
                session_id=session_id
            )
            
            # Execute tracking operation
            if operation == "track":
                result = await self._track_usage(task)
            elif operation == "analyze":
                result = await self._analyze_usage(task)
            elif operation == "report":
                result = await self._generate_report(task)
            elif operation == "set_limits":
                result = await self._set_limits(task)
            elif operation == "check_limits":
                result = await self._check_limits(task)
            elif operation == "optimize":
                result = await self._optimize_usage(task)
            else:
                result = await self._get_usage_summary(task)
            
            # Store result in memory
            result_memory_id = self.memory_manager.store_memory(
                content=f"Token tracking result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.AGENT,
                priority=MemoryPriority.MEDIUM,
                metadata={
                    "agent": "token_tracker",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "success": result.get("success", False)
                },
                tags=["token_tracking", operation, "usage_analysis"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "operation": operation,
                "result": result,
                "memory_ids": [task_memory_id, result_memory_id],
                "response_time": execution_time,
                "agent": "token_tracker",
                "metadata": {
                    "token_tracking": True,
                    "usage_monitoring": True,
                    "cost_analysis": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Token Tracker agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "agent": "token_tracker"
            }
    
    async def _track_usage(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Track token usage for a specific operation"""
        try:
            usage_data = task.get("usage_data", {})
            session_id = task.get("session_id", "unknown")
            
            # Create TokenUsage object
            token_usage = TokenUsage(
                model=usage_data.get("model", "unknown"),
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
                cost=self._calculate_cost(usage_data),
                timestamp=datetime.now().isoformat(),
                session_id=session_id,
                task_id=task.get("id", "unknown")
            )
            
            # Store usage
            self.usage_history.append(token_usage)
            
            # Update session usage
            if session_id not in self.session_usage:
                self.session_usage[session_id] = []
            self.session_usage[session_id].append(token_usage)
            
            # Update daily/hourly usage
            self._update_aggregated_usage(token_usage)
            
            # Check limits
            limit_check = self._check_usage_limits(token_usage)
            
            return {
                "success": True,
                "usage_tracked": asdict(token_usage),
                "limit_check": limit_check,
                "session_total": self._get_session_total(session_id),
                "daily_total": self._get_daily_total()
            }
            
        except Exception as e:
            logger.error(f"❌ Usage tracking failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _analyze_usage(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze usage patterns and trends"""
        try:
            time_range = task.get("time_range", "daily")  # daily, hourly, session
            session_id = task.get("session_id")
            
            if time_range == "session" and session_id:
                usage_data = self.session_usage.get(session_id, [])
                total_tokens = sum(usage.total_tokens for usage in usage_data)
                total_cost = sum(usage.cost for usage in usage_data)
                
                model_breakdown = {}
                for usage in usage_data:
                    if usage.model not in model_breakdown:
                        model_breakdown[usage.model] = {"tokens": 0, "cost": 0.0, "count": 0}
                    model_breakdown[usage.model]["tokens"] += usage.total_tokens
                    model_breakdown[usage.model]["cost"] += usage.cost
                    model_breakdown[usage.model]["count"] += 1
                
                return {
                    "success": True,
                    "time_range": time_range,
                    "session_id": session_id,
                    "total_tokens": total_tokens,
                    "total_cost": total_cost,
                    "model_breakdown": model_breakdown,
                    "usage_count": len(usage_data)
                }
            
            elif time_range == "daily":
                today = datetime.now().date().isoformat()
                daily_data = self.daily_usage.get(today, {"tokens": 0, "cost": 0.0, "count": 0})
                
                return {
                    "success": True,
                    "time_range": time_range,
                    "date": today,
                    "total_tokens": daily_data["tokens"],
                    "total_cost": daily_data["cost"],
                    "usage_count": daily_data["count"],
                    "limits": {
                        "token_limit": self.usage_limits.daily_token_limit,
                        "cost_limit": self.usage_limits.daily_cost_limit,
                        "token_usage_percent": (daily_data["tokens"] / self.usage_limits.daily_token_limit) * 100,
                        "cost_usage_percent": (daily_data["cost"] / self.usage_limits.daily_cost_limit) * 100
                    }
                }
            
            else:  # hourly
                current_hour = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
                hourly_data = self.hourly_usage.get(current_hour, {"tokens": 0, "cost": 0.0, "count": 0})
                
                return {
                    "success": True,
                    "time_range": time_range,
                    "hour": current_hour,
                    "total_tokens": hourly_data["tokens"],
                    "total_cost": hourly_data["cost"],
                    "usage_count": hourly_data["count"],
                    "limits": {
                        "token_limit": self.usage_limits.hourly_token_limit,
                        "cost_limit": self.usage_limits.hourly_cost_limit,
                        "token_usage_percent": (hourly_data["tokens"] / self.usage_limits.hourly_token_limit) * 100,
                        "cost_usage_percent": (hourly_data["cost"] / self.usage_limits.hourly_cost_limit) * 100
                    }
                }
            
        except Exception as e:
            logger.error(f"❌ Usage analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive usage report"""
        try:
            report_type = task.get("report_type", "summary")
            
            # Generate comprehensive report
            report = {
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_usage_entries": len(self.usage_history),
                    "active_sessions": len(self.session_usage),
                    "total_tokens_tracked": sum(usage.total_tokens for usage in self.usage_history),
                    "total_cost_tracked": sum(usage.cost for usage in self.usage_history)
                },
                "model_usage": {},
                "session_breakdown": {},
                "daily_trends": {},
                "limit_status": {}
            }
            
            # Model usage breakdown
            for usage in self.usage_history:
                if usage.model not in report["model_usage"]:
                    report["model_usage"][usage.model] = {
                        "total_tokens": 0,
                        "total_cost": 0.0,
                        "usage_count": 0,
                        "avg_tokens_per_request": 0
                    }
                
                model_stats = report["model_usage"][usage.model]
                model_stats["total_tokens"] += usage.total_tokens
                model_stats["total_cost"] += usage.cost
                model_stats["usage_count"] += 1
                model_stats["avg_tokens_per_request"] = model_stats["total_tokens"] / model_stats["usage_count"]
            
            # Session breakdown
            for session_id, session_usage in self.session_usage.items():
                report["session_breakdown"][session_id] = {
                    "total_tokens": sum(usage.total_tokens for usage in session_usage),
                    "total_cost": sum(usage.cost for usage in session_usage),
                    "usage_count": len(session_usage),
                    "models_used": list(set(usage.model for usage in session_usage))
                }
            
            # Daily trends
            report["daily_trends"] = dict(self.daily_usage)
            
            # Limit status
            today = datetime.now().date().isoformat()
            daily_data = self.daily_usage.get(today, {"tokens": 0, "cost": 0.0})
            
            report["limit_status"] = {
                "daily_token_usage": daily_data["tokens"],
                "daily_token_limit": self.usage_limits.daily_token_limit,
                "daily_token_percentage": (daily_data["tokens"] / self.usage_limits.daily_token_limit) * 100,
                "daily_cost_usage": daily_data["cost"],
                "daily_cost_limit": self.usage_limits.daily_cost_limit,
                "daily_cost_percentage": (daily_data["cost"] / self.usage_limits.daily_cost_limit) * 100
            }
            
            return {
                "success": True,
                "report": report
            }
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _set_limits(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Set usage limits"""
        try:
            limits = task.get("limits", {})
            
            if "daily_token_limit" in limits:
                self.usage_limits.daily_token_limit = limits["daily_token_limit"]
            if "daily_cost_limit" in limits:
                self.usage_limits.daily_cost_limit = limits["daily_cost_limit"]
            if "hourly_token_limit" in limits:
                self.usage_limits.hourly_token_limit = limits["hourly_token_limit"]
            if "hourly_cost_limit" in limits:
                self.usage_limits.hourly_cost_limit = limits["hourly_cost_limit"]
            if "session_token_limit" in limits:
                self.usage_limits.session_token_limit = limits["session_token_limit"]
            if "session_cost_limit" in limits:
                self.usage_limits.session_cost_limit = limits["session_cost_limit"]
            
            return {
                "success": True,
                "limits_updated": limits,
                "current_limits": asdict(self.usage_limits)
            }
            
        except Exception as e:
            logger.error(f"❌ Limit setting failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _check_limits(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Check current usage against limits"""
        try:
            session_id = task.get("session_id")
            
            # Check daily limits
            today = datetime.now().date().isoformat()
            daily_data = self.daily_usage.get(today, {"tokens": 0, "cost": 0.0})
            
            daily_check = {
                "token_usage": daily_data["tokens"],
                "token_limit": self.usage_limits.daily_token_limit,
                "token_percentage": (daily_data["tokens"] / self.usage_limits.daily_token_limit) * 100,
                "token_exceeded": daily_data["tokens"] > self.usage_limits.daily_token_limit,
                "cost_usage": daily_data["cost"],
                "cost_limit": self.usage_limits.daily_cost_limit,
                "cost_percentage": (daily_data["cost"] / self.usage_limits.daily_cost_limit) * 100,
                "cost_exceeded": daily_data["cost"] > self.usage_limits.daily_cost_limit
            }
            
            # Check session limits if session_id provided
            session_check = None
            if session_id:
                session_data = self.session_usage.get(session_id, [])
                session_tokens = sum(usage.total_tokens for usage in session_data)
                session_cost = sum(usage.cost for usage in session_data)
                
                session_check = {
                    "token_usage": session_tokens,
                    "token_limit": self.usage_limits.session_token_limit,
                    "token_percentage": (session_tokens / self.usage_limits.session_token_limit) * 100,
                    "token_exceeded": session_tokens > self.usage_limits.session_token_limit,
                    "cost_usage": session_cost,
                    "cost_limit": self.usage_limits.session_cost_limit,
                    "cost_percentage": (session_cost / self.usage_limits.session_cost_limit) * 100,
                    "cost_exceeded": session_cost > self.usage_limits.session_cost_limit
                }
            
            return {
                "success": True,
                "daily_check": daily_check,
                "session_check": session_check,
                "limits_exceeded": daily_check["token_exceeded"] or daily_check["cost_exceeded"] or 
                                 (session_check and (session_check["token_exceeded"] or session_check["cost_exceeded"]))
            }
            
        except Exception as e:
            logger.error(f"❌ Limit check failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _optimize_usage(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide usage optimization recommendations"""
        try:
            # Analyze model usage patterns
            model_efficiency = {}
            for usage in self.usage_history:
                if usage.model not in model_efficiency:
                    model_efficiency[usage.model] = {
                        "total_cost": 0.0,
                        "total_tokens": 0,
                        "usage_count": 0
                    }
                
                model_efficiency[usage.model]["total_cost"] += usage.cost
                model_efficiency[usage.model]["total_tokens"] += usage.total_tokens
                model_efficiency[usage.model]["usage_count"] += 1
            
            # Calculate cost per token for each model
            for model, stats in model_efficiency.items():
                if stats["total_tokens"] > 0:
                    stats["cost_per_token"] = stats["total_cost"] / stats["total_tokens"]
                else:
                    stats["cost_per_token"] = 0
            
            # Generate recommendations
            recommendations = []
            
            # Most expensive model
            if model_efficiency:
                most_expensive = max(model_efficiency.items(), key=lambda x: x[1]["cost_per_token"])
                recommendations.append({
                    "type": "cost_optimization",
                    "message": f"Consider using a more cost-effective model than {most_expensive[0]}",
                    "details": f"Current cost per token: ${most_expensive[1]['cost_per_token']:.6f}"
                })
            
            # Check for frequent small requests
            small_requests = [usage for usage in self.usage_history if usage.total_tokens < 100]
            if len(small_requests) > len(self.usage_history) * 0.3:
                recommendations.append({
                    "type": "efficiency_optimization",
                    "message": "Consider batching small requests to improve efficiency",
                    "details": f"{len(small_requests)} of {len(self.usage_history)} requests are small (<100 tokens)"
                })
            
            return {
                "success": True,
                "model_efficiency": model_efficiency,
                "recommendations": recommendations,
                "optimization_score": self._calculate_optimization_score(model_efficiency)
            }
            
        except Exception as e:
            logger.error(f"❌ Usage optimization failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_usage_summary(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get general usage summary"""
        try:
            return {
                "success": True,
                "total_entries": len(self.usage_history),
                "active_sessions": len(self.session_usage),
                "total_tokens": sum(usage.total_tokens for usage in self.usage_history),
                "total_cost": sum(usage.cost for usage in self.usage_history),
                "models_used": list(set(usage.model for usage in self.usage_history)),
                "tracking_config": self.tracking_config,
                "current_limits": asdict(self.usage_limits)
            }
            
        except Exception as e:
            logger.error(f"❌ Usage summary failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_cost(self, usage_data: Dict[str, Any]) -> float:
        """Calculate cost based on token usage"""
        model = usage_data.get("model", "unknown")
        prompt_tokens = usage_data.get("prompt_tokens", 0)
        completion_tokens = usage_data.get("completion_tokens", 0)
        
        if model in self.model_pricing:
            pricing = self.model_pricing[model]
            prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
            completion_cost = (completion_tokens / 1000) * pricing["completion"]
            return prompt_cost + completion_cost
        
        return 0.0
    
    def _update_aggregated_usage(self, usage: TokenUsage):
        """Update daily and hourly usage aggregates"""
        # Update daily usage
        date = datetime.fromisoformat(usage.timestamp).date().isoformat()
        if date not in self.daily_usage:
            self.daily_usage[date] = {"tokens": 0, "cost": 0.0, "count": 0}
        
        self.daily_usage[date]["tokens"] += usage.total_tokens
        self.daily_usage[date]["cost"] += usage.cost
        self.daily_usage[date]["count"] += 1
        
        # Update hourly usage
        hour = datetime.fromisoformat(usage.timestamp).replace(minute=0, second=0, microsecond=0).isoformat()
        if hour not in self.hourly_usage:
            self.hourly_usage[hour] = {"tokens": 0, "cost": 0.0, "count": 0}
        
        self.hourly_usage[hour]["tokens"] += usage.total_tokens
        self.hourly_usage[hour]["cost"] += usage.cost
        self.hourly_usage[hour]["count"] += 1
    
    def _check_usage_limits(self, usage: TokenUsage) -> Dict[str, Any]:
        """Check if usage exceeds limits"""
        alerts = []
        
        # Check daily limits
        today = datetime.now().date().isoformat()
        daily_data = self.daily_usage.get(today, {"tokens": 0, "cost": 0.0})
        
        if daily_data["tokens"] > self.usage_limits.daily_token_limit:
            alerts.append("Daily token limit exceeded")
        elif daily_data["tokens"] > self.usage_limits.daily_token_limit * self.tracking_config["alert_thresholds"]["token_warning"]:
            alerts.append("Daily token limit warning")
        
        if daily_data["cost"] > self.usage_limits.daily_cost_limit:
            alerts.append("Daily cost limit exceeded")
        elif daily_data["cost"] > self.usage_limits.daily_cost_limit * self.tracking_config["alert_thresholds"]["cost_warning"]:
            alerts.append("Daily cost limit warning")
        
        # Check session limits
        session_data = self.session_usage.get(usage.session_id, [])
        session_tokens = sum(u.total_tokens for u in session_data)
        session_cost = sum(u.cost for u in session_data)
        
        if session_tokens > self.usage_limits.session_token_limit:
            alerts.append("Session token limit exceeded")
        if session_cost > self.usage_limits.session_cost_limit:
            alerts.append("Session cost limit exceeded")
        
        return {
            "alerts": alerts,
            "limits_exceeded": len(alerts) > 0,
            "daily_usage": daily_data,
            "session_usage": {"tokens": session_tokens, "cost": session_cost}
        }
    
    def _get_session_total(self, session_id: str) -> Dict[str, Any]:
        """Get total usage for a session"""
        session_data = self.session_usage.get(session_id, [])
        return {
            "total_tokens": sum(usage.total_tokens for usage in session_data),
            "total_cost": sum(usage.cost for usage in session_data),
            "usage_count": len(session_data)
        }
    
    def _get_daily_total(self) -> Dict[str, Any]:
        """Get total usage for today"""
        today = datetime.now().date().isoformat()
        return self.daily_usage.get(today, {"tokens": 0, "cost": 0.0, "count": 0})
    
    def _calculate_optimization_score(self, model_efficiency: Dict[str, Any]) -> float:
        """Calculate optimization score based on usage patterns"""
        if not model_efficiency:
            return 0.0
        
        # Simple scoring based on cost efficiency
        total_cost = sum(stats["total_cost"] for stats in model_efficiency.values())
        total_tokens = sum(stats["total_tokens"] for stats in model_efficiency.values())
        
        if total_tokens == 0:
            return 0.0
        
        avg_cost_per_token = total_cost / total_tokens
        
        # Score based on cost efficiency (lower is better)
        # Normalize to 0-100 scale
        efficiency_score = max(0, min(100, 100 - (avg_cost_per_token * 100000)))
        
        return efficiency_score
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get token tracker agent statistics"""
        return {
            **self.stats,
            "tracking_config": self.tracking_config,
            "model_pricing": self.model_pricing,
            "current_limits": asdict(self.usage_limits),
            "total_usage_tracked": len(self.usage_history),
            "active_sessions": len(self.session_usage),
            "tracking_capabilities": [
                "token_usage_monitoring",
                "cost_calculation",
                "limit_enforcement",
                "usage_analytics",
                "optimization_recommendations",
                "comprehensive_reporting"
            ]
        }


def create_token_tracker_agent(config: Dict[str, Any]) -> TokenTrackerAgent:
    """Factory function to create token tracker agent"""
    return TokenTrackerAgent(config)