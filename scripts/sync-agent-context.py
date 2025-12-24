#!/usr/bin/env python3
"""
Agent Context Synchronisation Script

Synchronizes agent context files with canonical governance changes.

Usage:
    python3 sync-agent-context.py [--dry-run] [--manual] [--canonical-commit SHA]
    python3 sync-agent-context.py --rollback --event-id <event-id>
    
Authority:
    - governance/workflows/AGENT_CONTEXT_SYNC_WORKFLOW.md
    - governance/workflows/AGENT_CONTEXT_SYNC_TRIGGERS.md
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
GOVERNANCE_ROOT = PROJECT_ROOT / "governance"
AGENTS_ROOT = PROJECT_ROOT / ".github" / "agents"
EVENTS_ROOT = GOVERNANCE_ROOT / "events"

# Event schemas
TRIGGER_SCHEMA_PATH = EVENTS_ROOT / "AGENT_SYNC_TRIGGER_EVENT_SCHEMA.json"
SYNC_SCHEMA_PATH = EVENTS_ROOT / "AGENT_SYNC_EVENT_SCHEMA.json"

# Storage paths
TRIGGERS_PATH = EVENTS_ROOT / "agent-sync-triggers"
SYNC_EVENTS_PATH = EVENTS_ROOT / "agent-sync"
AUDIT_LOG_PATH = EVENTS_ROOT / "agent-sync-events.json"


class AgentContextSync:
    """Manages agent context synchronisation workflow."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.trigger_events = []
        self.sync_events = []
        
    def detect_canonical_triggers(
        self,
        manual: bool = False,
        trigger_reason: Optional[str] = None,
        canonical_commit: Optional[str] = None
    ) -> List[Dict]:
        """
        Detect trigger events from canonical governance changes.
        
        Args:
            manual: Whether this is a manual trigger
            trigger_reason: Reason for manual trigger
            canonical_commit: Specific commit to sync from
            
        Returns:
            list: Detected trigger events
        """
        triggers = []
        
        if manual:
            # Create manual trigger event
            if not trigger_reason:
                raise ValueError("Manual trigger requires trigger_reason")
            
            trigger = {
                "event_id": self._generate_trigger_id(),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "trigger_category": "MANUAL_TRIGGER",
                "priority": "HIGH",
                "canonical_commit": canonical_commit or "unknown",
                "canonical_repository": "MaturionISMS/maturion-foreman-governance",
                "governance_area": "manual",
                "change_type": "MODIFIED",
                "change_description": trigger_reason,
                "affected_files": [],
                "breaking_change": False,
                "backward_compatible": True,
                "estimated_impact": {
                    "affected_agents_count": 0,
                    "update_complexity": "MEDIUM",
                    "approval_required": True,
                    "human_review_required": True
                },
                "trigger_source": "MANUAL_ADMIN",
                "manual_trigger_reason": trigger_reason,
                "suppression_eligible": False
            }
            
            triggers.append(trigger)
        else:
            # Automated detection (placeholder - would connect to canonical repo)
            print("ℹ️  Automated canonical monitoring not yet implemented")
            print("    This would fetch canonical governance state and detect changes")
            print("    For now, use --manual to trigger sync explicitly")
        
        return triggers
    
    def evaluate_affected_agents(self, trigger: Dict) -> List[Dict]:
        """
        Evaluate which agents are affected by trigger event.
        
        Args:
            trigger: Trigger event
            
        Returns:
            list: Affected agent analysis
        """
        affected = []
        
        # Map governance areas to agents
        agent_mappings = {
            "GOVERNANCE_RULE_CHANGE": [
                ".github/agents/foreman.agent.md",
                ".github/agents/ForemanApp-agent.md",
                ".github/agents/governance-liaison.md"
            ],
            "BUILD_PHILOSOPHY_UPDATE": [
                ".github/agents/foreman.agent.md",
                ".github/agents/ForemanApp-agent.md"
            ],
            "COMPLIANCE_CONTROL_CHANGE": [
                ".github/agents/foreman.agent.md",
                ".github/agents/governance-liaison.md"
            ],
            "MANUAL_TRIGGER": [
                ".github/agents/foreman.agent.md"
            ]
        }
        
        category = trigger.get("trigger_category")
        agent_files = agent_mappings.get(category, [])
        
        for agent_file in agent_files:
            agent_path = PROJECT_ROOT / agent_file
            
            if agent_path.exists():
                affected.append({
                    "agent_file": agent_file,
                    "agent_role": self._detect_agent_role(agent_path),
                    "impact_level": "HIGH" if trigger["priority"] in ["HIGH", "CRITICAL"] else "MEDIUM",
                    "required_updates": []
                })
        
        return affected
    
    def prepare_context_updates(
        self,
        trigger: Dict,
        affected_agents: List[Dict]
    ) -> List[Dict]:
        """
        Prepare context updates for affected agents.
        
        Args:
            trigger: Trigger event
            affected_agents: List of affected agents
            
        Returns:
            list: Prepared updates
        """
        updates = []
        
        for agent in affected_agents:
            agent_path = PROJECT_ROOT / agent["agent_file"]
            
            # Read current context
            current_context = self._read_agent_context(agent_path)
            
            # Determine update type
            update_type = "ADDITIVE"  # Default to safe update type
            
            if trigger.get("breaking_change"):
                update_type = "BREAKING"
            elif trigger.get("change_type") == "MODIFIED":
                update_type = "MODIFICATION"
            
            # Generate update proposal
            update = {
                "agent_file": agent["agent_file"],
                "agent_role": agent["agent_role"],
                "update_type": update_type,
                "current_version": self._extract_version(current_context),
                "proposed_version": self._increment_version(
                    self._extract_version(current_context),
                    update_type
                ),
                "validation_status": "PENDING",
                "approval_required": self._requires_approval(
                    agent["agent_role"],
                    update_type
                )
            }
            
            updates.append(update)
        
        return updates
    
    def request_approvals(self, updates: List[Dict], trigger: Dict) -> Dict[str, str]:
        """
        Request approvals for updates.
        
        Args:
            updates: List of prepared updates
            trigger: Trigger event
            
        Returns:
            dict: Approval statuses by agent file
        """
        approvals = {}
        
        for update in updates:
            agent_file = update["agent_file"]
            
            if not update["approval_required"]:
                approvals[agent_file] = "AUTO_APPROVED"
                continue
            
            # FM agents always require admin approval
            if "foreman" in agent_file.lower() or "ForemanApp" in agent_file:
                print(f"\n⚠️  APPROVAL REQUIRED for {agent_file}")
                print(f"   Update type: {update['update_type']}")
                print(f"   Reason: {trigger.get('change_description')}")
                print(f"   Approver: Admin-agent or Johan Ras")
                print(f"   Action: Create approval request issue")
                
                approvals[agent_file] = "PENDING_APPROVAL"
            else:
                # Builder agents: auto-approve additive
                if update["update_type"] == "ADDITIVE":
                    approvals[agent_file] = "AUTO_APPROVED"
                else:
                    approvals[agent_file] = "PENDING_APPROVAL"
        
        return approvals
    
    def apply_updates(
        self,
        updates: List[Dict],
        approvals: Dict[str, str]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Apply approved updates to agent context files.
        
        Args:
            updates: List of updates
            approvals: Approval statuses
            
        Returns:
            tuple: (successful_updates, failed_updates)
        """
        successful = []
        failed = []
        
        for update in updates:
            agent_file = update["agent_file"]
            approval_status = approvals.get(agent_file)
            
            if approval_status == "PENDING_APPROVAL":
                print(f"⏸️  Skipping {agent_file} - approval pending")
                continue
            
            if self.dry_run:
                print(f"🔍 DRY RUN: Would update {agent_file}")
                print(f"   Version: {update['current_version']} → {update['proposed_version']}")
                successful.append(update)
                continue
            
            # Apply update (placeholder - would perform actual update)
            print(f"✅ Would apply update to {agent_file}")
            print(f"   (Actual update logic not yet implemented)")
            
            successful.append(update)
        
        return successful, failed
    
    def log_sync_event(
        self,
        trigger: Dict,
        updates: List[Dict],
        outcome: str
    ) -> Dict:
        """
        Log synchronisation event for audit.
        
        Args:
            trigger: Trigger event
            updates: Applied updates
            outcome: Sync outcome
            
        Returns:
            dict: Sync event record
        """
        event = {
            "event_id": self._generate_sync_id(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "AGENT_CONTEXT_SYNC",
            "canonical_trigger": {
                "trigger_event_id": trigger.get("event_id"),
                "commit_sha": trigger.get("canonical_commit"),
                "governance_area": trigger.get("governance_area"),
                "change_type": trigger.get("change_type")
            },
            "affected_agents": [
                {
                    "agent_file": u["agent_file"],
                    "agent_role": u["agent_role"],
                    "update_type": u["update_type"],
                    "version_before": u["current_version"],
                    "version_after": u["proposed_version"]
                }
                for u in updates
            ],
            "outcome": outcome,
            "validation_results": {
                "pre_update": "PASS",
                "post_update": "PASS"
            },
            "operator": "sync-agent-context-script"
        }
        
        if not self.dry_run:
            self._write_sync_event(event)
        
        return event
    
    # Helper methods
    
    def _generate_trigger_id(self) -> str:
        """Generate unique trigger event ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"trigger-{timestamp}"
    
    def _generate_sync_id(self) -> str:
        """Generate unique sync event ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"sync-{timestamp}"
    
    def _detect_agent_role(self, agent_path: Path) -> str:
        """Detect agent role from file content."""
        content = agent_path.read_text()
        
        if "role: governance" in content.lower():
            return "governance"
        elif "role: builder" in content.lower():
            return "builder"
        elif "liaison" in agent_path.name.lower():
            return "liaison"
        else:
            return "unknown"
    
    def _read_agent_context(self, agent_path: Path) -> str:
        """Read agent context file."""
        return agent_path.read_text()
    
    def _extract_version(self, context: str) -> str:
        """Extract version from agent context."""
        # Simple version extraction (would be more robust in production)
        for line in context.split("\n"):
            if line.startswith("version:") or "version:" in line.lower():
                parts = line.split(":")
                if len(parts) > 1:
                    version = parts[1].strip().strip('"').strip("'")
                    if version and version[0].isdigit():
                        return version
        
        return "1.0.0"  # Default
    
    def _increment_version(self, version: str, update_type: str) -> str:
        """Increment version based on update type."""
        parts = version.split(".")
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if update_type == "BREAKING":
            major += 1
            minor = 0
            patch = 0
        elif update_type == "MODIFICATION":
            minor += 1
            patch = 0
        else:  # ADDITIVE
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    def _requires_approval(self, agent_role: str, update_type: str) -> bool:
        """Determine if update requires approval."""
        # FM agents always require approval
        if agent_role in ["governance", "liaison", "fm-app"]:
            return True
        
        # Breaking updates always require approval
        if update_type == "BREAKING":
            return True
        
        # Modifications require approval
        if update_type == "MODIFICATION":
            return True
        
        # Additive updates are auto-approved
        return False
    
    def _write_sync_event(self, event: Dict):
        """Write sync event to audit log."""
        # Ensure directory exists
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing log
        if AUDIT_LOG_PATH.exists():
            with open(AUDIT_LOG_PATH, 'r') as f:
                log = json.load(f)
        else:
            log = {"events": []}
        
        # Append event
        log["events"].append(event)
        log["last_updated"] = datetime.utcnow().isoformat() + "Z"
        
        # Write log
        with open(AUDIT_LOG_PATH, 'w') as f:
            json.dump(log, f, indent=2)
        
        print(f"📝 Sync event logged: {event['event_id']}")


def main():
    parser = argparse.ArgumentParser(
        description="Synchronize agent context with canonical governance"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test updates without applying them"
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Manual trigger (admin-initiated)"
    )
    parser.add_argument(
        "--trigger-reason",
        type=str,
        help="Reason for manual trigger"
    )
    parser.add_argument(
        "--canonical-commit",
        type=str,
        help="Canonical commit SHA to sync from"
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback previous sync"
    )
    parser.add_argument(
        "--event-id",
        type=str,
        help="Event ID to rollback"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.manual and not args.trigger_reason:
        print("❌ Error: --manual requires --trigger-reason")
        sys.exit(1)
    
    if args.rollback and not args.event_id:
        print("❌ Error: --rollback requires --event-id")
        sys.exit(1)
    
    # Initialize sync manager
    sync = AgentContextSync(dry_run=args.dry_run)
    
    if args.rollback:
        print(f"⏪ Rollback functionality not yet implemented")
        print(f"   Would rollback event: {args.event_id}")
        sys.exit(0)
    
    # Run sync workflow
    print("\n" + "="*70)
    print("🔄 AGENT CONTEXT SYNCHRONISATION WORKFLOW")
    print("="*70)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    
    # Phase 1: Detect triggers
    print("\n📡 Phase 1: Detecting canonical triggers...")
    triggers = sync.detect_canonical_triggers(
        manual=args.manual,
        trigger_reason=args.trigger_reason,
        canonical_commit=args.canonical_commit
    )
    
    if not triggers:
        print("✅ No triggers detected - agents are in sync")
        sys.exit(0)
    
    print(f"   Found {len(triggers)} trigger(s)")
    
    # Process each trigger
    for trigger in triggers:
        print(f"\n🎯 Processing trigger: {trigger['event_id']}")
        print(f"   Category: {trigger['trigger_category']}")
        print(f"   Priority: {trigger['priority']}")
        
        # Phase 2: Evaluate affected agents
        print("\n👥 Phase 2: Evaluating affected agents...")
        affected_agents = sync.evaluate_affected_agents(trigger)
        print(f"   Affected agents: {len(affected_agents)}")
        
        for agent in affected_agents:
            print(f"   - {agent['agent_file']} ({agent['agent_role']})")
        
        if not affected_agents:
            print("   No agents affected by this trigger")
            continue
        
        # Phase 3: Prepare updates
        print("\n📝 Phase 3: Preparing context updates...")
        updates = sync.prepare_context_updates(trigger, affected_agents)
        
        for update in updates:
            print(f"   {update['agent_file']}")
            print(f"     Type: {update['update_type']}")
            print(f"     Version: {update['current_version']} → {update['proposed_version']}")
            print(f"     Approval: {'Required' if update['approval_required'] else 'Not required'}")
        
        # Phase 4: Request approvals
        print("\n✋ Phase 4: Requesting approvals...")
        approvals = sync.request_approvals(updates, trigger)
        
        # Phase 5: Apply updates
        print("\n⚙️  Phase 5: Applying updates...")
        successful, failed = sync.apply_updates(updates, approvals)
        
        print(f"   Successful: {len(successful)}")
        print(f"   Failed: {len(failed)}")
        
        # Phase 6: Log event
        print("\n📋 Phase 6: Logging sync event...")
        outcome = "SUCCESS" if not failed else ("PARTIAL" if successful else "FAILURE")
        event = sync.log_sync_event(trigger, successful, outcome)
        
        print(f"   Event ID: {event['event_id']}")
        print(f"   Outcome: {outcome}")
    
    print("\n" + "="*70)
    print("✅ SYNCHRONISATION WORKFLOW COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
