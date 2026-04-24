"""
Enhanced Destiny - Professional Digital Marketing Agent Interface
Full-featured Streamlit app with real platform integration
"""

import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
from agent import DestinyAgent
from config import Config

# Page config
st.set_page_config(
    page_title="Destiny - AI Digital Marketing Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .success-banner {
        background: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = DestinyAgent()
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.session_state.agent = None

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# === SIDEBAR ===
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=destiny&backgroundColor=667eea", width=100)
    st.title("🎯 Destiny Agent")
    
    st.divider()
    
    # ML Learning Status
    st.subheader("🧠 Hybrid Learning")
    
    agent = st.session_state.agent
    if agent and hasattr(agent, 'learning_initialized') and agent.learning_initialized:
        try:
            if hasattr(agent, 'learning_system') and agent.learning_system:
                learning_insights = agent.learning_system.get_learning_insights()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Models", learning_insights['system_status'].get('models_trained', 0))
                    st.metric("Predictions", learning_insights['system_status'].get('predictions_made', 0))
                with col2:
                    st.metric("Adaptations", learning_insights['system_status'].get('adaptations_performed', 0))
                    learning_status = "🟢 Active" if learning_insights['system_status'].get('is_learning', False) else "🟡 Ready"
                    st.metric("Status", learning_status)
                
                if st.button("📊 View ML Dashboard", use_container_width=True):
                    st.session_state['show_ml_dashboard'] = True
            else:
                st.warning("Learning system not available")
        except Exception as e:
            st.error(f"Error getting learning insights: {e}")
    else:
        st.info("🔄 Initialize hybrid learning...")
        if st.button("Initialize Now", use_container_width=True):
            if agent and hasattr(agent, 'learning_system') and agent.learning_system:
                with st.spinner("Training ML models..."):
                    try:
                        result = agent.learning_system.initialize_system(auto_train=True)
                        if result.get('system_ready', False):
                            agent.learning_initialized = True
                            st.success("✓ ML models trained!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Failed to train models: {e}")
            else:
                st.error("Learning system not available")
    
    st.divider()
    
    # Platform Status
    st.subheader("🔌 Platform Connections")
    try:
        platforms = Config.get_configured_platforms()
        
        for platform, connected in platforms.items():
            if connected:
                st.success(f"✅ {platform}")
            else:
                st.warning(f"⚠️ {platform} (Demo Mode)")
        
        if not any(platforms.values()):
            st.info("💡 Running in demo mode. Add API keys to `.env` for real integrations.")
    except:
        st.info("Platform configuration not available")
    
    st.divider()
    
    # Agent Memory
    st.subheader("🧠 Agent Memory")
    
    if agent:
        try:
            memory_stats = agent.get_memory_insights()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Goals", memory_stats.get('total_goals_processed', 0))
                st.metric("Actions", memory_stats.get('total_actions_taken', 0))
            with col2:
                st.metric("Success", memory_stats.get('average_success_rate', '0%'))
                st.metric("Status", memory_stats.get('learning_progress', 'Starting'))
        except Exception as e:
            st.info(f"Memory not available: {e}")
    else:
        st.info("Agent not initialized")
    
    st.divider()
    
    # Available Tools
    with st.expander("🔧 Available Tools"):
        if agent:
            try:
                tools = agent.tools.get_available_tools()
                tool_categories = {
                    'Content': [t for t in tools if 'generate' in t or 'content' in t],
                    'Social Media': [t for t in tools if 'post_to' in t],
                    'Campaigns': [t for t in tools if 'campaign' in t],
                    'Analytics': [t for t in tools if 'analytic' in t or 'report' in t],
                    'Research': [t for t in tools if 'analyz' in t or 'research' in t or 'trend' in t]
                }
                
                for category, category_tools in tool_categories.items():
                    if category_tools:
                        st.write(f"**{category}** ({len(category_tools)})")
                        for tool in category_tools[:3]:
                            st.caption(f"• {tool.replace('_', ' ').title()}")
            except Exception as e:
                st.info(f"Tools not available: {e}")
        else:
            st.info("Agent not initialized")
    
    st.divider()
    
    if agent and st.button("🗑️ Clear Memory", use_container_width=True):
        try:
            agent.memory.sessions = []
            agent.memory.save_memory()
            st.success("Memory cleared!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear memory: {e}")

# === MAIN CONTENT ===

# Header
st.markdown('<h1 class="main-header">Destiny AI Digital Marketing Manager</h1>', unsafe_allow_html=True)
st.markdown("""
**Professional autonomous agent** that plans, creates, and executes complete digital marketing campaigns.  
Connect your platforms, set your goals, and watch Destiny work autonomously.
""")

st.divider()

# === MODE SELECTION ===
st.header("1️⃣ Select Operation Mode")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Quick Action Mode")
    st.write("Execute individual marketing tasks:")
    st.write("• Generate content")
    st.write("• Post to social media")
    st.write("• Analyze audience")
    st.write("• Track analytics")
    quick_mode = st.button("Use Quick Mode", type="secondary", use_container_width=True)

with col2:
    st.subheader("🚀 Campaign Mode")
    st.write("Create full marketing campaigns:")
    st.write("• Multi-platform strategy")
    st.write("• Content calendar (10+ pieces)")
    st.write("• Automated publishing")
    st.write("• Performance tracking")
    campaign_mode = st.button("Use Campaign Mode", type="primary", use_container_width=True)

# Store mode in session state
if quick_mode:
    st.session_state['mode'] = 'quick'
if campaign_mode:
    st.session_state['mode'] = 'campaign'

selected_mode = st.session_state.get('mode', 'quick')

st.info(f"**Current Mode:** {'🚀 Campaign Mode' if selected_mode == 'campaign' else '🎯 Quick Action Mode'}")

st.divider()

# === GOAL INPUT ===
st.header("2️⃣ Define Your Marketing Goal")

# Example goals based on mode
if selected_mode == 'campaign':
    examples = [
        "Launch a 30-day brand awareness campaign for our new AI product",
        "Create and execute a lead generation campaign targeting small businesses",
        "Build a comprehensive content marketing strategy for Q1",
        "Launch multi-platform social media campaign to boost engagement",
        "Create and track a sales-focused promotional campaign"
    ]
else:
    examples = [
        "Create an engaging LinkedIn post about AI innovation",
        "Generate a blog post about digital marketing trends",
        "Analyze our target audience demographics",
        "Post our latest update to Facebook and LinkedIn",
        "Get analytics from all our social media platforms"
    ]

selected_example = st.selectbox(
    "Choose an example or write your own:",
    ["Custom Goal"] + examples
)

if selected_example == "Custom Goal":
    user_goal = st.text_area(
        "What do you want to achieve?",
        placeholder="Example: Create a LinkedIn post about our new product launch",
        height=120
    )
else:
    user_goal = st.text_area(
        "What do you want to achieve?",
        value=selected_example,
        height=120
    )

# Platform selection for campaign mode
if selected_mode == 'campaign':
    st.subheader("📱 Select Target Platforms")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        use_facebook = st.checkbox("Facebook", value=True)
    with col2:
        use_linkedin = st.checkbox("LinkedIn", value=True)
    with col3:
        use_instagram = st.checkbox("Instagram", value=False)
    with col4:
        use_twitter = st.checkbox("Twitter/X", value=False)

# === EXECUTION ===
st.divider()

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    run_button = st.button(
        f"{'🚀 Launch Campaign' if selected_mode == 'campaign' else '⚡ Execute Task'}",
        type="primary",
        use_container_width=True
    )

with col2:
    if st.button("📊 View Analytics", use_container_width=True):
        st.session_state['show_analytics'] = True

with col3:
    if st.button("📚 View Memory", use_container_width=True):
        st.session_state['show_memory'] = True

# === MAIN EXECUTION ===
agent = st.session_state.agent

if run_button and user_goal.strip() and agent:
    
    # Show progress
    with st.spinner(f"{'🚀 Destiny is creating your campaign...' if selected_mode == 'campaign' else '⚡ Destiny is working...'}"):
        
        try:
            # Execute agent
            advanced_mode = (selected_mode == 'campaign')
            session_result = agent.process_goal(user_goal, advanced_mode=advanced_mode)
            
            # Success banner
            st.markdown("""
            <div class="success-banner">
                <h3>✅ Execution Complete!</h3>
                <p>Destiny has successfully processed your goal. Review the results below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Store result in session state
            st.session_state.last_result = session_result
            
        except Exception as e:
            st.error(f"Execution failed: {e}")
            session_result = None

elif run_button and not user_goal.strip():
    st.error("⚠️ Please enter a goal before running Destiny.")
elif run_button and not agent:
    st.error("⚠️ Agent not initialized. Please check the sidebar.")

# Show results if available
if 'last_result' in st.session_state and st.session_state.last_result:
    session_result = st.session_state.last_result
    
    # === RESULTS TABS ===
    if selected_mode == 'campaign':
        tabs = st.tabs([
            "📋 Campaign Plan",
            "🔮 ML Predictions",
            "📝 Content Created",
            "⚡ Actions Executed",
            "📊 Performance",
            "🎯 Evaluation",
            "🧠 Learning Insights"
        ])
    else:
        tabs = st.tabs([
            "📋 Plan",
            "🔮 ML Predictions",
            "⚡ Actions",
            "📈 Results",
            "🎯 Evaluation",
            "🧠 Learning"
        ])
    
    # TAB 1: Plan
    with tabs[0]:
        st.subheader("Strategic Plan")
        st.markdown(f"**Goal:** {session_result.get('goal', 'N/A')}")
        st.markdown(f"**Mode:** {'Full Campaign' if selected_mode == 'campaign' else 'Quick Action'}")
        
        plan = session_result.get('plan', [])
        if plan:
            for i, step in enumerate(plan, 1):
                if step.startswith('🧠'):
                    st.info(step)
                else:
                    st.markdown(f"**{i}.** {step}")
        else:
            st.info("No plan available")
    
    # TAB 2: ML Predictions
    with tabs[1]:
        st.subheader("🔮 Machine Learning Predictions")
        
        if session_result.get('ml_predictions'):
            ml_preds = session_result['ml_predictions']
            
            st.markdown("**Pre-Campaign Predictions** (Based on historical marketing data)")
            
            # Engagement Prediction
            st.write("---")
            st.write("**📊 Engagement Forecast:**")
            
            eng_pred = ml_preds.get('predictions', {}).get('engagement', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Predicted Engagement Rate",
                    f"{eng_pred.get('predicted_engagement_rate', 0):.2f}%"
                )
            with col2:
                st.metric(
                    "Confidence",
                    eng_pred.get('confidence', 'medium').title()
                )
            with col3:
                if 'model_performance' in eng_pred:
                    st.metric(
                        "Model R² Score",
                        f"{eng_pred['model_performance'].get('r2', 0):.3f}"
                    )
            
            # Conversion Prediction
            st.write("---")
            st.write("**💰 Conversion Forecast:**")
            
            conv_pred = ml_preds.get('predictions', {}).get('conversion', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Predicted Conversion Rate",
                    f"{conv_pred.get('predicted_conversion_rate', 0):.2f}%"
                )
            with col2:
                st.metric(
                    "Expected Conversions",
                    conv_pred.get('predicted_conversions', 'N/A')
                )
            
            # ROI Prediction
            st.write("---")
            st.write("**📈 ROI Forecast:**")
            
            roi_pred = ml_preds.get('predictions', {}).get('roi', {})
            
            col1, col2 = st.columns(2)
            with col1:
                roi_val = roi_pred.get('predicted_roi', 0)
                st.metric(
                    "Predicted ROI",
                    f"{roi_val:.1f}%",
                    delta="Positive" if roi_val > 0 else "Negative"
                )
            with col2:
                st.metric(
                    "Est. Revenue",
                    f"${roi_pred.get('estimated_revenue', 0):,.0f}"
                )
            
            # Recommended Strategy
            if 'recommended_strategy' in ml_preds:
                st.write("---")
                st.write("**🎯 ML-Recommended Strategy:**")
                
                strategy = ml_preds['recommended_strategy']
                
                st.write("**Top Platforms:**")
                for platform_rec in strategy.get('recommended_platforms', [])[:2]:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"• **{platform_rec.get('platform', 'N/A')}**: {platform_rec.get('expected_engagement', 0):.1f}% engagement")
                    with col2:
                        st.write(f"${platform_rec.get('budget_allocation', 0):,.0f} budget")
                
                if 'expected_performance' in strategy:
                    st.write("**Expected Performance:**")
                    perf = strategy['expected_performance']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Impressions", f"{perf.get('impressions', 0):,}")
                    with col2:
                        st.metric("Engagement", f"{perf.get('engagement', 0):,}")
                    with col3:
                        st.metric("Leads", f"{perf.get('estimated_leads', 0):,}")
            
            # Adaptation insights (if available)
            if session_result.get('adaptation_insights'):
                st.write("---")
                st.write("**🔄 Real-Time Adaptation:**")
                
                adaptation = session_result['adaptation_insights']
                
                st.info("System adapted predictions based on actual results")
                
                if adaptation.get('adjustments'):
                    st.write("**Recommended Adjustments:**")
                    for adj in adaptation['adjustments']:
                        st.warning(f"**{adj.get('metric', 'N/A').title()}**: {adj.get('issue', 'N/A')}")
                        st.write(f"→ {adj.get('recommendation', 'N/A')}")
        else:
            st.info("💡 ML predictions available in Campaign Mode with trained models")
            
            if agent and not agent.learning_initialized:
                if st.button("Train ML Models Now"):
                    with st.spinner("Training models on marketing datasets..."):
                        try:
                            if hasattr(agent, 'learning_system') and agent.learning_system:
                                result = agent.learning_system.initialize_system(auto_train=True)
                                if result.get('system_ready', False):
                                    agent.learning_initialized = True
                                    st.success("✓ Models trained! Run a campaign to see predictions.")
                                    st.rerun()
                        except Exception as e:
                            st.error(f"Failed to train models: {e}")
    
    # TAB 3: Actions/Content
    with tabs[2]:
        if selected_mode == 'campaign':
            st.subheader("Generated Content")
            
            # Show campaign details
            actions = session_result.get('actions', [])
            for action in actions:
                if action.get('tool') == 'create_campaign':
                    result = action.get('result', {})
                    campaign = result.get('campaign', {})
                    content_schedule = result.get('content_schedule', [])
                    
                    # Campaign overview
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        campaign_id = campaign.get('campaign_id', 'N/A')
                        st.metric("Campaign ID", campaign_id[:20] + "..." if len(campaign_id) > 20 else campaign_id)
                    with col2:
                        st.metric("Content Pieces", campaign.get('posts_count', 0))
                    with col3:
                        st.metric("Platforms", len(campaign.get('platforms', [])))
                    
                    # Show content pieces
                    if content_schedule:
                        st.write("---")
                        st.write("**Content Calendar:**")
                        
                        for idx, content_item in enumerate(content_schedule[:5], 1):  # Show first 5
                            with st.expander(f"Content {idx}: {content_item.get('platform', 'N/A').title()} - {content_item.get('content_type', 'N/A').replace('_', ' ').title()}"):
                                st.write("**Platform:**", content_item.get('platform', 'N/A'))
                                st.write("**Type:**", content_item.get('content_type', 'N/A').replace('_', ' ').title())
                                st.write("**Scheduled:**", content_item.get('scheduled_date', 'N/A')[:10])
                                st.write("**Content:**")
                                st.text_area("", content_item.get('content', 'No content')[:500], height=150, key=f"content_{idx}", disabled=True)
                                if content_item.get('hashtags'):
                                    st.write("**Hashtags:**", " ".join(content_item.get('hashtags', [])))
                        
                        if len(content_schedule) > 5:
                            st.info(f"+ {len(content_schedule) - 5} more content pieces in campaign")
        else:
            st.subheader("Actions Executed")
            
            actions = session_result.get('actions', [])
            for i, action in enumerate(actions, 1):
                success = action.get('success', False)
                tool_name = action.get('tool', 'Unknown')
                
                with st.expander(
                    f"{'✅' if success else '❌'} Action {i}: {tool_name.replace('_', ' ').title()}",
                    expanded=(i <= 2)
                ):
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.write("**Status:**")
                        if success:
                            st.success("Success")
                        else:
                            st.error("Failed")
                        
                        st.write("**Tool:**")
                        st.code(tool_name)
                    
                    with col2:
                        st.write("**Result:**")
                        result = action.get('result', {})
                        
                        if isinstance(result, dict):
                            # Show key metrics
                            if 'content' in result:
                                st.text_area("Generated Content", str(result['content'])[:500], height=100, disabled=True)
                            elif 'platform' in result:
                                st.json(result)
                            else:
                                st.json(result)
                        else:
                            st.text(str(result)[:500])
    
    # TAB 4: Results
    with tabs[3 if selected_mode == 'campaign' else 3]:
        st.subheader("Execution Results")
        
        results = session_result.get('results', [])
        success_count = sum(1 for r in results if '✓' in str(r))
        total_count = len(results) if results else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Steps", total_count)
        with col2:
            st.metric("Successful", success_count)
        with col3:
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0
            st.metric("Success Rate", f"{success_rate:.0f}%")
        
        st.write("---")
        
        for result in results:
            if '✓' in str(result):
                st.success(result)
            elif '✗' in str(result):
                st.error(result)
            else:
                st.info(result)
    
    # TAB 5: Evaluation
    with tabs[4 if selected_mode == 'campaign' else 4]:
        st.subheader("Performance Evaluation")
        
        eval_data = session_result.get('evaluation', {})
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Success Score", f"{eval_data.get('success_score', 0):.0f}%")
        with col2:
            st.metric("Plan Quality", f"{eval_data.get('plan_quality_score', 0):.0f}%")
        with col3:
            st.metric("Execution", f"{eval_data.get('execution_score', 0):.0f}%")
        with col4:
            st.metric("Assessment", eval_data.get('overall_assessment', 'N/A'))
        
        # Visualization
        if eval_data:
            fig = go.Figure(data=[
                go.Bar(
                    x=['Success', 'Plan Quality', 'Execution'],
                    y=[
                        eval_data.get('success_score', 0),
                        eval_data.get('plan_quality_score', 0),
                        eval_data.get('execution_score', 0)
                    ],
                    marker_color=['#28a745', '#667eea', '#ffc107']
                )
            ])
            fig.update_layout(
                title="Performance Metrics",
                yaxis_title="Score (%)",
                yaxis=dict(range=[0, 100]),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Strengths and improvements
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**💪 Strengths:**")
            for strength in eval_data.get('strengths', []):
                st.success(f"✓ {strength}")
        
        with col2:
            st.write("**📈 Improvements:**")
            for weakness in eval_data.get('weaknesses', []):
                st.warning(f"• {weakness}")
    
    # TAB 6: Learning/Learning Insights
    with tabs[5 if selected_mode == 'campaign' else 5]:
        if selected_mode == 'campaign':
            st.subheader("🧠 Hybrid Learning System")
            
            if session_result.get('learning_status'):
                learning = session_result['learning_status']
                
                st.write("**System Overview:**")
                
                col1, col2, col3, col4 = st.columns(4)
                
                sys_status = learning.get('system_status', {})
                with col1:
                    st.metric("Models Trained", sys_status.get('models_trained', 0))
                with col2:
                    st.metric("Predictions Made", sys_status.get('predictions_made', 0))
                with col3:
                    st.metric("Adaptations", sys_status.get('adaptations_performed', 0))
                with col4:
                    status = "🟢 Learning" if sys_status.get('is_learning', False) else "🟡 Ready"
                    st.metric("Status", status)
        else:
            st.subheader("Agent Memory")
            
            st.write("**This Session:**")
            st.json({
                'goal': session_result.get('goal', 'N/A')[:100] + "...",
                'steps_planned': len(session_result.get('plan', [])),
                'actions_executed': len(session_result.get('actions', [])),
                'success_score': session_result.get('evaluation', {}).get('success_score', 0),
                'past_experiences_used': session_result.get('past_experiences_used', 0)
            })
            
            memory_stats = session_result.get('memory_stats', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sessions", memory_stats.get('total_sessions', 0))
            with col2:
                st.metric("Total Actions", memory_stats.get('total_actions', 0))
            with col3:
                st.metric("Avg Success", f"{memory_stats.get('avg_success_rate', 0):.1f}%")
    
    # TAB 7: Learning Insights (Campaign only)
    if selected_mode == 'campaign' and len(tabs) > 6:
        with tabs[6]:
            st.subheader("Complete Learning Report")
            
            if agent and agent.learning_initialized and hasattr(agent, 'learning_system'):
                if st.button("Generate Full Learning Report"):
                    with st.spinner("Generating comprehensive report..."):
                        try:
                            report = agent.learning_system.generate_learning_report()
                            st.json(report)
                        except Exception as e:
                            st.error(f"Failed to generate report: {e}")
            else:
                st.info("Complete learning insights available with trained ML models")

# === ANALYTICS VIEW ===
if st.session_state.get('show_analytics', False):
    st.divider()
    st.header("📊 Analytics Dashboard")
    
    # Placeholder analytics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Impressions", "45,230", "+15%")
    with col2:
        st.metric("Engagement Rate", "6.8%", "+2.1%")
    with col3:
        st.metric("Click-Through Rate", "3.2%", "+0.8%")
    with col4:
        st.metric("Conversions", "234", "+28")
    
    # Platform breakdown
    st.subheader("Performance by Platform")
    
    platform_data = {
        'Platform': ['Facebook', 'LinkedIn', 'Instagram', 'Twitter'],
        'Impressions': [15000, 20000, 8000, 2230],
        'Engagement': [900, 1400, 680, 120]
    }
    
    df = pd.DataFrame(platform_data)
    
    fig = px.bar(df, x='Platform', y=['Impressions', 'Engagement'], barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Close Analytics"):
        st.session_state['show_analytics'] = False
        st.rerun()

# === ML DASHBOARD ===
if st.session_state.get('show_ml_dashboard', False) and agent and hasattr(agent, 'learning_system'):
    st.divider()
    st.header("🧠 Machine Learning Dashboard")
    
    if agent.learning_initialized:
        try:
            # Get comprehensive learning report
            report = agent.learning_system.generate_learning_report()
            
            # Overview metrics
            st.subheader("📊 System Overview")
            
            overview = report.get('system_overview', {})
            sys_status = overview.get('system_status', {})
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Models Trained", sys_status.get('models_trained', 0))
            with col2:
                st.metric("Total Predictions", sys_status.get('predictions_made', 0))
            with col3:
                st.metric("Adaptations", sys_status.get('adaptations_performed', 0))
            with col4:
                learning_state = "🟢 Active Learning" if sys_status.get('is_learning', False) else "🟡 Ready"
                st.metric("Learning State", learning_state)
            
            # Model Performance
            st.write("---")
            st.subheader("🎯 Model Performance")
            
            if overview.get('model_performance', {}).get('models_trained'):
                models = overview['model_performance']['models_trained']
                perf_data = overview['model_performance']['model_performance']
                
                perf_df = []
                for model in models:
                    if model in perf_data:
                        perf_df.append({
                            'Model': model.title(),
                            'R² Score': perf_data[model].get('r2', 0),
                            'MSE': perf_data[model].get('mse', 0),
                            'Status': '✅ Good' if perf_data[model].get('r2', 0) > 0.7 else '⚠️ Fair' if perf_data[model].get('r2', 0) > 0.5 else '❌ Needs Improvement'
                        })
                
                if perf_df:
                    df = pd.DataFrame(perf_df)
                    st.dataframe(df, use_container_width=True)
            
            # Learning Progress
            if overview.get('learning_progress'):
                st.write("---")
                st.subheader("📈 Learning Progress")
                
                progress = overview['learning_progress']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Training Sessions", progress.get('training_sessions', 0))
                with col2:
                    st.metric("Adaptation Cycles", progress.get('adaptation_sessions', 0))
                
                if progress.get('accuracy_trend') and len(progress['accuracy_trend']) > 1:
                    trend_data = progress['accuracy_trend']
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=list(range(1, len(trend_data) + 1)),
                            y=trend_data,
                            mode='lines+markers',
                            name='Accuracy Improvement',
                            line=dict(color='#667eea')
                        )
                    ])
                    fig.update_layout(
                        title="Prediction Accuracy Improvement Over Time",
                        xaxis_title="Adaptation Cycle",
                        yaxis_title="Accuracy Improvement (%)",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error generating ML report: {e}")
    else:
        st.warning("⚠️ ML system not initialized")
        if st.button("Initialize ML System"):
            with st.spinner("Initializing hybrid learning system..."):
                try:
                    result = agent.learning_system.initialize_system(auto_train=True)
                    if result.get('system_ready', False):
                        agent.learning_initialized = True
                        st.success("✓ System initialized!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to initialize: {e}")
    
    if st.button("Close ML Dashboard"):
        st.session_state['show_ml_dashboard'] = False
        st.rerun()

# === FOOTER ===
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px;'>
    <h3>🎯 Destiny - AI Digital Marketing Manager</h3>
    <p><strong>Autonomous agent</strong> for professional digital marketing</p>
    <p>Connects to real platforms • Generates AI-powered content • Learns from experience</p>
    <p style='margin-top: 20px;'><em>Graduation Project - AI Systems Engineering</em></p>
</div>
""", unsafe_allow_html=True)