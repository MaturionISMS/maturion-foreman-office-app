"""
Wave 2.0 QA Infrastructure — Subwave 2.6: Advanced Analytics Phase 2
QA Range: QA-446 to QA-460 (15 QA components)

Authority: BL-019 Emergency Corrective Action Plan
Purpose: QA-to-Red tests for Advanced Analytics Phase 2

Test Categories:
- Trend Analysis (QA-446 to QA-450)
- Predictive Analytics (QA-451 to QA-455)
- Custom Report Generation (QA-456 to QA-460)
"""

import pytest
import sys
from datetime import datetime, timedelta
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

from foreman.analytics.trend_analyzer import TrendAnalyzer
from foreman.analytics.predictive_analytics import PredictiveAnalytics
from foreman.analytics.report_generator import ReportGenerator


@pytest.mark.wave2
@pytest.mark.subwave_2_6
class TestTrendAnalysis:
    """QA-446 to QA-450: Trend Analysis"""

    def test_qa_446_trend_calculation(self):
        """QA-446: Trend calculation"""
        # Arrange
        organisation_id = "test_org_446"
        analyzer = TrendAnalyzer(organisation_id)
        
        data_points = [
            {"timestamp": "2026-01-01", "value": 10},
            {"timestamp": "2026-01-02", "value": 15},
            {"timestamp": "2026-01-03", "value": 20},
            {"timestamp": "2026-01-04", "value": 25}
        ]
        
        # Act
        trend = analyzer.calculate_trend("build_success_rate", data_points)
        
        # Assert
        assert trend is not None, "Trend result should be returned"
        assert "direction" in trend, "Trend should include direction"
        assert "slope" in trend, "Trend should include slope"
        assert "confidence" in trend, "Trend should include confidence"
        assert "data_point_count" in trend, "Trend should include data point count"
        assert trend["direction"] == "increasing", "Trend should be increasing"
        assert trend["slope"] > 0, "Slope should be positive for increasing trend"
        assert trend["data_point_count"] == 4, "Should count all data points"

    def test_qa_447_trend_visualization(self):
        """QA-447: Trend visualization"""
        # Arrange
        organisation_id = "test_org_447"
        analyzer = TrendAnalyzer(organisation_id)
        
        data_points = [
            {"timestamp": "2026-01-01", "value": 100},
            {"timestamp": "2026-01-02", "value": 110},
            {"timestamp": "2026-01-03", "value": 105}
        ]
        
        # Act
        viz_data = analyzer.prepare_visualization_data("cost_trend", data_points)
        
        # Assert
        assert viz_data is not None, "Visualization data should be returned"
        assert "series" in viz_data, "Should include series data"
        assert "x_axis" in viz_data, "Should include x-axis configuration"
        assert "y_axis" in viz_data, "Should include y-axis configuration"
        assert "chart_type" in viz_data, "Should include chart type"
        assert len(viz_data["series"]) > 0, "Should have at least one series"
        assert viz_data["chart_type"] == "line", "Should default to line chart for trends"

    def test_qa_448_trend_forecasting(self):
        """QA-448: Trend forecasting"""
        # Arrange
        organisation_id = "test_org_448"
        analyzer = TrendAnalyzer(organisation_id)
        
        data_points = [
            {"timestamp": "2026-01-01", "value": 50},
            {"timestamp": "2026-01-02", "value": 55},
            {"timestamp": "2026-01-03", "value": 60}
        ]
        
        # Act
        forecast = analyzer.forecast_trend("build_time", data_points, periods=3)
        
        # Assert
        assert forecast is not None, "Forecast should be returned"
        assert "forecast_values" in forecast, "Should include forecast values"
        assert "confidence_interval" in forecast, "Should include confidence intervals"
        assert "accuracy_estimate" in forecast, "Should include accuracy estimate"
        assert len(forecast["forecast_values"]) == 3, "Should forecast 3 periods"
        assert "lower" in forecast["confidence_interval"], "Should have lower bound"
        assert "upper" in forecast["confidence_interval"], "Should have upper bound"
        assert len(forecast["confidence_interval"]["lower"]) == 3, "Lower bounds for all periods"

    def test_qa_449_trend_anomaly_detection(self):
        """QA-449: Trend anomaly detection"""
        # Arrange
        organisation_id = "test_org_449"
        analyzer = TrendAnalyzer(organisation_id)
        
        # Normal data with one clear anomaly
        data_points = [
            {"timestamp": "2026-01-01", "value": 100},
            {"timestamp": "2026-01-02", "value": 105},
            {"timestamp": "2026-01-03", "value": 500},  # Clear anomaly
            {"timestamp": "2026-01-04", "value": 110},
            {"timestamp": "2026-01-05", "value": 107}
        ]
        
        # Act - use lower sensitivity to detect the anomaly
        anomalies = analyzer.detect_anomalies("cost_metric", data_points, sensitivity=1.5)
        
        # Assert
        assert anomalies is not None, "Anomalies result should be returned"
        assert isinstance(anomalies, list), "Anomalies should be a list"
        assert len(anomalies) > 0, "Should detect at least one anomaly"
        assert "timestamp" in anomalies[0], "Anomaly should have timestamp"
        assert "value" in anomalies[0], "Anomaly should have value"
        assert "deviation" in anomalies[0], "Anomaly should have deviation"
        assert "severity" in anomalies[0], "Anomaly should have severity"

    def test_qa_450_trend_comparison(self):
        """QA-450: Trend comparison"""
        # Arrange
        organisation_id = "test_org_450"
        analyzer = TrendAnalyzer(organisation_id)
        
        data_points_1 = [
            {"timestamp": "2026-01-01", "value": 10},
            {"timestamp": "2026-01-02", "value": 20},
            {"timestamp": "2026-01-03", "value": 30}
        ]
        
        data_points_2 = [
            {"timestamp": "2026-01-01", "value": 15},
            {"timestamp": "2026-01-02", "value": 25},
            {"timestamp": "2026-01-03", "value": 35}
        ]
        
        # Act
        comparison = analyzer.compare_trends(
            "metric_a", data_points_1,
            "metric_b", data_points_2
        )
        
        # Assert
        assert comparison is not None, "Comparison result should be returned"
        assert "trend_1" in comparison, "Should include first trend"
        assert "trend_2" in comparison, "Should include second trend"
        assert "correlation" in comparison, "Should include correlation"
        assert "divergence" in comparison, "Should include divergence"
        assert "relationship" in comparison, "Should classify relationship"
        assert comparison["trend_1"]["direction"] == "increasing", "Trend 1 should be increasing"
        assert comparison["trend_2"]["direction"] == "increasing", "Trend 2 should be increasing"


