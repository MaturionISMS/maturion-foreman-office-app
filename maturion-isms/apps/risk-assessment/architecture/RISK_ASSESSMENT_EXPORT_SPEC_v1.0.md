# RISK_ASSESSMENT_EXPORT_SPEC_v1.0.md

## Risk Assessment - Export Specification
**Version**: 1.0  
**Date**: 2025-12-04

## Export Formats
- CSV: Spreadsheet format for Excel/Sheets
- JSON: Machine-readable format
- PDF: Human-readable reports

## Export Endpoints
- `/api/risk-assessment/export/csv`: Export to CSV
- `/api/risk-assessment/export/json`: Export to JSON
- `/api/risk-assessment/export/pdf`: Export to PDF

## Export Scope
- All records (filtered by organisation_id)
- Selected records (by ID list)
- Filtered records (by search/filter criteria)
- Date range exports

## Security
- Requires authentication
- RLS policies enforced
- Audit log entry created
- Rate limiting applied

## File Format
- UTF-8 encoding
- Standard delimiters (CSV)
- Pretty-printed JSON
- A4 page size (PDF)

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
