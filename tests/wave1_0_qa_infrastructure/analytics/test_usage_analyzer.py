"""
QA-132 to QA-136: Usage Analyzer Tests

Tests for the Analytics Subsystem - Usage Analyzer component.

Architectural Reference:
- Component: ANALYTICS-01 Metrics Dashboard
- Location: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- QA Range: QA-132 to QA-136 (5 QA components)

Expected State: RED (intentionally failing until implementation exists)
"""

import pytest
from datetime import datetime, timedelta


@pytest.mark.analytics
@pytest.mark.wave1_0
class TestUsageAnalyzer:
    """Test suite for Usage Analyzer component (QA-132 to QA-136)"""
    
    def test_qa_132_render_analytics_section(self, test_organisation_id, create_qa_evidence):
        """
        QA-132: Render analytics section
        
        Verify:
        - Key metrics display
        - Chart rendering
        - Time period selection
        
        Expected: FAIL - No analytics UI implementation exists yet
        """
        from foreman.analytics.usage_analyzer import UsageAnalyzer
        from foreman.ui.analytics_renderer import AnalyticsRenderer
        
        analyzer = UsageAnalyzer(organisation_id=test_organisation_id)
        renderer = AnalyticsRenderer()
        
        # Get analytics data
        analytics_data = analyzer.get_analytics_summary()
        
        # Render analytics section
        rendered_section = renderer.render_analytics_section(analytics_data)
        
        # Verify key metrics are displayed
        assert "builder_activations" in rendered_section, \
            "Analytics section must display builder activation count"
        assert "intent_submissions" in rendered_section, \
            "Analytics section must display intent submission count"
        assert "build_executions" in rendered_section, \
            "Analytics section must display build execution count"
        
        # Verify chart rendering
        assert rendered_section.get("charts") is not None, \
            "Analytics section must include charts"
        assert len(rendered_section["charts"]) > 0, \
            "Analytics section must render at least one chart"
        
        # Verify time period selection
        assert "time_period_selector" in rendered_section, \
            "Analytics section must include time period selector"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-132",
            "PASS",
            {
                "metrics_displayed": list(rendered_section.keys()),
                "chart_count": len(rendered_section.get("charts", [])),
                "time_periods_available": rendered_section.get("time_period_selector", {}).get("options", [])
            }
        )
    
    def test_qa_133_display_build_success_rate(self, test_organisation_id, create_qa_evidence):
        """
        QA-133: Display build success rate
        
        Verify:
        - Calculation of success rate
        - Trend visualization
        - Drill-down availability
        
        Expected: FAIL - No build success rate tracking implemented yet
        """
        from foreman.analytics.usage_analyzer import UsageAnalyzer
        from foreman.analytics.metrics_calculator import MetricsCalculator
        
        analyzer = UsageAnalyzer(organisation_id=test_organisation_id)
        calculator = MetricsCalculator()
        
        # Add test build data
        analyzer.record_build_completion(build_id="build-001", status="SUCCESS")
        analyzer.record_build_completion(build_id="build-002", status="SUCCESS")
        analyzer.record_build_completion(build_id="build-003", status="FAILURE")
        
        # Calculate success rate
        success_rate = calculator.calculate_build_success_rate(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        # Verify calculation
        assert success_rate is not None, \
            "Success rate calculation must return a value"
        assert 0 <= success_rate <= 100, \
            "Success rate must be between 0 and 100"
        assert abs(success_rate - 66.67) < 1, \
            "Success rate should be ~66.67% (2 of 3 builds successful)"
        
        # Verify trend visualization
        trend_data = calculator.get_success_rate_trend(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        assert trend_data is not None, \
            "Trend data must be available"
        assert "data_points" in trend_data, \
            "Trend must include data points"
        
        # Verify drill-down availability
        drill_down = analyzer.get_build_details_for_period(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        assert drill_down is not None, \
            "Drill-down data must be available"
        assert len(drill_down) == 3, \
            "Drill-down must include all 3 builds"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-133",
            "PASS",
            {
                "success_rate": success_rate,
                "trend_data_points": len(trend_data.get("data_points", [])),
                "drill_down_builds": len(drill_down)
            }
        )
    
    def test_qa_134_display_average_build_time(self, test_organisation_id, create_qa_evidence):
        """
        QA-134: Display average build time
        
        Verify:
        - Calculation of average build time
        - Comparison to baseline
        - Breakdown by wave
        
        Expected: FAIL - No build time tracking implemented yet
        """
        from foreman.analytics.usage_analyzer import UsageAnalyzer
        from foreman.analytics.metrics_calculator import MetricsCalculator
        
        analyzer = UsageAnalyzer(organisation_id=test_organisation_id)
        calculator = MetricsCalculator()
        
        # Record build times
        analyzer.record_build_time(build_id="build-001", wave="wave-1.0", duration_minutes=45)
        analyzer.record_build_time(build_id="build-002", wave="wave-1.0", duration_minutes=50)
        analyzer.record_build_time(build_id="build-003", wave="wave-1.1", duration_minutes=30)
        
        # Calculate average build time
        avg_time = calculator.calculate_average_build_time(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        # Verify calculation
        assert avg_time is not None, \
            "Average build time must be calculated"
        assert avg_time > 0, \
            "Average build time must be positive"
        assert abs(avg_time - 41.67) < 1, \
            "Average build time should be ~41.67 minutes"
        
        # Verify baseline comparison
        baseline = calculator.get_baseline_build_time(organisation_id=test_organisation_id)
        comparison = calculator.compare_to_baseline(avg_time, baseline)
        
        assert comparison is not None, \
            "Baseline comparison must be available"
        assert "percentage_difference" in comparison, \
            "Comparison must include percentage difference"
        
        # Verify breakdown by wave
        by_wave = calculator.get_build_time_by_wave(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        assert "wave-1.0" in by_wave, \
            "Breakdown must include wave-1.0"
        assert "wave-1.1" in by_wave, \
            "Breakdown must include wave-1.1"
        assert abs(by_wave["wave-1.0"] - 47.5) < 1, \
            "Wave 1.0 average should be ~47.5 minutes"
        assert abs(by_wave["wave-1.1"] - 30) < 1, \
            "Wave 1.1 average should be 30 minutes"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-134",
            "PASS",
            {
                "average_build_time_minutes": avg_time,
                "baseline_comparison": comparison,
                "breakdown_by_wave": by_wave
            }
        )
    
    def test_qa_135_display_cost_metrics(self, test_organisation_id, create_qa_evidence):
        """
        QA-135: Display cost metrics
        
        Verify:
        - Total cost display
        - Cost per build
        - Cost per QA component
        
        Expected: FAIL - No cost metrics implemented yet
        """
        from foreman.analytics.usage_analyzer import UsageAnalyzer
        from foreman.analytics.metrics_calculator import MetricsCalculator
        
        analyzer = UsageAnalyzer(organisation_id=test_organisation_id)
        calculator = MetricsCalculator()
        
        # Record cost data
        analyzer.record_build_cost(build_id="build-001", cost_usd=12.50, qa_components=50)
        analyzer.record_build_cost(build_id="build-002", cost_usd=15.00, qa_components=60)
        analyzer.record_build_cost(build_id="build-003", cost_usd=10.00, qa_components=40)
        
        # Calculate total cost
        total_cost = calculator.calculate_total_cost(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        # Verify total cost
        assert total_cost is not None, \
            "Total cost must be calculated"
        assert abs(total_cost - 37.50) < 0.01, \
            "Total cost should be $37.50"
        
        # Calculate cost per build
        cost_per_build = calculator.calculate_cost_per_build(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        assert cost_per_build is not None, \
            "Cost per build must be calculated"
        assert abs(cost_per_build - 12.50) < 0.01, \
            "Cost per build should be $12.50"
        
        # Calculate cost per QA component
        cost_per_qa = calculator.calculate_cost_per_qa_component(
            organisation_id=test_organisation_id,
            time_period="30d"
        )
        
        assert cost_per_qa is not None, \
            "Cost per QA component must be calculated"
        assert abs(cost_per_qa - 0.25) < 0.01, \
            "Cost per QA should be $0.25"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-135",
            "PASS",
            {
                "total_cost_usd": total_cost,
                "cost_per_build_usd": cost_per_build,
                "cost_per_qa_component_usd": cost_per_qa
            }
        )
    
    def test_qa_136_metrics_dashboard_failure_modes(self, test_organisation_id, create_qa_evidence):
        """
        QA-136: Metrics Dashboard failure modes
        
        Verify:
        - Data load failure UX
        - Calculation error handling
        
        Expected: FAIL - No failure mode handling implemented yet
        """
        from foreman.analytics.usage_analyzer import UsageAnalyzer
        from foreman.ui.analytics_renderer import AnalyticsRenderer
        from foreman.analytics.exceptions import DataLoadError, CalculationError
        
        analyzer = UsageAnalyzer(organisation_id=test_organisation_id)
        renderer = AnalyticsRenderer()
        
        # Test data load failure
        try:
            # Simulate data load failure by using invalid organisation_id
            analyzer_invalid = UsageAnalyzer(organisation_id="invalid-org")
            analytics_data = analyzer_invalid.get_analytics_summary()
            
            # Should not reach here if failure handling is correct
            assert False, "Data load failure should raise DataLoadError"
        except DataLoadError as e:
            # Verify error is properly caught and formatted
            assert str(e) != "", \
                "DataLoadError must have error message"
            
            # Verify error UX
            error_ui = renderer.render_error_state(e)
            assert error_ui is not None, \
                "Error UI must be rendered for data load failures"
            assert "retry_button" in error_ui, \
                "Error UI must include retry button"
            assert "error_message" in error_ui, \
                "Error UI must include user-friendly error message"
        
        # Test calculation error
        try:
            from foreman.analytics.metrics_calculator import MetricsCalculator
            calculator = MetricsCalculator()
            
            # Simulate calculation error (e.g., division by zero)
            success_rate = calculator.calculate_build_success_rate(
                organisation_id=test_organisation_id,
                time_period="30d"  # No data for this period
            )
            
            # If no data, should return 0 or None, not crash
            assert success_rate is not None or success_rate == 0, \
                "Calculator should handle no-data case gracefully"
        except CalculationError as e:
            # Verify calculation error handling
            assert str(e) != "", \
                "CalculationError must have error message"
            
            error_ui = renderer.render_calculation_error(e)
            assert error_ui is not None, \
                "Error UI must be rendered for calculation errors"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-136",
            "PASS",
            {
                "data_load_error_handled": True,
                "calculation_error_handled": True,
                "error_ui_available": True
            }
        )
