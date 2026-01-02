"""
ESC-03: Silence Detector
QA-105 to QA-109

Monitors build heartbeats and detects silence (2+ hours without updates).
Differentiates between intentional pauses and actual stalls.

**Inputs:**
- BuildHeartbeat event from EXEC-02 Build State Manager
- BuildPaused command from Build Control API

**Outputs:**
- SilenceDetected event → ESC-02 Escalation Manager
- SilenceRecovered event → ESC-02, CROSS-05 Audit Logger

**Failure Modes:**
- False positive prevention → Check pause state before escalating
- Heartbeat update failure → Log error, continue monitoring
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum


class SilenceType(Enum):
    """Types of silence."""
    INTENTIONAL_PAUSE = "intentional_pause"
    ACTUAL_STALL = "actual_stall"
    UNKNOWN = "unknown"


@dataclass
class BuildMonitor:
    """Tracks heartbeat for a specific build."""
    build_id: str
    last_update: datetime
    is_paused: bool = False
    pause_reason: Optional[str] = None
    silence_detected: bool = False
    silence_type: SilenceType = SilenceType.UNKNOWN
    escalated: bool = False


class SilenceDetector:
    """
    ESC-03: Silence Detector
    
    Monitors build heartbeats and detects stalls.
    Implements QA-105 to QA-109.
    """
    
    def __init__(self, silence_threshold_hours: float = 2.0):
        self.monitored_builds: Dict[str, BuildMonitor] = {}
        self.silence_threshold = timedelta(hours=silence_threshold_hours)
    
    def monitor_heartbeat(self, build_id: str, last_update: Optional[datetime] = None) -> Dict[str, any]:
        """
        QA-105: Monitor build heartbeat.
        
        Tracks last update time, compares with threshold, detects silence.
        
        Args:
            build_id: ID of build to monitor
            last_update: Timestamp of last update (defaults to now)
            
        Returns:
            Dict containing monitoring status
        """
        if last_update is None:
            last_update = datetime.now()
        
        if build_id not in self.monitored_builds:
            # Start monitoring new build
            self.monitored_builds[build_id] = BuildMonitor(
                build_id=build_id,
                last_update=last_update
            )
            
            return {
                'build_id': build_id,
                'status': 'monitoring_started',
                'last_update': last_update.isoformat(),
                'threshold': self.silence_threshold.total_seconds() / 3600,
                'silence_detected': False
            }
        
        # Update existing monitor
        monitor = self.monitored_builds[build_id]
        monitor.last_update = last_update
        
        # Check for silence
        elapsed = datetime.now() - monitor.last_update
        is_silent = elapsed >= self.silence_threshold
        
        return {
            'build_id': build_id,
            'last_update': last_update.isoformat(),
            'elapsed_hours': elapsed.total_seconds() / 3600,
            'threshold_hours': self.silence_threshold.total_seconds() / 3600,
            'silence_detected': is_silent,
            'is_paused': monitor.is_paused
        }
    
    def detect_silence(self, build_id: str) -> Dict[str, any]:
        """
        QA-106: Detect silence.
        
        Checks if build has been silent for 2+ hours. If yes, triggers escalation.
        
        Args:
            build_id: ID of build to check
            
        Returns:
            Dict containing detection result and escalation status
            
        Raises:
            KeyError: If build_id not being monitored
        """
        if build_id not in self.monitored_builds:
            raise KeyError(f"Build {build_id} not being monitored")
        
        monitor = self.monitored_builds[build_id]
        
        # Check elapsed time
        elapsed = datetime.now() - monitor.last_update
        is_silent = elapsed >= self.silence_threshold
        
        if is_silent and not monitor.silence_detected:
            # New silence detection
            monitor.silence_detected = True
            
            # Determine silence type
            monitor.silence_type = self._determine_silence_type(monitor)
            
            # Only escalate for actual stalls
            escalation_triggered = False
            if monitor.silence_type == SilenceType.ACTUAL_STALL:
                escalation_context = self._create_escalation_context(monitor, elapsed)
                self._trigger_escalation(monitor, escalation_context)
                monitor.escalated = True
                escalation_triggered = True
            
            return {
                'build_id': build_id,
                'silence_detected': True,
                'elapsed_hours': elapsed.total_seconds() / 3600,
                'threshold_hours': self.silence_threshold.total_seconds() / 3600,
                'silence_type': monitor.silence_type.value,
                'escalation_triggered': escalation_triggered,
                'escalation_context': self._create_escalation_context(monitor, elapsed) if escalation_triggered else None
            }
        
        return {
            'build_id': build_id,
            'silence_detected': is_silent,
            'already_detected': monitor.silence_detected,
            'silence_type': monitor.silence_type.value if is_silent else None
        }
    
    def differentiate_silence_type(self, build_id: str) -> Dict[str, any]:
        """
        QA-107: Differentiate silence types.
        
        Distinguishes between intentional pause and actual stall.
        
        Args:
            build_id: ID of build to analyze
            
        Returns:
            Dict containing silence type analysis
        """
        if build_id not in self.monitored_builds:
            raise KeyError(f"Build {build_id} not being monitored")
        
        monitor = self.monitored_builds[build_id]
        silence_type = self._determine_silence_type(monitor)
        
        return {
            'build_id': build_id,
            'silence_type': silence_type.value,
            'is_intentional_pause': silence_type == SilenceType.INTENTIONAL_PAUSE,
            'is_actual_stall': silence_type == SilenceType.ACTUAL_STALL,
            'is_paused': monitor.is_paused,
            'pause_reason': monitor.pause_reason,
            'handling': 'no_escalation' if silence_type == SilenceType.INTENTIONAL_PAUSE else 'escalate'
        }
    
    def handle_silence_recovery(self, build_id: str) -> Dict[str, any]:
        """
        QA-108: Silence recovery.
        
        Handles heartbeat restoration and escalation closure.
        
        Args:
            build_id: ID of recovered build
            
        Returns:
            Dict containing recovery status
        """
        if build_id not in self.monitored_builds:
            raise KeyError(f"Build {build_id} not being monitored")
        
        monitor = self.monitored_builds[build_id]
        
        was_silent = monitor.silence_detected
        was_escalated = monitor.escalated
        
        # Update heartbeat
        monitor.last_update = datetime.now()
        monitor.silence_detected = False
        
        # Close escalation if one was created
        if monitor.escalated:
            self._close_escalation(monitor)
            monitor.escalated = False
        
        return {
            'build_id': build_id,
            'heartbeat_restored': True,
            'was_silent': was_silent,
            'escalation_closed': was_escalated,
            'restored_at': datetime.now().isoformat()
        }
    
    def pause_build(self, build_id: str, reason: str) -> None:
        """Mark build as intentionally paused."""
        if build_id not in self.monitored_builds:
            self.monitored_builds[build_id] = BuildMonitor(
                build_id=build_id,
                last_update=datetime.now()
            )
        
        monitor = self.monitored_builds[build_id]
        monitor.is_paused = True
        monitor.pause_reason = reason
    
    def resume_build(self, build_id: str) -> None:
        """Mark build as resumed."""
        if build_id in self.monitored_builds:
            monitor = self.monitored_builds[build_id]
            monitor.is_paused = False
            monitor.pause_reason = None
            monitor.last_update = datetime.now()
    
    def handle_failure_modes(self, failure_type: str, **kwargs) -> Dict[str, any]:
        """
        QA-109: Handle silence detector failure modes.
        
        Handles:
        - False positive prevention
        - Heartbeat update failure
        
        Args:
            failure_type: Type of failure
            **kwargs: Additional context
            
        Returns:
            Dict describing how failure was handled
        """
        if failure_type == 'false_positive':
            build_id = kwargs.get('build_id')
            if build_id and build_id in self.monitored_builds:
                monitor = self.monitored_builds[build_id]
                
                # Check pause state before escalating
                if monitor.is_paused:
                    return {
                        'status': 'false_positive_prevented',
                        'reason': 'Build is intentionally paused',
                        'pause_reason': monitor.pause_reason,
                        'escalation_suppressed': True
                    }
            
            return {
                'status': 'checked',
                'escalation_allowed': True
            }
        
        elif failure_type == 'heartbeat_update_failure':
            error = kwargs.get('error')
            build_id = kwargs.get('build_id')
            
            # Log error but continue monitoring
            return {
                'status': 'logged',
                'error': str(error),
                'build_id': build_id,
                'monitoring_continued': True,
                'action': 'Continue with last known update time'
            }
        
        return {'status': 'error', 'reason': f'Unknown failure type: {failure_type}'}
    
    def _determine_silence_type(self, monitor: BuildMonitor) -> SilenceType:
        """Determine if silence is intentional pause or actual stall."""
        if monitor.is_paused:
            return SilenceType.INTENTIONAL_PAUSE
        else:
            return SilenceType.ACTUAL_STALL
    
    def _create_escalation_context(self, monitor: BuildMonitor, elapsed: timedelta) -> Dict[str, any]:
        """Create context for silence escalation."""
        return {
            'issue': 'BuildSilence',
            'build_id': monitor.build_id,
            'elapsed_hours': elapsed.total_seconds() / 3600,
            'threshold_hours': self.silence_threshold.total_seconds() / 3600,
            'last_update': monitor.last_update.isoformat(),
            'is_paused': monitor.is_paused
        }
    
    def _trigger_escalation(self, monitor: BuildMonitor, context: Dict[str, any]) -> None:
        """Trigger escalation to ESC-02."""
        # In production, this would create actual escalation via ESC-02
        pass
    
    def _close_escalation(self, monitor: BuildMonitor) -> None:
        """Close escalation when silence recovers."""
        # In production, this would close actual escalation via ESC-02
        pass
