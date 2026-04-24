# memory.py
"""
Memory system for Destiny agent
Stores and retrieves past experiences for learning
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class Memory:
    """Memory system for agent learning"""
    
    def __init__(self, memory_file: str = 'destiny_memory.json'):
        self.memory_file = memory_file
        self.sessions = self._load_memory()
    
    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load memory from file"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_memory(self):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def store_session(self, goal: str, plan: List[str], 
                     actions: List[Dict], results: List[str], 
                     evaluation: Dict[str, Any]):
        """Store a session in memory"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'goal': goal,
            'plan': plan,
            'actions': actions,
            'results': results,
            'evaluation': evaluation
        }
        self.sessions.append(session)
        self.save_memory()
    
    def get_relevant_experiences(self, goal: str) -> List[Dict]:
        """Retrieve relevant past experiences"""
        if not self.sessions:
            return []
        
        goal_lower = goal.lower()
        goal_words = set(re.findall(r'\w+', goal_lower))
        
        relevant = []
        for session in self.sessions[-20:]:  # Check last 20 sessions
            session_goal = session['goal'].lower()
            session_words = set(re.findall(r'\w+', session_goal))
            
            # Calculate word overlap
            overlap = goal_words.intersection(session_words)
            if overlap:
                # Calculate relevance score
                relevance_score = len(overlap) / len(goal_words)
                if relevance_score > 0.2:  # At least 20% overlap
                    relevant.append(session)
        
        # Return most relevant first (newest first if tied)
        relevant.sort(
            key=lambda x: (
                len(set(re.findall(r'\w+', x['goal'].lower()))
                     .intersection(goal_words)) / len(goal_words),
                x['timestamp']
            ),
            reverse=True
        )
        
        return relevant[:5]  # Return top 5 most relevant
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all stored sessions"""
        return self.sessions.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total_sessions = len(self.sessions)
        total_actions = sum(len(session.get('actions', [])) for session in self.sessions)
        
        if total_sessions > 0:
            avg_success = sum(
                session.get('evaluation', {}).get('success_score', 0) 
                for session in self.sessions
            ) / total_sessions
        else:
            avg_success = 0
        
        return {
            'total_sessions': total_sessions,
            'total_actions': total_actions,
            'avg_success_rate': avg_success,
            'memory_file': self.memory_file,
            'last_session': self.sessions[-1]['timestamp'] if self.sessions else None
        }
    
    def clear_memory(self):
        """Clear all memory"""
        self.sessions = []
        self.save_memory()
    
    def get_session_by_id(self, index: int) -> Dict[str, Any]:
        """Get session by index"""
        if 0 <= index < len(self.sessions):
            return self.sessions[index]
        return {}
    
    def get_sessions_by_date(self, start_date: str, end_date: Optional[str] = None) -> List[Dict]:
        """Get sessions within date range"""
        if end_date is None:
            end_date = datetime.now().isoformat()
        
        filtered = []
        for session in self.sessions:
            if start_date <= session['timestamp'] <= end_date:
                filtered.append(session)
        
        return filtered