@pytest.mark.wave2
@pytest.mark.subwave_2_6
class TestPredictiveAnalytics:
    """QA-451 to QA-455: Predictive Analytics"""

    def test_qa_451_model_initialization(self):
        """QA-451: Predictive model initialization"""
        # Arrange
        organisation_id = "test_org_451"
        analytics = PredictiveAnalytics(organisation_id)
        
        model_config = {
            "model_type": "linear_regression",
            "parameters": {
                "learning_rate": 0.01,
                "epochs": 100
            }
        }
        
        # Act
        model_state = analytics.initialize_model(model_config)
        
        # Assert
        assert model_state is not None, "Model state should be returned"
        assert "model_id" in model_state, "Should have model ID"
        assert "status" in model_state, "Should have status"
        assert "config" in model_state, "Should store configuration"
        assert "organisation_id" in model_state, "Should include organisation_id"
        assert model_state["status"] == "initialized", "Status should be initialized"
        assert model_state["organisation_id"] == organisation_id, "Tenant isolation maintained"

    def test_qa_452_prediction_generation(self):
        """QA-452: Prediction generation"""
        # Arrange
        organisation_id = "test_org_452"
        analytics = PredictiveAnalytics(organisation_id)
        
        # Initialize model first
        model_config = {
            "model_type": "linear_regression",
            "parameters": {"learning_rate": 0.01}
        }
        model_state = analytics.initialize_model(model_config)
        model_id = model_state["model_id"]
        
        input_data = {
            "features": [1.0, 2.0, 3.0, 4.0, 5.0]
        }
        
        # Act
        prediction = analytics.generate_prediction(model_id, input_data)
        
        # Assert
        assert prediction is not None, "Prediction should be returned"
        assert "prediction_id" in prediction, "Should have prediction ID"
        assert "model_id" in prediction, "Should reference model"
        assert "predicted_value" in prediction, "Should have predicted value"
        assert "confidence" in prediction, "Should have confidence score"
        assert "timestamp" in prediction, "Should have timestamp"
        assert prediction["model_id"] == model_id, "Should match model ID"
        assert 0.0 <= prediction["confidence"] <= 1.0, "Confidence should be between 0 and 1"

    def test_qa_453_accuracy_tracking(self):
        """QA-453: Prediction accuracy tracking"""
        # Arrange
        organisation_id = "test_org_453"
        analytics = PredictiveAnalytics(organisation_id)
        
        # Initialize model and make prediction
        model_config = {"model_type": "linear_regression", "parameters": {"learning_rate": 0.01}}
        model_state = analytics.initialize_model(model_config)
        model_id = model_state["model_id"]
        
        input_data = {"features": [2.0, 4.0, 6.0]}
        prediction = analytics.generate_prediction(model_id, input_data)
        prediction_id = prediction["prediction_id"]
        
        actual_value = 4.5
        
        # Act
        accuracy_record = analytics.track_accuracy(prediction_id, actual_value)
        
        # Assert
        assert accuracy_record is not None, "Accuracy record should be returned"
        assert "prediction_id" in accuracy_record, "Should reference prediction"
        assert "actual_value" in accuracy_record, "Should have actual value"
        assert "predicted_value" in accuracy_record, "Should have predicted value"
        assert "absolute_error" in accuracy_record, "Should have absolute error"
        assert "relative_error" in accuracy_record, "Should have relative error"
        assert "accuracy" in accuracy_record, "Should have accuracy score"
        assert accuracy_record["actual_value"] == actual_value, "Should match actual value"
        assert 0.0 <= accuracy_record["accuracy"] <= 1.0, "Accuracy should be between 0 and 1"

    def test_qa_454_prediction_visualization(self):
        """QA-454: Prediction visualization"""
        # Arrange
        organisation_id = "test_org_454"
        analytics = PredictiveAnalytics(organisation_id)
        
        # Initialize model and make predictions
        model_config = {"model_type": "linear_regression", "parameters": {"learning_rate": 0.01}}
        model_state = analytics.initialize_model(model_config)
        model_id = model_state["model_id"]
        
        prediction_ids = []
        for i in range(3):
            input_data = {"features": [float(i), float(i+1)]}
            prediction = analytics.generate_prediction(model_id, input_data)
            prediction_ids.append(prediction["prediction_id"])
            # Track accuracy
            analytics.track_accuracy(prediction["prediction_id"], float(i) + 0.5)
        
        # Act
        viz_data = analytics.prepare_prediction_visualization(model_id, prediction_ids)
        
        # Assert
        assert viz_data is not None, "Visualization data should be returned"
        assert "model_id" in viz_data, "Should reference model"
        assert "predictions" in viz_data, "Should include predictions"
        assert "accuracy_trend" in viz_data, "Should include accuracy trend"
        assert "chart_config" in viz_data, "Should include chart configuration"
        assert len(viz_data["predictions"]) > 0, "Should have prediction data points"
        assert len(viz_data["accuracy_trend"]) > 0, "Should have accuracy trend data"

    def test_qa_455_prediction_error_handling(self):
        """QA-455: Prediction error handling"""
        # Arrange
        organisation_id = "test_org_455"
        analytics = PredictiveAnalytics(organisation_id)
        
        # Initialize model
        model_config = {"model_type": "linear_regression", "parameters": {"learning_rate": 0.01}}
        model_state = analytics.initialize_model(model_config)
        model_id = model_state["model_id"]
        
        error_context = {
            "error_type": "invalid_input",
            "error_message": "Missing required features"
        }
        
        # Act
        error_record = analytics.handle_prediction_error(model_id, error_context)
        
        # Assert
        assert error_record is not None, "Error record should be returned"
        assert "model_id" in error_record, "Should reference model"
        assert "error_type" in error_record, "Should have error type"
        assert "error_message" in error_record, "Should have error message"
        assert "recovery_action" in error_record, "Should have recovery action"
        assert "fallback_strategy" in error_record, "Should have fallback strategy"
        assert "handled" in error_record, "Should indicate handled status"
        assert error_record["handled"] == True, "Error should be marked as handled"
        assert error_record["recovery_action"] != "", "Should provide recovery action"


