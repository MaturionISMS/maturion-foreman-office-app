"""
Build Control API

Provides REST API endpoints for the Build Control Panel UI.
Handles build execution requests and invokes the Build Authorization Gate.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
import logging
from typing import Dict, Any

# Handle both relative and absolute imports
try:
    from .build_authorization_gate import BuildAuthorizationGate, GateResult
    from .build_node_inspector import BuildNodeInspector
    from .build_intervention import BuildInterventionController
except ImportError:
    from build_authorization_gate import BuildAuthorizationGate, GateResult
    from build_node_inspector import BuildNodeInspector
    from build_intervention import BuildInterventionController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable CORS for local development

# Initialize gate validator, inspector, and intervention controller
repo_root = Path(__file__).parent.parent.parent
gate_validator = BuildAuthorizationGate(repo_root=repo_root)
node_inspector = BuildNodeInspector(repo_root=repo_root)
intervention_controller = BuildInterventionController(repo_root=repo_root)


@app.route('/')
def index():
    """Serve the Build Control Panel UI"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Build Control API',
        'version': '1.0.0'
    })


@app.route('/api/builds', methods=['GET'])
def list_builds():
    """
    List available builds
    
    Returns:
        JSON array of build IDs and their status
    """
    try:
        builds_dir = repo_root / "architecture" / "builds"
        
        if not builds_dir.exists():
            return jsonify({
                'builds': [],
                'message': 'No builds directory found'
            })
        
        builds = []
        for build_path in builds_dir.iterdir():
            if build_path.is_dir():
                build_id = build_path.name
                
                # Check if authorization evidence exists
                auth_evidence = build_path / "authorization-evidence"
                has_authorization = auth_evidence.exists()
                
                # Try to load the authorization result
                status = "UNKNOWN"
                if has_authorization:
                    result_file = auth_evidence / "authorization-decision.md"
                    if result_file.exists():
                        content = result_file.read_text()
                        if "PASS" in content:
                            status = "AUTHORIZED"
                        elif "FAIL" in content:
                            status = "BLOCKED"
                
                builds.append({
                    'id': build_id,
                    'status': status,
                    'has_authorization': has_authorization
                })
        
        return jsonify({
            'builds': builds,
            'count': len(builds)
        })
    
    except Exception as e:
        logger.error(f"Error listing builds: {str(e)}")
        return jsonify({
            'error': 'Failed to list builds',
            'details': str(e)
        }), 500


@app.route('/api/builds/<build_id>/validate', methods=['POST'])
def validate_build(build_id: str):
    """
    Request Build Execution Readiness Gate validation
    
    This is the explicit human action required to initiate build validation.
    
    Args:
        build_id: The unique identifier for the build
        
    Returns:
        JSON with validation results (PASS/FAIL) and blocking conditions
    """
    try:
        logger.info(f"Received build validation request for: {build_id}")
        
        # Invoke Build Authorization Gate
        result = gate_validator.validate(build_id)
        
        logger.info(f"Build validation completed: {result.gate_result.value}")
        
        # Generate evidence package
        evidence_path = gate_validator.generate_evidence_package(result)
        logger.info(f"Evidence package generated at: {evidence_path}")
        
        # Return structured response
        response = {
            'build_id': build_id,
            'gate_result': result.gate_result.value,
            'timestamp': result.timestamp,
            'summary': result.summary,
            'preconditions': [
                {
                    'name': pr.name,
                    'status': pr.status.value,
                    'message': pr.message,
                    'evidence_count': len(pr.evidence_paths),
                    'blocking_conditions': pr.blocking_conditions
                }
                for pr in result.precondition_results
            ],
            'evidence_path': evidence_path,
            'can_proceed': result.gate_result == GateResult.PASS
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error validating build {build_id}: {str(e)}")
        return jsonify({
            'error': 'Build validation failed',
            'details': str(e),
            'build_id': build_id
        }), 500


@app.route('/api/builds/<build_id>/execute', methods=['POST'])
def execute_build(build_id: str):
    """
    Request build execution (ONLY if gate passed)
    
    This endpoint enforces that builds cannot execute without authorization.
    
    Args:
        build_id: The unique identifier for the build
        
    Returns:
        JSON with execution status or blocking message
    """
    try:
        logger.info(f"Received build execution request for: {build_id}")
        
        # First, check if build is authorized
        evidence_dir = repo_root / "architecture" / "builds" / build_id / "authorization-evidence"
        
        if not evidence_dir.exists():
            return jsonify({
                'error': 'Build not authorized',
                'message': 'Build must pass Authorization Gate before execution',
                'action_required': 'Run validation first',
                'build_id': build_id
            }), 403
        
        # Check authorization decision
        decision_file = evidence_dir / "authorization-decision.md"
        if not decision_file.exists():
            return jsonify({
                'error': 'Build authorization incomplete',
                'message': 'No authorization decision found',
                'action_required': 'Run validation first',
                'build_id': build_id
            }), 403
        
        content = decision_file.read_text()
        if "PASS" not in content:
            # Load blocker report
            blocker_file = evidence_dir / "blocker-report.md"
            blocker_message = "Build is blocked due to failed preconditions"
            if blocker_file.exists():
                blocker_message = blocker_file.read_text()
            
            return jsonify({
                'error': 'Build execution blocked',
                'message': 'Build failed Authorization Gate',
                'action_required': 'Resolve blocking conditions',
                'blocker_details': blocker_message,
                'build_id': build_id
            }), 403
        
        # Build is authorized - proceed with execution routing
        # NOTE: Actual execution is out of scope for this issue
        # This is where we would route to pipeline/CI/CD systems
        
        return jsonify({
            'status': 'authorized',
            'message': 'Build authorization confirmed. Ready for execution.',
            'build_id': build_id,
            'note': 'Actual build execution is delegated to CI/CD pipeline (not implemented in this scope)'
        })
    
    except Exception as e:
        logger.error(f"Error executing build {build_id}: {str(e)}")
        return jsonify({
            'error': 'Build execution request failed',
            'details': str(e),
            'build_id': build_id
        }), 500


@app.route('/api/builds/<build_id>/status', methods=['GET'])
def get_build_status(build_id: str):
    """
    Get current status of a build
    
    Args:
        build_id: The unique identifier for the build
        
    Returns:
        JSON with build status and authorization state
    """
    try:
        evidence_dir = repo_root / "architecture" / "builds" / build_id / "authorization-evidence"
        
        if not evidence_dir.exists():
            return jsonify({
                'build_id': build_id,
                'status': 'NOT_VALIDATED',
                'message': 'Build has not been validated yet'
            })
        
        # Load result JSON
        result_file = evidence_dir / "gate-validation-result.json"
        if result_file.exists():
            import json
            with open(result_file) as f:
                result_data = json.load(f)
            
            return jsonify({
                'build_id': build_id,
                'status': result_data['gate_result'],
                'timestamp': result_data['timestamp'],
                'summary': result_data['summary'],
                'preconditions': result_data['precondition_results']
            })
        else:
            return jsonify({
                'build_id': build_id,
                'status': 'INCOMPLETE',
                'message': 'Validation started but incomplete'
            })
    
    except Exception as e:
        logger.error(f"Error getting build status {build_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to get build status',
            'details': str(e),
            'build_id': build_id
        }), 500


