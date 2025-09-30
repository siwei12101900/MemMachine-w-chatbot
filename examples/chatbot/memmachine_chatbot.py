"""
MemMachine Chatbot Client
A simple chatbot client for interacting with MemMachine's REST API.
"""

import os
import requests
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple


class MemMachineChatbot:
    """
    A chatbot client that interfaces with MemMachine's REST API for memory storage and retrieval.
    
    Args:
        base_url: The base URL of the MemMachine API (default: http://localhost:8080)
        user_id: The user ID for this chatbot session
        session_id: Optional session ID (auto-generated if not provided)
        agent_id: The agent ID (default: "chatbot_assistant")
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        user_id: str = "user",
        session_id: Optional[str] = None,
        agent_id: str = "chatbot_assistant"
    ):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.agent_id = agent_id
        self.session_id = session_id or f"session_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Verify connection
        self._check_health()
    
    def _check_health(self) -> bool:
        """Check if the MemMachine API is healthy."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.logger.info("✓ Successfully connected to MemMachine API")
                return True
            else:
                self.logger.warning(f"MemMachine API returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to connect to MemMachine API at {self.base_url}: {e}")
            return False
    
    def _create_session_data(self) -> Dict[str, Any]:
        """Create session data structure."""
        return {
            "user_id": [self.user_id],
            "session_id": self.session_id,
            "agent_id": [self.agent_id],
            "group_id": None
        }
    
    def add_memory(
        self,
        content: str,
        producer: str,
        produced_for: str,
        episode_type: str = "dialog",
        metadata: Optional[Dict[str, Any]] = None,
        verbose: bool = False
    ) -> Tuple[bool, float]:
        """
        Add a memory episode to MemMachine.
        
        Args:
            content: The content to store
            producer: Who produced this content (e.g., "user", "assistant")
            produced_for: Who this content was produced for
            episode_type: Type of episode (default: "dialog")
            metadata: Optional metadata dictionary
            verbose: If True, log detailed HTTP request information
            
        Returns:
            Tuple of (success: bool, elapsed_time: float in seconds)
        """
        start_time = time.time()
        
        try:
            episode_data = {
                "session": self._create_session_data(),
                "producer": producer,
                "produced_for": produced_for,
                "episode_content": content,
                "episode_type": episode_type,
                "metadata": metadata or {
                    "timestamp": datetime.now().isoformat(),
                    "speaker": producer
                }
            }
            
            # Use episodic-only endpoint to avoid profile memory bugs
            endpoint = f"{self.base_url}/v1/memories/episodic"
            
            if verbose:
                self.logger.info(f"HTTP POST {endpoint}")
                self.logger.info(f"  Payload: producer={producer}, content={content[:50]}...")
            
            response = requests.post(
                endpoint,
                json=episode_data,
                timeout=30
            )
            
            elapsed = time.time() - start_time
            
            if verbose:
                self.logger.info(f"  Response: {response.status_code} {response.reason}")
                self.logger.info(f"  Time: {elapsed:.3f}s")
            
            if response.status_code == 200:
                self.logger.debug(f"Memory added successfully: {content[:50]}...")
                return True, elapsed
            else:
                self.logger.error(f"Failed to add memory: {response.status_code} - {response.text}")
                return False, elapsed
                
        except requests.exceptions.RequestException as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Error adding memory: {e}")
            return False, elapsed
    
    def search_memory(
        self,
        query: str,
        limit: int = 5,
        filter_params: Optional[Dict[str, Any]] = None,
        verbose: bool = False
    ) -> Tuple[Dict[str, Any], float]:
        """
        Search memories in MemMachine.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            filter_params: Optional filter parameters
            verbose: If True, log detailed HTTP request information
            
        Returns:
            Tuple of (results: Dict, elapsed_time: float in seconds)
        """
        start_time = time.time()
        
        try:
            search_data = {
                "session": self._create_session_data(),
                "query": query,
                "limit": limit,
                "filter": filter_params
            }
            
            # Use episodic-only search endpoint to avoid profile memory bugs
            endpoint = f"{self.base_url}/v1/memories/episodic/search"
            
            if verbose:
                self.logger.info(f"HTTP POST {endpoint}")
                self.logger.info(f"  Query: '{query}', Limit: {limit}")
            
            response = requests.post(
                endpoint,
                json=search_data,
                timeout=30
            )
            
            elapsed = time.time() - start_time
            
            if verbose:
                self.logger.info(f"  Response: {response.status_code} {response.reason}")
                self.logger.info(f"  Time: {elapsed:.3f}s")
            
            if response.status_code == 200:
                result = response.json()
                if verbose:
                    episodic_count = len(result.get("content", {}).get("episodic_memory", []))
                    self.logger.info(f"  Found: {episodic_count} memories")
                self.logger.debug(f"Memory search successful for query: {query}")
                return result.get("content", {}), elapsed
            else:
                self.logger.error(f"Failed to search memory: {response.status_code} - {response.text}")
                return {"episodic_memory": [], "profile_memory": []}, elapsed
                
        except requests.exceptions.RequestException as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Error searching memory: {e}")
            return {"episodic_memory": [], "profile_memory": []}, elapsed
    
    def recall(self, query: str) -> str:
        """
        Recall memories and format them as a readable string.
        
        Args:
            query: What to recall
            
        Returns:
            Formatted string of recalled memories
        """
        memories, _ = self.search_memory(query)
        
        episodic = memories.get("episodic_memory", [])
        profile = memories.get("profile_memory", [])
        
        result_parts = []
        
        if profile:
            result_parts.append("=== Profile Information ===")
            for item in profile:
                if isinstance(item, dict):
                    result_parts.append(f"- {item}")
                else:
                    result_parts.append(f"- {item}")
        
        if episodic:
            result_parts.append("\n=== Conversation History ===")
            for item in episodic:
                if isinstance(item, dict):
                    content = item.get('content', item.get('episode_content', str(item)))
                    producer = item.get('producer', 'unknown')
                    result_parts.append(f"{producer}: {content}")
                else:
                    result_parts.append(f"- {item}")
        
        if not result_parts:
            return "No memories found."
        
        return "\n".join(result_parts)
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """
        Get all sessions from MemMachine.
        
        Returns:
            List of session dictionaries
        """
        try:
            response = requests.get(f"{self.base_url}/v1/sessions", timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("sessions", [])
            else:
                self.logger.error(f"Failed to get sessions: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []
    
    def delete_session(self) -> bool:
        """
        Delete the current session data from MemMachine.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            delete_data = {
                "session": self._create_session_data()
            }
            
            response = requests.delete(
                f"{self.base_url}/v1/memories",
                json=delete_data,
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info(f"Session {self.session_id} deleted successfully")
                return True
            else:
                self.logger.error(f"Failed to delete session: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error deleting session: {e}")
            return False
    
    def store_user_message(self, message: str, verbose: bool = False) -> Tuple[bool, float]:
        """
        Store a user message in memory.
        
        Args:
            message: The user's message
            verbose: If True, log detailed HTTP request information
            
        Returns:
            Tuple of (success: bool, elapsed_time: float)
        """
        return self.add_memory(
            content=message,
            producer=self.user_id,
            produced_for=self.agent_id,
            episode_type="dialog",
            metadata={
                "timestamp": datetime.now().isoformat(),
                "speaker": "user",
                "type": "user_message"
            },
            verbose=verbose
        )
    
    def store_assistant_message(self, message: str, verbose: bool = False) -> Tuple[bool, float]:
        """
        Store an assistant message in memory.
        
        Args:
            message: The assistant's message
            verbose: If True, log detailed HTTP request information
            
        Returns:
            Tuple of (success: bool, elapsed_time: float)
        """
        return self.add_memory(
            content=message,
            producer=self.agent_id,
            produced_for=self.user_id,
            episode_type="dialog",
            metadata={
                "timestamp": datetime.now().isoformat(),
                "speaker": "assistant",
                "type": "assistant_message"
            },
            verbose=verbose
        )

