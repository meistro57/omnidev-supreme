"""
MeistroCraft GitHub Integrator Agent Integration
Migrated from MeistroCraft's github_client.py and github_workflows.py
"""

import asyncio
import json
import os
import base64
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    from github import Github, GithubException
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False

import requests

from ..registry.agent_registry import BaseAgent, AgentMetadata, AgentType, AgentStatus
from ...memory.memory_manager import memory_manager, MemoryType, MemoryPriority
from ...orchestration.model_orchestrator import model_orchestrator, TaskRequest, TaskComplexity, ModelCapability

logger = logging.getLogger(__name__)


class GitHubIntegratorAgent(BaseAgent):
    """
    GitHub Integrator Agent - Manages GitHub operations and workflow automation
    Integrated from MeistroCraft system
    """
    
    def __init__(self, config: Dict[str, Any]):
        metadata = AgentMetadata(
            name="github_integrator",
            agent_type=AgentType.DEPLOYER,
            description="Manages GitHub operations and workflow automation",
            capabilities=[
                "repository_management",
                "pull_request_automation",
                "issue_tracking",
                "workflow_automation",
                "branch_management",
                "file_operations",
                "ci_cd_integration",
                "github_api_integration"
            ],
            model_requirements=["analysis", "reasoning", "text_generation"],
            priority=6,  # Medium priority for GitHub operations
            max_concurrent_tasks=5,
            timeout_seconds=300  # 5 minutes for GitHub operations
        )
        
        super().__init__(metadata, config)
        self.memory_manager = memory_manager
        self.orchestrator = model_orchestrator
        
        # GitHub configuration
        self.github_config = {
            "api_token": config.get("github_api_token"),
            "base_url": "https://api.github.com",
            "timeout": 30,
            "retry_attempts": 3,
            "rate_limit_handling": True
        }
        
        # Initialize GitHub client
        self.github_client = None
        if PYGITHUB_AVAILABLE and self.github_config["api_token"]:
            self.github_client = Github(self.github_config["api_token"])
        
        # GitHub operations
        self.github_operations = {
            "repository": "Repository management (create, fork, list)",
            "pull_request": "Pull request automation (create, update, merge)",
            "issue": "Issue tracking (create, update, close)",
            "workflow": "Workflow automation and CI/CD",
            "branch": "Branch management (create, delete, merge)",
            "file": "File operations (read, write, delete)",
            "webhook": "Webhook management and event handling"
        }
        
        # Workflow templates
        self.workflow_templates = {
            "meistrocraft_success": {
                "name": "MeistroCraft Success - {filename}",
                "description": "Successful MeistroCraft execution",
                "labels": ["meistrocraft", "success", "automated"],
                "branch_prefix": "meistrocraft/success"
            },
            "meistrocraft_failure": {
                "name": "MeistroCraft Failure - {filename}",
                "description": "Failed MeistroCraft execution",
                "labels": ["meistrocraft", "failure", "bug"],
                "branch_prefix": "meistrocraft/failure"
            },
            "code_review": {
                "name": "Code Review - {filename}",
                "description": "Code review and quality check",
                "labels": ["code-review", "quality", "review-required"],
                "branch_prefix": "review"
            }
        }
        
        logger.info("🐙 GitHub Integrator Agent initialized")
    
    async def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for GitHub integrator agent"""
        task_type = task.get("type", "").lower()
        content = task.get("content", "").lower()
        
        # Check if task requires GitHub operations
        github_keywords = [
            "github", "repository", "repo", "pull request", "pr", "issue",
            "commit", "branch", "workflow", "ci/cd", "merge", "fork"
        ]
        
        return any(keyword in content for keyword in github_keywords) or task_type == "github"
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub integration task"""
        try:
            self.status = AgentStatus.BUSY
            start_time = datetime.now()
            
            # Extract task information
            user_request = task.get("content", "")
            operation = task.get("operation", "repository")
            repository = task.get("repository", "")
            session_id = task.get("session_id")
            
            # Validate GitHub configuration
            if not self.github_config["api_token"]:
                raise Exception("GitHub API token not configured")
            
            # Store task in memory
            task_memory_id = self.memory_manager.store_memory(
                content=f"GitHub integration task: {operation} - {user_request}",
                memory_type=MemoryType.TASK,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "github_integrator",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "repository": repository,
                    "session_id": session_id
                },
                session_id=session_id
            )
            
            # Get project context
            context = await self.get_project_context(session_id)
            
            # Execute GitHub operation
            github_result = await self._execute_github_operation(
                operation, task, context
            )
            
            # Store GitHub result in memory
            result_memory_id = self.memory_manager.store_memory(
                content=f"GitHub operation result: {json.dumps(github_result, indent=2)}",
                memory_type=MemoryType.PROJECT,
                priority=MemoryPriority.HIGH,
                metadata={
                    "agent": "github_integrator",
                    "task_id": task.get("id"),
                    "operation": operation,
                    "repository": repository,
                    "success": github_result.get("success", False),
                    "github_object_type": github_result.get("object_type", "unknown")
                },
                tags=["github", operation, repository.split("/")[-1] if "/" in repository else "unknown"],
                session_id=session_id
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update status
            self.status = AgentStatus.IDLE
            
            return {
                "success": True,
                "operation": operation,
                "repository": repository,
                "github_result": github_result,
                "memory_ids": [task_memory_id, result_memory_id],
                "response_time": execution_time,
                "agent": "github_integrator",
                "metadata": {
                    "github_integration": True,
                    "api_version": "v3",
                    "authenticated": bool(self.github_client)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ GitHub Integrator agent execution failed: {e}")
            self.status = AgentStatus.ERROR
            
            return {
                "success": False,
                "error": str(e),
                "response_time": 0,
                "agent": "github_integrator"
            }
    
    async def _execute_github_operation(self, operation: str, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific GitHub operation"""
        try:
            if operation == "repository":
                return await self._handle_repository_operation(task, context)
            elif operation == "pull_request":
                return await self._handle_pull_request_operation(task, context)
            elif operation == "issue":
                return await self._handle_issue_operation(task, context)
            elif operation == "workflow":
                return await self._handle_workflow_operation(task, context)
            elif operation == "branch":
                return await self._handle_branch_operation(task, context)
            elif operation == "file":
                return await self._handle_file_operation(task, context)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}",
                    "available_operations": list(self.github_operations.keys())
                }
                
        except Exception as e:
            logger.error(f"❌ GitHub operation {operation} failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "operation": operation
            }
    
    async def _handle_repository_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle repository operations"""
        try:
            action = task.get("action", "list")
            repository = task.get("repository", "")
            
            if action == "list":
                repos = []
                if self.github_client:
                    user = self.github_client.get_user()
                    for repo in user.get_repos():
                        repos.append({
                            "name": repo.name,
                            "full_name": repo.full_name,
                            "description": repo.description,
                            "private": repo.private,
                            "language": repo.language,
                            "stars": repo.stargazers_count,
                            "forks": repo.forks_count,
                            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None
                        })
                
                return {
                    "success": True,
                    "object_type": "repository_list",
                    "repositories": repos,
                    "count": len(repos)
                }
            
            elif action == "create":
                repo_name = task.get("repo_name", "")
                description = task.get("description", "")
                private = task.get("private", False)
                
                if not repo_name:
                    return {"success": False, "error": "Repository name required"}
                
                if self.github_client:
                    user = self.github_client.get_user()
                    repo = user.create_repo(
                        name=repo_name,
                        description=description,
                        private=private
                    )
                    
                    return {
                        "success": True,
                        "object_type": "repository",
                        "repository": {
                            "name": repo.name,
                            "full_name": repo.full_name,
                            "description": repo.description,
                            "private": repo.private,
                            "clone_url": repo.clone_url,
                            "html_url": repo.html_url
                        }
                    }
                
                return {"success": False, "error": "GitHub client not available"}
            
            elif action == "fork":
                if not repository:
                    return {"success": False, "error": "Repository required for fork"}
                
                if self.github_client:
                    source_repo = self.github_client.get_repo(repository)
                    forked_repo = source_repo.create_fork()
                    
                    return {
                        "success": True,
                        "object_type": "repository",
                        "repository": {
                            "name": forked_repo.name,
                            "full_name": forked_repo.full_name,
                            "description": forked_repo.description,
                            "private": forked_repo.private,
                            "clone_url": forked_repo.clone_url,
                            "html_url": forked_repo.html_url,
                            "fork": True,
                            "parent": repository
                        }
                    }
                
                return {"success": False, "error": "GitHub client not available"}
            
            else:
                return {"success": False, "error": f"Unknown repository action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Repository operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_pull_request_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pull request operations"""
        try:
            action = task.get("action", "list")
            repository = task.get("repository", "")
            
            if not repository:
                return {"success": False, "error": "Repository required"}
            
            if action == "list":
                prs = []
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    for pr in repo.get_pulls():
                        prs.append({
                            "number": pr.number,
                            "title": pr.title,
                            "state": pr.state,
                            "author": pr.user.login,
                            "created_at": pr.created_at.isoformat(),
                            "updated_at": pr.updated_at.isoformat(),
                            "html_url": pr.html_url
                        })
                
                return {
                    "success": True,
                    "object_type": "pull_request_list",
                    "pull_requests": prs,
                    "count": len(prs)
                }
            
            elif action == "create":
                title = task.get("title", "")
                body = task.get("body", "")
                head = task.get("head", "")
                base = task.get("base", "main")
                
                if not all([title, head]):
                    return {"success": False, "error": "Title and head branch required"}
                
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    pr = repo.create_pull(
                        title=title,
                        body=body,
                        head=head,
                        base=base
                    )
                    
                    return {
                        "success": True,
                        "object_type": "pull_request",
                        "pull_request": {
                            "number": pr.number,
                            "title": pr.title,
                            "state": pr.state,
                            "author": pr.user.login,
                            "html_url": pr.html_url,
                            "created_at": pr.created_at.isoformat()
                        }
                    }
                
                return {"success": False, "error": "GitHub client not available"}
            
            else:
                return {"success": False, "error": f"Unknown pull request action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Pull request operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_issue_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle issue operations"""
        try:
            action = task.get("action", "list")
            repository = task.get("repository", "")
            
            if not repository:
                return {"success": False, "error": "Repository required"}
            
            if action == "list":
                issues = []
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    for issue in repo.get_issues():
                        issues.append({
                            "number": issue.number,
                            "title": issue.title,
                            "state": issue.state,
                            "author": issue.user.login,
                            "created_at": issue.created_at.isoformat(),
                            "updated_at": issue.updated_at.isoformat(),
                            "html_url": issue.html_url,
                            "labels": [label.name for label in issue.labels]
                        })
                
                return {
                    "success": True,
                    "object_type": "issue_list",
                    "issues": issues,
                    "count": len(issues)
                }
            
            elif action == "create":
                title = task.get("title", "")
                body = task.get("body", "")
                labels = task.get("labels", [])
                
                if not title:
                    return {"success": False, "error": "Title required"}
                
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    issue = repo.create_issue(
                        title=title,
                        body=body,
                        labels=labels
                    )
                    
                    return {
                        "success": True,
                        "object_type": "issue",
                        "issue": {
                            "number": issue.number,
                            "title": issue.title,
                            "state": issue.state,
                            "author": issue.user.login,
                            "html_url": issue.html_url,
                            "created_at": issue.created_at.isoformat(),
                            "labels": [label.name for label in issue.labels]
                        }
                    }
                
                return {"success": False, "error": "GitHub client not available"}
            
            else:
                return {"success": False, "error": f"Unknown issue action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Issue operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_workflow_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow operations"""
        try:
            # This would handle CI/CD workflow operations
            # For now, return basic workflow info
            return {
                "success": True,
                "object_type": "workflow",
                "message": "Workflow operations not yet implemented",
                "available_templates": list(self.workflow_templates.keys())
            }
            
        except Exception as e:
            logger.error(f"❌ Workflow operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_branch_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle branch operations"""
        try:
            action = task.get("action", "list")
            repository = task.get("repository", "")
            
            if not repository:
                return {"success": False, "error": "Repository required"}
            
            if action == "list":
                branches = []
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    for branch in repo.get_branches():
                        branches.append({
                            "name": branch.name,
                            "commit": branch.commit.sha,
                            "protected": branch.protected
                        })
                
                return {
                    "success": True,
                    "object_type": "branch_list",
                    "branches": branches,
                    "count": len(branches)
                }
            
            else:
                return {"success": False, "error": f"Unknown branch action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ Branch operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_file_operation(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file operations"""
        try:
            action = task.get("action", "read")
            repository = task.get("repository", "")
            file_path = task.get("file_path", "")
            
            if not all([repository, file_path]):
                return {"success": False, "error": "Repository and file path required"}
            
            if action == "read":
                if self.github_client:
                    repo = self.github_client.get_repo(repository)
                    file_content = repo.get_contents(file_path)
                    
                    return {
                        "success": True,
                        "object_type": "file",
                        "file": {
                            "path": file_content.path,
                            "name": file_content.name,
                            "size": file_content.size,
                            "content": file_content.decoded_content.decode('utf-8'),
                            "sha": file_content.sha,
                            "html_url": file_content.html_url
                        }
                    }
                
                return {"success": False, "error": "GitHub client not available"}
            
            else:
                return {"success": False, "error": f"Unknown file action: {action}"}
                
        except Exception as e:
            logger.error(f"❌ File operation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_project_context(self, session_id: str) -> Dict[str, Any]:
        """Get project context for GitHub operations"""
        try:
            # Get recent GitHub operations
            github_items = self.memory_manager.search_memory(
                query="github_integrator",
                memory_type=MemoryType.PROJECT,
                use_vector=True,
                limit=5
            )
            
            context = {
                "github_operations": [],
                "repositories": [],
                "workflow_history": []
            }
            
            # Extract GitHub operations
            for item in github_items:
                if "repository" in item.metadata:
                    context["github_operations"].append({
                        "operation": item.metadata.get("operation", "unknown"),
                        "repository": item.metadata.get("repository", "unknown"),
                        "success": item.metadata.get("success", False),
                        "created_at": item.created_at.isoformat()
                    })
                    
                    if item.metadata["repository"] not in context["repositories"]:
                        context["repositories"].append(item.metadata["repository"])
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Failed to get project context: {e}")
            return {}
    
    async def get_agent_stats(self) -> Dict[str, Any]:
        """Get GitHub integrator agent statistics"""
        return {
            **self.stats,
            "github_operations": list(self.github_operations.keys()),
            "workflow_templates": list(self.workflow_templates.keys()),
            "github_client_available": bool(self.github_client),
            "operations_completed": len(self.memory_manager.search_memory(
                query="github_integrator",
                memory_type=MemoryType.PROJECT,
                limit=1000
            )),
            "github_capabilities": [
                "repository_management",
                "pull_request_automation",
                "issue_tracking",
                "workflow_automation",
                "branch_management",
                "file_operations",
                "api_integration"
            ]
        }


def create_github_integrator_agent(config: Dict[str, Any]) -> GitHubIntegratorAgent:
    """Factory function to create GitHub integrator agent"""
    return GitHubIntegratorAgent(config)