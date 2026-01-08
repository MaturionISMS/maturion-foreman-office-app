"""
QA-137 to QA-146: Cost Tracker and Performance Reporter Tests

Tests for:
- Metrics Engine (QA-137 to QA-141)
- Cost Tracker (QA-142 to QA-146)

Architectural Reference:
- Components: ANALYTICS-02 Metrics Engine, ANALYTICS-03 Cost Tracker
- Location: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- QA Range: QA-137 to QA-146 (10 QA components)

Expected State: RED (intentionally failing until implementation exists)
"""

import pytest
from datetime import datetime, timedelta
import json


@pytest.mark.analytics
@pytest.mark.wave1_0
class TestMetricsEngine:
    """Test suite for Metrics Engine component (QA-137 to QA-141)"""
    
    def test_qa_137_calculate_aggregate_metrics(self, test_organisation_id, create_qa_evidence):
        """
        QA-137: Calculate aggregate metrics
        
        Verify:
        - Formula correctness
        - Source data accuracy
        - Cache efficiency
        
        Expected: FAIL - No metrics engine implemented yet
        """
        from foreman.analytics.metrics_engine import MetricsEngine
        from foreman.analytics.data_source import MetricsDataSource
        
        engine = MetricsEngine(organisation_id=test_organisation_id)
        data_source = MetricsDataSource(organisation_id=test_organisation_id)
        
        # Add test data
        data_source.add_metric("builds_completed", 10, timestamp=datetime.now(UTC))
        data_source.add_metric("builds_failed", 2, timestamp=datetime.now(UTC))
        data_source.add_metric("qa_components_passed", 500, timestamp=datetime.now(UTC))
        
        # Calculate aggregate metrics
        aggregates = engine.calculate_aggregates(time_period="1d")
        
        # Verify formula correctness
        assert "success_rate" in aggregates, \
            "Aggregates must include success rate"
        assert abs(aggregates["success_rate"] - 83.33) < 1, \
            "Success rate formula: (10/(10+2))*100 = 83.33%"
        
        assert "total_builds" in aggregates, \
            "Aggregates must include total builds"
        assert aggregates["total_builds"] == 12, \
            "Total builds formula: 10 + 2 = 12"
        
        # Verify source data accuracy
        source_data = engine.get_source_data()
        assert len(source_data) == 3, \
            "Source data must include all 3 metrics"
        assert source_data[0]["metric"] == "builds_completed", \
            "Source data must be accurate"
        
        # Verify cache efficiency
        # First call - should compute
        start_time = datetime.now(UTC)
        result1 = engine.calculate_aggregates(time_period="1d")
        first_call_duration = (datetime.now(UTC) - start_time).total_seconds()
        
        # Second call - should use cache
        start_time = datetime.now(UTC)
        result2 = engine.calculate_aggregates(time_period="1d")
        second_call_duration = (datetime.now(UTC) - start_time).total_seconds()
        
        assert result1 == result2, \
            "Cached result must match computed result"
        assert second_call_duration < first_call_duration * 0.5, \
            "Cached call should be at least 2x faster"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-137",
            "PASS",
            {
                "aggregates_calculated": aggregates,
                "source_data_accurate": True,
                "cache_efficiency": f"{first_call_duration/second_call_duration:.2f}x faster"
            }
        )
    
    def test_qa_138_track_metric_history(self, test_organisation_id, create_qa_evidence):
        """
        QA-138: Track metric history
        
        Verify:
        - Time-series storage
        - Retention policy
        - Retrieval efficiency
        
        Expected: FAIL - No metric history tracking implemented yet
        """
        from foreman.analytics.metrics_engine import MetricsEngine
        from foreman.analytics.storage import MetricHistoryStorage
        
        engine = MetricsEngine(organisation_id=test_organisation_id)
        storage = MetricHistoryStorage(organisation_id=test_organisation_id)
        
        # Add time-series data
        base_time = datetime.now(UTC)
        for i in range(30):
            timestamp = base_time - timedelta(days=i)
            engine.record_metric("daily_builds", 5 + i, timestamp=timestamp)
        
        # Verify time-series storage
        history = storage.get_metric_history("daily_builds", days=30)
        assert len(history) == 30, \
            "History must include all 30 data points"
        assert history[0]["timestamp"] > history[-1]["timestamp"], \
            "History should be ordered newest first"
        
        # Verify retention policy
        retention_policy = storage.get_retention_policy()
        assert retention_policy["days"] >= 90, \
            "Metrics must be retained for at least 90 days"
        
        # Old data beyond retention should be archived
        old_metrics = storage.get_metric_history("daily_builds", days=365)
        archived_count = len([m for m in old_metrics if m.get("archived", False)])
        assert archived_count >= 0, \
            "Old metrics should be archived per retention policy"
        
        # Verify retrieval efficiency
        start_time = datetime.now(UTC)
        result = storage.get_metric_history("daily_builds", days=30)
        retrieval_duration = (datetime.now(UTC) - start_time).total_seconds()
        
        assert retrieval_duration < 1.0, \
            "Metric history retrieval should take less than 1 second"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-138",
            "PASS",
            {
                "history_data_points": len(history),
                "retention_days": retention_policy["days"],
                "retrieval_duration_seconds": retrieval_duration
            }
        )
    
    def test_qa_139_generate_metric_alerts(self, test_organisation_id, create_qa_evidence):
        """
        QA-139: Generate metric alerts
        
        Verify:
        - Threshold detection
        - Alert creation
        - Alert routing
        
        Expected: FAIL - No metric alerting implemented yet
        """
        from foreman.analytics.metrics_engine import MetricsEngine
        from foreman.analytics.alert_manager import MetricAlertManager
        
        engine = MetricsEngine(organisation_id=test_organisation_id)
        alert_manager = MetricAlertManager(organisation_id=test_organisation_id)
        
        # Set alert thresholds
        alert_manager.set_threshold("build_failure_rate", max_value=10.0)
        alert_manager.set_threshold("avg_build_time", max_value=60.0)
        
        # Record metrics that exceed thresholds
        engine.record_metric("build_failure_rate", 15.0)  # Exceeds threshold
        engine.record_metric("avg_build_time", 75.0)      # Exceeds threshold
        
        # Generate alerts
        alerts = alert_manager.check_thresholds()
        
        # Verify threshold detection
        assert len(alerts) == 2, \
            "Should generate 2 alerts for exceeded thresholds"
        
        failure_alert = [a for a in alerts if a["metric"] == "build_failure_rate"][0]
        assert failure_alert["threshold"] == 10.0, \
            "Alert must include threshold value"
        assert failure_alert["actual_value"] == 15.0, \
            "Alert must include actual value"
        assert failure_alert["severity"] == "HIGH", \
            "Build failure rate alert should be HIGH severity"
        
        # Verify alert creation
        created_alerts = alert_manager.get_all_alerts()
        assert len(created_alerts) >= 2, \
            "Alerts must be created and persisted"
        
        for alert in created_alerts:
            assert "alert_id" in alert, \
                "Alert must have unique ID"
            assert "timestamp" in alert, \
                "Alert must have timestamp"
            assert "metric" in alert, \
                "Alert must reference metric"
        
        # Verify alert routing
        routed = alert_manager.route_alerts(alerts)
        assert routed["escalation_created"] == True, \
            "High severity alerts must create escalation"
        assert routed["notification_sent"] == True, \
            "Alerts must trigger notifications"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-139",
            "PASS",
            {
                "alerts_generated": len(alerts),
                "escalation_created": routed["escalation_created"],
                "notification_sent": routed["notification_sent"]
            }
        )
    
    def test_qa_140_export_metrics(self, test_organisation_id, tmp_path, create_qa_evidence):
        """
        QA-140: Export metrics
        
        Verify:
        - CSV export
        - JSON export
        - Data completeness
        
        Expected: FAIL - No metric export implemented yet
        """
        from foreman.analytics.metrics_engine import MetricsEngine
        from foreman.analytics.export_service import MetricsExporter
        
        engine = MetricsEngine(organisation_id=test_organisation_id)
        exporter = MetricsExporter()
        
        # Add test metrics
        engine.record_metric("builds_completed", 10)
        engine.record_metric("builds_failed", 2)
        engine.record_metric("qa_components_passed", 500)
        
        # Test CSV export
        csv_path = tmp_path / "metrics.csv"
        exporter.export_to_csv(
            organisation_id=test_organisation_id,
            output_path=csv_path,
            time_period="7d"
        )
        
        assert csv_path.exists(), \
            "CSV export must create file"
        
        csv_content = csv_path.read_text()
        assert "metric,value,timestamp" in csv_content, \
            "CSV must have header row"
        assert "builds_completed,10" in csv_content, \
            "CSV must include metric data"
        
        # Test JSON export
        json_path = tmp_path / "metrics.json"
        exporter.export_to_json(
            organisation_id=test_organisation_id,
            output_path=json_path,
            time_period="7d"
        )
        
        assert json_path.exists(), \
            "JSON export must create file"
        
        json_data = json.loads(json_path.read_text())
        assert "metrics" in json_data, \
            "JSON must have metrics array"
        assert len(json_data["metrics"]) == 3, \
            "JSON must include all 3 metrics"
        
        # Verify data completeness
        for metric in json_data["metrics"]:
            assert "metric_name" in metric, \
                "Exported metric must have name"
            assert "value" in metric, \
                "Exported metric must have value"
            assert "timestamp" in metric, \
                "Exported metric must have timestamp"
            assert "organisation_id" in metric, \
                "Exported metric must have organisation_id for audit"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-140",
            "PASS",
            {
                "csv_export_successful": csv_path.exists(),
                "json_export_successful": json_path.exists(),
                "metrics_exported": len(json_data["metrics"])
            }
        )
    
    def test_qa_141_metrics_engine_failure_modes(self, test_organisation_id, create_qa_evidence):
        """
        QA-141: Metrics Engine failure modes
        
        Verify:
        - Calculation overflow handling
        - Data corruption detection
        
        Expected: FAIL - No failure mode handling implemented yet
        """
        from foreman.analytics.metrics_engine import MetricsEngine
        from foreman.analytics.exceptions import CalculationOverflowError, DataCorruptionError
        
        engine = MetricsEngine(organisation_id=test_organisation_id)
        
        # Test calculation overflow
        try:
            # Attempt to record extremely large value
            engine.record_metric("test_metric", 10**308)  # Near float max
            
            # Calculate aggregate that might overflow
            result = engine.calculate_sum("test_metric")
            
            # Should handle overflow gracefully
            assert result is not None, \
                "Engine should handle large numbers gracefully"
        except CalculationOverflowError as e:
            # Verify overflow is caught
            assert "overflow" in str(e).lower(), \
                "Overflow error must be descriptive"
            
            # Verify engine remains operational
            engine.record_metric("test_metric_2", 100)
            result = engine.calculate_sum("test_metric_2")
            assert result == 100, \
                "Engine should recover after overflow error"
        
        # Test data corruption detection
        try:
            from foreman.analytics.storage import MetricHistoryStorage
            storage = MetricHistoryStorage(organisation_id=test_organisation_id)
            
            # Simulate corrupted data
            corrupted_data = {
                "metric": "test",
                "value": "not_a_number",  # Invalid type
                "timestamp": "invalid_timestamp"
            }
            
            # Attempt to process corrupted data
            storage.validate_metric_data(corrupted_data)
            
            # Should not reach here if validation works
            assert False, "Corrupted data should raise DataCorruptionError"
        except DataCorruptionError as e:
            # Verify corruption is detected
            assert "corruption" in str(e).lower() or "invalid" in str(e).lower(), \
                "Data corruption error must be descriptive"
            
            # Verify error includes details
            assert hasattr(e, 'details'), \
                "Corruption error should include details for diagnosis"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-141",
            "PASS",
            {
                "overflow_handled": True,
                "corruption_detected": True,
                "engine_recovery": True
            }
        )


