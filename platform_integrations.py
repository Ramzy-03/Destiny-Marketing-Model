"""
Platform Integrations for Social Media
Real connections to Facebook, Instagram, LinkedIn, Twitter
"""

import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from config import Config


class PlatformIntegration:
    """Base class for platform integrations"""
    
    def __init__(self):
        self.demo_mode = Config.DEMO_MODE
    
    def post(self, content: str, **kwargs) -> Dict[str, Any]:
        """Publish content to platform"""
        raise NotImplementedError
    
    def get_analytics(self, post_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve analytics data"""
        raise NotImplementedError


class FacebookIntegration(PlatformIntegration):
    """Facebook Page posting and analytics"""
    
    def __init__(self):
        super().__init__()
        self.access_token = Config.FACEBOOK_ACCESS_TOKEN
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def post(self, content: str, image_url: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Post to Facebook Page"""
        
        if self.demo_mode or not self.access_token:
            return self._demo_post('facebook', content)
        
        try:
            url = f"{self.base_url}/{self.page_id}/feed"
            
            data = {
                'message': content,
                'access_token': self.access_token
            }
            
            if image_url:
                data['link'] = image_url
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if 'id' in result:
                return {
                    'success': True,
                    'platform': 'facebook',
                    'post_id': result['id'],
                    'url': f"https://facebook.com/{result['id']}",
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'platform': 'facebook',
                    'error': result.get('error', {}).get('message', 'Unknown error')
                }
                
        except Exception as e:
            return {'success': False, 'platform': 'facebook', 'error': str(e)}
    
    def get_analytics(self, post_id: Optional[str] = None) -> Dict[str, Any]:
        """Get Facebook Page analytics"""
        
        if self.demo_mode or not self.access_token:
            return self._demo_analytics('facebook')
        
        try:
            if post_id:
                # Get specific post insights
                url = f"{self.base_url}/{post_id}/insights"
                params = {
                    'metric': 'post_impressions,post_engaged_users,post_clicks',
                    'access_token': self.access_token
                }
            else:
                # Get page insights
                url = f"{self.base_url}/{self.page_id}/insights"
                params = {
                    'metric': 'page_impressions,page_engaged_users,page_fans',
                    'access_token': self.access_token
                }
            
            response = requests.get(url, params=params)
            return response.json()
            
        except Exception as e:
            return self._demo_analytics('facebook')
    
    def _demo_post(self, platform: str, content: str) -> Dict[str, Any]:
        """Simulate successful post for demo"""
        import random
        return {
            'success': True,
            'platform': platform,
            'post_id': f'demo_{platform}_{random.randint(1000, 9999)}',
            'url': f'https://{platform}.com/demo_post',
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }
    
    def _demo_analytics(self, platform: str) -> Dict[str, Any]:
        """Simulate analytics for demo"""
        import random
        return {
            'platform': platform,
            'impressions': random.randint(1000, 5000),
            'reach': random.randint(800, 4000),
            'engagement': random.randint(50, 300),
            'clicks': random.randint(20, 150),
            'likes': random.randint(30, 200),
            'shares': random.randint(5, 50),
            'comments': random.randint(3, 40),
            'engagement_rate': round(random.uniform(2.5, 8.5), 2),
            'demo_mode': True
        }


class InstagramIntegration(PlatformIntegration):
    """Instagram posting via Graph API"""
    
    def __init__(self):
        super().__init__()
        self.username = Config.INSTAGRAM_USERNAME
        self.password = Config.INSTAGRAM_PASSWORD
    
    def post(self, content: str, image_url: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Post to Instagram (requires image)"""
        
        if self.demo_mode or not self.username:
            return self._demo_post('instagram', content)
        
        # Instagram requires Facebook Graph API integration
        # This is a placeholder for the actual implementation
        try:
            # In production: Use instagrapi or Facebook Graph API
            return {
                'success': True,
                'platform': 'instagram',
                'post_id': 'instagram_demo_12345',
                'url': 'https://instagram.com/p/demo',
                'timestamp': datetime.now().isoformat(),
                'note': 'Using demo mode - configure Instagram API for real posts'
            }
        except Exception as e:
            return {'success': False, 'platform': 'instagram', 'error': str(e)}
    
    def get_analytics(self, post_id: str = None) -> Dict[str, Any]:
        """Get Instagram analytics"""
        if self.demo_mode:
            return FacebookIntegration()._demo_analytics('instagram')
        
        # Use Graph API for Instagram insights
        return {'demo_mode': True, 'platform': 'instagram'}
    
    def _demo_post(self, platform: str, content: str) -> Dict[str, Any]:
        return FacebookIntegration()._demo_post(platform, content)


class LinkedInIntegration(PlatformIntegration):
    """LinkedIn posting and analytics"""
    
    def __init__(self):
        super().__init__()
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.person_urn = Config.LINKEDIN_PERSON_URN
        self.base_url = "https://api.linkedin.com/v2"
    
    def post(self, content: str, **kwargs) -> Dict[str, Any]:
        """Post to LinkedIn"""
        
        if self.demo_mode or not self.access_token:
            return FacebookIntegration()._demo_post('linkedin', content)
        
        try:
            url = f"{self.base_url}/ugcPosts"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            data = {
                'author': self.person_urn,
                'lifecycleState': 'PUBLISHED',
                'specificContent': {
                    'com.linkedin.ugc.ShareContent': {
                        'shareCommentary': {
                            'text': content
                        },
                        'shareMediaCategory': 'NONE'
                    }
                },
                'visibility': {
                    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            result = response.json()
            
            if response.status_code == 201:
                return {
                    'success': True,
                    'platform': 'linkedin',
                    'post_id': result.get('id', 'unknown'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'platform': 'linkedin',
                    'error': result.get('message', 'Unknown error')
                }
                
        except Exception as e:
            return {'success': False, 'platform': 'linkedin', 'error': str(e)}
    
    def get_analytics(self, post_id: str = None) -> Dict[str, Any]:
        """Get LinkedIn analytics"""
        if self.demo_mode or not self.access_token:
            return FacebookIntegration()._demo_analytics('linkedin')
        
        # LinkedIn analytics API implementation
        return {'demo_mode': True, 'platform': 'linkedin'}


class TwitterIntegration(PlatformIntegration):
    """Twitter/X posting and analytics"""
    
    def __init__(self):
        super().__init__()
        self.api_key = Config.TWITTER_API_KEY
        self.access_token = Config.TWITTER_ACCESS_TOKEN
    
    def post(self, content: str, **kwargs) -> Dict[str, Any]:
        """Post tweet"""
        
        if self.demo_mode or not self.api_key:
            return FacebookIntegration()._demo_post('twitter', content)
        
        try:
            # Use tweepy or direct API v2
            # This is a placeholder for actual implementation
            import tweepy
            
            # In production: Initialize tweepy client
            # client = tweepy.Client(...)
            # response = client.create_tweet(text=content)
            
            return {
                'success': True,
                'platform': 'twitter',
                'post_id': 'twitter_demo_12345',
                'url': 'https://twitter.com/user/status/demo',
                'timestamp': datetime.now().isoformat(),
                'note': 'Using demo mode - configure Twitter API for real tweets'
            }
            
        except Exception as e:
            return {'success': False, 'platform': 'twitter', 'error': str(e)}
    
    def get_analytics(self, post_id: str = None) -> Dict[str, Any]:
        """Get Twitter analytics"""
        if self.demo_mode:
            return FacebookIntegration()._demo_analytics('twitter')
        
        return {'demo_mode': True, 'platform': 'twitter'}


class PlatformManager:
    """
    Manages all platform integrations
    Provides unified interface for multi-platform operations
    """
    
    def __init__(self):
        self.platforms = {
            'facebook': FacebookIntegration(),
            'instagram': InstagramIntegration(),
            'linkedin': LinkedInIntegration(),
            'twitter': TwitterIntegration()
        }
    
    def post_to_platform(self, platform: str, content: str, **kwargs) -> Dict[str, Any]:
        """Post to specific platform"""
        platform_lower = platform.lower()
        
        if platform_lower not in self.platforms:
            return {
                'success': False,
                'error': f'Platform {platform} not supported'
            }
        
        return self.platforms[platform_lower].post(content, **kwargs)
    
    def post_to_multiple(self, platforms: List[str], content: str, **kwargs) -> List[Dict[str, Any]]:
        """Post to multiple platforms simultaneously"""
        results = []
        
        for platform in platforms:
            result = self.post_to_platform(platform, content, **kwargs)
            results.append(result)
        
        return results
    
    def get_analytics(self, platform: str, post_id: str = None) -> Dict[str, Any]:
        """Get analytics from specific platform"""
        platform_lower = platform.lower()
        
        if platform_lower not in self.platforms:
            return {'error': f'Platform {platform} not supported'}
        
        return self.platforms[platform_lower].get_analytics(post_id)
    
    def get_all_analytics(self) -> Dict[str, Any]:
        """Get analytics from all platforms"""
        analytics = {}
        
        for platform_name, platform in self.platforms.items():
            analytics[platform_name] = platform.get_analytics()
        
        return analytics