@pytest.mark.wave2
@pytest.mark.subwave_2_6
class TestCustomReportGeneration:
    """QA-456 to QA-460: Custom Report Generation"""

    def test_qa_456_template_creation(self):
        """QA-456: Report template creation"""
        # Arrange
        organisation_id = "test_org_456"
        generator = ReportGenerator(organisation_id)
        
        template_config = {
            "name": "Monthly Analytics Report",
            "sections": [
                {"name": "Summary", "type": "summary"},
                {"name": "Trends", "type": "chart"},
                {"name": "Details", "type": "table"}
            ],
            "formatting": {
                "page_size": "A4",
                "orientation": "portrait"
            }
        }
        
        # Act
        template = generator.create_template(template_config)
        
        # Assert
        assert template is not None, "Template should be returned"
        assert "template_id" in template, "Should have template ID"
        assert "name" in template, "Should have name"
        assert "sections" in template, "Should have sections"
        assert "formatting" in template, "Should have formatting"
        assert "organisation_id" in template, "Should include organisation_id"
        assert template["name"] == "Monthly Analytics Report", "Name should match"
        assert len(template["sections"]) == 3, "Should have 3 sections"
        assert template["organisation_id"] == organisation_id, "Tenant isolation maintained"

    def test_qa_457_data_aggregation(self):
        """QA-457: Report data aggregation"""
        # Arrange
        organisation_id = "test_org_457"
        generator = ReportGenerator(organisation_id)
        
        data_sources = [
            {
                "source": "builds",
                "data": [
                    {"value": 10, "category": "success"},
                    {"value": 20, "category": "success"}
                ]
            },
            {
                "source": "tests",
                "data": [
                    {"value": 15, "category": "passed"},
                    {"value": 25, "category": "passed"}
                ]
            }
        ]
        
        aggregation_rules = {
            "type": "sum",
            "group_by": "category"
        }
        
        # Act
        aggregated_data = generator.aggregate_data(data_sources, aggregation_rules)
        
        # Assert
        assert aggregated_data is not None, "Aggregated data should be returned"
        assert "aggregation_id" in aggregated_data, "Should have aggregation ID"
        assert "total_records" in aggregated_data, "Should have total record count"
        assert "aggregated_value" in aggregated_data, "Should have aggregated value"
        assert "grouped_results" in aggregated_data, "Should have grouped results"
        assert aggregated_data["total_records"] == 4, "Should count all records"
        assert aggregated_data["aggregated_value"] == 70, "Should sum all values (10+20+15+25)"

    def test_qa_458_report_rendering(self):
        """QA-458: Report rendering"""
        # Arrange
        organisation_id = "test_org_458"
        generator = ReportGenerator(organisation_id)
        
        # Create template
        template_config = {
            "name": "Test Report",
            "sections": [
                {"name": "Overview", "type": "summary", "metrics": [
                    {"key": "total_builds", "label": "Total Builds"}
                ]}
            ]
        }
        template = generator.create_template(template_config)
        template_id = template["template_id"]
        
        # Prepare data
        report_data = {
            "total_builds": 100,
            "success_rate": 95.5
        }
        
        # Act
        rendered_report = generator.render_report(template_id, report_data)
        
        # Assert
        assert rendered_report is not None, "Rendered report should be returned"
        assert "report_id" in rendered_report, "Should have report ID"
        assert "template_id" in rendered_report, "Should reference template"
        assert "sections" in rendered_report, "Should have rendered sections"
        assert "status" in rendered_report, "Should have status"
        assert rendered_report["status"] == "rendered", "Status should be rendered"
        assert len(rendered_report["sections"]) > 0, "Should have at least one section"
        assert rendered_report["template_id"] == template_id, "Should match template ID"

    def test_qa_459_report_export(self):
        """QA-459: Report export"""
        # Arrange
        organisation_id = "test_org_459"
        generator = ReportGenerator(organisation_id)
        
        # Create and render report
        template_config = {
            "name": "Export Test Report",
            "sections": [{"name": "Data", "type": "summary"}]
        }
        template = generator.create_template(template_config)
        report_data = {"metric": 42}
        rendered_report = generator.render_report(template["template_id"], report_data)
        report_id = rendered_report["report_id"]
        
        # Act
        export_result = generator.export_report(report_id, format="json")
        
        # Assert
        assert export_result is not None, "Export result should be returned"
        assert "report_id" in export_result, "Should reference report"
        assert "format" in export_result, "Should have format"
        assert "file_path" in export_result, "Should have file path"
        assert "file_size" in export_result, "Should have file size"
        assert "status" in export_result, "Should have status"
        assert export_result["format"] == "json", "Format should match"
        assert export_result["status"] == "completed", "Export should be completed"
        assert export_result["file_size"] > 0, "File should have content"

    def test_qa_460_report_scheduling(self):
        """QA-460: Report scheduling"""
        # Arrange
        organisation_id = "test_org_460"
        generator = ReportGenerator(organisation_id)
        
        # Create template
        template_config = {
            "name": "Scheduled Report",
            "sections": [{"name": "Summary", "type": "summary"}]
        }
        template = generator.create_template(template_config)
        template_id = template["template_id"]
        
        schedule_config = {
            "frequency": "daily",
            "recipients": ["admin@example.com", "team@example.com"],
            "format": "pdf"
        }
        
        # Act
        schedule = generator.schedule_report(template_id, schedule_config)
        
        # Assert
        assert schedule is not None, "Schedule should be returned"
        assert "schedule_id" in schedule, "Should have schedule ID"
        assert "template_id" in schedule, "Should reference template"
        assert "frequency" in schedule, "Should have frequency"
        assert "recipients" in schedule, "Should have recipients"
        assert "next_run" in schedule, "Should have next run time"
        assert "status" in schedule, "Should have status"
        assert schedule["status"] == "active", "Schedule should be active"
        assert schedule["frequency"] == "daily", "Frequency should match"
        assert len(schedule["recipients"]) == 2, "Should have all recipients"
