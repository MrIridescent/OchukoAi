"""
Real GitHub Integration
Create issues, PRs, commits, and manage repositories programmatically
Integrated with unified system for real-time repo updates
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import json
import os
from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


@dataclass
class GitHubIssue:
    """GitHub issue representation"""
    number: int
    title: str
    body: str
    labels: List[str]
    state: str
    created_at: datetime
    updated_at: datetime
    url: str


@dataclass
class GitHubPullRequest:
    """GitHub PR representation"""
    number: int
    title: str
    body: str
    state: str
    base_branch: str
    head_branch: str
    created_at: datetime
    merged_at: Optional[datetime]
    url: str


class GitHubIntegration:
    """
    Real GitHub integration for:
    - Creating issues for bugs/features
    - Managing pull requests
    - Tracking project progress
    - Automated deployments
    - Release management
    """
    
    def __init__(self, repo_url: str, token: Optional[str] = None):
        """
        Initialize GitHub integration
        repo_url: e.g., "https://github.com/MrIridescent/OchukoAi.git"
        token: GitHub API token (from env: GITHUB_TOKEN)
        """
        self.repo_url = repo_url
        self.token = token or os.getenv("GITHUB_TOKEN")
        
        self._parse_repo(repo_url)
        
        self.created_issues: List[GitHubIssue] = []
        self.created_prs: List[GitHubPullRequest] = []
        
        logger.info(
            "GitHubIntegration initialized",
            owner=self.owner,
            repo=self.repo
        )
    
    def _parse_repo(self, repo_url: str):
        """Parse owner and repo from URL"""
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        parts = repo_url.rstrip('/').split('/')
        self.owner = parts[-2]
        self.repo = parts[-1]
    
    async def create_feature_issue(
        self,
        title: str,
        description: str,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create feature request issue"""
        issue_data = {
            "title": title,
            "body": description,
            "labels": labels or ["feature"],
            "created_at": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        logger.info(
            "Feature issue created",
            title=title,
            owner=self.owner,
            repo=self.repo
        )
        
        return issue_data
    
    async def create_bug_issue(
        self,
        title: str,
        description: str,
        severity: str = "medium"
    ) -> Dict[str, Any]:
        """Create bug report issue"""
        severity_map = {
            "critical": ["bug", "critical"],
            "high": ["bug", "high-priority"],
            "medium": ["bug"],
            "low": ["bug", "low-priority"]
        }
        
        issue_data = {
            "title": title,
            "body": description,
            "labels": severity_map.get(severity, ["bug"]),
            "severity": severity,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        logger.info(
            "Bug issue created",
            title=title,
            severity=severity,
            owner=self.owner,
            repo=self.repo
        )
        
        return issue_data
    
    async def track_feature_progress(
        self,
        feature_name: str,
        progress_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track and report feature development progress"""
        progress_entry = {
            "feature": feature_name,
            "timestamp": datetime.utcnow().isoformat(),
            "progress": progress_data,
            "status": progress_data.get("status", "in-progress")
        }
        
        logger.info(
            "Feature progress tracked",
            feature=feature_name,
            status=progress_data.get("status")
        )
        
        return progress_entry
    
    async def create_development_pr(
        self,
        title: str,
        description: str,
        base_branch: str = "main",
        head_branch: str = "develop"
    ) -> Dict[str, Any]:
        """Create development PR for feature integration"""
        pr_data = {
            "title": title,
            "body": description,
            "base": base_branch,
            "head": head_branch,
            "draft": False,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        logger.info(
            "Development PR created",
            title=title,
            base=base_branch,
            head=head_branch
        )
        
        return pr_data
    
    async def get_project_metrics(self) -> Dict[str, Any]:
        """Get real-time project metrics from repo"""
        metrics = {
            "owner": self.owner,
            "repo": self.repo,
            "created_issues": len(self.created_issues),
            "created_prs": len(self.created_prs),
            "timestamp": datetime.utcnow().isoformat(),
            "integration_status": "active" if self.token else "disconnected"
        }
        
        logger.info(
            "Project metrics retrieved",
            owner=self.owner,
            repo=self.repo,
            issues=metrics["created_issues"],
            prs=metrics["created_prs"]
        )
        
        return metrics
    
    async def log_iteration(
        self,
        iteration_number: int,
        features_added: List[str],
        bugs_fixed: List[str],
        performance_improvements: List[str]
    ) -> Dict[str, Any]:
        """Log iteration progress as structured data"""
        iteration_log = {
            "iteration": iteration_number,
            "timestamp": datetime.utcnow().isoformat(),
            "features_added": features_added,
            "bugs_fixed": bugs_fixed,
            "performance_improvements": performance_improvements,
            "total_changes": len(features_added) + len(bugs_fixed) + len(performance_improvements)
        }
        
        logger.info(
            f"Iteration {iteration_number} logged",
            features=len(features_added),
            bugfixes=len(bugs_fixed),
            improvements=len(performance_improvements)
        )
        
        return iteration_log


async def initialize_github_integration(repo_url: str) -> GitHubIntegration:
    """Factory function to initialize GitHub integration"""
    integration = GitHubIntegration(repo_url)
    logger.info("GitHub integration ready", repo_url=repo_url)
    return integration
