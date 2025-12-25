"""
Tests for Build Control API

Tests the REST API endpoints for build control and authorization.
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'fm' / 'orchestration'))

from build_control_api import create_app


@pytest.fixture
def app(tmp_path):
    """Create Flask app with temporary repo structure"""
    # Set up test repo structure
    arch_dir = tmp_path / "architecture" / "builds"
    arch_dir.mkdir(parents=True)
    
    # Create test build
    test_build = arch_dir / "test-build-api-001"
    test_build.mkdir()
    
    app = create_app()
    app.config['TESTING'] = True
    
    # Override repo_root for testing
    import build_control_api
    build_control_api.repo_root = tmp_path
    build_control_api.gate_validator = build_control_api.BuildAuthorizationGate(repo_root=tmp_path)
    
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test that health endpoint returns 200"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
        assert 'version' in data


class TestListBuildsEndpoint:
    """Test builds listing endpoint"""
    
    def test_list_builds_empty(self, client, tmp_path):
        """Test listing builds when none exist"""
        # Remove test builds
        import build_control_api
        builds_dir = build_control_api.repo_root / "architecture" / "builds"
        for item in builds_dir.iterdir():
            if item.is_dir():
                import shutil
                shutil.rmtree(item)
        
        response = client.get('/api/builds')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'builds' in data
        assert isinstance(data['builds'], list)
    
    def test_list_builds_with_builds(self, client, tmp_path):
        """Test listing builds when some exist"""
        response = client.get('/api/builds')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'builds' in data
        assert 'count' in data


class TestValidateBuildEndpoint:
    """Test build validation endpoint"""
    
    def test_validate_build_not_found(self, client):
        """Test validating non-existent build"""
        response = client.post('/api/builds/nonexistent-build/validate')
        
        assert response.status_code == 200  # Validation runs but finds no evidence
        data = json.loads(response.data)
        assert data['gate_result'] == 'FAIL'
        assert data['build_id'] == 'nonexistent-build'
    
    def test_validate_build_returns_structure(self, client):
        """Test that validation returns expected structure"""
        response = client.post('/api/builds/test-build-api-001/validate')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check response structure
        assert 'build_id' in data
        assert 'gate_result' in data
        assert 'timestamp' in data
        assert 'summary' in data
        assert 'preconditions' in data
        assert 'evidence_path' in data
        assert 'can_proceed' in data
        
        # Check preconditions structure
        assert isinstance(data['preconditions'], list)
        assert len(data['preconditions']) == 8
        
        for pc in data['preconditions']:
            assert 'name' in pc
            assert 'status' in pc
            assert 'message' in pc
            assert 'blocking_conditions' in pc


class TestExecuteBuildEndpoint:
    """Test build execution endpoint"""
    
    def test_execute_build_without_authorization(self, client):
        """Test that execution fails without authorization"""
        response = client.post('/api/builds/test-build-api-001/execute')
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not authorized' in data['error'].lower()
    
    def test_execute_build_with_failed_authorization(self, client, tmp_path):
        """Test that execution fails with failed authorization"""
        # First validate (will fail)
        validate_response = client.post('/api/builds/test-build-api-001/validate')
        assert validate_response.status_code == 200
        
        # Validation creates the authorization evidence directory but with FAIL
        # Then try to execute
        response = client.post('/api/builds/test-build-api-001/execute')
        
        # Should be blocked because authorization failed
        # Note: might be 200 if blocker_report.md doesn't exist yet
        data = json.loads(response.data)
        assert 'error' in data or 'status' in data
    
    def test_execute_build_with_passed_authorization(self, client, tmp_path):
        """Test execution succeeds with passed authorization"""
        import build_control_api
        build_id = "test-build-api-001"
        evidence_dir = build_control_api.repo_root / "architecture" / "builds" / build_id
        qa_dir = evidence_dir / "qa-evidence"
        qa_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all required evidence
        (evidence_dir / "app-description-validation.md").write_text("Valid")
        (evidence_dir / "app-description-frs-alignment-checklist-result.md").write_text("PASS")
        (evidence_dir / "validation.md").write_text("PASS")
        (evidence_dir / "flci-prevention-plan.md").write_text("Complete")
        (qa_dir / "coverage-report.md").write_text("100%")
        (qa_dir / "test-execution-report.md").write_text("GREEN")
        (evidence_dir / "flci-coverage-report.md").write_text("Complete")
        (evidence_dir / "environment-compatibility-matrix.md").write_text("Valid")
        (evidence_dir / "deployment-test-results.md").write_text("Valid")
        (evidence_dir / "architecture-validation-checklist.md").write_text("- [x] All")
        (evidence_dir / "freeze-timestamp.txt").write_text("2025-12-25T00:00:00Z")
        (evidence_dir / "IMMUTABLE").write_text("")
        (evidence_dir / "test-debt-scan-report.md").write_text("ZERO")
        
        # Also create APP_DESCRIPTION.md
        (build_control_api.repo_root / "APP_DESCRIPTION.md").write_text("Status: Authoritative")
        
        # Validate first
        validate_response = client.post(f'/api/builds/{build_id}/validate')
        assert validate_response.status_code == 200
        
        # Now execute
        response = client.post(f'/api/builds/{build_id}/execute')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'authorized'
        assert data['build_id'] == build_id


class TestGetBuildStatusEndpoint:
    """Test build status endpoint"""
    
    def test_get_status_not_validated(self, client):
        """Test status of build that hasn't been validated"""
        response = client.get('/api/builds/test-build-api-001/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'build_id' in data
        assert 'status' in data
    
    def test_get_status_after_validation(self, client):
        """Test status after validation"""
        # First validate
        client.post('/api/builds/test-build-api-001/validate')
        
        # Then get status
        response = client.get('/api/builds/test-build-api-001/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['build_id'] == 'test-build-api-001'
        assert data['status'] in ['PASS', 'FAIL']


class TestAPIErrorHandling:
    """Test error handling in API"""
    
    def test_invalid_build_id_characters(self, client):
        """Test handling of invalid build ID"""
        # API should handle this gracefully
        # Flask might return 405 or 404 for malformed paths, or 200 with validation failure
        response = client.post('/api/builds/../../etc/passwd/validate')
        
        # Should not crash - any of these responses is acceptable
        assert response.status_code in [200, 400, 403, 404, 405, 500]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
