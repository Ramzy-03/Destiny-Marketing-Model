# test_complete.py
"""
Test the complete hybrid learning system
"""

from HybridLearningSystemLocal import HybridLearningSystem

def main():
    print("Testing Hybrid Learning System with Local Data\n")
    
    # Initialize system
    system = HybridLearningSystem(data_folder=r"E:\destiny\data")
    
    print("1. Initializing system...")
    init_results = system.initialize_system(auto_train=True, load_all=True)
    
    print(f"\nInitialization Results:")
    print(f"Status: {init_results['status']}")
    print(f"System Ready: {init_results['system_ready']}")
    print(f"Models Trained: {init_results['models_trained']}")
    
    print("\n2. Generating learning report...")
    try:
        report = system.generate_learning_report()
        print(f"✓ Learning report generated successfully")
        print(f"Recommendations: {len(report['recommendations'])}")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
    
    print("\n3. Getting learning insights...")
    insights = system.get_learning_insights()
    print(f"Models Trained: {insights['system_status']['models_trained']}")
    print(f"Predictions Made: {insights['system_status']['predictions_made']}")
    
    print("\n4. Making a test prediction...")
    campaign_params = {
        'platform': 'Instagram',
        'budget': 10000,
        'content_type': 'Video',
        'duration_days': 30,
        'goal': 'conversions'
    }
    
    prediction = system.predict_campaign_performance(campaign_params)
    print(f"✓ Prediction made successfully")
    print(f"Predicted Engagement: {prediction['predictions']['engagement']['predicted_engagement_rate']}%")
    print(f"Confidence: {prediction['confidence']}")
    
    print("\n5. Generating data report...")
    data_report = system.generate_data_report()
    print(f"Data Directory: {data_report['data_directory']}")
    print(f"Datasets Available: {data_report['datasets_available']}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()