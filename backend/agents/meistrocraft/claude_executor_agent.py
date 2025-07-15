"""
MeistroCraft Claude Executor Agent Integration
Migrated from MeistroCraft's Claude Code CLI integration
"""

import asyncio
import json
import subprocess
import tempfile
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class ClaudeExecutorAgent(BaseAgent):
    """
    Claude Executor Agent - Executes strategic plans using Claude Code CLI
    Integrated from MeistroCraft system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="claude_executor",
            agent_type=AgentType.CODER,
            description="Executes strategic plans using Claude Code CLI integration",
            capabilities=[
                "claude_cli_integration",
                "strategic_execution",
                "multi_language_coding",
                "task_execution",
                "code_generation",
                "project_implementation",
                "file_operations",
                "cli_automation"
            ],
            model_requirements=["code_generation", "analysis", "reasoning"],
            priority=8,  # High priority for execution
            max_concurrent_tasks=3,
            timeout_seconds=900  # Longer timeout for complex execution
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # MeistroCraft-specific configuration
        self.meistrocraft_config = {
            "claude_cli_path": "claude",  # Assume claude is in PATH
            "session_persistence": True,
            "file_operations": True,
            "workspace_management": True,
            "execution_style": "strategic"
        }
        
        # Claude CLI integration settings
        self.claude_cli_settings = {
            "max_output_length": 50000,
            "timeout_seconds": 300,
            "retry_attempts": 3,
            "session_management": True
        }
        
        # Execution patterns from MeistroCraft
        self.execution_patterns = {
            "direct": "Execute Claude CLI commands directly",
            "structured": "Use structured task execution with context",
            "iterative": "Iterative execution with feedback loops",
            "collaborative": "Coordinate with other agents during execution"
        }
        
        logger.info("🎭 Claude Executor Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for Claude executor agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires Claude CLI execution
        claude_keywords = [
            "execute", "implement", "code", "generate", "create", "build",
            "develop", "write", "claude", "cli", "command"
        ]
        
        return any(keyword in content for keyword in claude_keywords) or task_type == "execution"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using Claude CLI"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            execution_style = task.get("execution_style", "structured")
            session_id = task.get("session_id")
            strategic_plan = task.get("strategic_plan", {})
            
            # Get project context
            context = await self.get_project_context(session_id)
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"Claude Executor task: {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "claude_executor",
                    "task_id": task.get("id"),
                    "execution_style": execution_style,
                    "has_strategic_plan": bool(strategic_plan),
                    "session_id": session_id
                },
                session_id=session_id
            )
            
            # Prepare Claude CLI execution
            claude_request = self._prepare_claude_request(
                user_request, execution_style, strategic_plan, context
            )
            
            # Execute using Claude CLI
            execution_result = await self._execute_claude_cli(
                claude_request, task.get("id", "unknown")
            )
            
            # Process execution results
            processed_result = self._process_execution_result(execution_result)
            
            # Store execution results in memory
            result_memory_id = self.memory_manager.store_memory(
                content=f"Claude execution result: {json.dumps(processed_result, indent=2)}",
                memory_type=MemoryType.CODE,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "claude_executor",
                    "task_id": task.get("id"),
                    "execution_style": execution_style,
                    "success": processed_result.get("success", False),
                    "output_length": len(processed_result.get("output", "")),
                    "files_created": len(processed_result.get("files_created", []))
                },
                tags=["claude_execution", "strategic_implementation", execution_style],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "execution_result": processed_result,
                "execution_style": execution_style,
                "strategic_plan_used": bool(strategic_plan),
                "memory_ids": [task_memory_id, result_memory_id],
                "response_time": execution_time,
                "agent": "claude_executor",
                "metadata": {
                    "execution_quality": "strategic",
                    "claude_cli_integration": True,
                    "session_persistence": True,
                    "file_operations": processed_result.get("files_created", [])
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Claude Executor agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "agent": "claude_executor"
            }
    
    def _prepare_claude_request(self, user_request: str, execution_style: str, 
                               strategic_plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Prepare Claude CLI request based on MeistroCraft patterns"""
        
        # Include strategic plan context if available
        plan_context = ""
        if strategic_plan:
            plan_context = f"""
Strategic Plan Context:
- Project: {strategic_plan.get('project_overview', {}).get('title', 'Unknown')}
- Approach: {strategic_plan.get('orchestration_strategy', {}).get('approach', 'Unknown')}
- Tasks: {len(strategic_plan.get('tasks', []))} tasks planned
- Success Criteria: {strategic_plan.get('project_overview', {}).get('success_criteria', [])}

Current Task Context:
"""
        
        # Include session context
        session_context = ""
        if context.get("session_info"):
            session_context = f"""
Session Context:
- Session ID: {context['session_info'].get('session_id', 'Unknown')}
- Previous Work: {len(context.get('previous_executions', []))} executions
- Files Created: {context.get('files_created', [])}

"""
        
        # Build the comprehensive request
        claude_request = f"""
{plan_context}

{session_context}

Main Request: {user_request}

Execution Style: {execution_style}
Pattern: {self.execution_patterns.get(execution_style, 'Structured execution')}

Please provide a comprehensive implementation that:
1. Follows the strategic plan context (if provided)
2. Implements the requested functionality completely
3. Creates well-structured, production-ready code
4. Includes proper error handling and documentation
5. Provides clear explanations of implementation choices
6. Suggests improvements and next steps

If this is part of a larger project, ensure consistency with previous work and maintain architectural coherence.
"""
        
        return claude_request
    
    async def _execute_claude_cli(self, request: str, task_id: str) -> Dict[str, Any]:
        """Execute Claude CLI command"""
        try:
            # Create temporary file for request
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(request)
                temp_file_path = temp_file.name
            
            try:
                # Execute Claude CLI command
                cmd = [
                    self.meistrocraft_config["claude_cli_path"],
                    "--file", temp_file_path
                ]
                
                # Add session management if available
                if self.claude_cli_settings["session_management"]:
                    cmd.extend(["--session", f"omnidev_{task_id}"])
                
                # Execute command
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=os.getcwd()
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.claude_cli_settings["timeout_seconds"]
                )
                
                return {
                    "success": process.returncode == 0,
                    "output": stdout.decode('utf-8'),
                    "error": stderr.decode('utf-8'),
                    "return_code": process.returncode,
                    "command": ' '.join(cmd)
                }
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except asyncio.TimeoutError:
            logger.error(f"❌ Claude CLI execution timeout for task {task_id}")
            return {
                "success": False,
                "output": "",
                "error": "Execution timeout",
                "return_code": -1,
                "command": "timeout"
            }
        except Exception as e:
            logger.error(f"❌ Claude CLI execution failed: {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1,
                "command": "error"
            }
    
    def _process_execution_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process Claude CLI execution result"""
        try:
            processed = {
                "success": raw_result.get("success", False),
                "output": raw_result.get("output", ""),
                "error": raw_result.get("error", ""),
                "return_code": raw_result.get("return_code", -1),
                "command": raw_result.get("command", ""),
                "files_created": [],
                "code_blocks": [],
                "explanations": [],
                "suggestions": []
            }
            
            # Extract information from output
            output = processed["output"]
            if output:
                # Extract file creation patterns
                file_patterns = [
                    r"Created file: (.+)",
                    r"Saved to: (.+)",
                    r"File written: (.+)"
                ]
                
                import re
                for pattern in file_patterns:
                    matches = re.findall(pattern, output)
                    processed["files_created"].extend(matches)
                
                # Extract code blocks
                code_blocks = re.findall(r'```(\w+)?\n(.*?)```', output, re.DOTALL)
                processed["code_blocks"] = [
                    {"language": lang or "text", "content": code}
                    for lang, code in code_blocks
                ]
                
                # Extract explanations (lines starting with explanation keywords)
                explanation_lines = []
                for line in output.split('\n'):
                    if any(keyword in line.lower() for keyword in ["explanation", "note", "important", "this"]):
                        explanation_lines.append(line.strip())
                processed["explanations"] = explanation_lines
                
                # Extract suggestions (lines with suggestion keywords)
                suggestion_lines = []
                for line in output.split('\n'):
                    if any(keyword in line.lower() for keyword in ["suggest", "recommend", "consider", "improve"]):
                        suggestion_lines.append(line.strip())
                processed["suggestions"] = suggestion_lines
            
            # Add execution metadata
            processed["execution_metadata"] = {
                "processed_at": datetime.now().isoformat(),
                "executor": "claude_executor",
                "output_length": len(output),
                "code_blocks_count": len(processed["code_blocks"]),
                "files_created_count": len(processed["files_created"])
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"❌ Result processing failed: {e}")
            return {
                "success": False,
                "output": raw_result.get("output", ""),
                "error": f"Processing failed: {str(e)}",
                "execution_metadata": {"processed_at": datetime.now().isoformat(), "processing_error": True}
            }
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context for Claude execution"""
        try:
            # Get previous executions
            execution_items = self.memory_manager.search_memory(
                query="claude_executor",
                memory_type=MemoryType.CODE,
                use_vector=True,
                limit=5
            )
            
            # Get session information
            session_items = self.memory_manager.search_memory(
                query="session",
                memory_type=MemoryType.SESSION,
                use_vector=True,
                limit=2
            )
            
            context = {
                "session_info": {},
                "previous_executions": [],
                "files_created": [],
                "execution_patterns": []
            }
            
            # Extract previous executions
            for item in execution_items:
                if "files_created" in item.metadata:
                    context["previous_executions"].append({
                        "success": item.metadata.get("success", False),
                        "files_created": item.metadata.get("files_created", 0),
                        "execution_style": item.metadata.get("execution_style", "unknown"),
                        "created_at": item.created_at.isoformat()
                    })
                    
                    # Collect files created
                    context["files_created"].extend(item.metadata.get("files_created", []))
            
            # Extract session information
            for item in session_items:
                if "session_id" in item.metadata:
                    context["session_info"] = {
                        "session_id": item.metadata["session_id"],
                        "created_at": item.created_at.isoformat()
                    }
            
            # Analyze execution patterns
            execution_styles = [exec_info.get("execution_style") for exec_info in context["previous_executions"]]
            context["execution_patterns"] = list(set(execution_styles))
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get Claude executor agent statistics"""
        return {
            **self.stats,
            "execution_patterns": list(self.execution_patterns.keys()),
            "meistrocraft_config": self.meistrocraft_config,
            "claude_cli_settings": self.claude_cli_settings,
            "executions_completed": len(self.memory_manager.search_memory(
                query="claude_executor",
                memory_type=MemoryType.CODE,
                limit=1000
            )),
            "execution_capabilities": [
                "claude_cli_integration",
                "strategic_execution",
                "session_management",
                "file_operations",
                "multi_language_support",
                "collaborative_execution"
            ]
        }


def create_claude_executor_agent(config: Dict[str, Any]) -> ClaudeExecutorAgent:
    """Factory function to create Claude executor agent"""
    return ClaudeExecutorAgent(config)