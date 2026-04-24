"""
Hybrid Learning System - Complete Version
Combines offline ML training on local datasets + real-time API adaptation
"""

from typing import Dict, Any, List
from data_manager import DataManager
from ml_models import MarketingPredictor
from datetime import datetime
import pandas as pd
import numpy as np


class HybridLearningSystem:
    """
    Complete Hybrid Intelligence System using local datasets
    """
    
    def __init__(self, data_folder: str = r"E:\destiny\data"):
        self.data_manager = DataManager(data_dir=data_folder)
        self.predictor = MarketingPredictor()
        
        self.training_history = []
        self.adaptation_history = []
        self.performance_metrics = {
            'predictions_made': 0,
            'adaptations_performed': 0,
            'accuracy_improvements': [],
            'datasets_used': []
        }
    
    def initialize_system(self, auto_train: bool = True, load_all: bool = True) -> Dict[str, Any]:
        """Initialize system with local data"""
        print("[HYBRID] Initializing Hybrid Learning System...")
        
        results = {
            'status': 'initializing',
            'datasets_loaded': [],
            'models_trained': [],
            'system_ready': False,
            'data_source': 'local_files'
        }
        
        # Try to load data
        print("[HYBRID] Loading local data files...")
        
        loaded_datasets = {}
        try:
            if load_all:
                all_datasets = self.data_manager.load_all_datasets()
                loaded_datasets = all_datasets
                
                for name, df in all_datasets.items():
                    if not df.empty:
                        results['datasets_loaded'].append({
                            'name': name,
                            'rows': len(df),
                            'columns': len(df.columns)
                        })
                        self.performance_metrics['datasets_used'].append(name)
                        print(f"[HYBRID] ✓ Loaded {name}: {len(df)} samples")
                    else:
                        print(f"[HYBRID] ⚠ {name} is empty")
            else:
                # Load specific datasets
                datasets_to_load = ['campaign_performance', 'ad_engagement', 'engagement_metrics']
                
                for dataset_name in datasets_to_load:
                    try:
                        df = self.data_manager.load_dataset(dataset_name)
                        if not df.empty:
                            loaded_datasets[dataset_name] = df
                            results['datasets_loaded'].append({
                                'name': dataset_name,
                                'rows': len(df),
                                'columns': len(df.columns)
                            })
                            self.performance_metrics['datasets_used'].append(dataset_name)
                            print(f"[HYBRID] ✓ Loaded {dataset_name}: {len(df)} samples")
                        else:
                            print(f"[HYBRID] ⚠ {dataset_name} is empty")
                    except Exception as e:
                        print(f"[HYBRID] ⚠ Failed to load {dataset_name}: {e}")
        except Exception as e:
            print(f"[HYBRID] Error loading datasets: {e}")
            loaded_datasets = {}
        
        # Train models
        if auto_train and loaded_datasets:
            print("[HYBRID] Training ML models on local data...")
            
            training_results = self.train_all_models(loaded_datasets)
            results['models_trained'] = training_results['models']
            results['training_performance'] = training_results['performance']
            
            if training_results['success']:
                results['system_ready'] = True
                results['status'] = 'ready'
                print("[HYBRID] ✓ System ready for predictions")
            else:
                results['status'] = 'partial'
                print("[HYBRID] ⚠ System partially ready")
        else:
            results['status'] = 'data_only' if loaded_datasets else 'failed'
            print("[HYBRID] Data loaded, models not trained")
        
        results['data_statistics'] = self.data_manager.get_dataset_statistics()
        
        return results
    
    def train_all_models(self, datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Train all ML models on available datasets"""
        
        results = {
            'success': False,
            'models': [],
            'performance': {}
        }
        
        # Train engagement model
        engagement_sources = ['engagement_metrics', 'viral_trends', 'ad_engagement']
        engagement_df = None
        
        for source in engagement_sources:
            if source in datasets and not datasets[source].empty:
                engagement_df = datasets[source]
                print(f"[HYBRID] Using {source} for engagement model")
                break
        
        if engagement_df is not None:
            try:
                eng_result = self.predictor.train_engagement_model(engagement_df)
                if eng_result['success']:
                    results['models'].append('engagement')
                    results['performance']['engagement'] = eng_result
                    
                    self.training_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'model': 'engagement',
                        'samples': len(engagement_df),
                        'performance': eng_result
                    })
            except Exception as e:
                print(f"[HYBRID] Error training engagement model: {e}")
        
        # Train conversion model
        conversion_sources = ['ad_engagement', 'campaign_performance', 'marketing_campaign']
        conversion_df = None
        
        for source in conversion_sources:
            if source in datasets and not datasets[source].empty:
                conversion_df = datasets[source]
                print(f"[HYBRID] Using {source} for conversion model")
                break
        
        if conversion_df is not None:
            try:
                conv_result = self.predictor.train_conversion_model(conversion_df)
                if conv_result['success']:
                    results['models'].append('conversion')
                    results['performance']['conversion'] = conv_result
                    
                    self.training_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'model': 'conversion',
                        'samples': len(conversion_df),
                        'performance': conv_result
                    })
            except Exception as e:
                print(f"[HYBRID] Error training conversion model: {e}")
        
        # Train ROI model
        roi_sources = ['campaign_performance', 'marketing_campaign']
        roi_df = None
        
        for source in roi_sources:
            if source in datasets and not datasets[source].empty:
                roi_df = datasets[source]
                print(f"[HYBRID] Using {source} for ROI model")
                break
        
        if roi_df is not None:
            try:
                roi_result = self.predictor.train_roi_model(roi_df)
                if roi_result['success']:
                    results['models'].append('roi')
                    results['performance']['roi'] = roi_result
                    
                    self.training_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'model': 'roi',
                        'samples': len(roi_df),
                        'performance': roi_result
                    })
            except Exception as e:
                print(f"[HYBRID] Error training ROI model: {e}")
        
        results['success'] = len(results['models']) > 0
        self.predictor.is_trained = results['success']
        
        return results
    
    def predict_campaign_performance(self, campaign_params: Dict[str, Any]) -> Dict[str, Any]:
        """Make hybrid prediction for campaign performance"""
        print("[HYBRID] Making hybrid prediction...")
        
        platform = campaign_params.get('platform', 'LinkedIn')
        budget = campaign_params.get('budget', 5000)
        content_type = campaign_params.get('content_type', 'Image')
        duration_days = campaign_params.get('duration_days', 30)
        
        # ML-based predictions
        engagement_pred = self.predictor.predict_engagement(
            platform=platform,
            content_type=content_type,
            budget=budget
        )
        
        # Estimate other metrics
        estimated_impressions = int(budget * 15)  # Average CPM-based
        engagement_rate = engagement_pred.get('predicted_engagement_rate', 2.5)
        estimated_clicks = int(estimated_impressions * engagement_rate / 100)
        
        conversion_pred = self.predictor.predict_conversion(
            platform=platform,
            budget=budget,
            impressions=estimated_impressions,
            clicks=estimated_clicks
        )
        
        roi_pred = self.predictor.predict_roi(
            budget=budget,
            impressions=estimated_impressions,
            engagement=estimated_clicks,
            leads=conversion_pred.get('predicted_conversions', 50)
        )
        
        # Get optimal strategy
        strategy = self.predictor.get_optimal_strategy(
            goal=campaign_params.get('goal', 'awareness'),
            budget=budget
        )
        
        prediction = {
            'campaign_params': campaign_params,
            'predictions': {
                'engagement': engagement_pred,
                'conversion': conversion_pred,
                'roi': roi_pred
            },
            'recommended_strategy': strategy,
            'confidence': self._calculate_confidence(),
            'prediction_timestamp': datetime.now().isoformat()
        }
        
        self.performance_metrics['predictions_made'] += 1
        
        return prediction
    
    def adapt_from_realtime_results(self, predicted: Dict[str, Any],
                                    actual: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt predictions based on real-time API results"""
        print("[HYBRID] Adapting from real-time results...")
        
        adaptation = {
            'timestamp': datetime.now().isoformat(),
            'predicted_values': {},
            'actual_values': {},
            'deltas': {},
            'adjustments': []
        }
        
        # Compare predictions with actuals
        metrics_to_check = ['engagement_rate', 'clicks', 'conversions', 'roi']
        
        for metric in metrics_to_check:
            # Try to find the metric in predictions and actuals
            pred_val = None
            actual_val = None
            
            # Check various locations for the metric
            if 'predictions' in predicted:
                for model_type, model_pred in predicted['predictions'].items():
                    if metric in model_pred:
                        pred_val = model_pred[metric]
                        break
                    elif f'predicted_{metric}' in model_pred:
                        pred_val = model_pred[f'predicted_{metric}']
                        break
            
            if metric in actual:
                actual_val = actual[metric]
            
            if pred_val is not None and actual_val is not None:
                delta = actual_val - pred_val
                delta_pct = (delta / pred_val * 100) if pred_val != 0 else 0
                
                adaptation['predicted_values'][metric] = pred_val
                adaptation['actual_values'][metric] = actual_val
                adaptation['deltas'][metric] = {
                    'absolute': delta,
                    'percentage': round(delta_pct, 2)
                }
                
                # Generate adjustment recommendations
                if abs(delta_pct) > 20:
                    adaptation['adjustments'].append({
                        'metric': metric,
                        'issue': f"Prediction off by {delta_pct:.1f}%",
                        'recommendation': self._generate_adjustment(metric, delta_pct)
                    })
        
        # Update predictor with real data
        self.predictor.update_with_realtime_data(actual)
        
        # Store adaptation history
        self.adaptation_history.append(adaptation)
        self.performance_metrics['adaptations_performed'] += 1
        
        # Calculate accuracy improvement
        if len(self.adaptation_history) > 1:
            accuracy_improvement = self._calculate_accuracy_trend()
            self.performance_metrics['accuracy_improvements'].append(accuracy_improvement)
        
        print(f"[HYBRID] Adaptation complete - {len(adaptation['adjustments'])} adjustments recommended")
        
        return adaptation
    
    def _generate_adjustment(self, metric: str, delta_pct: float) -> str:
        """Generate specific adjustment recommendation"""
        
        if metric == 'engagement_rate':
            if delta_pct < -20:
                return "Increase content quality, use more video, optimize posting times"
            else:
                return "Current content strategy performing well, maintain approach"
        
        elif metric == 'conversions':
            if delta_pct < -20:
                return "Strengthen CTAs, improve landing pages, better audience targeting"
            else:
                return "Conversion optimization working, scale budget"
        
        elif metric == 'roi':
            if delta_pct < -20:
                return "Reduce cost-per-click, focus on high-converting channels"
            else:
                return "ROI positive, increase investment in top performers"
        
        return "Monitor performance and adjust iteratively"
    
    def _calculate_confidence(self) -> str:
        """Calculate confidence level in predictions"""
        
        if not self.predictor.is_trained:
            return "low"
        
        if len(self.adaptation_history) > 5:
            return "high"
        elif len(self.adaptation_history) > 2:
            return "medium"
        elif len(self.training_history) > 0:
            return "fair"
        else:
            return "low"
    
    def _calculate_accuracy_trend(self) -> float:
        """Calculate if predictions are getting more accurate over time"""
        
        if len(self.adaptation_history) < 2:
            return 0.0
        
        # Compare recent vs older adaptations
        recent = self.adaptation_history[-3:] if len(self.adaptation_history) >= 3 else self.adaptation_history
        older_start = max(0, len(self.adaptation_history) - 6)
        older_end = max(0, len(self.adaptation_history) - 3)
        older = self.adaptation_history[older_start:older_end]
        
        if not older or not recent:
            return 0.0
        
        def avg_delta(adaptations):
            deltas = []
            for adapt in adaptations:
                for metric_deltas in adapt.get('deltas', {}).values():
                    if isinstance(metric_deltas, dict):
                        deltas.append(abs(metric_deltas.get('percentage', 0)))
            return sum(deltas) / len(deltas) if deltas else 0
        
        recent_avg_error = avg_delta(recent)
        older_avg_error = avg_delta(older)
        
        improvement = older_avg_error - recent_avg_error
        
        return round(improvement, 2)
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about the learning system"""
        
        insights = {
            'system_status': {
                'models_trained': len(self.predictor.models),
                'predictions_made': self.performance_metrics['predictions_made'],
                'adaptations_performed': self.performance_metrics['adaptations_performed'],
                'is_learning': len(self.adaptation_history) > 0,
                'datasets_used': self.performance_metrics['datasets_used']
            },
            'model_performance': self.predictor.get_model_status(),
            'learning_progress': {
                'training_sessions': len(self.training_history),
                'adaptation_sessions': len(self.adaptation_history),
                'accuracy_trend': self.performance_metrics['accuracy_improvements'][-5:] if self.performance_metrics['accuracy_improvements'] else []
            },
            'data_stats': self.data_manager.get_dataset_statistics()
        }
        
        # Add feature importance insights
        if hasattr(self.predictor, 'feature_importance') and self.predictor.feature_importance:
            insights['key_factors'] = {}
            
            for model_name, importance_dict in self.predictor.feature_importance.items():
                top_features = sorted(
                    importance_dict.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                
                insights['key_factors'][model_name] = [
                    {
                        'feature': feat[0],
                        'importance': round(feat[1], 3)
                    }
                    for feat in top_features
                ]
        
        return insights
    
    def generate_learning_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning report"""
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'system_overview': self.get_learning_insights(),
            'training_history': self.training_history[-5:] if self.training_history else [],
            'recent_adaptations': self.adaptation_history[-5:] if self.adaptation_history else [],
            'recommendations': []
        }
        
        # Generate recommendations
        insights = report['system_overview']
        
        if insights['system_status']['predictions_made'] < 10:
            report['recommendations'].append({
                'priority': 'high',
                'recommendation': 'Make more predictions to improve learning',
                'action': 'Run more campaigns to gather data'
            })
        
        if insights['system_status']['adaptations_performed'] < 5:
            report['recommendations'].append({
                'priority': 'medium',
                'recommendation': 'Compare predictions with actual results more frequently',
                'action': 'Enable real-time feedback loop'
            })
        
        if len(insights['learning_progress']['accuracy_trend']) > 3:
            avg_improvement = sum(insights['learning_progress']['accuracy_trend']) / len(insights['learning_progress']['accuracy_trend'])
            
            if avg_improvement > 0:
                report['recommendations'].append({
                    'priority': 'info',
                    'recommendation': f'System is learning! Accuracy improving by {avg_improvement:.1f}% per cycle',
                    'action': 'Continue current approach'
                })
            elif avg_improvement < 0:
                report['recommendations'].append({
                    'priority': 'warning',
                    'recommendation': f'Accuracy decreasing by {abs(avg_improvement):.1f}% per cycle',
                    'action': 'Review model training and data quality'
                })
        
        return report
    
    def generate_data_report(self) -> Dict[str, Any]:
        """Generate report about the data being used"""
        
        data_stats = self.data_manager.get_dataset_statistics()
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'data_source': 'local_csv_files',
            'data_directory': self.data_manager.data_dir,
            'datasets_available': data_stats.get('available_datasets', 0),
            'datasets_loaded': data_stats.get('loaded_datasets', 0),
            'local_files_count': data_stats.get('local_file_count', 0),
            'dataset_details': data_stats.get('dataset_details', {}),
            'recommendations': []
        }
        
        # Generate data quality recommendations
        if data_stats.get('loaded_datasets', 0) == 0:
            report['recommendations'].append({
                'priority': 'high',
                'issue': 'No datasets loaded',
                'solution': 'Check data directory path and file permissions'
            })
        
        if data_stats.get('loaded_datasets', 0) < 2:
            report['recommendations'].append({
                'priority': 'medium',
                'issue': 'Limited data sources',
                'solution': 'Load more datasets for better model accuracy'
            })
        
        return report