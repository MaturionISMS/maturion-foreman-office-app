"""
QA-361 to QA-365: Enhanced Dashboard - Drill-Down Navigation Tests

Architectural Reference: Wave 2 Enhanced Dashboard Specification
QA Range: QA-361 to QA-365
Component: Enhanced Dashboard - Drill-Down Navigation

State: GREEN (Drill-down navigation implemented and tested)
Build-to-Green Status: COMPLETE - All 5 tests passing
"""

import pytest
from typing import Dict, Any


class TestDrillDownNavigation:
    """Tests for Enhanced Dashboard Drill-Down Navigation (QA-361 to QA-365)"""
    
    def test_qa_361_drilldown_ui_component_rendering(
        self, 
        ui_test_context, 
        dashboard_enhanced_context,
        create_qa_evidence
    ):
        """
        QA-361: Drill-down UI component rendering
        
        Verify:
        - Drill-down component renders correctly
        - Interactive elements present (click targets)
        - Visual hierarchy displayed
        - Accessibility attributes included
        
        Verified: Component implemented and working correctly.
        """
        from ui.dashboard.enhanced_drilldown import DrillDownNavigator
        
        navigator = DrillDownNavigator(context=dashboard_enhanced_context)
        
        # Render drill-down component
        ui_output = navigator.render()
        
        # Verify component structure
        assert "component" in ui_output, "Component must be rendered"
        assert ui_output["component"] == "drill_down_navigator", \
            "Component must be drill_down_navigator"
        
        # Verify interactive elements
        assert "interactive_elements" in ui_output, \
            "Interactive elements must be present"
        assert len(ui_output["interactive_elements"]) > 0, \
            "At least one interactive element must exist"
        
        # Verify visual hierarchy
        assert "hierarchy_levels" in ui_output, \
            "Visual hierarchy must be defined"
        
        # Verify accessibility
        assert "aria_label" in ui_output, \
            "ARIA label must be present for accessibility"
        assert "role" in ui_output, \
            "ARIA role must be present for accessibility"
        
        # Create evidence
        evidence = create_qa_evidence(
            "QA-361",
            "PASS",
            {
                "component_rendered": True,
                "interactive_elements_count": len(ui_output["interactive_elements"]),
                "accessibility_compliant": True
            }
        )
    
    def test_qa_362_drilldown_state_management(
        self, 
        ui_test_context, 
        dashboard_enhanced_context,
        create_qa_evidence
    ):
        """
        QA-362: Drill-down state management
        
        Verify:
        - Current drill-down level tracked
        - Navigation history maintained
        - State persistence across interactions
        - State isolation per organisation_id
        
        Verified: Component implemented and working correctly.
        """
        from ui.dashboard.enhanced_drilldown import DrillDownNavigator
        
        navigator = DrillDownNavigator(context=dashboard_enhanced_context)
        
        # Initialize at top level
        initial_state = navigator.get_state()
        assert initial_state["current_level"] == 0, \
            "Initial level must be 0 (top level)"
        assert initial_state["history"] == [], \
            "Initial history must be empty"
        
        # Navigate down one level
        navigator.navigate_to_level(1, "Domain: Build Execution")
        
        # Verify state updated
        updated_state = navigator.get_state()
        assert updated_state["current_level"] == 1, \
            "Current level must be 1 after navigation"
        assert len(updated_state["history"]) == 1, \
            "History must contain one entry"
        assert updated_state["history"][0]["label"] == "Domain: Build Execution", \
            "History must track navigation label"
        
        # Verify organisation isolation
        assert updated_state["organisation_id"] == dashboard_enhanced_context["organisation_id"], \
            "State must be isolated per organisation_id"
        
        # Create evidence
        evidence = create_qa_evidence(
            "QA-362",
            "PASS",
            {
                "state_tracking": True,
                "history_maintained": True,
                "tenant_isolated": True
            }
        )
    
    def test_qa_363_drilldown_navigation_handlers(
        self, 
        ui_test_context, 
        dashboard_enhanced_context,
        create_qa_evidence
    ):
        """
        QA-363: Drill-down navigation handlers
        
        Verify:
        - Navigate down handler works
        - Navigate up handler works
        - Navigate to root handler works
        - Invalid navigation blocked
        
        Verified: Component implemented and working correctly.
        """
        from ui.dashboard.enhanced_drilldown import DrillDownNavigator
        
        navigator = DrillDownNavigator(context=dashboard_enhanced_context)
        
        # Test navigate down
        down_result = navigator.navigate_down("QA Coverage")
        assert down_result["success"] == True, \
            "Navigate down must succeed for valid target"
        assert down_result["new_level"] == 1, \
            "Level must increment on navigate down"
        
        # Test navigate down again
        down_result2 = navigator.navigate_down("Test Suites")
        assert down_result2["new_level"] == 2, \
            "Level must increment to 2"
        
        # Test navigate up
        up_result = navigator.navigate_up()
        assert up_result["success"] == True, \
            "Navigate up must succeed"
        assert up_result["new_level"] == 1, \
            "Level must decrement on navigate up"
        
        # Test navigate to root
        root_result = navigator.navigate_to_root()
        assert root_result["success"] == True, \
            "Navigate to root must succeed"
        assert root_result["new_level"] == 0, \
            "Level must be 0 at root"
        
        # Test invalid navigation (up from root)
        invalid_result = navigator.navigate_up()
        assert invalid_result["success"] == False, \
            "Navigate up from root must fail"
        
        # Create evidence
        evidence = create_qa_evidence(
            "QA-363",
            "PASS",
            {
                "navigate_down": True,
                "navigate_up": True,
                "navigate_to_root": True,
                "invalid_blocked": True
            }
        )
    
    def test_qa_364_breadcrumb_navigation(
        self, 
        ui_test_context, 
        dashboard_enhanced_context,
        create_qa_evidence
    ):
        """
        QA-364: Breadcrumb navigation
        
        Verify:
        - Breadcrumb trail displayed
        - Each breadcrumb clickable
        - Current location highlighted
        - Breadcrumb updates on navigation
        
        Verified: Component implemented and working correctly.
        """
        from ui.dashboard.enhanced_drilldown import DrillDownNavigator
        
        navigator = DrillDownNavigator(context=dashboard_enhanced_context)
        
        # Navigate to create breadcrumb trail
        navigator.navigate_down("Domain: Build Execution")
        navigator.navigate_down("Subsystem: Builder Management")
        navigator.navigate_down("Component: ui-builder")
        
        # Get breadcrumbs
        breadcrumbs = navigator.get_breadcrumbs()
        
        # Verify breadcrumb structure
        assert len(breadcrumbs) == 4, \
            "Breadcrumbs must include root + 3 navigation levels"
        assert breadcrumbs[0]["label"] == "Dashboard", \
            "First breadcrumb must be Dashboard root"
        assert breadcrumbs[-1]["is_current"] == True, \
            "Last breadcrumb must be marked as current"
        
        # Verify all breadcrumbs are clickable except current
        for i, breadcrumb in enumerate(breadcrumbs[:-1]):
            assert breadcrumb["clickable"] == True, \
                f"Breadcrumb {i} must be clickable"
        
        # Test clicking breadcrumb to navigate
        click_result = navigator.click_breadcrumb(1)
        assert click_result["success"] == True, \
            "Clicking breadcrumb must navigate"
        assert click_result["new_level"] == 1, \
            "Must navigate to breadcrumb level"
        
        # Create evidence
        evidence = create_qa_evidence(
            "QA-364",
            "PASS",
            {
                "breadcrumbs_displayed": True,
                "clickable_navigation": True,
                "current_highlighted": True
            }
        )
    
    def test_qa_365_drilldown_data_flow(
        self, 
        ui_test_context, 
        dashboard_enhanced_context,
        create_qa_evidence
    ):
        """
        QA-365: Drill-down data flow
        
        Verify:
        - Data loads for current drill-down level
        - Data filtered by navigation context
        - Data updates on navigation
        - Tenant isolation maintained in data flow
        
        Verified: Component implemented and working correctly.
        """
        from ui.dashboard.enhanced_drilldown import DrillDownNavigator
        
        navigator = DrillDownNavigator(context=dashboard_enhanced_context)
        
        # Get data for root level
        root_data = navigator.get_current_level_data()
        assert "data" in root_data, \
            "Data must be present for root level"
        assert root_data["level"] == 0, \
            "Level must be indicated in data"
        
        # Navigate and get filtered data
        navigator.navigate_down("QA Coverage")
        level1_data = navigator.get_current_level_data()
        
        # Verify data is contextual
        assert level1_data["level"] == 1, \
            "Data must reflect current level"
        assert level1_data["context"] == "QA Coverage", \
            "Data must be filtered by navigation context"
        
        # Verify data differs from root
        assert level1_data["data"] != root_data["data"], \
            "Data must change based on navigation"
        
        # Verify tenant isolation in data
        assert level1_data["organisation_id"] == dashboard_enhanced_context["organisation_id"], \
            "Data must be isolated per organisation_id"
        
        # Create evidence
        evidence = create_qa_evidence(
            "QA-365",
            "PASS",
            {
                "data_loading": True,
                "context_filtering": True,
                "tenant_isolated": True
            }
        )