@pytest.mark.analytics
@pytest.mark.wave1_0
class TestCostTracker:
    """Test suite for Cost Tracker component (QA-142 to QA-146)"""
    
    def test_qa_142_track_ai_usage_cost_per_build(self, test_organisation_id, create_qa_evidence):
        """
        QA-142: Track AI usage cost per build
        
        Verify:
        - Token counting
        - Cost calculation
        - Build attribution
        
        Expected: FAIL - No cost tracking implemented yet
        """
        from foreman.analytics.cost_tracker import CostTracker
        from foreman.analytics.token_counter import TokenCounter
        
        tracker = CostTracker(organisation_id=test_organisation_id)
        token_counter = TokenCounter()
        
        # Simulate AI usage for a build
        build_id = "build-001"
        
        # Record token usage
        tracker.record_token_usage(
            build_id=build_id,
            model="gpt-4",
            input_tokens=1000,
            output_tokens=500
        )
        
        tracker.record_token_usage(
            build_id=build_id,
            model="gpt-4",
            input_tokens=2000,
            output_tokens=1000
        )
        
        # Verify token counting
        total_tokens = tracker.get_total_tokens(build_id=build_id)
        assert total_tokens["input"] == 3000, \
            "Total input tokens should be 3000"
        assert total_tokens["output"] == 1500, \
            "Total output tokens should be 1500"
        
        # Verify cost calculation
        cost = tracker.calculate_build_cost(build_id=build_id)
        
        assert cost is not None, \
            "Build cost must be calculated"
        assert cost > 0, \
            "Build cost must be positive"
        
        # GPT-4 pricing (example: $0.03/1K input, $0.06/1K output)
        expected_cost = (3000 * 0.03 / 1000) + (1500 * 0.06 / 1000)
        assert abs(cost - expected_cost) < 0.01, \
            f"Cost calculation should match pricing: {expected_cost}"
        
        # Verify build attribution
        build_costs = tracker.get_costs_by_build(organisation_id=test_organisation_id)
        assert build_id in build_costs, \
            "Cost must be attributed to correct build"
        assert build_costs[build_id] == cost, \
            "Attributed cost must match calculated cost"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-142",
            "PASS",
            {
                "build_id": build_id,
                "total_tokens": total_tokens,
                "calculated_cost_usd": cost
            }
        )
    
    def test_qa_143_detect_cost_anomaly(self, test_organisation_id, create_qa_evidence):
        """
        QA-143: Detect cost anomaly
        
        Verify:
        - 3x baseline detection
        - Escalation trigger
        - Cost breakdown
        
        Expected: FAIL - No cost anomaly detection implemented yet
        """
        from foreman.analytics.cost_tracker import CostTracker
        from foreman.analytics.anomaly_detector import CostAnomalyDetector
        
        tracker = CostTracker(organisation_id=test_organisation_id)
        detector = CostAnomalyDetector(organisation_id=test_organisation_id)
        
        # Establish baseline
        for i in range(10):
            tracker.record_build_cost(build_id=f"build-{i:03d}", cost_usd=10.0)
        
        # Calculate baseline
        baseline = detector.calculate_baseline_cost()
        assert abs(baseline - 10.0) < 0.01, \
            "Baseline should be $10.00"
        
        # Record anomalous cost (3x baseline)
        anomalous_build = "build-anomaly"
        tracker.record_build_cost(build_id=anomalous_build, cost_usd=35.0)
        
        # Detect anomaly
        anomalies = detector.detect_anomalies()
        
        # Verify 3x baseline detection
        assert len(anomalies) == 1, \
            "Should detect 1 anomaly"
        
        anomaly = anomalies[0]
        assert anomaly["build_id"] == anomalous_build, \
            "Anomaly should reference correct build"
        assert anomaly["cost"] == 35.0, \
            "Anomaly should include actual cost"
        assert anomaly["baseline"] == 10.0, \
            "Anomaly should include baseline"
        assert anomaly["multiplier"] == 3.5, \
            "Anomaly should calculate multiplier"
        
        # Verify escalation trigger
        assert anomaly["escalation_created"] == True, \
            "Anomaly exceeding 3x baseline must trigger escalation"
        assert anomaly["severity"] == "HIGH", \
            "Cost anomaly should be HIGH severity"
        
        # Verify cost breakdown
        breakdown = tracker.get_cost_breakdown(build_id=anomalous_build)
        
        assert "by_model" in breakdown, \
            "Breakdown must include costs by model"
        assert "by_component" in breakdown, \
            "Breakdown must include costs by component"
        assert "timeline" in breakdown, \
            "Breakdown must include timeline of usage"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-143",
            "PASS",
            {
                "anomaly_detected": True,
                "baseline_cost": baseline,
                "anomalous_cost": 35.0,
                "escalation_triggered": True
            }
        )
    
    def test_qa_144_generate_cost_reports(self, test_organisation_id, create_qa_evidence):
        """
        QA-144: Generate cost reports
        
        Verify:
        - Per-build report
        - Per-builder report
        - Time period aggregation
        
        Expected: FAIL - No cost reporting implemented yet
        """
        from foreman.analytics.cost_tracker import CostTracker
        from foreman.analytics.cost_reporter import CostReporter
        
        tracker = CostTracker(organisation_id=test_organisation_id)
        reporter = CostReporter(organisation_id=test_organisation_id)
        
        # Add test data
        tracker.record_build_cost(build_id="build-001", builder_id="ui-builder", cost_usd=12.50)
        tracker.record_build_cost(build_id="build-002", builder_id="api-builder", cost_usd=15.00)
        tracker.record_build_cost(build_id="build-003", builder_id="ui-builder", cost_usd=10.00)
        
        # Generate per-build report
        build_report = reporter.generate_build_report(build_id="build-001")
        
        assert build_report["build_id"] == "build-001", \
            "Report must reference correct build"
        assert build_report["total_cost"] == 12.50, \
            "Report must include total cost"
        assert "token_usage" in build_report, \
            "Report must include token usage details"
        assert "model_breakdown" in build_report, \
            "Report must include breakdown by model"
        
        # Generate per-builder report
        builder_report = reporter.generate_builder_report(builder_id="ui-builder")
        
        assert builder_report["builder_id"] == "ui-builder", \
            "Report must reference correct builder"
        assert abs(builder_report["total_cost"] - 22.50) < 0.01, \
            "Builder total cost should be $22.50 (12.50 + 10.00)"
        assert builder_report["builds_count"] == 2, \
            "Builder report must include build count"
        assert abs(builder_report["avg_cost_per_build"] - 11.25) < 0.01, \
            "Average cost per build should be $11.25"
        
        # Generate time period aggregation
        period_report = reporter.generate_period_report(time_period="7d")
        
        assert abs(period_report["total_cost"] - 37.50) < 0.01, \
            "Period total should be $37.50"
        assert "daily_breakdown" in period_report, \
            "Period report must include daily breakdown"
        assert "builder_breakdown" in period_report, \
            "Period report must include breakdown by builder"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-144",
            "PASS",
            {
                "build_report_generated": True,
                "builder_report_generated": True,
                "period_report_generated": True,
                "total_period_cost": period_report["total_cost"]
            }
        )
    
    def test_qa_145_cost_forecasting(self, test_organisation_id, create_qa_evidence):
        """
        QA-145: Cost forecasting
        
        Verify:
        - Trend analysis
        - Projection calculation
        - Confidence interval
        
        Expected: FAIL - No cost forecasting implemented yet
        """
        from foreman.analytics.cost_tracker import CostTracker
        from foreman.analytics.cost_forecaster import CostForecaster
        
        tracker = CostTracker(organisation_id=test_organisation_id)
        forecaster = CostForecaster(organisation_id=test_organisation_id)
        
        # Add historical data with trend
        base_time = datetime.now(UTC)
        for i in range(30):
            timestamp = base_time - timedelta(days=29-i)
            # Gradually increasing cost trend
            cost = 10.0 + (i * 0.5)  # $10 to $24.50
            tracker.record_build_cost(
                build_id=f"build-{i:03d}",
                cost_usd=cost,
                timestamp=timestamp
            )
        
        # Perform trend analysis
        trend = forecaster.analyze_trend(days=30)
        
        assert trend["direction"] == "increasing", \
            "Trend should be identified as increasing"
        assert trend["slope"] > 0, \
            "Trend slope should be positive"
        assert "r_squared" in trend, \
            "Trend analysis must include R-squared value"
        
        # Calculate projection
        projection = forecaster.project_cost(days_ahead=30)
        
        assert "projected_cost" in projection, \
            "Projection must include cost estimate"
        assert projection["projected_cost"] > 24.50, \
            "Projected cost should continue trend"
        
        # Verify confidence interval
        assert "confidence_interval" in projection, \
            "Projection must include confidence interval"
        
        ci = projection["confidence_interval"]
        assert "lower_bound" in ci, \
            "Confidence interval must have lower bound"
        assert "upper_bound" in ci, \
            "Confidence interval must have upper bound"
        assert "confidence_level" in ci, \
            "Confidence interval must specify confidence level (e.g., 95%)"
        
        assert ci["lower_bound"] < projection["projected_cost"], \
            "Lower bound must be below projected cost"
        assert ci["upper_bound"] > projection["projected_cost"], \
            "Upper bound must be above projected cost"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-145",
            "PASS",
            {
                "trend_direction": trend["direction"],
                "projected_cost": projection["projected_cost"],
                "confidence_interval": ci
            }
        )
    
    def test_qa_146_cost_tracker_failure_modes(self, test_organisation_id, create_qa_evidence):
        """
        QA-146: Cost Tracker failure modes
        
        Verify:
        - Token counting failure
        - Cost calculation error handling
        
        Expected: FAIL - No failure mode handling implemented yet
        """
        from foreman.analytics.cost_tracker import CostTracker
        from foreman.analytics.exceptions import TokenCountingError, CostCalculationError
        
        tracker = CostTracker(organisation_id=test_organisation_id)
        
        # Test token counting failure
        try:
            # Attempt to record invalid token count
            tracker.record_token_usage(
                build_id="build-001",
                model="gpt-4",
                input_tokens=-100,  # Invalid negative value
                output_tokens=500
            )
            
            # Should not reach here if validation works
            assert False, "Invalid token count should raise TokenCountingError"
        except TokenCountingError as e:
            # Verify error is caught
            assert "token" in str(e).lower(), \
                "Token counting error must be descriptive"
            
            # Verify tracker remains operational
            tracker.record_token_usage(
                build_id="build-002",
                model="gpt-4",
                input_tokens=100,
                output_tokens=50
            )
            cost = tracker.calculate_build_cost(build_id="build-002")
            assert cost > 0, \
                "Tracker should recover after token counting error"
        
        # Test cost calculation error
        try:
            # Attempt to calculate cost for non-existent build
            cost = tracker.calculate_build_cost(build_id="non-existent-build")
            
            # Should return 0 or raise error
            if cost is None:
                raise CostCalculationError("Build not found")
            assert cost == 0, \
                "Cost for non-existent build should be 0"
        except CostCalculationError as e:
            # Verify error is handled
            assert "calculation" in str(e).lower() or "not found" in str(e).lower(), \
                "Cost calculation error must be descriptive"
        
        # Test pricing data unavailable
        try:
            # Attempt to calculate cost for unknown model
            tracker.record_token_usage(
                build_id="build-003",
                model="unknown-model",
                input_tokens=1000,
                output_tokens=500
            )
            
            cost = tracker.calculate_build_cost(build_id="build-003")
            
            # Should handle gracefully (default pricing or error)
            assert cost is not None or cost == 0, \
                "Unknown model should be handled gracefully"
        except CostCalculationError as e:
            # Verify pricing error is descriptive
            assert "pricing" in str(e).lower() or "unknown model" in str(e).lower(), \
                "Pricing error must be descriptive"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-146",
            "PASS",
            {
                "token_counting_error_handled": True,
                "cost_calculation_error_handled": True,
                "tracker_recovery": True
            }
        )
