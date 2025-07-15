"""
MeistroCraft Session Manager Agent Integration
Migrated from MeistroCraft's SessionManager class
"""

import asyncio
import json
import os
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class SessionManagerAgent(BaseAgent):
    """
    Session Manager Agent - Manages persistent sessions and workspace coordination
    Integrated from MeistroCraft system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="session_manager",
            agent_type=AgentType.MEMORY,
            description="Manages persistent sessions and workspace coordination",
            capabilities=[
                "session_management",
                "workspace_coordination",
                "context_persistence",
                "session_analytics",
                "multi_session_tracking",
                "session_recovery",
                "workspace_isolation",
                "session_optimization"
            ],
            model_requirements=["analysis", "memory", "coordination"],
            priority=7,  # High priority for session management
            max_concurrent_tasks=10,  # Can handle many sessions
            timeout_seconds=180  # Quick session operations
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # Session management configuration
        self.session_config = {
            "session_timeout": 3600,  # 1 hour timeout
            "max_active_sessions": 100,
            "session_cleanup_interval": 300,  # 5 minutes
            "workspace_isolation": True,
            "session_persistence": True
        }
        
        # Active sessions tracking
        self.active_sessions = {}
        self.session_workspaces = {}
        self.session_analytics = {}
        
        # Session lifecycle states
        self.session_states = {
            "created": "Session created but not active",
            "active": "Session is currently active",
            "idle": "Session is idle but preserved",
            "suspended": "Session temporarily suspended",
            "expired": "Session has expired",
            "archived": "Session archived for history"
        }
        
        logger.info("📋 Session Manager Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for session manager agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires session management
        session_keywords = [
            "session", "workspace", "context", "manage", "track",
            "persist", "isolate", "coordinate", "cleanup"
        ]
        
        return any(keyword in content for keyword in session_keywords) or task_type == "session_management"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute session management task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            operation = task.get("operation", "manage")
            session_id = task.get("session_id")
            user_request = task.get("content", "")
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Session management task: {operation} - {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "session_manager",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "session_id": session_id
                },
                session_id=session_id
            )
            
            # Execute operation based on type
            if operation == "create":
                result = await self._create_session(task)
            elif operation == "get":
                result = await self._get_session(task)
            elif operation == "update":
                result = await self._update_session(task)
            elif operation == "delete":
                result = await self._delete_session(task)
            elif operation == "list":
                result = await self._list_sessions(task)
            elif operation == "analytics":
                result = await self._get_session_analytics(task)
            elif operation == "cleanup":
                result = await self._cleanup_sessions(task)
            else:
                result = await self._manage_session(task)
            
            # Store result in memory
            result_memory_id = self.memory_manager.store_memory(
                content=f"Session management result: {json.dumps(result, indent=2)}",
                memory_type=MemoryType.SESSION,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "session_manager",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "success": result.get("success", False),
                    "session_count": len(result.get("sessions", []))
                },
                tags=["session_management", operation, "workspace"],
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
                "agent": "session_manager",
                "metadata": {
                    "session_management": True,
                    "workspace_isolation": self.session_config["workspace_isolation"],
                    "persistence": self.session_config["session_persistence"]
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Session Manager agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "agent": "session_manager"
            }
    
    async def _create_session(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new session"""
        try:
            session_id = task.get("session_id") or str(uuid.uuid4())
            session_name = task.get("session_name", f"Session {session_id[:8]}")
            project_description = task.get("project_description", "")
            
            # Create workspace directory
            workspace_path = await self._create_workspace(session_id, project_description)
            
            # Create session data
            session_data = {
                "id": session_id,
                "name": session_name,
                "created_at": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat(),
                "state": "created",
                "workspace_path": workspace_path,
                "project_description": project_description,
                "task_history": [],
                "context": {},
                "analytics": {
                    "tasks_completed": 0,
                    "total_execution_time": 0,
                    "models_used": {},
                    "tokens_used": 0
                }
            }
            
            # Store in active sessions
            self.active_sessions[session_id] = session_data
            self.session_workspaces[session_id] = workspace_path
            
            # Store in memory
            session_memory_id = self.memory_manager.store_memory(
                content=f"Session created: {json.dumps(session_data, indent=2)}",
                memory_type=MemoryType.SESSION,
                priority=MemoryPriority.HIGH,
                metadata={
                    "session_id": session_id,
                    "session_name": session_name,
                    "workspace_path": workspace_path,
                    "state": "created"
                },
                tags=["session_created", "workspace", "active"],
                session_id=session_id
            )
            
            return {
                "success": True,
                "session_id": session_id,
                "session_data": session_data,
                "workspace_path": workspace_path,
                "memory_id": session_memory_id
            }
            
        except Exception as e:
            logger.error(f"❌ Session creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_session(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get session information"""
        try:
            session_id = task.get("session_id")
            
            if not session_id:
                return {"success": False, "error": "Session ID required"}
            
            # Check active sessions first
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                session_data["last_used"] = datetime.now().isoformat()
                return {
                    "success": True,
                    "session_data": session_data,
                    "source": "active_cache"
                }
            
            # Search in memory
            session_items = self.memory_manager.search_memory(
                query=f"session_id:{session_id}",
                memory_type=MemoryType.SESSION,
                use_vector=False,
                limit=1
            )
            
            if session_items:
                session_item = session_items[0]
                session_data = json.loads(session_item.content.split("Session created: ")[1])
                
                # Restore to active sessions
                self.active_sessions[session_id] = session_data
                self.session_workspaces[session_id] = session_data.get("workspace_path", "")
                
                return {
                    "success": True,
                    "session_data": session_data,
                    "source": "memory_restored"
                }
            
            return {
                "success": False,
                "error": f"Session {session_id} not found"
            }
            
        except Exception as e:
            logger.error(f"❌ Session retrieval failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _update_session(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Update session information"""
        try:
            session_id = task.get("session_id")
            updates = task.get("updates", {})
            
            if not session_id:
                return {"success": False, "error": "Session ID required"}
            
            # Get current session
            session_result = await self._get_session({"session_id": session_id})
            if not session_result["success"]:
                return session_result
            
            session_data = session_result["session_data"]
            
            # Apply updates
            for key, value in updates.items():
                if key in session_data:
                    session_data[key] = value
            
            session_data["last_used"] = datetime.now().isoformat()
            
            # Update active sessions
            self.active_sessions[session_id] = session_data
            
            # Store updated session in memory
            session_memory_id = self.memory_manager.store_memory(
                content=f"Session updated: {json.dumps(session_data, indent=2)}",
                memory_type=MemoryType.SESSION,
                priority=MemoryPriority.HIGH,
                metadata={
                    "session_id": session_id,
                    "updated_fields": list(updates.keys()),
                    "state": session_data.get("state", "active")
                },
                tags=["session_updated", "workspace", "active"],
                session_id=session_id
            )
            
            return {
                "success": True,
                "session_data": session_data,
                "updates_applied": list(updates.keys()),
                "memory_id": session_memory_id
            }
            
        except Exception as e:
            logger.error(f"❌ Session update failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _delete_session(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delete session"""
        try:
            session_id = task.get("session_id")
            archive = task.get("archive", True)
            
            if not session_id:
                return {"success": False, "error": "Session ID required"}
            
            # Get session data before deletion
            session_result = await self._get_session({"session_id": session_id})
            if not session_result["success"]:
                return session_result
            
            session_data = session_result["session_data"]
            
            # Archive session if requested
            if archive:
                session_data["state"] = "archived"
                session_data["archived_at"] = datetime.now().isoformat()
                
                archive_memory_id = self.memory_manager.store_memory(
                    content=f"Session archived: {json.dumps(session_data, indent=2)}",
                    memory_type=MemoryType.SESSION,
                    priority=MemoryPriority.MEDIUM,
                    metadata={
                        "session_id": session_id,
                        "state": "archived",
                        "archived_at": session_data["archived_at"]
                    },
                    tags=["session_archived", "workspace", "deleted"],
                    session_id=session_id
                )
            
            # Remove from active sessions
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            if session_id in self.session_workspaces:
                del self.session_workspaces[session_id]
            if session_id in self.session_analytics:
                del self.session_analytics[session_id]
            
            # Clean up workspace if needed
            workspace_path = session_data.get("workspace_path")
            if workspace_path and os.path.exists(workspace_path):
                # In a real implementation, you might want to clean up the workspace
                pass
            
            return {
                "success": True,
                "session_id": session_id,
                "archived": archive,
                "workspace_path": workspace_path,
                "archive_memory_id": archive_memory_id if archive else None
            }
            
        except Exception as e:
            logger.error(f"❌ Session deletion failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _list_sessions(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """List all sessions"""
        try:
            include_archived = task.get("include_archived", False)
            limit = task.get("limit", 100)
            
            sessions = []
            
            # Add active sessions
            for session_id, session_data in self.active_sessions.items():
                if session_data.get("state") != "archived" or include_archived:
                    sessions.append({
                        "id": session_id,
                        "name": session_data.get("name", "Unknown"),
                        "created_at": session_data.get("created_at"),
                        "last_used": session_data.get("last_used"),
                        "state": session_data.get("state", "active"),
                        "task_count": len(session_data.get("task_history", [])),
                        "workspace_path": session_data.get("workspace_path")
                    })
            
            # Add sessions from memory if needed
            if len(sessions) < limit:
                memory_sessions = self.memory_manager.search_memory(
                    query="session_id",
                    memory_type=MemoryType.SESSION,
                    use_vector=False,
                    limit=limit - len(sessions)
                )
                
                for item in memory_sessions:
                    if "session_id" in item.metadata:
                        session_id = item.metadata["session_id"]
                        if session_id not in [s["id"] for s in sessions]:
                            sessions.append({
                                "id": session_id,
                                "name": item.metadata.get("session_name", "Unknown"),
                                "created_at": item.created_at.isoformat(),
                                "last_used": item.created_at.isoformat(),
                                "state": item.metadata.get("state", "unknown"),
                                "task_count": 0,
                                "workspace_path": item.metadata.get("workspace_path")
                            })
            
            return {
                "success": True,
                "sessions": sessions[:limit],
                "total_sessions": len(sessions),
                "active_sessions": len(self.active_sessions),
                "include_archived": include_archived
            }
            
        except Exception as e:
            logger.error(f"❌ Session listing failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_session_analytics(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get session analytics"""
        try:
            session_id = task.get("session_id")
            
            if session_id:
                # Get analytics for specific session
                if session_id in self.active_sessions:
                    session_data = self.active_sessions[session_id]
                    return {
                        "success": True,
                        "session_analytics": session_data.get("analytics", {}),
                        "session_id": session_id
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Session {session_id} not found in active sessions"
                    }
            else:
                # Get global analytics
                total_sessions = len(self.active_sessions)
                total_tasks = sum(len(session.get("task_history", [])) for session in self.active_sessions.values())
                
                states = {}
                for session in self.active_sessions.values():
                    state = session.get("state", "unknown")
                    states[state] = states.get(state, 0) + 1
                
                return {
                    "success": True,
                    "global_analytics": {
                        "total_sessions": total_sessions,
                        "total_tasks": total_tasks,
                        "session_states": states,
                        "average_tasks_per_session": total_tasks / total_sessions if total_sessions > 0 else 0
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Session analytics failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _cleanup_sessions(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Clean up expired sessions"""
        try:
            cleanup_count = 0
            timeout_minutes = self.session_config["session_timeout"] / 60
            
            expired_sessions = []
            current_time = datetime.now()
            
            for session_id, session_data in list(self.active_sessions.items()):
                last_used = datetime.fromisoformat(session_data.get("last_used", session_data.get("created_at")))
                if (current_time - last_used).total_seconds() > self.session_config["session_timeout"]:
                    expired_sessions.append(session_id)
            
            # Archive expired sessions
            for session_id in expired_sessions:
                await self._delete_session({
                    "session_id": session_id,
                    "archive": True
                })
                cleanup_count += 1
            
            return {
                "success": True,
                "cleanup_count": cleanup_count,
                "expired_sessions": expired_sessions,
                "timeout_minutes": timeout_minutes
            }
            
        except Exception as e:
            logger.error(f"❌ Session cleanup failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _manage_session(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """General session management"""
        try:
            # This is a catch-all for general session management tasks
            return {
                "success": True,
                "message": "Session management completed",
                "active_sessions": len(self.active_sessions),
                "session_config": self.session_config
            }
            
        except Exception as e:
            logger.error(f"❌ Session management failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _create_workspace(self, session_id: str, description: str) -> str:
        """Create isolated workspace for session"""
        try:
            # In a real implementation, you would create actual directories
            # For now, we'll return a virtual workspace path
            workspace_path = f"/workspaces/session_{session_id}"
            
            # Store workspace info
            self.session_workspaces[session_id] = workspace_path
            
            return workspace_path
            
        except Exception as e:
            logger.error(f"❌ Workspace creation failed: {e}")
            return f"/workspaces/session_{session_id}_error"
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get session manager agent statistics"""
        return {
            **self.stats,
            "session_config": self.session_config,
            "active_sessions": len(self.active_sessions),
            "session_workspaces": len(self.session_workspaces),
            "session_states": list(self.session_states.keys()),
            "sessions_managed": len(self.memory_manager.search_memory(
                query="session_manager",
                memory_type=MemoryType.SESSION,
                limit=1000
            )),
            "session_capabilities": [
                "session_creation",
                "workspace_isolation",
                "context_persistence",
                "session_recovery",
                "analytics_tracking",
                "automated_cleanup"
            ]
        }


def create_session_manager_agent(config: Dict[str, Any]) -> SessionManagerAgent:
    """Factory function to create session manager agent"""
    return SessionManagerAgent(config)