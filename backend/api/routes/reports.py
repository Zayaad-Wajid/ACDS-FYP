"""
Reports API Routes
===================
API endpoints for AI-powered report generation.
"""

from typing import Optional
from datetime import datetime, timezone, timedelta
from enum import Enum
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

# Local model definitions
class ReportType(str, Enum):
    THREAT_SUMMARY = "threat_summary"
    DETECTION_ANALYSIS = "detection_analysis"
    INCIDENT_LOG = "incident_log"
    PERFORMANCE_METRICS = "performance_metrics"
    EXECUTIVE_SUMMARY = "executive_summary"
    COMPLIANCE_REPORT = "compliance_report"

class ReportRequest(BaseModel):
    report_type: ReportType
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_details: bool = True
    format: str = "json"

# Import report agent
try:
    from agents.report_agent import ReportGenerationAgent
except ImportError:
    try:
        from backend.agents.report_agent import ReportGenerationAgent
    except ImportError:
        ReportGenerationAgent = None

router = APIRouter(prefix="/reports", tags=["Reports"])

# Initialize report agent
report_agent = ReportGenerationAgent() if ReportGenerationAgent else None


@router.post("/generate")
async def generate_report(request: ReportRequest):
    """
    Generate an AI-powered threat report.
    
    Creates comprehensive reports based on threat data,
    detection logs, and system metrics.
    """
    try:
        # Set default date range if not provided
        end_date = request.end_date or datetime.now(timezone.utc)
        start_date = request.start_date or (end_date - timedelta(days=7))
        
        # Get mock threat data (would come from database in production)
        threat_data = _get_threat_data(start_date, end_date)
        
        # Generate report
        report = report_agent.generate_report(
            report_type=request.report_type.value,
            threat_data=threat_data,
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "success": True,
            "report": report
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def get_report_types():
    """Get available report types and their descriptions."""
    return {
        "success": True,
        "report_types": [
            {
                "type": "threat_summary",
                "name": "Threat Summary",
                "description": "Overview of all detected threats with severity breakdown"
            },
            {
                "type": "detection_analysis",
                "name": "Detection Analysis",
                "description": "Detailed analysis of detection patterns and trends"
            },
            {
                "type": "incident_log",
                "name": "Incident Log",
                "description": "Chronological log of all security incidents"
            },
            {
                "type": "performance_metrics",
                "name": "Performance Metrics",
                "description": "System performance and detection accuracy metrics"
            },
            {
                "type": "executive_summary",
                "name": "Executive Summary",
                "description": "High-level summary for management review"
            },
            {
                "type": "compliance_report",
                "name": "Compliance Report",
                "description": "Compliance-focused security posture report"
            }
        ]
    }


@router.get("/")
async def get_reports_list(
    report_type: Optional[str] = None,
    limit: int = Query(20, le=100)
):
    """Get list of previously generated reports."""
    # In production, this would fetch from database
    return {
        "success": True,
        "reports": [],
        "count": 0
    }


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Get a specific report by ID."""
    # In production, this would fetch from database
    raise HTTPException(status_code=404, detail="Report not found")


@router.get("/{report_id}/export")
async def export_report(
    report_id: str,
    format: str = Query("json", regex="^(json|pdf|html|txt)$")
):
    """
    Export a report in the specified format.
    
    Supported formats: json, pdf, html, txt
    """
    # In production, this would generate the export
    raise HTTPException(status_code=404, detail="Report not found")


@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """Delete a report."""
    # In production, this would delete from database
    raise HTTPException(status_code=404, detail="Report not found")


def _get_threat_data(start_date: datetime, end_date: datetime) -> dict:
    """
    Get threat data for report generation.
    In production, this would query the database.
    """
    # Mock data for demonstration
    return {
        "total_scans": 1250,
        "threats_detected": 47,
        "threats_blocked": 42,
        "false_positives": 3,
        "severity_breakdown": {
            "CRITICAL": 5,
            "HIGH": 12,
            "MEDIUM": 18,
            "LOW": 12
        },
        "threat_types": {
            "phishing": 28,
            "spear_phishing": 8,
            "business_email_compromise": 6,
            "credential_harvesting": 5
        },
        "daily_stats": [
            {"date": "2024-01-01", "scans": 180, "threats": 7},
            {"date": "2024-01-02", "scans": 175, "threats": 5},
            {"date": "2024-01-03", "scans": 190, "threats": 8},
            {"date": "2024-01-04", "scans": 165, "threats": 4},
            {"date": "2024-01-05", "scans": 200, "threats": 9},
            {"date": "2024-01-06", "scans": 170, "threats": 6},
            {"date": "2024-01-07", "scans": 170, "threats": 8},
        ],
        "top_senders": [
            {"email": "suspicious@phishing-domain.com", "count": 8},
            {"email": "fake-bank@scam.net", "count": 6},
            {"email": "urgent-verify@malicious.org", "count": 5},
        ],
        "response_actions": {
            "quarantined": 35,
            "blocked_senders": 18,
            "notifications_sent": 47
        },
        "model_performance": {
            "accuracy": 0.94,
            "precision": 0.92,
            "recall": 0.96,
            "f1_score": 0.94
        }
    }
