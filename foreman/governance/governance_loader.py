"""
GOV-01: Governance Loader
QA-117 to QA-120

Loads governance repository at startup, parses rules, caches in memory.
Ensures governance rules are available for validation and enforcement.

**Inputs:**
- Startup trigger
- GovernanceRefresh command

**Outputs:**
- GovernanceLoaded event → GOV-02, GOV-03
- GovernanceRulesAvailable → All components

**Failure Modes:**
- Repository unavailable → Retry 3x → Use cached version → Escalate if critical
- Parse failure → Log error, skip malformed rules, escalate
- Cache corruption → Rebuild cache from source
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class GovernanceRule:
    """Represents a parsed governance rule."""
    rule_id: str
    name: str
    category: str  # 'validation' or 'enforcement'
    content: str
    severity: str  # 'hard' or 'soft'
    source_file: str
    loaded_at: datetime = field(default_factory=datetime.now)


class GovernanceLoader:
    """
    GOV-01: Governance Loader
    
    Loads and parses governance rules from repository.
    Implements QA-117 to QA-120.
    """
    
    def __init__(self, governance_repo_path: Optional[str] = None):
        self.governance_repo_path = governance_repo_path or "governance"
        self.rules: Dict[str, GovernanceRule] = {}
        self.cache: Dict[str, any] = {}
        self.load_status: Dict[str, any] = {}
        self.max_retries = 3
    
    def load_governance_repository(self) -> Dict[str, any]:
        """
        QA-117: Load governance repository at startup.
        
        Clones/pulls repository, loads BUILD_PHILOSOPHY.md and specs.
        
        Returns:
            Dict containing load status and summary
            
        Raises:
            RuntimeError: If repository unavailable after retries
        """
        retry_count = 0
        last_error = None
        
        while retry_count < self.max_retries:
            try:
                # QA-117: Clone/pull repository
                repo_status = self._sync_repository()
                
                # Load BUILD_PHILOSOPHY.md
                philosophy_loaded = self._load_build_philosophy()
                
                # Load governance specs
                specs_loaded = self._load_governance_specs()
                
                self.load_status = {
                    'status': 'success',
                    'repository_synced': repo_status,
                    'build_philosophy_loaded': philosophy_loaded,
                    'specs_loaded': specs_loaded,
                    'rules_count': len(self.rules),
                    'loaded_at': datetime.now().isoformat(),
                    'retry_count': retry_count
                }
                
                return self.load_status
            
            except Exception as e:
                last_error = e
                retry_count += 1
                
                if retry_count >= self.max_retries:
                    # QA-120: Repository unavailable handling
                    # Try to use cached version
                    if self._has_valid_cache():
                        self._load_from_cache()
                        return {
                            'status': 'cached',
                            'warning': 'Repository unavailable, using cached rules',
                            'error': str(last_error),
                            'rules_count': len(self.rules),
                            'cache_age': self._get_cache_age()
                        }
                    
                    # No cache available - escalate
                    raise RuntimeError(
                        f"Governance repository unavailable after {self.max_retries} retries: {str(last_error)}"
                    )
        
        return {'status': 'error'}  # Should not reach here
    
    def parse_governance_rules(self) -> Dict[str, any]:
        """
        QA-118: Parse governance rules.
        
        Extracts rules from loaded files, creates validation and enforcement rules.
        
        Returns:
            Dict containing parsing results
        """
        validation_rules: List[GovernanceRule] = []
        enforcement_rules: List[GovernanceRule] = []
        parse_errors: List[Dict[str, any]] = []
        
        # Parse BUILD_PHILOSOPHY.md
        try:
            philosophy_rules = self._parse_build_philosophy()
            for rule in philosophy_rules:
                if rule.category == 'validation':
                    validation_rules.append(rule)
                else:
                    enforcement_rules.append(rule)
                self.rules[rule.rule_id] = rule
        except Exception as e:
            # QA-120: Parse failure handling
            parse_errors.append({
                'file': 'BUILD_PHILOSOPHY.md',
                'error': str(e),
                'action': 'logged_and_escalated'
            })
        
        # Parse governance specs
        spec_files = [
            'minimum-architecture-template.md',
            'qa-governance.md',
            'qa-minimum-coverage-requirements.md',
            'versioning-rules.md'
        ]
        
        for spec_file in spec_files:
            try:
                spec_rules = self._parse_spec_file(spec_file)
                for rule in spec_rules:
                    if rule.category == 'validation':
                        validation_rules.append(rule)
                    else:
                        enforcement_rules.append(rule)
                    self.rules[rule.rule_id] = rule
            except Exception as e:
                # Skip malformed rules, log error
                parse_errors.append({
                    'file': spec_file,
                    'error': str(e),
                    'action': 'skipped'
                })
        
        return {
            'validation_rules_count': len(validation_rules),
            'enforcement_rules_count': len(enforcement_rules),
            'total_rules': len(self.rules),
            'parse_errors': parse_errors,
            'status': 'success' if not parse_errors else 'partial_success'
        }
    
    def cache_governance(self) -> Dict[str, any]:
        """
        QA-119: Cache governance in memory.
        
        Creates in-memory cache for fast access.
        Supports cache refresh on governance updates.
        
        Returns:
            Dict containing cache status
        """
        try:
            # Build cache structure
            self.cache = {
                'rules': {rule_id: self._serialize_rule(rule) for rule_id, rule in self.rules.items()},
                'categories': {
                    'validation': [r.rule_id for r in self.rules.values() if r.category == 'validation'],
                    'enforcement': [r.rule_id for r in self.rules.values() if r.category == 'enforcement']
                },
                'severity': {
                    'hard': [r.rule_id for r in self.rules.values() if r.severity == 'hard'],
                    'soft': [r.rule_id for r in self.rules.values() if r.severity == 'soft']
                },
                'cached_at': datetime.now().isoformat()
            }
            
            # Persist cache to disk for recovery
            self._persist_cache()
            
            return {
                'status': 'cached',
                'rules_count': len(self.rules),
                'cache_size_kb': len(json.dumps(self.cache)) / 1024,
                'cached_at': self.cache['cached_at']
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def refresh_cache(self) -> Dict[str, any]:
        """Refresh cache when governance is updated."""
        # Reload from repository
        load_result = self.load_governance_repository()
        
        if load_result['status'] == 'success':
            # Parse rules
            parse_result = self.parse_governance_rules()
            
            # Update cache
            cache_result = self.cache_governance()
            
            return {
                'status': 'refreshed',
                'load_result': load_result,
                'parse_result': parse_result,
                'cache_result': cache_result
            }
        
        return {
            'status': 'failed',
            'reason': 'Repository load failed'
        }
    
    def get_rule(self, rule_id: str) -> Optional[GovernanceRule]:
        """Get a specific rule by ID."""
        return self.rules.get(rule_id)
    
    def get_rules_by_category(self, category: str) -> List[GovernanceRule]:
        """Get all rules in a category."""
        return [rule for rule in self.rules.values() if rule.category == category]
    
    def get_rules_by_severity(self, severity: str) -> List[GovernanceRule]:
        """Get all rules with a severity level."""
        return [rule for rule in self.rules.values() if rule.severity == severity]
    
    def handle_failure_modes(self, failure_type: str, **kwargs) -> Dict[str, any]:
        """
        QA-120: Handle governance loader failure modes.
        
        Handles:
        - Repository unavailable
        - Parse failure
        - Cache corruption
        
        Args:
            failure_type: Type of failure
            **kwargs: Additional context
            
        Returns:
            Dict describing how failure was handled
        """
        if failure_type == 'repository_unavailable':
            if self._has_valid_cache():
                self._load_from_cache()
                return {
                    'status': 'using_cache',
                    'cache_age': self._get_cache_age(),
                    'rules_count': len(self.rules)
                }
            else:
                return {
                    'status': 'critical',
                    'action': 'escalate',
                    'reason': 'No valid cache available'
                }
        
        elif failure_type == 'parse_failure':
            file_name = kwargs.get('file_name')
            error = kwargs.get('error')
            
            return {
                'status': 'logged',
                'file': file_name,
                'error': str(error),
                'action': 'skipped_malformed_rules',
                'escalated': True
            }
        
        elif failure_type == 'cache_corruption':
            # Rebuild cache from source
            try:
                self.cache = {}
                self.load_governance_repository()
                self.parse_governance_rules()
                self.cache_governance()
                
                return {
                    'status': 'recovered',
                    'action': 'rebuilt_cache_from_source',
                    'rules_count': len(self.rules)
                }
            except Exception as e:
                return {
                    'status': 'failed',
                    'action': 'escalate',
                    'error': str(e)
                }
        
        return {'status': 'error', 'reason': f'Unknown failure type: {failure_type}'}
    
    def _sync_repository(self) -> Dict[str, any]:
        """Sync governance repository (clone/pull)."""
        # In production, this would do actual git operations
        return {
            'synced': True,
            'method': 'simulated',
            'timestamp': datetime.now().isoformat()
        }
    
    def _load_build_philosophy(self) -> bool:
        """Load BUILD_PHILOSOPHY.md."""
        # In production, this would read actual file
        return True
    
    def _load_governance_specs(self) -> Dict[str, bool]:
        """Load governance specification files."""
        # In production, this would read actual files
        return {
            'minimum-architecture-template.md': True,
            'qa-governance.md': True,
            'qa-minimum-coverage-requirements.md': True,
            'versioning-rules.md': True
        }
    
    def _parse_build_philosophy(self) -> List[GovernanceRule]:
        """Parse BUILD_PHILOSOPHY.md into rules."""
        # Simulated rules for testing
        return [
            GovernanceRule(
                rule_id='BP-001',
                name='One-Time Build Correctness',
                category='enforcement',
                content='Build must be correct on first attempt',
                severity='hard',
                source_file='BUILD_PHILOSOPHY.md'
            ),
            GovernanceRule(
                rule_id='BP-002',
                name='Zero Regression',
                category='enforcement',
                content='No breaking changes to working code',
                severity='hard',
                source_file='BUILD_PHILOSOPHY.md'
            )
        ]
    
    def _parse_spec_file(self, filename: str) -> List[GovernanceRule]:
        """Parse a spec file into rules."""
        # Simulated parsing for testing
        return []
    
    def _serialize_rule(self, rule: GovernanceRule) -> Dict[str, any]:
        """Serialize a rule for caching."""
        return {
            'rule_id': rule.rule_id,
            'name': rule.name,
            'category': rule.category,
            'content': rule.content,
            'severity': rule.severity,
            'source_file': rule.source_file,
            'loaded_at': rule.loaded_at.isoformat()
        }
    
    def _persist_cache(self) -> None:
        """Persist cache to disk."""
        # In production, would write to file
        pass
    
    def _has_valid_cache(self) -> bool:
        """Check if valid cache exists."""
        return bool(self.cache and 'rules' in self.cache)
    
    def _get_cache_age(self) -> str:
        """Get age of cache."""
        if 'cached_at' in self.cache:
            cached_time = datetime.fromisoformat(self.cache['cached_at'])
            age = datetime.now() - cached_time
            return f"{age.total_seconds() / 3600:.1f} hours"
        return "unknown"
    
    def _load_from_cache(self) -> None:
        """Load rules from cache."""
        if self._has_valid_cache():
            self.rules = {}
            for rule_id, rule_data in self.cache['rules'].items():
                self.rules[rule_id] = GovernanceRule(
                    rule_id=rule_data['rule_id'],
                    name=rule_data['name'],
                    category=rule_data['category'],
                    content=rule_data['content'],
                    severity=rule_data['severity'],
                    source_file=rule_data['source_file'],
                    loaded_at=datetime.fromisoformat(rule_data['loaded_at'])
                )