@app.route('/api/build-tree/inspect/<node_type>/<node_id>', methods=['GET'])
def inspect_node(node_type: str, node_id: str):
    """
    Inspect a build node and return comprehensive drill-down information.
    
    Implements BUILD_NODE_INSPECTION_MODEL.md (G-C9).
    Enforces principle: "No status without explanation."
    
    Args:
        node_type: Type of node ('program', 'wave', 'sub-wave', 'task')
        node_id: Unique identifier for the node
        
    Query Parameters:
        depth: Inspection depth level (1-5), default: 3
        include_children: Include child nodes (true/false), default: false
        
    Returns:
        JSON with comprehensive node inspection data
    """
    try:
        # Parse query parameters
        depth = int(request.args.get('depth', 3))
        include_children = request.args.get('include_children', 'false').lower() == 'true'
        
        logger.info(f"Node inspection request: {node_type}/{node_id} (depth={depth})")
        
        # Perform inspection
        inspection_data = node_inspector.inspect_node(
            node_type=node_type,
            node_id=node_id,
            depth=depth,
            include_children=include_children
        )
        
        # Log inspection for audit trail
        node_inspector.log_inspection(
            node_id=node_id,
            node_type=node_type,
            inspected_by=request.remote_addr or "unknown",
            inspection_depth=depth,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({
            'success': True,
            'data': inspection_data
        })
    
    except ValueError as e:
        logger.warning(f"Invalid inspection request: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'details': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error inspecting node {node_type}/{node_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Node inspection failed',
            'details': str(e)
        }), 500


@app.route('/api/evidence/<evidence_id>/artifact', methods=['GET'])
def get_evidence_artifact(evidence_id: str):
    """
    Get evidence artifact (read-only).
    
    Args:
        evidence_id: Unique identifier for the evidence artifact
        
    Returns:
        Redirect to artifact location or artifact content
    """
    try:
        # TODO: Implement evidence artifact retrieval
        # For now, return a placeholder
        return jsonify({
            'evidence_id': evidence_id,
            'message': 'Evidence artifact retrieval not yet implemented',
            'note': 'This endpoint will return read-only access to evidence artifacts'
        }), 501
    
    except Exception as e:
        logger.error(f"Error retrieving evidence artifact {evidence_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve evidence artifact',
            'details': str(e)
        }), 500


# ===== INTERVENTION ENDPOINTS =====
# Implements BUILD_INTERVENTION_AND_ALERT_MODEL.md (G-C10)

