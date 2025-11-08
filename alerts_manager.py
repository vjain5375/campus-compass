"""
Alerts Manager
Handles personalized alerts and reminders based on academic calendar
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import json


class AlertsManager:
    """Manages personalized alerts and reminders"""
    
    def __init__(self, alerts_file: str = "alerts.json"):
        """
        Initialize Alerts Manager
        
        Args:
            alerts_file: Path to JSON file storing alerts
        """
        self.alerts_file = Path(alerts_file)
        self.alerts = self._load_alerts()
    
    def _load_alerts(self) -> Dict:
        """Load alerts from JSON file"""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {"users": {}, "deadlines": []}
        return {"users": {}, "deadlines": []}
    
    def _save_alerts(self):
        """Save alerts to JSON file"""
        try:
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.alerts, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving alerts: {e}")
    
    def extract_deadlines_from_text(self, text: str, source: str = "Unknown") -> List[Dict]:
        """
        Extract deadlines and important dates from document text
        
        Args:
            text: Document text to parse
            source: Source document name
            
        Returns:
            List of deadline dictionaries
        """
        deadlines = []
        
        # Patterns to match dates and deadlines
        date_patterns = [
            # "Deadline: January 15, 2025"
            r'(?:deadline|due date|last date|closing date|registration|submission)[\s:]+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            # "By December 31, 2024"
            r'(?:by|before|until|till)[\s]+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            # "On March 1st, 2025"
            r'(?:on|starting|from)[\s]+([A-Z][a-z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})',
            # "DD/MM/YYYY" or "MM/DD/YYYY"
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            # "YYYY-MM-DD"
            r'(\d{4}-\d{2}-\d{2})',
        ]
        
        # Context keywords
        context_keywords = [
            'registration', 'fee payment', 'course drop', 'add course',
            'exam', 'assignment', 'project submission', 'thesis',
            'scholarship', 'application', 'admission', 'enrollment'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1) if match.groups() else match.group(0)
                
                # Try to parse the date
                parsed_date = self._parse_date(date_str)
                if parsed_date:
                    # Get context around the match
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end]
                    
                    # Extract event description
                    event = self._extract_event_description(context, date_str)
                    
                    deadline = {
                        'date': parsed_date.isoformat(),
                        'event': event,
                        'source': source,
                        'context': context.strip()
                    }
                    
                    # Avoid duplicates
                    if not any(d.get('date') == deadline['date'] and 
                              d.get('event') == deadline['event'] 
                              for d in deadlines):
                        deadlines.append(deadline)
        
        return deadlines
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        date_str = date_str.strip()
        
        # Try different date formats
        formats = [
            '%B %d, %Y',      # January 15, 2025
            '%B %d %Y',       # January 15 2025
            '%b %d, %Y',       # Jan 15, 2025
            '%b %d %Y',       # Jan 15 2025
            '%d/%m/%Y',       # 15/01/2025
            '%m/%d/%Y',       # 01/15/2025
            '%Y-%m-%d',       # 2025-01-15
            '%d-%m-%Y',       # 15-01-2025
            '%m-%d-%Y',       # 01-15-2025
        ]
        
        # Remove ordinal suffixes
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _extract_event_description(self, context: str, date_str: str) -> str:
        """Extract event description from context"""
        # Look for keywords before the date
        keywords = [
            'registration', 'fee payment', 'course drop', 'add course',
            'exam', 'assignment', 'project', 'thesis', 'scholarship',
            'application', 'admission', 'enrollment', 'deadline',
            'submission', 'due date'
        ]
        
        context_lower = context.lower()
        for keyword in keywords:
            if keyword in context_lower:
                # Get sentence or phrase containing the keyword
                sentences = re.split(r'[.!?]\s+', context)
                for sentence in sentences:
                    if keyword in sentence.lower() and date_str in sentence:
                        # Clean up the sentence
                        event = sentence.strip()
                        if len(event) > 150:
                            event = event[:150] + "..."
                        return event
        
        # Default: return a short context snippet
        return context[:100].strip() + "..." if len(context) > 100 else context.strip()
    
    def add_deadlines_from_documents(self, documents: List[Dict]):
        """
        Extract and add deadlines from processed documents
        
        Args:
            documents: List of document chunks with metadata
        """
        all_deadlines = []
        
        for doc in documents:
            text = doc.get('text', '')
            source = doc.get('metadata', {}).get('source', 'Unknown')
            
            deadlines = self.extract_deadlines_from_text(text, source)
            all_deadlines.extend(deadlines)
        
        # Merge with existing deadlines
        existing_dates = {d.get('date'): d for d in self.alerts.get('deadlines', [])}
        for deadline in all_deadlines:
            key = deadline['date']
            if key not in existing_dates:
                existing_dates[key] = deadline
        
        self.alerts['deadlines'] = list(existing_dates.values())
        self._save_alerts()
    
    def get_upcoming_deadlines(self, days_ahead: int = 30, user_id: str = "default") -> List[Dict]:
        """
        Get upcoming deadlines for a user
        
        Args:
            days_ahead: Number of days to look ahead
            user_id: User identifier
            
        Returns:
            List of upcoming deadline dictionaries
        """
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        upcoming = []
        for deadline in self.alerts.get('deadlines', []):
            try:
                deadline_date = datetime.fromisoformat(deadline['date']).date()
                if today <= deadline_date <= end_date:
                    # Check if user has opted in for this type of alert
                    user_prefs = self.alerts.get('users', {}).get(user_id, {})
                    if user_prefs.get('enabled', True):  # Default to enabled
                        days_until = (deadline_date - today).days
                        deadline_copy = deadline.copy()
                        deadline_copy['days_until'] = days_until
                        upcoming.append(deadline_copy)
            except Exception:
                continue
        
        # Sort by date
        upcoming.sort(key=lambda x: x.get('date', ''))
        return upcoming
    
    def opt_in_user(self, user_id: str, enabled: bool = True):
        """Opt in/out a user for alerts"""
        if 'users' not in self.alerts:
            self.alerts['users'] = {}
        
        if user_id not in self.alerts['users']:
            self.alerts['users'][user_id] = {}
        
        self.alerts['users'][user_id]['enabled'] = enabled
        self.alerts['users'][user_id]['updated'] = datetime.now().isoformat()
        self._save_alerts()
    
    def is_user_opted_in(self, user_id: str = "default") -> bool:
        """Check if user has opted in for alerts"""
        user_prefs = self.alerts.get('users', {}).get(user_id, {})
        return user_prefs.get('enabled', True)  # Default to enabled
    
    def get_all_deadlines(self) -> List[Dict]:
        """Get all stored deadlines"""
        return self.alerts.get('deadlines', [])
    
    def clear_deadlines(self):
        """Clear all deadlines"""
        self.alerts['deadlines'] = []
        self._save_alerts()

