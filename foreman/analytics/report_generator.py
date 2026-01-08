"""
Custom Report Generator for Advanced Analytics Phase 2.

QA Coverage: QA-456 to QA-460
Provides report template creation, data aggregation, rendering, export, and scheduling.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

# Shared storage for report templates, data, and schedules
_report_templates = {}
_report_data = {}
_rendered_reports = {}
_report_schedules = {}


def clear_all():
    """Clear all report generator state for testing."""
    global _report_templates, _report_data, _rendered_reports, _report_schedules
    _report_templates = {}
    _report_data = {}
    _rendered_reports = {}
    _report_schedules = {}


class ReportGenerator:
    """Generates custom reports with templates, aggregation, and scheduling. QA-456 to QA-460"""
    
    def __init__(self, organisation_id: str):
        """
        Initialize report generator for organisation.
        
        Args:
            organisation_id: Organisation ID for tenant isolation
        """
        self.organisation_id = organisation_id
        if organisation_id not in _report_templates:
            _report_templates[organisation_id] = {}
        if organisation_id not in _report_data:
            _report_data[organisation_id] = {}
        if organisation_id not in _rendered_reports:
            _rendered_reports[organisation_id] = {}
        if organisation_id not in _report_schedules:
            _report_schedules[organisation_id] = {}
    
    def create_template(self, template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a report template. QA-456
        
        Args:
            template_config: Configuration including name, sections, and formatting
        
        Returns:
            Created template with ID and metadata
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate configuration
        if not template_config.get('name'):
            raise ValueError("Template name is required")
        if not template_config.get('sections'):
            raise ValueError("Template sections are required")
        
        # Generate template ID
        template_id = f"template_{self.organisation_id}_{datetime.now().timestamp()}"
        
        # Create template
        template = {
            "template_id": template_id,
            "name": template_config['name'],
            "sections": template_config['sections'],
            "formatting": template_config.get('formatting', {
                "page_size": "A4",
                "orientation": "portrait",
                "font": "Arial",
                "font_size": 12
            }),
            "organisation_id": self.organisation_id,
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
        # Store template
        _report_templates[self.organisation_id][template_id] = template
        
        return template
    
    def aggregate_data(self, data_sources: List[Dict[str, Any]], aggregation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate data from multiple sources. QA-457
        
        Args:
            data_sources: List of data sources to aggregate
            aggregation_rules: Rules for aggregation (e.g., sum, average, count)
        
        Returns:
            Aggregated data ready for report rendering
        """
        aggregation_type = aggregation_rules.get('type', 'sum')
        group_by = aggregation_rules.get('group_by', None)
        
        # Collect all data points
        all_data = []
        for source in data_sources:
            source_data = source.get('data', [])
            all_data.extend(source_data)
        
        if not all_data:
            return {
                "total_records": 0,
                "aggregated_value": 0,
                "grouped_results": {},
                "aggregation_type": aggregation_type
            }
        
        # Aggregate data
        if aggregation_type == 'sum':
            aggregated_value = sum(item.get('value', 0) for item in all_data)
        elif aggregation_type == 'average':
            values = [item.get('value', 0) for item in all_data]
            aggregated_value = sum(values) / len(values) if values else 0
        elif aggregation_type == 'count':
            aggregated_value = len(all_data)
        elif aggregation_type == 'max':
            aggregated_value = max(item.get('value', 0) for item in all_data)
        elif aggregation_type == 'min':
            aggregated_value = min(item.get('value', 0) for item in all_data)
        else:
            aggregated_value = len(all_data)  # Default to count
        
        # Group by if specified
        grouped_results = {}
        if group_by:
            for item in all_data:
                group_key = item.get(group_by, 'unknown')
                if group_key not in grouped_results:
                    grouped_results[group_key] = []
                grouped_results[group_key].append(item)
        
        # Store aggregated data
        aggregation_id = f"agg_{self.organisation_id}_{datetime.now().timestamp()}"
        aggregated_data = {
            "aggregation_id": aggregation_id,
            "total_records": len(all_data),
            "aggregated_value": aggregated_value,
            "grouped_results": grouped_results,
            "aggregation_type": aggregation_type,
            "timestamp": datetime.now().isoformat()
        }
        
        _report_data[self.organisation_id][aggregation_id] = aggregated_data
        
        return aggregated_data
    
    def render_report(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render a report using template and data. QA-458
        
        Args:
            template_id: ID of the template to use
            data: Data to populate the report
        
        Returns:
            Rendered report with content and metadata
        
        Raises:
            ValueError: If template not found
        """
        # Validate template exists
        if template_id not in _report_templates[self.organisation_id]:
            raise ValueError(f"Template {template_id} not found")
        
        template = _report_templates[self.organisation_id][template_id]
        
        # Generate report ID
        report_id = f"report_{self.organisation_id}_{datetime.now().timestamp()}"
        
        # Render report sections
        rendered_sections = []
        for section in template['sections']:
            section_name = section.get('name', 'Untitled')
            section_type = section.get('type', 'text')
            
            # Render section based on type
            if section_type == 'table':
                content = self._render_table_section(data, section)
            elif section_type == 'chart':
                content = self._render_chart_section(data, section)
            elif section_type == 'summary':
                content = self._render_summary_section(data, section)
            else:
                content = str(data.get(section_name, ''))
            
            rendered_sections.append({
                "name": section_name,
                "type": section_type,
                "content": content
            })
        
        # Create rendered report
        rendered_report = {
            "report_id": report_id,
            "template_id": template_id,
            "template_name": template['name'],
            "sections": rendered_sections,
            "formatting": template['formatting'],
            "organisation_id": self.organisation_id,
            "generated_at": datetime.now().isoformat(),
            "status": "rendered"
        }
        
        # Store rendered report
        _rendered_reports[self.organisation_id][report_id] = rendered_report
        
        return rendered_report
    
    def _render_table_section(self, data: Dict[str, Any], section: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to render table section."""
        data_key = section.get('data_key', 'table_data')
        table_data = data.get(data_key, [])
        
        return {
            "type": "table",
            "headers": section.get('headers', []),
            "rows": table_data
        }
    
    def _render_chart_section(self, data: Dict[str, Any], section: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to render chart section."""
        data_key = section.get('data_key', 'chart_data')
        chart_data = data.get(data_key, [])
        
        return {
            "type": "chart",
            "chart_type": section.get('chart_type', 'bar'),
            "data": chart_data,
            "x_axis": section.get('x_axis', 'X'),
            "y_axis": section.get('y_axis', 'Y')
        }
    
    def _render_summary_section(self, data: Dict[str, Any], section: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to render summary section."""
        metrics = section.get('metrics', [])
        summary = {}
        
        for metric in metrics:
            metric_key = metric.get('key', '')
            metric_label = metric.get('label', metric_key)
            summary[metric_label] = data.get(metric_key, 0)
        
        return {
            "type": "summary",
            "metrics": summary
        }
    
    def export_report(self, report_id: str, format: str) -> Dict[str, Any]:
        """
        Export rendered report to specified format. QA-459
        
        Args:
            report_id: ID of the rendered report
            format: Export format (pdf, html, json, csv)
        
        Returns:
            Export result with file path and metadata
        
        Raises:
            ValueError: If report not found or format unsupported
        """
        # Validate report exists
        if report_id not in _rendered_reports[self.organisation_id]:
            raise ValueError(f"Report {report_id} not found")
        
        # Validate format
        supported_formats = ['pdf', 'html', 'json', 'csv']
        if format not in supported_formats:
            raise ValueError(f"Unsupported format: {format}. Supported: {supported_formats}")
        
        report = _rendered_reports[self.organisation_id][report_id]
        
        # Generate export file path
        file_name = f"{report_id}.{format}"
        file_path = f"/tmp/reports/{self.organisation_id}/{file_name}"
        
        # Export based on format
        if format == 'json':
            content = json.dumps(report, indent=2)
        elif format == 'html':
            content = self._export_to_html(report)
        elif format == 'pdf':
            content = f"PDF export of {report['template_name']}"
        elif format == 'csv':
            content = self._export_to_csv(report)
        else:
            content = str(report)
        
        # Create export record
        export_record = {
            "report_id": report_id,
            "format": format,
            "file_path": file_path,
            "file_size": len(content),
            "exported_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        return export_record
    
    def _export_to_html(self, report: Dict[str, Any]) -> str:
        """Helper to export report to HTML."""
        html = f"<html><head><title>{report['template_name']}</title></head><body>"
        html += f"<h1>{report['template_name']}</h1>"
        
        for section in report['sections']:
            html += f"<div class='section'><h2>{section['name']}</h2>"
            html += f"<div>{section['content']}</div></div>"
        
        html += "</body></html>"
        return html
    
    def _export_to_csv(self, report: Dict[str, Any]) -> str:
        """Helper to export report to CSV."""
        csv_lines = [f"Report: {report['template_name']}"]
        
        for section in report['sections']:
            csv_lines.append(f"\n{section['name']}")
            if isinstance(section['content'], dict) and section['content'].get('type') == 'table':
                headers = section['content'].get('headers', [])
                csv_lines.append(','.join(headers))
                for row in section['content'].get('rows', []):
                    csv_lines.append(','.join(str(cell) for cell in row))
        
        return '\n'.join(csv_lines)
    
    def schedule_report(self, template_id: str, schedule_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule automatic report generation. QA-460
        
        Args:
            template_id: ID of template to use
            schedule_config: Schedule configuration (frequency, time, recipients)
        
        Returns:
            Schedule record with ID and configuration
        
        Raises:
            ValueError: If template not found or schedule invalid
        """
        # Validate template exists
        if template_id not in _report_templates[self.organisation_id]:
            raise ValueError(f"Template {template_id} not found")
        
        # Validate schedule configuration
        if not schedule_config.get('frequency'):
            raise ValueError("Schedule frequency is required")
        
        # Generate schedule ID
        schedule_id = f"schedule_{self.organisation_id}_{datetime.now().timestamp()}"
        
        # Calculate next run time
        frequency = schedule_config['frequency']
        if frequency == 'daily':
            next_run = datetime.now() + timedelta(days=1)
        elif frequency == 'weekly':
            next_run = datetime.now() + timedelta(weeks=1)
        elif frequency == 'monthly':
            next_run = datetime.now() + timedelta(days=30)
        else:
            next_run = datetime.now() + timedelta(hours=1)
        
        # Create schedule
        schedule = {
            "schedule_id": schedule_id,
            "template_id": template_id,
            "frequency": frequency,
            "recipients": schedule_config.get('recipients', []),
            "format": schedule_config.get('format', 'pdf'),
            "next_run": next_run.isoformat(),
            "status": "active",
            "organisation_id": self.organisation_id,
            "created_at": datetime.now().isoformat()
        }
        
        # Store schedule
        _report_schedules[self.organisation_id][schedule_id] = schedule
        
        return schedule
