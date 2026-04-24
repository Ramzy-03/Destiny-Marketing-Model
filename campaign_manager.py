"""
Campaign Manager - Orchestrates Multi-Channel Marketing Campaigns
Manages end-to-end campaign lifecycle
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
from content_generator import ContentGenerator
from platform_integrations import PlatformManager


class Campaign:
    """Represents a marketing campaign"""
    
    def __init__(self, campaign_id: str, name: str, goal: str, 
                 platforms: List[str], duration_days: int, budget: float):
        self.campaign_id = campaign_id
        self.name = name
        self.goal = goal
        self.platforms = platforms
        self.duration_days = duration_days
        self.budget = budget
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=duration_days)
        self.status = 'planned'
        self.posts = []
        self.analytics = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert campaign to dictionary"""
        return {
            'campaign_id': self.campaign_id,
            'name': self.name,
            'goal': self.goal,
            'platforms': self.platforms,
            'duration_days': self.duration_days,
            'budget': self.budget,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'posts_count': len(self.posts),
            'analytics': self.analytics
        }


class CampaignManager:
    """
    Manages marketing campaigns across platforms
    Handles content creation, scheduling, and performance tracking
    """
    
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.platform_mgr = PlatformManager()
        self.active_campaigns = {}
        self.campaign_history = []
    
    def create_campaign(self, name: str, goal: str, platforms: List[str],
                       duration_days: int = 30, budget: float = 5000) -> Campaign:
        """
        Create a new marketing campaign
        
        This is where the agent plans a comprehensive campaign
        """
        import random
        campaign_id = f"camp_{datetime.now().strftime('%Y%m%d')}_{random.randint(1000, 9999)}"
        
        campaign = Campaign(
            campaign_id=campaign_id,
            name=name,
            goal=goal,
            platforms=platforms,
            duration_days=duration_days,
            budget=budget
        )
        
        self.active_campaigns[campaign_id] = campaign
        
        print(f"[CAMPAIGN] Created campaign: {campaign_id}")
        return campaign
    
    def generate_campaign_content(self, campaign: Campaign, 
                                 content_pieces: int = 5) -> List[Dict[str, Any]]:
        """
        Generate content for entire campaign
        
        Agent autonomously creates content strategy
        """
        print(f"[CAMPAIGN] Generating {content_pieces} content pieces...")
        
        content_schedule = []
        
        # Determine content types based on campaign goal
        content_types = self._plan_content_types(campaign.goal)
        
        for i in range(content_pieces):
            # Select content type
            content_type = content_types[i % len(content_types)]
            
            # Generate for each platform
            for platform in campaign.platforms:
                content = self.content_gen.generate_content(
                    content_type=content_type,
                    params={
                        'topic': campaign.goal,
                        'platform': platform,
                        'tone': 'professional',
                        'target_audience': 'business professionals'
                    }
                )
                
                # Optimize for platform
                optimized = self.content_gen.optimize_for_platform(content, platform)
                
                # Add hashtags
                hashtags = self.content_gen.generate_hashtags(campaign.goal, platform)
                
                content_item = {
                    'content_id': f"{campaign.campaign_id}_content_{i}_{platform}",
                    'platform': platform,
                    'content_type': content_type,
                    'content': optimized,
                    'hashtags': hashtags,
                    'scheduled_date': (
                        campaign.start_date + timedelta(days=i * (campaign.duration_days // content_pieces))
                    ).isoformat(),
                    'status': 'draft'
                }
                
                content_schedule.append(content_item)
        
        campaign.posts = content_schedule
        return content_schedule
    
    def _plan_content_types(self, goal: str) -> List[str]:
        """
        Intelligent content type selection based on goal
        Agent reasoning for content strategy
        """
        goal_lower = goal.lower()
        
        if 'aware' in goal_lower or 'brand' in goal_lower:
            return ['social_post', 'blog_post', 'social_post', 'video_script', 'social_post']
        elif 'lead' in goal_lower:
            return ['email_campaign', 'social_post', 'blog_post', 'ad_copy', 'social_post']
        elif 'engage' in goal_lower:
            return ['social_post', 'social_post', 'video_script', 'social_post', 'social_post']
        elif 'sale' in goal_lower:
            return ['ad_copy', 'email_campaign', 'social_post', 'ad_copy', 'blog_post']
        else:
            return ['social_post', 'blog_post', 'social_post', 'email_campaign', 'social_post']
    
    def publish_content(self, campaign_id: str, content_id: str) -> Dict[str, Any]:
        """
        Publish specific content piece
        
        Agent executes the planned content
        """
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {'success': False, 'error': 'Campaign not found'}
        
        # Find content
        content_item = None
        for post in campaign.posts:
            if post['content_id'] == content_id:
                content_item = post
                break
        
        if not content_item:
            return {'success': False, 'error': 'Content not found'}
        
        # Publish to platform
        result = self.platform_mgr.post_to_platform(
            platform=content_item['platform'],
            content=content_item['content']
        )
        
        # Update content status
        content_item['status'] = 'published' if result['success'] else 'failed'
        content_item['publish_result'] = result
        
        return result
    
    def publish_campaign(self, campaign_id: str) -> List[Dict[str, Any]]:
        """
        Publish all campaign content
        
        Agent executes full campaign
        """
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return [{'success': False, 'error': 'Campaign not found'}]
        
        print(f"[CAMPAIGN] Publishing campaign: {campaign_id}")
        
        results = []
        for content_item in campaign.posts:
            result = self.publish_content(campaign_id, content_item['content_id'])
            results.append({
                'content_id': content_item['content_id'],
                'platform': content_item['platform'],
                'result': result
            })
        
        campaign.status = 'active'
        return results
    
    def track_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """
        Track campaign performance across all platforms
        
        Agent observes results
        """
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {'error': 'Campaign not found'}
        
        print(f"[CAMPAIGN] Tracking performance: {campaign_id}")
        
        # Aggregate analytics from all platforms
        total_analytics = {
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'posts_published': len([p for p in campaign.posts if p['status'] == 'published']),
            'platforms': campaign.platforms,
            'by_platform': {}
        }
        
        # Get analytics from each platform
        for platform in campaign.platforms:
            platform_analytics = self.platform_mgr.get_analytics(platform)
            total_analytics['by_platform'][platform] = platform_analytics
        
        # Calculate overall metrics
        total_analytics['overall'] = self._calculate_overall_metrics(
            total_analytics['by_platform']
        )
        
        campaign.analytics = total_analytics
        return total_analytics
    
    def _calculate_overall_metrics(self, platform_analytics: Dict) -> Dict[str, Any]:
        """Calculate aggregated metrics across platforms"""
        
        total_impressions = 0
        total_engagement = 0
        total_clicks = 0
        
        for platform, metrics in platform_analytics.items():
            if isinstance(metrics, dict):
                total_impressions += metrics.get('impressions', 0)
                total_engagement += metrics.get('engagement', 0)
                total_clicks += metrics.get('clicks', 0)
        
        return {
            'total_impressions': total_impressions,
            'total_engagement': total_engagement,
            'total_clicks': total_clicks,
            'avg_engagement_rate': round(
                (total_engagement / total_impressions * 100) if total_impressions > 0 else 0,
                2
            ),
            'click_through_rate': round(
                (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
                2
            )
        }
    
    def optimize_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """
        Analyze performance and suggest optimizations
        
        Agent learns and improves
        """
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {'error': 'Campaign not found'}
        
        analytics = campaign.analytics
        if not analytics:
            analytics = self.track_campaign_performance(campaign_id)
        
        optimizations = {
            'campaign_id': campaign_id,
            'current_performance': analytics.get('overall', {}),
            'recommendations': []
        }
        
        # Analyze performance by platform
        for platform, metrics in analytics.get('by_platform', {}).items():
            if isinstance(metrics, dict):
                engagement_rate = metrics.get('engagement_rate', 0)
                
                if engagement_rate < 3.0:
                    optimizations['recommendations'].append({
                        'platform': platform,
                        'issue': 'Low engagement rate',
                        'suggestion': f'Adjust posting times and content format for {platform}',
                        'action': 'increase_content_frequency'
                    })
                elif engagement_rate > 7.0:
                    optimizations['recommendations'].append({
                        'platform': platform,
                        'success': 'High engagement rate',
                        'suggestion': f'Allocate more budget to {platform}',
                        'action': 'scale_up_investment'
                    })
        
        # Overall recommendations
        overall = analytics.get('overall', {})
        if overall.get('total_clicks', 0) < 100:
            optimizations['recommendations'].append({
                'type': 'general',
                'issue': 'Low click-through rate',
                'suggestion': 'Strengthen call-to-action in content',
                'action': 'improve_cta'
            })
        
        return optimizations
    
    def get_campaign_report(self, campaign_id: str) -> Dict[str, Any]:
        """Generate comprehensive campaign report"""
        
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {'error': 'Campaign not found'}
        
        # Ensure we have latest analytics
        if not campaign.analytics:
            self.track_campaign_performance(campaign_id)
        
        # Get optimizations
        optimizations = self.optimize_campaign(campaign_id)
        
        report = {
            'campaign': campaign.to_dict(),
            'content_summary': {
                'total_pieces': len(campaign.posts),
                'by_platform': {},
                'by_type': {}
            },
            'performance': campaign.analytics,
            'optimizations': optimizations,
            'roi_estimate': self._calculate_roi(campaign),
            'generated_at': datetime.now().isoformat()
        }
        
        # Count content by platform and type
        for post in campaign.posts:
            platform = post['platform']
            content_type = post['content_type']
            
            report['content_summary']['by_platform'][platform] = \
                report['content_summary']['by_platform'].get(platform, 0) + 1
            
            report['content_summary']['by_type'][content_type] = \
                report['content_summary']['by_type'].get(content_type, 0) + 1
        
        return report
    
    def _calculate_roi(self, campaign: Campaign) -> Dict[str, Any]:
        """Calculate estimated ROI"""
        
        analytics = campaign.analytics.get('overall', {})
        clicks = analytics.get('total_clicks', 100)
        
        # Simplified ROI calculation
        estimated_conversions = clicks * 0.02  # 2% conversion rate
        avg_customer_value = 500
        estimated_revenue = estimated_conversions * avg_customer_value
        roi = ((estimated_revenue - campaign.budget) / campaign.budget) * 100
        
        return {
            'budget': campaign.budget,
            'estimated_revenue': round(estimated_revenue, 2),
            'estimated_conversions': round(estimated_conversions, 1),
            'roi_percentage': round(roi, 2),
            'note': 'Estimated based on industry averages'
        }