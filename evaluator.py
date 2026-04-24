# evaluator.py
"""
Evaluation system for Destiny agent
Assesses performance and provides feedback
"""

from typing import List, Dict, Any


class Evaluator:
    """Evaluates agent performance"""
    
    def __init__(self):
        self.evaluation_criteria = {
            'plan_completeness': {
                'weight': 0.3,
                'description': 'How complete and strategic the plan was'
            },
            'execution_success': {
                'weight': 0.4,
                'description': 'Success rate of executed actions'
            },
            'goal_alignment': {
                'weight': 0.2,
                'description': 'How well results align with original goal'
            },
            'learning_applied': {
                'weight': 0.1,
                'description': 'Use of past experiences'
            }
        }
    
    def evaluate_session(self, goal: str, plan: List[str], 
                        actions: List[Dict], results: List[str]) -> Dict[str, Any]:
        """
        Evaluate a complete session
        """
        
        # Calculate scores
        plan_score = self._evaluate_plan(plan, goal)
        execution_score = self._evaluate_execution(actions, results)
        goal_alignment_score = self._evaluate_goal_alignment(goal, results)
        learning_score = self._evaluate_learning(plan)
        
        # Weighted average
        success_score = (
            plan_score * self.evaluation_criteria['plan_completeness']['weight'] +
            execution_score * self.evaluation_criteria['execution_success']['weight'] +
            goal_alignment_score * self.evaluation_criteria['goal_alignment']['weight'] +
            learning_score * self.evaluation_criteria['learning_applied']['weight']
        )
        
        # Determine assessment
        if success_score >= 90:
            overall_assessment = "Excellent"
        elif success_score >= 75:
            overall_assessment = "Good"
        elif success_score >= 60:
            overall_assessment = "Satisfactory"
        elif success_score >= 40:
            overall_assessment = "Needs Improvement"
        else:
            overall_assessment = "Poor"
        
        # Generate insights
        strengths, weaknesses = self._identify_strengths_weaknesses(
            plan_score, execution_score, goal_alignment_score, learning_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            strengths, weaknesses, success_score
        )
        
        # Key insights
        key_insights = self._generate_key_insights(actions, results)
        
        return {
            'success_score': round(success_score, 2),
            'plan_quality_score': round(plan_score, 2),
            'execution_score': round(execution_score, 2),
            'goal_alignment_score': round(goal_alignment_score, 2),
            'learning_score': round(learning_score, 2),
            'overall_assessment': overall_assessment,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'key_insights': key_insights
        }
    
    def _evaluate_plan(self, plan: List[str], goal: str) -> float:
        """Evaluate the quality of the plan"""
        if not plan:
            return 0.0
        
        # Check for comprehensive planning
        score = 30.0  # Base score
        
        # Plan length bonus
        if len(plan) >= 5:
            score += 20.0
        elif len(plan) >= 3:
            score += 10.0
        
        # Strategic elements
        strategic_indicators = [
            'research', 'analyze', 'strategy', 'campaign',
            'audience', 'competitor', 'track', 'optimize'
        ]
        
        plan_text = ' '.join(plan).lower()
        strategic_count = sum(1 for indicator in strategic_indicators 
                             if indicator in plan_text)
        
        score += min(strategic_count * 10, 30)
        
        # Learning bonus
        if any('🧠' in step for step in plan):
            score += 10.0
        
        return min(score, 100.0)
    
    def _evaluate_execution(self, actions: List[Dict], results: List[str]) -> float:
        """Evaluate execution success"""
        if not actions:
            return 0.0
        
        # Count successes
        successful_actions = sum(1 for action in actions if action.get('success', False))
        success_rate = (successful_actions / len(actions)) * 100
        
        # Quality bonus
        quality_bonus = 0
        for action in actions:
            if action.get('success'):
                result = action.get('result', {})
                if isinstance(result, dict):
                    if 'content' in result or 'campaign_id' in result:
                        quality_bonus += 5
        
        total_score = min(success_rate + quality_bonus, 100.0)
        return total_score
    
    def _evaluate_goal_alignment(self, goal: str, results: List[str]) -> float:
        """Evaluate how well results align with goal"""
        goal_lower = goal.lower()
        results_text = ' '.join(results).lower()
        
        # Check goal keywords in results
        goal_words = set(word for word in goal_lower.split() if len(word) > 3)
        if not goal_words:
            return 50.0  # Default score for simple goals
        
        matches = sum(1 for word in goal_words if word in results_text)
        alignment_percentage = (matches / len(goal_words)) * 100
        
        # Bonus for campaign creation
        if 'campaign' in goal_lower and any('campaign_id' in str(r) for r in results):
            alignment_percentage += 20
        
        return min(alignment_percentage, 100.0)
    
    def _evaluate_learning(self, plan: List[str]) -> float:
        """Evaluate use of past learning"""
        # Check for learning indicators
        learning_indicators = [
            '🧠', 'learning', 'past', 'experience', 'memory',
            'adapted', 'learned', 'previous', 'success'
        ]
        
        plan_text = ' '.join(plan).lower()
        learning_count = sum(1 for indicator in learning_indicators 
                            if indicator in plan_text)
        
        if learning_count >= 2:
            return 100.0
        elif learning_count == 1:
            return 50.0
        else:
            return 0.0
    
    def _identify_strengths_weaknesses(self, plan_score: float, 
                                      execution_score: float,
                                      goal_alignment_score: float,
                                      learning_score: float) -> tuple:
        """Identify strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Plan quality
        if plan_score >= 80:
            strengths.append("Strong strategic planning")
        elif plan_score <= 40:
            weaknesses.append("Plan needs more strategic depth")
        
        # Execution
        if execution_score >= 85:
            strengths.append("Excellent execution success rate")
        elif execution_score <= 50:
            weaknesses.append("Execution success rate needs improvement")
        
        # Goal alignment
        if goal_alignment_score >= 90:
            strengths.append("Results closely align with goals")
        elif goal_alignment_score <= 60:
            weaknesses.append("Better alignment with original goals needed")
        
        # Learning
        if learning_score >= 80:
            strengths.append("Good application of past learnings")
        elif learning_score <= 30:
            weaknesses.append("Could benefit more from past experiences")
        
        # Default if none identified
        if not strengths:
            strengths.append("Successfully completed the session")
        if not weaknesses:
            weaknesses.append("No significant issues identified")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, strengths: List[str], 
                                 weaknesses: List[str], 
                                 success_score: float) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if success_score < 70:
            recommendations.append("Consider more comprehensive planning before execution")
        
        if "Execution success rate needs improvement" in weaknesses:
            recommendations.append("Review failed tools and consider alternative approaches")
        
        if "Better alignment with original goals needed" in weaknesses:
            recommendations.append("Ensure each action directly contributes to the main goal")
        
        if "Could benefit more from past experiences" in weaknesses:
            recommendations.append("Review past successful sessions for insights")
        
        # Always include improvement suggestions
        if success_score >= 85:
            recommendations.append("Continue current successful strategies")
            recommendations.append("Consider scaling successful approaches")
        else:
            recommendations.append("Implement the above improvements for better results")
        
        return recommendations
    
    def _generate_key_insights(self, actions: List[Dict], results: List[str]) -> List[str]:
        """Generate key insights from the session"""
        insights = []
        
        # Count successful tools
        successful_tools = {}
        for action in actions:
            if action.get('success'):
                tool = action.get('tool', 'unknown')
                successful_tools[tool] = successful_tools.get(tool, 0) + 1
        
        if successful_tools:
            top_tool = max(successful_tools.items(), key=lambda x: x[1])
            insights.append(f"Most successful tool: {top_tool[0]} ({top_tool[1]} successful executions)")
        
        # Campaign insights
        campaign_actions = [a for a in actions if 'campaign' in str(a.get('tool', ''))]
        if campaign_actions:
            insights.append("Campaign management tools were effectively utilized")
        
        # Content generation insights
        content_actions = [a for a in actions if 'generate' in str(a.get('tool', ''))]
        if content_actions:
            insights.append(f"Generated {len(content_actions)} content pieces")
        
        # Overall performance insight
        success_rate = sum(1 for a in actions if a.get('success')) / len(actions) * 100 if actions else 0
        insights.append(f"Overall success rate: {success_rate:.1f}%")
        
        return insights