"""
Configuration Management for Destiny
Handles API keys and platform credentials securely
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Centralized configuration for all platform integrations
    """
    
    # Claude API for content generation
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', 'demo_key')
    
    # Social Media Platform APIs
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID', '')
    
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')
    
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    LINKEDIN_PERSON_URN = os.getenv('LINKEDIN_PERSON_URN', '')
    
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', '')
    
    # Agent Settings - FIXED: Make demo mode default to True
    ENABLE_REAL_API_CALLS = os.getenv('ENABLE_REAL_API_CALLS', 'false').lower() == 'true'
    DEMO_MODE = os.getenv('DEMO_MODE', 'true').lower() == 'true'
    
    @classmethod
    def validate_platform(cls, platform: str) -> bool:
        """Check if platform credentials are configured"""
        if cls.DEMO_MODE:
            return False  # Always return False in demo mode
            
        platform_checks = {
            'facebook': bool(cls.FACEBOOK_ACCESS_TOKEN and cls.FACEBOOK_PAGE_ID),
            'instagram': bool(cls.INSTAGRAM_USERNAME and cls.INSTAGRAM_PASSWORD),
            'linkedin': bool(cls.LINKEDIN_ACCESS_TOKEN and cls.LINKEDIN_PERSON_URN),
            'twitter': bool(cls.TWITTER_API_KEY and cls.TWITTER_ACCESS_TOKEN),
            'claude': bool(cls.CLAUDE_API_KEY and cls.CLAUDE_API_KEY != 'demo_key')
        }
        return platform_checks.get(platform.lower(), False)
    
    @classmethod
    def get_configured_platforms(cls) -> Dict[str, bool]:
        """Get status of all platform configurations"""
        return {
            'Claude API': cls.validate_platform('claude'),
            'Facebook': cls.validate_platform('facebook'),
            'Instagram': cls.validate_platform('instagram'),
            'LinkedIn': cls.validate_platform('linkedin'),
            'Twitter': cls.validate_platform('twitter')
        }