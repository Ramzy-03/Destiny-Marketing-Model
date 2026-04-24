"""
Content Generator using Claude API
Real AI-powered content creation for digital marketing
"""

import anthropic
from typing import Dict, Any, List
from config import Config


class ContentGenerator:
    """
    AI-powered content generation using Claude
    Creates professional marketing content for various platforms
    """
    
    def __init__(self):
        self.client = None
        if Config.CLAUDE_API_KEY:
            try:
                # Try to initialize Claude client
                # Compatible with both old and new versions
                import anthropic
                self.client = anthropic.Anthropic(api_key=Config.CLAUDE_API_KEY)
            except TypeError:
                # Fallback for older versions
                try:
                    import anthropic
                    self.client = anthropic.Client(api_key=Config.CLAUDE_API_KEY)
                except:
                    print("[CONTENT GEN] Could not initialize Claude client - using demo mode")
                    self.client = None
            except Exception as e:
                print(f"[CONTENT GEN] Error initializing Claude: {e}")
                self.client = None
        
        self.demo_mode = Config.DEMO_MODE or not self.client
    
    def generate_content(self, content_type: str, params: Dict[str, Any]) -> str:
        """
        Generate marketing content using Claude API
        Falls back to demo content if API is not configured
        """
        if self.demo_mode or not self.client:
            return self._generate_demo_content(content_type, params)
        
        try:
            prompt = self._build_prompt(content_type, params)
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"[CONTENT GEN] Error with Claude API: {e}")
            return self._generate_demo_content(content_type, params)
    
    def _build_prompt(self, content_type: str, params: Dict[str, Any]) -> str:
        """Build appropriate prompt for Claude based on content type"""
        
        topic = params.get('topic', 'business growth')
        tone = params.get('tone', 'professional')
        platform = params.get('platform', 'general')
        target_audience = params.get('target_audience', 'business professionals')
        
        prompts = {
            'social_post': f"""Create an engaging social media post for {platform}.

Topic: {topic}
Tone: {tone}
Target Audience: {target_audience}

Requirements:
- Platform-optimized format
- Include relevant hashtags (3-5)
- Compelling call-to-action
- 150-280 characters
- Engaging and shareable

Generate ONLY the post content, no explanations.""",

            'blog_post': f"""Write a professional blog post about {topic}.

Tone: {tone}
Target Audience: {target_audience}

Requirements:
- Engaging title
- Clear introduction
- 3-4 main sections with subheadings
- Practical insights and examples
- Strong conclusion with CTA
- 800-1000 words
- SEO-friendly

Format with proper markdown headings.""",

            'email_campaign': f"""Create a marketing email about {topic}.

Tone: {tone}
Target Audience: {target_audience}

Requirements:
- Compelling subject line
- Personalized greeting
- Clear value proposition
- 2-3 key benefits
- Strong call-to-action
- Professional signature
- 200-300 words

Include subject line at the top.""",

            'ad_copy': f"""Write ad copy for a digital advertising campaign about {topic}.

Tone: {tone}
Target Audience: {target_audience}

Create 3 variations:
1. Short (25-30 words) - for display ads
2. Medium (50-75 words) - for social ads
3. Long (100-125 words) - for landing pages

Each should include:
- Attention-grabbing headline
- Key benefit
- Clear CTA

Format each variation clearly.""",

            'video_script': f"""Write a video script about {topic}.

Tone: {tone}
Target Audience: {target_audience}
Duration: 60-90 seconds

Include:
- Hook (first 5 seconds)
- Problem presentation
- Solution overview
- Benefits (2-3 key points)
- Call-to-action
- Closing

Format with timestamps and scene descriptions."""
        }
        
        return prompts.get(content_type, prompts['social_post'])
    
    def _generate_demo_content(self, content_type: str, params: Dict[str, Any]) -> str:
        """Generate demo content when API is not available"""
        
        topic = params.get('topic', 'business growth')
        platform = params.get('platform', 'LinkedIn')
        
        demo_templates = {
            'social_post': f"""🚀 Excited to share insights on {topic}!

In today's competitive landscape, innovation isn't optional—it's essential. Here's what we're learning:

✅ Data-driven decisions lead to 3x better outcomes
✅ Customer-centric approaches build lasting relationships
✅ Continuous learning drives sustainable growth

What's your biggest challenge in {topic}? Let's discuss! 👇

#BusinessGrowth #Innovation #Strategy #Leadership #Digital Marketing

[DEMO MODE - Enable Claude API for custom content]""",

            'blog_post': f"""# The Ultimate Guide to {topic.title()}

## Introduction

In today's rapidly evolving business landscape, understanding {topic} has become crucial for success. This comprehensive guide will walk you through proven strategies and actionable insights.

## Why {topic.title()} Matters

Recent studies show that businesses focusing on {topic} see up to 45% improvement in their key metrics. Here's what you need to know.

## Key Strategies

### Strategy 1: Data-Driven Decision Making
Leverage analytics to inform your approach and measure results effectively.

### Strategy 2: Customer-Centric Focus
Put your audience at the center of everything you do.

### Strategy 3: Continuous Optimization
Test, learn, and iterate for ongoing improvement.

## Implementation Roadmap

1. **Assessment Phase**: Understand your current position
2. **Planning Phase**: Develop your strategy
3. **Execution Phase**: Implement with precision
4. **Optimization Phase**: Refine based on results

## Conclusion

Mastering {topic} is a journey, not a destination. Start implementing these strategies today and track your progress.

**Ready to transform your approach?** Contact us to learn more!

[DEMO MODE - Enable Claude API for custom content]""",

            'email_campaign': f"""Subject: Transform Your {topic.title()} Strategy Today

Hi there,

Are you struggling to achieve the results you want with {topic}? You're not alone.

We've helped hundreds of businesses like yours achieve breakthrough results through our proven framework:

✓ **Increase Efficiency**: Save 20+ hours per week
✓ **Boost Results**: See measurable improvements in 30 days
✓ **Gain Clarity**: Know exactly what to do next

Our clients typically see:
• 3x improvement in key metrics
• 50% reduction in wasted effort
• Clear, actionable roadmap to success

**Ready to get started?** 
Click here to schedule your free strategy session →

Looking forward to your success,
Your Marketing Team

P.S. Limited spots available this month - book now!

[DEMO MODE - Enable Claude API for custom content]"""
        }
        
        return demo_templates.get(content_type, demo_templates['social_post'])
    
    def generate_hashtags(self, topic: str, platform: str, count: int = 5) -> List[str]:
        """Generate relevant hashtags for social media posts"""
        
        # Platform-specific hashtag strategies
        if platform.lower() == 'linkedin':
            base_tags = ['#BusinessGrowth', '#Leadership', '#Innovation', '#Strategy']
        elif platform.lower() == 'instagram':
            base_tags = ['#Entrepreneurship', '#BusinessTips', '#Success', '#Motivation']
        elif platform.lower() == 'twitter':
            base_tags = ['#Tech', '#Business', '#Startup', '#Growth']
        else:
            base_tags = ['#Marketing', '#Digital', '#Business', '#Growth']
        
        # Add topic-specific tags
        topic_words = topic.split()
        for word in topic_words[:2]:
            if len(word) > 3:
                base_tags.append(f'#{word.capitalize()}')
        
        return base_tags[:count]
    
    def optimize_for_platform(self, content: str, platform: str) -> str:
        """Optimize content for specific platform requirements"""
        
        if platform.lower() == 'twitter' and len(content) > 280:
            # Truncate for Twitter
            return content[:277] + '...'
        elif platform.lower() == 'instagram':
            # Add more hashtags for Instagram
            hashtags = self.generate_hashtags('marketing', 'instagram', 10)
            return f"{content}\n\n{' '.join(hashtags)}"
        elif platform.lower() == 'linkedin':
            # Professional formatting for LinkedIn
            return content
        
        return content