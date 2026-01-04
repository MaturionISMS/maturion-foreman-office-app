"""
BuildVisibilityUI (BUILD-04)

QA Coverage: QA-089 to QA-092

Manages UI for build progress visualization.
"""

from typing import Dict, Any, List


class BuildVisibilityUI:
    """
    BUILD-04: Build Visibility UI
    
    Handles UI for:
    - Build progress rendering
    - Builder status display
    - QA status grid
    - Real-time build updates
    """
    
    def __init__(self, context: Dict[str, Any]):
        """Initialize build visibility UI."""
        self.context = context
    
    def render_build_progress(self, build_progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-089: Render build progress.
        
        Args:
            build_progress_data: Build progress data
            
        Returns:
            Build progress UI output
        """
        return {
            "currentState": {
                "wave": build_progress_data.get("currentWave"),
                "phase": "build-to-green"
            },
            "progressBar": {
                "percentage": build_progress_data.get("progressPercentage"),
                "visualIndicator": {
                    "type": "bar",
                    "color": "blue"
                }
            },
            "qaSummary": {
                "total": build_progress_data.get("totalQA"),
                "green": build_progress_data.get("greenQA"),
                "red": build_progress_data.get("redQA")
            }
        }
    
    def render_builder_status(self, builders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        QA-090: Render builder status.
        
        Args:
            builders: List of builder data
            
        Returns:
            Builder status UI output
        """
        builder_uis = []
        for builder in builders:
            builder_ui = {
                "name": builder.get("name"),
                "statusIndicator": {
                    "status": builder.get("status"),
                    "visual": f"status-{builder.get('status')}"
                },
                "qaAssignment": {
                    "range": builder.get("assignedQA")
                },
                "progress": {
                    "green": builder.get("greenCount"),
                    "total": builder.get("totalCount"),
                    "percentage": (builder.get("greenCount", 0) / builder.get("totalCount", 1)) * 100
                }
            }
            builder_uis.append(builder_ui)
        
        return {
            "builders": builder_uis
        }
    
    def render_qa_status_grid(self, qa_status_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        QA-091: Render QA status grid.
        
        Args:
            qa_status_data: List of QA status items
            
        Returns:
            QA status grid UI output
        """
        cells = []
        for qa_item in qa_status_data:
            qa_id = qa_item.get("qaId")
            status = qa_item.get("status")
            
            cells.append({
                "qaId": qa_id,
                "status": status,
                "colorClass": f"qa-{status.lower()}",
                "clickable": True,
                "detailLink": f"/qa/{qa_id}/detail"
            })
        
        return {
            "grid": {
                "cells": cells,
                "layout": "responsive-grid",
                "columns": "auto",
                "responsive": True
            },
            "legend": {
                "GREEN": "Passing",
                "RED": "Failing",
                "AMBER": "Warnings"
            }
        }
    
    def apply_build_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-092: Apply real-time build update.
        
        Args:
            update_data: Build update data
            
        Returns:
            Build update UI output
        """
        return {
            "updateType": "realtime",
            "updatedBuilder": update_data.get("builder"),
            "newStatus": update_data.get("status"),
            "animation": {
                "enabled": True,
                "type": "pulse"
            },
            "notification": {
                "show": True,
                "message": f"Builder {update_data.get('builder')} status updated",
                "duration": 3000
            }
        }
    
    def apply_progress_update(self, updated_progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-092: Apply progress update.
        
        Args:
            updated_progress: Updated progress data
            
        Returns:
            Progress update UI output
        """
        return {
            "updateType": "realtime",
            "qaSummary": {
                "total": updated_progress.get("totalQA"),
                "green": updated_progress.get("greenQA"),
                "red": updated_progress.get("redQA")
            },
            "progressBar": {
                "percentage": updated_progress.get("progressPercentage")
            },
            "updateNotification": {
                "visible": True,
                "message": "Build progress updated",
                "type": "info"
            }
        }
