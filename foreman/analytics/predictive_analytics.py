"""
Predictive Analytics for Advanced Analytics Phase 2.

QA Coverage: QA-451 to QA-455
Provides predictive model initialization, prediction generation, accuracy tracking,
visualization, and error handling.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

# Shared storage for predictive models and predictions
_predictive_models = {}
_predictions = {}
_accuracy_metrics = {}


def clear_all():
    """Clear all predictive analytics state for testing."""
    global _predictive_models, _predictions, _accuracy_metrics
    _predictive_models = {}
    _predictions = {}
    _accuracy_metrics = {}


class PredictiveAnalytics:
    """Provides predictive analytics capabilities. QA-451 to QA-455"""
    
    def __init__(self, organisation_id: str):
        """
        Initialize predictive analytics for organisation.
        
        Args:
            organisation_id: Organisation ID for tenant isolation
        """
        self.organisation_id = organisation_id
        if organisation_id not in _predictive_models:
            _predictive_models[organisation_id] = {}
        if organisation_id not in _predictions:
            _predictions[organisation_id] = {}
        if organisation_id not in _accuracy_metrics:
            _accuracy_metrics[organisation_id] = {}
    
    def initialize_model(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initialize a predictive model. QA-451
        
        Args:
            model_config: Configuration for the model including type, parameters
        
        Returns:
            Model state with ID and status
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate configuration
        if not model_config.get('model_type'):
            raise ValueError("model_type is required")
        if not model_config.get('parameters'):
            raise ValueError("parameters are required")
        
        # Generate model ID
        model_id = f"model_{self.organisation_id}_{datetime.now().timestamp()}"
        
        # Initialize model state
        model_state = {
            "model_id": model_id,
            "status": "initialized",
            "config": model_config,
            "organisation_id": self.organisation_id,
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        # Store model
        _predictive_models[self.organisation_id][model_id] = model_state
        
        return model_state
    
    def generate_prediction(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate prediction using a model. QA-452
        
        Args:
            model_id: ID of the model to use
            input_data: Input data for prediction
        
        Returns:
            Prediction with value, confidence, and metadata
        
        Raises:
            ValueError: If model not found or input invalid
        """
        # Validate model exists
        if model_id not in _predictive_models[self.organisation_id]:
            raise ValueError(f"Model {model_id} not found")
        
        model = _predictive_models[self.organisation_id][model_id]
        
        # Validate model is ready
        if model["status"] not in ["initialized", "trained"]:
            raise ValueError(f"Model {model_id} is not ready for predictions")
        
        # Validate input data
        if not input_data.get('features'):
            raise ValueError("features are required for prediction")
        
        # Generate prediction (simplified algorithm)
        features = input_data['features']
        
        # Simple prediction logic based on feature values
        if isinstance(features, list):
            predicted_value = sum(features) / len(features) if features else 0.0
        else:
            predicted_value = 0.0
        
        # Calculate confidence (higher for more features)
        confidence = min(len(features) / 10.0, 0.95) if isinstance(features, list) else 0.5
        
        # Create prediction record
        prediction_id = f"pred_{model_id}_{datetime.now().timestamp()}"
        prediction = {
            "prediction_id": prediction_id,
            "model_id": model_id,
            "predicted_value": predicted_value,
            "confidence": confidence,
            "input_data": input_data,
            "timestamp": datetime.now().isoformat(),
            "organisation_id": self.organisation_id
        }
        
        # Store prediction
        _predictions[self.organisation_id][prediction_id] = prediction
        
        return prediction
    
    def track_accuracy(self, prediction_id: str, actual_value: float) -> Dict[str, Any]:
        """
        Track prediction accuracy. QA-453
        
        Args:
            prediction_id: ID of the prediction
            actual_value: Actual observed value
        
        Returns:
            Accuracy metrics including error and accuracy score
        
        Raises:
            ValueError: If prediction not found
        """
        # Validate prediction exists
        if prediction_id not in _predictions[self.organisation_id]:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        prediction = _predictions[self.organisation_id][prediction_id]
        predicted_value = prediction["predicted_value"]
        
        # Calculate error metrics
        absolute_error = abs(predicted_value - actual_value)
        relative_error = (absolute_error / abs(actual_value)) if actual_value != 0 else 0.0
        
        # Calculate accuracy score (inverse of relative error, capped at 1.0)
        accuracy = max(0.0, 1.0 - relative_error)
        
        # Store accuracy metrics
        accuracy_record = {
            "prediction_id": prediction_id,
            "model_id": prediction["model_id"],
            "predicted_value": predicted_value,
            "actual_value": actual_value,
            "absolute_error": absolute_error,
            "relative_error": relative_error,
            "accuracy": accuracy,
            "tracked_at": datetime.now().isoformat()
        }
        
        _accuracy_metrics[self.organisation_id][prediction_id] = accuracy_record
        
        # Update model accuracy statistics
        model_id = prediction["model_id"]
        model = _predictive_models[self.organisation_id].get(model_id)
        if model:
            if "accuracy_stats" not in model:
                model["accuracy_stats"] = {
                    "total_predictions": 0,
                    "total_accuracy": 0.0,
                    "average_accuracy": 0.0
                }
            
            stats = model["accuracy_stats"]
            stats["total_predictions"] += 1
            stats["total_accuracy"] += accuracy
            stats["average_accuracy"] = stats["total_accuracy"] / stats["total_predictions"]
        
        return accuracy_record
    
    def prepare_prediction_visualization(self, model_id: str, historical_predictions: List[str]) -> Dict[str, Any]:
        """
        Prepare visualization data for predictions. QA-454
        
        Args:
            model_id: Model ID
            historical_predictions: List of prediction IDs to visualize
        
        Returns:
            Visualization data with predicted vs actual values
        """
        viz_data = {
            "model_id": model_id,
            "predictions": [],
            "accuracy_trend": [],
            "chart_config": {
                "type": "scatter",
                "x_axis": "Predicted Value",
                "y_axis": "Actual Value"
            }
        }
        
        for pred_id in historical_predictions:
            prediction = _predictions[self.organisation_id].get(pred_id)
            accuracy = _accuracy_metrics[self.organisation_id].get(pred_id)
            
            if prediction and accuracy:
                viz_data["predictions"].append({
                    "predicted": prediction["predicted_value"],
                    "actual": accuracy["actual_value"],
                    "confidence": prediction["confidence"],
                    "timestamp": prediction["timestamp"]
                })
                
                viz_data["accuracy_trend"].append({
                    "timestamp": accuracy["tracked_at"],
                    "accuracy": accuracy["accuracy"]
                })
        
        return viz_data
    
    def handle_prediction_error(self, model_id: str, error_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle prediction errors. QA-455
        
        Args:
            model_id: Model ID where error occurred
            error_context: Context information about the error
        
        Returns:
            Error handling result with recovery actions
        """
        error_type = error_context.get('error_type', 'unknown')
        error_message = error_context.get('error_message', '')
        
        # Determine recovery action based on error type
        if error_type == 'invalid_input':
            recovery_action = "validate_and_retry"
            fallback_strategy = "use_default_values"
        elif error_type == 'model_not_ready':
            recovery_action = "initialize_model"
            fallback_strategy = "use_baseline_prediction"
        elif error_type == 'insufficient_data':
            recovery_action = "collect_more_data"
            fallback_strategy = "use_historical_average"
        else:
            recovery_action = "log_and_alert"
            fallback_strategy = "skip_prediction"
        
        # Create error record
        error_record = {
            "model_id": model_id,
            "error_type": error_type,
            "error_message": error_message,
            "recovery_action": recovery_action,
            "fallback_strategy": fallback_strategy,
            "timestamp": datetime.now().isoformat(),
            "organisation_id": self.organisation_id,
            "handled": True
        }
        
        # Update model status if needed
        if model_id in _predictive_models[self.organisation_id]:
            model = _predictive_models[self.organisation_id][model_id]
            if "error_count" not in model:
                model["error_count"] = 0
            model["error_count"] += 1
            model["last_error"] = error_record
        
        return error_record