@app.route('/api/build-tree/alert', methods=['POST'])
def issue_alert():
    """
    Issue a non-blocking alert for a build node.
    
    Request Body:
        {
            "scope_level": "step" | "sub-wave" | "wave" | "application",
            "target_node_id": "string",
            "rationale": "string (min 20 chars)",
            "triggered_by": "string"
        }
        
    Returns:
        JSON with alert ID and routing information
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['scope_level', 'target_node_id', 'rationale', 'triggered_by']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        logger.info(f"Alert request: {data['scope_level']}/{data['target_node_id']}")
        
        # Issue alert
        result = intervention_controller.issue_alert(
            scope_level=data['scope_level'],
            target_node_id=data['target_node_id'],
            rationale=data['rationale'],
            triggered_by=data['triggered_by'],
            triggered_by_type=data.get('triggered_by_type', 'human'),
            ip_address=request.remote_addr
        )
        
        return jsonify(result), 201
    
    except ValueError as e:
        logger.warning(f"Invalid alert request: {str(e)}")
        return jsonify({
            'error': 'Invalid request',
            'details': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error issuing alert: {str(e)}")
        return jsonify({
            'error': 'Failed to issue alert',
            'details': str(e)
        }), 500


@app.route('/api/build-tree/emergency-stop', methods=['POST'])
def issue_emergency_stop():
    """
    Issue an immediate emergency stop for a build scope.
    
    Request Body:
        {
            "scope_level": "step" | "sub-wave" | "wave" | "application",
            "target_node_id": "string",
            "critical_rationale": "string (min 50 chars)",
            "confirmation": {
                "acknowledged_impact": true,
                "typed_confirmation": "STOP"
            },
            "triggered_by": "string"
        }
        
    Returns:
        JSON with stop ID and affected nodes
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['scope_level', 'target_node_id', 'critical_rationale', 'confirmation', 'triggered_by']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        logger.warning(f"⚠️ EMERGENCY STOP request: {data['scope_level']}/{data['target_node_id']}")
        
        # Issue emergency stop
        result = intervention_controller.issue_emergency_stop(
            scope_level=data['scope_level'],
            target_node_id=data['target_node_id'],
            critical_rationale=data['critical_rationale'],
            triggered_by=data['triggered_by'],
            confirmation=data['confirmation'],
            triggered_by_type=data.get('triggered_by_type', 'human'),
            ip_address=request.remote_addr
        )
        
        return jsonify(result), 201
    
    except ValueError as e:
        logger.warning(f"Invalid emergency stop request: {str(e)}")
        return jsonify({
            'error': 'Invalid request',
            'details': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error issuing emergency stop: {str(e)}")
        return jsonify({
            'error': 'Failed to issue emergency stop',
            'details': str(e)
        }), 500


@app.route('/api/build-tree/intervention/<intervention_id>/context', methods=['GET'])
def get_intervention_context(intervention_id: str):
    """
    Get full context for an intervention (alert or stop).
    
    Args:
        intervention_id: ID of the intervention
        
    Returns:
        JSON with full context including node state, evidence, blockers, etc.
    """
    try:
        logger.info(f"Context request for intervention {intervention_id}")
        
        # Get intervention context
        result = intervention_controller.get_intervention_context(intervention_id)
        
        return jsonify(result)
    
    except FileNotFoundError as e:
        logger.warning(f"Intervention not found: {intervention_id}")
        return jsonify({
            'error': 'Intervention not found',
            'intervention_id': intervention_id
        }), 404
    
    except Exception as e:
        logger.error(f"Error retrieving intervention context: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve context',
            'details': str(e)
        }), 500


@app.route('/api/build-tree/emergency-stop/<stop_id>/resume', methods=['POST'])
def resume_after_stop(stop_id: str):
    """
    Resume execution after an emergency stop.
    
    Args:
        stop_id: ID of the stop to resume
        
    Request Body:
        {
            "authorized_by": "string",
            "resolution_summary": "string (min 50 chars)",
            "resume_conditions": ["string"]
        }
        
    Returns:
        JSON with resumption status
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['authorized_by', 'resolution_summary', 'resume_conditions']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        logger.info(f"Resume request for stop {stop_id} by {data['authorized_by']}")
        
        # Resume execution
        result = intervention_controller.resume_after_stop(
            stop_id=stop_id,
            authorized_by=data['authorized_by'],
            resolution_summary=data['resolution_summary'],
            resume_conditions=data['resume_conditions']
        )
        
        return jsonify(result)
    
    except FileNotFoundError as e:
        logger.warning(f"Stop not found: {stop_id}")
        return jsonify({
            'error': 'Stop not found',
            'stop_id': stop_id
        }), 404
    
    except ValueError as e:
        logger.warning(f"Invalid resume request: {str(e)}")
        return jsonify({
            'error': 'Invalid request',
            'details': str(e)
        }), 400
    
    except PermissionError as e:
        logger.warning(f"Unauthorized resume attempt: {str(e)}")
        return jsonify({
            'error': 'Unauthorized',
            'details': str(e)
        }), 403
    
    except Exception as e:
        logger.error(f"Error resuming after stop: {str(e)}")
        return jsonify({
            'error': 'Failed to resume',
            'details': str(e)
        }), 500


def create_app():
    """Application factory"""
    return app


if __name__ == '__main__':
    logger.info("Starting Build Control API server...")
    logger.info(f"Repository root: {repo_root}")
    app.run(host='0.0.0.0', port=5000, debug=True)
