"""
Enhanced Destiny Agent - Professional Digital Marketing Manager
Autonomous agent with real platform integration capabilities
"""

from typing import List, Dict, Any, Tuple
from tools import MarketingTools
from memory import Memory
from evaluator import Evaluator


class DestinyAgent:
    def __init__(self):
        print("[AGENT] Initializing Destiny Agent...")
        self.tools = MarketingTools()
        self.memory = Memory()
        self.evaluator = Evaluator()
        try:
            from HybridLearningSystemLocal import HybridLearningSystem
            print("[AGENT] Initializing Hybrid Learning System...")
            self.learning_system = HybridLearningSystem(data_folder=r"E:\destiny\data")
            self.learning_initialized = False
            print("[AGENT] ✓ Learning system initialized")
        except ImportError as e:
            print(f"[AGENT] ⚠ Could not import HybridLearningSystem: {e}")
            print("[AGENT] Running without machine learning capabilities")
            self.learning_system = None
            self.learning_initialized = False
        except Exception as e:
            print(f"[AGENT] ⚠ Error initializing learning system: {e}")
            self.learning_system = None
            self.learning_initialized = False
        self.current_goal = None
        self.current_plan = []
        self.current_actions = []
        self.current_results = []
        self.current_campaign_id = None
        self.current_predictions = None
        
        print("[AGENT] ✓ Agent initialized successfully")
    def process_goal(self, goal: str, advanced_mode: bool = False) -> Dict[str, Any]:
        """
        Main agentic loop with hybrid learning integration
        """
        print(f"[AGENT] Processing goal: {goal}")
        print(f"[AGENT] Advanced mode: {advanced_mode}")
        
        # Initialize hybrid learning if not done
        if self.learning_system and not self.learning_initialized:
            print("[AGENT] Initializing hybrid learning system...")
            try:
                init_result = self.learning_system.initialize_system(auto_train=True)
                self.learning_initialized = init_result.get('system_ready', False)
                if self.learning_initialized:
                    print("[AGENT] ✓ Hybrid learning system ready")
                else:
                    print("[AGENT] ⚠ Hybrid learning system partially ready")
            except Exception as e:
                print(f"[AGENT] ⚠ Failed to initialize learning system: {e}")
                self.learning_initialized = False
        
        # Reset session
        self.current_goal = goal
        self.current_plan = []
        self.current_actions = []
        self.current_results = []
        
        # Learn from past
        past_experiences = self.memory.get_relevant_experiences(goal)
        
        # NEW: Make ML-based predictions before planning
        if self.learning_initialized and advanced_mode:
            try:
                campaign_params = self._extract_campaign_params(goal)
                self.current_predictions = self.learning_system.predict_campaign_performance(campaign_params)
                print(f"[AGENT] ML Prediction - Expected Engagement: {self.current_predictions['predictions']['engagement']['predicted_engagement_rate']:.2f}%")
            except Exception as e:
                print(f"[AGENT] ⚠ Failed to make ML predictions: {e}")
                self.current_predictions = None
        plan = self._create_enhanced_plan(goal, past_experiences, advanced_mode)
        self.current_plan = plan
        actions, results = self._execute_enhanced_plan(plan, advanced_mode)
        self.current_actions = actions
        self.current_results = results
        evaluation = self.evaluator.evaluate_session(goal, plan, actions, results)
        
        # NEW: Adapt from real results (closes the learning loop)
        adaptation_insights = None
        if self.learning_initialized and self.current_predictions and actions:
            actual_results = self._extract_actual_results(actions)
            if actual_results:
                try:
                    adaptation_insights = self.learning_system.adapt_from_realtime_results(
                        predicted=self.current_predictions['predictions'],
                        actual=actual_results
                    )
                    print("[AGENT] ✓ Adapted predictions from real results")
                except Exception as e:
                    print(f"[AGENT] ⚠ Failed to adapt predictions: {e}")
        
        # Store in memory for learning
        self.memory.store_session(goal, plan, actions, results, evaluation)
        
        # Get learning insights
        learning_status = None
        if self.learning_initialized:
            try:
                learning_status = self.learning_system.get_learning_insights()
            except Exception as e:
                print(f"[AGENT] ⚠ Failed to get learning insights: {e}")
        
        return {
            'goal': goal,
            'plan': plan,
            'actions': actions,
            'results': results,
            'evaluation': evaluation,
            'past_experiences_used': len(past_experiences),
            'memory_stats': self.memory.get_statistics(),
            'campaign_id': self.current_campaign_id,
            'ml_predictions': self.current_predictions,
            'adaptation_insights': adaptation_insights,
            'learning_status': learning_status
        }
    
    def _create_enhanced_plan(self, goal: str, past_experiences: List[Dict],
                            advanced_mode: bool) -> List[str]:
        """
        Create advanced marketing plan
        """
        print("[AGENT] Creating enhanced strategic plan...")
        
        goal_lower = goal.lower()
        
        # Classify goal type for better planning
        if any(word in goal_lower for word in ['campaign', 'launch', 'promotion']):
            plan = self._plan_full_campaign(goal, advanced_mode)
        elif any(word in goal_lower for word in ['aware', 'visibility', 'brand', 'reach']):
            plan = self._plan_awareness_strategy(goal, advanced_mode)
        elif any(word in goal_lower for word in ['lead', 'prospect', 'contact']):
            plan = self._plan_lead_generation_strategy(goal, advanced_mode)
        elif any(word in goal_lower for word in ['engage', 'community', 'follower']):
            plan = self._plan_engagement_strategy(goal, advanced_mode)
        elif any(word in goal_lower for word in ['sale', 'revenue', 'convert']):
            plan = self._plan_sales_strategy(goal, advanced_mode)
        elif any(word in goal_lower for word in ['content', 'post', 'blog']):
            plan = self._plan_content_creation(goal, advanced_mode)
        else:
            plan = self._plan_comprehensive_marketing(goal, advanced_mode)
        
        # Adapt from memory
        if past_experiences:
            print(f"[AGENT] Applying learnings from {len(past_experiences)} past experiences...")
            plan = self._adapt_plan_from_memory(plan, past_experiences)
        
        return plan
    
    def _plan_full_campaign(self, goal: str, advanced: bool) -> List[str]:
        """Plan a complete marketing campaign"""
        if advanced:
            return [
                "Step 1: Conduct comprehensive audience and competitor research",
                "Step 2: Create multi-platform marketing campaign with defined goals",
                "Step 3: Generate content calendar with 10+ pieces across platforms",
                "Step 4: Launch campaign across Facebook, LinkedIn, and Instagram",
                "Step 5: Set up real-time analytics tracking and monitoring",
                "Step 6: Analyze performance metrics and optimize strategy",
                "Step 7: Generate detailed campaign performance report"
            ]
        else:
            return [
                "Step 1: Analyze target audience",
                "Step 2: Set up marketing campaign structure",
                "Step 3: Generate initial content pieces",
                "Step 4: Track campaign setup progress"
            ]
    
    def _plan_awareness_strategy(self, goal: str, advanced: bool) -> List[str]:
        """Plan brand awareness campaign"""
        if advanced:
            return [
                "Step 1: Research target audience demographics and preferences",
                "Step 2: Analyze competitor positioning and market gaps",
                "Step 3: Generate engaging blog post for SEO and thought leadership",
                "Step 4: Create optimized social media posts for LinkedIn and Facebook",
                "Step 5: Post content to multiple platforms simultaneously",
                "Step 6: Track impressions, reach, and engagement metrics",
                "Step 7: Optimize content strategy based on performance data"
            ]
        else:
            return [
                "Step 1: Analyze target audience",
                "Step 2: Generate awareness-focused content",
                "Step 3: Post to primary social platform",
                "Step 4: Track initial performance"
            ]
    
    def _plan_lead_generation_strategy(self, goal: str, advanced: bool) -> List[str]:
        """Plan lead generation campaign"""
        if advanced:
            return [
                "Step 1: Analyze target audience and identify pain points",
                "Step 2: Research competitor lead generation tactics",
                "Step 3: Create lead magnet content (blog post + email campaign)",
                "Step 4: Generate conversion-optimized ad copy",
                "Step 5: Set up multi-platform campaign with clear CTAs",
                "Step 6: Launch campaign and track conversion metrics",
                "Step 7: Optimize based on conversion rate and cost per lead"
            ]
        else:
            return [
                "Step 1: Identify target audience",
                "Step 2: Create lead generation content",
                "Step 3: Generate email campaign",
                "Step 4: Track lead metrics"
            ]
    
    def _plan_engagement_strategy(self, goal: str, advanced: bool) -> List[str]:
        """Plan engagement-focused strategy"""
        if advanced:
            return [
                "Step 1: Analyze current engagement patterns and trends",
                "Step 2: Research trending topics and content formats",
                "Step 3: Generate interactive social media content",
                "Step 4: Post engaging content to Instagram and LinkedIn",
                "Step 5: Monitor engagement rates and community response",
                "Step 6: Respond to top comments and build relationships",
                "Step 7: Adjust strategy based on engagement data"
            ]
        else:
            return [
                "Step 1: Analyze audience preferences",
                "Step 2: Create engaging social content",
                "Step 3: Post to social platforms",
                "Step 4: Monitor engagement"
            ]
    
    def _plan_sales_strategy(self, goal: str, advanced: bool) -> List[str]:
        """Plan sales conversion campaign"""
        if advanced:
            return [
                "Step 1: Research competitor pricing and positioning",
                "Step 2: Analyze customer buying journey and touchpoints",
                "Step 3: Generate conversion-focused ad copy and offers",
                "Step 4: Create nurturing email campaign sequence",
                "Step 5: Launch multi-channel sales campaign",
                "Step 6: Track ROI, conversion rates, and customer acquisition cost",
                "Step 7: Optimize for maximum ROI and scale winning strategies"
            ]
        else:
            return [
                "Step 1: Research target customers",
                "Step 2: Create sales-focused content",
                "Step 3: Launch promotional campaign",
                "Step 4: Track sales metrics"
            ]
    
    def _plan_content_creation(self, goal: str, advanced: bool) -> List[str]:
        """Plan content creation and distribution"""
        if advanced:
            return [
                "Step 1: Analyze trending topics and audience interests",
                "Step 2: Generate comprehensive blog post with SEO optimization",
                "Step 3: Create social media adaptations for each platform",
                "Step 4: Generate email campaign to promote content",
                "Step 5: Distribute content across all platforms",
                "Step 6: Track content performance and engagement",
                "Step 7: Identify top-performing content for future strategy"
            ]
        else:
            return [
                "Step 1: Identify content topic",
                "Step 2: Generate content",
                "Step 3: Post to social media",
                "Step 4: Track basic metrics"
            ]
    
    def _plan_comprehensive_marketing(self, goal: str, advanced: bool) -> List[str]:
        """General comprehensive marketing plan"""
        if advanced:
            return [
                "Step 1: Conduct comprehensive audience and market research",
                "Step 2: Analyze competitors and identify opportunities",
                "Step 3: Create full marketing campaign with clear objectives",
                "Step 4: Generate multi-format content (blog, email, social, ads)",
                "Step 5: Launch campaign across multiple platforms",
                "Step 6: Track comprehensive analytics across all channels",
                "Step 7: Generate optimization recommendations and scale strategy"
            ]
        else:
            return [
                "Step 1: Research target audience",
                "Step 2: Generate marketing content",
                "Step 3: Execute marketing actions",
                "Step 4: Track performance"
            ]
    
    def _adapt_plan_from_memory(self, plan: List[str], past_experiences: List[Dict]) -> List[str]:
        """Learn from past experiences"""
        successful_tools = set()
        
        for exp in past_experiences:
            if exp.get('evaluation', {}).get('success_score', 0) > 75:
                for action in exp.get('actions', []):
                    if action.get('success'):
                        successful_tools.add(action.get('tool', ''))
        
        if successful_tools:
            learning_note = f"🧠 Learning: Past success with {', '.join(list(successful_tools)[:3])}"
            plan.append(learning_note)
        
        return plan
    
    def _execute_enhanced_plan(self, plan: List[str], advanced_mode: bool) -> Tuple[List[Dict], List[str]]:
        """
        Execute plan with enhanced tool capabilities
        """
        print("[AGENT] Executing enhanced plan...")
        
        actions = []
        results = []
        generated_content = {}  # Store generated content for reuse
        
        for i, step in enumerate(plan, 1):
            # Skip learning notes
            if step.startswith('🧠'):
                continue
            
            print(f"[AGENT] Step {i}: {step}")
            
            # Enhanced reasoning for tool selection
            tool_name, params = self._enhanced_tool_selection(
                step, generated_content, advanced_mode
            )
            
            if tool_name:
                # Execute tool
                try:
                    action_result = self.tools.execute_tool(tool_name, params)
                    actions.append(action_result)
                    
                    # Store generated content for next steps
                    if action_result.get('success'):
                        result = action_result.get('result', {})
                        
                        # Save content for reuse
                        if 'content' in str(result):
                            if isinstance(result, dict) and 'content' in result:
                                generated_content['last_content'] = result
                            elif isinstance(result, str):
                                generated_content['last_content'] = result
                        
                        # Save campaign ID for tracking
                        if isinstance(result, dict) and 'campaign_id' in result:
                            self.current_campaign_id = result['campaign_id']
                            generated_content['campaign_id'] = result['campaign_id']
                        
                        result_summary = f"✓ Step {i}: {tool_name} completed successfully"
                        results.append(result_summary)
                    else:
                        result_summary = f"✗ Step {i}: {tool_name} failed - {action_result.get('error', 'Unknown')}"
                        results.append(result_summary)
                except Exception as e:
                    error_summary = f"✗ Step {i}: {tool_name} raised exception - {str(e)}"
                    results.append(error_summary)
                    actions.append({
                        'success': False,
                        'tool': tool_name,
                        'error': str(e),
                        'timestamp': 'error'
                    })
            else:
                results.append(f"○ Step {i}: Planning step")
        
        return actions, results
    
    def _enhanced_tool_selection(self, step: str, context: Dict[str, Any],
                                advanced: bool) -> Tuple[str, Dict[str, Any]]:
        """
        Enhanced tool selection with context awareness
        """
        step_lower = step.lower()
        
        # Research tools
        if 'audience' in step_lower and 'analyz' in step_lower:
            return 'audience_analysis', {'business_type': 'general'}
        
        elif 'competitor' in step_lower or 'market' in step_lower:
            return 'competitor_research', {'industry': 'tech'}
        
        elif 'trend' in step_lower:
            return 'trend_analysis', {'industry': 'general'}
        
        # Content generation tools
        elif 'blog' in step_lower:
            return 'generate_blog_post', {
                'topic': self.current_goal,
                'tone': 'professional',
                'target_audience': 'business professionals'
            }
        
        elif 'email' in step_lower:
            return 'generate_email_campaign', {
                'topic': self.current_goal,
                'tone': 'professional'
            }
        
        elif 'ad' in step_lower:
            return 'generate_ad_copy', {
                'topic': self.current_goal,
                'tone': 'compelling'
            }
        
        # Posting tools
        elif 'post' in step_lower and 'facebook' in step_lower:
            content = context.get('last_content', 'Generated content')
            if isinstance(content, dict):
                content = str(content.get('content', 'Marketing update'))
            return 'post_to_facebook', {'content': content[:500]}
        
        elif 'post' in step_lower and 'linkedin' in step_lower:
            content = context.get('last_content', 'Generated content')
            if isinstance(content, dict):
                content = str(content.get('content', 'Professional update'))
            return 'post_to_linkedin', {'content': content[:500]}
        
        elif 'post' in step_lower and 'instagram' in step_lower:
            content = context.get('last_content', 'Generated content')
            if isinstance(content, dict):
                content = str(content.get('content', 'Inspiring update'))
            return 'post_to_instagram', {'content': content[:500], 'image_url': 'placeholder'}
        
        elif 'post' in step_lower and ('multiple' in step_lower or 'all' in step_lower):
            content = context.get('last_content', 'Generated content')
            if isinstance(content, dict):
                content = str(content.get('content', 'Marketing update'))
            return 'post_to_multiple_platforms', {
                'platforms': ['facebook', 'linkedin'],
                'content': content[:500]
            }
        
        # Campaign tools
        elif 'create' in step_lower and 'campaign' in step_lower:
            return 'create_campaign', {
                'name': f"{self.current_goal[:30]} Campaign",
                'goal': self.current_goal,
                'platforms': ['facebook', 'linkedin', 'instagram'],
                'duration_days': 30,
                'budget': 5000,
                'content_pieces': 10 if advanced else 5
            }
        
        elif 'launch' in step_lower and 'campaign' in step_lower:
            campaign_id = context.get('campaign_id', '')
            if campaign_id:
                return 'launch_campaign', {'campaign_id': campaign_id}
        
        elif 'track' in step_lower and 'campaign' in step_lower:
            campaign_id = context.get('campaign_id', '')
            if campaign_id:
                return 'track_campaign', {'campaign_id': campaign_id}
        
        elif 'optimize' in step_lower:
            campaign_id = context.get('campaign_id', '')
            if campaign_id:
                return 'optimize_campaign', {'campaign_id': campaign_id}
        
        # Analytics tools
        elif 'track' in step_lower or 'analytic' in step_lower or 'performance' in step_lower:
            return 'get_all_analytics', {}
        
        elif 'report' in step_lower:
            params = {}
            if context.get('campaign_id'):
                params['campaign_id'] = context['campaign_id']
            return 'generate_report', params
        
        # Content generation fallback
        elif 'generat' in step_lower or 'create' in step_lower:
            return 'generate_content', {
                'content_type': 'social_post',
                'topic': self.current_goal,
                'platform': 'linkedin',
                'tone': 'professional'
            }
        
        return None, {}
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get current session summary"""
        return {
            'goal': self.current_goal,
            'plan': self.current_plan,
            'actions_count': len(self.current_actions),
            'results': self.current_results,
            'campaign_id': self.current_campaign_id
        }
    
    def get_memory_insights(self) -> Dict[str, Any]:
        """Get memory and learning insights"""
        stats = self.memory.get_statistics()
        all_sessions = self.memory.get_all_sessions()
        
        insights = {
            'total_goals_processed': stats['total_sessions'],
            'total_actions_taken': stats['total_actions'],
            'average_success_rate': f"{stats['avg_success_rate']:.1f}%",
            'learning_progress': "Improving" if stats['total_sessions'] > 1 else "Initial session",
            'recent_sessions': all_sessions[-3:] if all_sessions else []
        }
        
        # Add hybrid learning insights
        if self.learning_initialized:
            try:
                ml_insights = self.learning_system.get_learning_insights()
                insights['ml_learning'] = {
                    'models_trained': ml_insights['system_status']['models_trained'],
                    'predictions_made': ml_insights['system_status']['predictions_made'],
                    'is_learning': ml_insights['system_status']['is_learning']
                }
            except Exception as e:
                print(f"[AGENT] Failed to get learning insights: {e}")
        
        return insights
    
    def _extract_campaign_params(self, goal: str) -> Dict[str, Any]:
        """Extract campaign parameters from goal for ML prediction"""
        goal_lower = goal.lower()
        
        # Determine platform
        platform = 'LinkedIn'  # default
        if 'facebook' in goal_lower:
            platform = 'Facebook'
        elif 'instagram' in goal_lower:
            platform = 'Instagram'
        elif 'twitter' in goal_lower:
            platform = 'Twitter'
        
        # Determine content type
        content_type = 'Image'
        if 'video' in goal_lower:
            content_type = 'Video'
        elif 'blog' in goal_lower:
            content_type = 'Article'
        
        return {
            'platform': platform,
            'budget': 5000,  # default
            'content_type': content_type,
            'duration_days': 30,
            'goal': goal
        }
    
    def _extract_actual_results(self, actions: List[Dict]) -> Dict[str, Any]:
        """Extract actual results from executed actions for adaptation"""
        actual = {}
        
        for action in actions:
            if not action.get('success'):
                continue
            
            result = action.get('result', {})
            
            # Extract metrics from different action types
            if isinstance(result, dict):
                if 'engagement_rate' in result:
                    actual['engagement_rate'] = result['engagement_rate']
                if 'clicks' in result:
                    actual['clicks'] = result['clicks']
                if 'conversions' in result:
                    actual['conversions'] = result['conversions']
                if 'roi' in result or 'roi_percentage' in result:
                    actual['roi'] = result.get('roi', result.get('roi_percentage', 0))
                
                # Extract from analytics
                if 'overall' in result:
                    overall = result['overall']
                    if 'total_clicks' in overall:
                        actual['clicks'] = overall['total_clicks']
                    if 'avg_engagement_rate' in overall:
                        actual['engagement_rate'] = overall['avg_engagement_rate']
        
        return actual if actual else None