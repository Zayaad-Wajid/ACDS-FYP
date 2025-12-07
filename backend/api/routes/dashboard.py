"""
Dashboard API Routes
=====================
API endpoints for dashboard data and real-time statistics.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Query
import random

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats():
    """
    Get main dashboard statistics.
    
    Returns key metrics for the dashboard overview.
    """
    # In production, these would come from the database
    return {
        "success": True,
        "stats": {
            "total_threats": 1247,
            "threats_blocked": 1189,
            "active_threats": 12,
            "resolved_today": 8,
            "detection_rate": 95.3,
            "false_positive_rate": 2.1,
            "avg_response_time_ms": 245,
            "emails_scanned_today": 3421,
            "model_accuracy": 97.2,
            "system_uptime": "99.9%"
        },
        # Also include top-level for frontend compatibility
        "total_threats": 1247,
        "threats_blocked": 1189,
        "active_threats": 12,
        "resolved_today": 8,
        "detection_rate": 95.3,
        "emails_scanned_today": 3421,
        "model_accuracy": 97.2
    }


# Frontend-compatible routes
@router.get("/recent-threats")
async def get_recent_threats_compat(
    limit: int = Query(10, le=50),
    severity: Optional[str] = None
):
    """Get recent threats (frontend compatible route)."""
    return await get_recent_threats(limit, severity)


@router.get("/model-status")
async def get_model_status_compat():
    """Get model status (frontend compatible route)."""
    perf = await get_model_performance()
    return {
        "success": True,
        "model_loaded": True,
        "version": "2.0.0",
        "last_trained": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
        "accuracy": 97.2,
        "precision": 96.8,
        "recall": 98.1,
        "f1_score": 97.4,
        "total_predictions": 45892,
        "confusion_matrix": {
            "tp": 2341,
            "fp": 48,
            "fn": 47,
            "tn": 43456
        },
        "accuracy_history": [
            {"date": "2025-11-28", "accuracy": 96.5},
            {"date": "2025-11-29", "accuracy": 96.8},
            {"date": "2025-11-30", "accuracy": 97.0},
            {"date": "2025-12-01", "accuracy": 97.1},
            {"date": "2025-12-02", "accuracy": 97.2},
            {"date": "2025-12-03", "accuracy": 97.2},
            {"date": "2025-12-04", "accuracy": 97.2}
        ],
        "logs": [
            {"timestamp": datetime.now(timezone.utc).isoformat(), "event": "Model prediction", "status": "success"},
            {"timestamp": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(), "event": "Batch scan completed", "status": "success"},
            {"timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(), "event": "Model health check", "status": "success"}
        ]
    }


@router.get("/activity")
async def get_activity_compat(limit: int = Query(20, le=100)):
    """Get activity (frontend compatible route)."""
    # Generate activity data for timeline
    activity = []
    for i in range(7):
        date = datetime.now(timezone.utc) - timedelta(days=6 - i)
        activity.append({
            "date": date.strftime("%Y-%m-%d"),
            "threats": random.randint(10, 50),
            "scans": random.randint(200, 500),
            "blocked": random.randint(8, 45)
        })
    return {
        "success": True,
        "activity": activity
    }


@router.get("/threats/recent")
async def get_recent_threats(
    limit: int = Query(10, le=50),
    severity: Optional[str] = None
):
    """
    Get recent threat detections.
    
    Returns list of recently detected threats for the dashboard feed.
    """
    # Mock data - would come from database
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    threat_types = ["Phishing", "Spear Phishing", "BEC", "Credential Harvesting"]
    statuses = ["Active", "Resolved", "Investigating", "Quarantined"]
    
    threats = []
    for i in range(limit):
        threat_severity = severity or random.choice(severities)
        threats.append({
            "id": f"THR-{1000 + i}",
            "type": random.choice(threat_types),
            "severity": threat_severity,
            "confidence": round(random.uniform(75, 99), 1),
            "status": random.choice(statuses),
            "source": f"suspicious_{i}@phishing-domain.com",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 48))).isoformat(),
            "description": "Suspicious email with phishing indicators detected"
        })
    
    return {
        "success": True,
        "threats": threats,
        "count": len(threats)
    }


@router.get("/threats/timeline")
async def get_threat_timeline(
    days: int = Query(7, le=30)
):
    """
    Get threat detection timeline data for charts.
    """
    timeline = []
    for i in range(days):
        date = datetime.now(timezone.utc) - timedelta(days=days - i - 1)
        timeline.append({
            "date": date.strftime("%Y-%m-%d"),
            "threats_detected": random.randint(10, 50),
            "threats_blocked": random.randint(8, 45),
            "emails_scanned": random.randint(200, 500)
        })
    
    return {
        "success": True,
        "timeline": timeline
    }


@router.get("/threats/by-severity")
async def get_threats_by_severity():
    """
    Get threat breakdown by severity level.
    """
    return {
        "success": True,
        "breakdown": {
            "CRITICAL": 15,
            "HIGH": 47,
            "MEDIUM": 89,
            "LOW": 96
        }
    }


@router.get("/threats/by-type")
async def get_threats_by_type():
    """
    Get threat breakdown by attack type.
    """
    return {
        "success": True,
        "breakdown": {
            "Phishing": 145,
            "Spear Phishing": 42,
            "Business Email Compromise": 28,
            "Credential Harvesting": 35,
            "Malware Distribution": 18,
            "Other": 12
        }
    }


@router.get("/activity/recent")
async def get_recent_activity(limit: int = Query(20, le=100)):
    """
    Get recent system activity log.
    """
    activities = [
        {"type": "scan", "message": "Email scanned - Clean", "timestamp": datetime.now(timezone.utc).isoformat()},
        {"type": "threat", "message": "Phishing email detected and quarantined", "timestamp": datetime.now(timezone.utc).isoformat()},
        {"type": "block", "message": "Sender blocked: malicious@phishing.com", "timestamp": datetime.now(timezone.utc).isoformat()},
        {"type": "report", "message": "Daily threat report generated", "timestamp": datetime.now(timezone.utc).isoformat()},
        {"type": "feedback", "message": "False positive reported and reviewed", "timestamp": datetime.now(timezone.utc).isoformat()},
    ]
    
    return {
        "success": True,
        "activities": activities * (limit // 5 + 1),
        "count": limit
    }


@router.get("/model/performance")
async def get_model_performance():
    """
    Get ML model performance metrics.
    """
    return {
        "success": True,
        "performance": {
            "accuracy": 97.2,
            "precision": 96.8,
            "recall": 98.1,
            "f1_score": 97.4,
            "auc_roc": 99.1,
            "total_predictions": 45892,
            "true_positives": 2341,
            "false_positives": 48,
            "true_negatives": 43456,
            "false_negatives": 47,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    }


@router.get("/alerts")
async def get_active_alerts():
    """
    Get active system alerts and notifications.
    """
    return {
        "success": True,
        "alerts": [
            {
                "id": "alert-001",
                "type": "warning",
                "title": "Elevated Threat Activity",
                "message": "15% increase in phishing attempts detected in the last hour",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "read": False
            },
            {
                "id": "alert-002",
                "type": "info",
                "title": "Model Update Available",
                "message": "New model version 2.1.0 is available for deployment",
                "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
                "read": True
            }
        ],
        "unread_count": 1
    }


@router.get("/system/health")
async def get_system_health():
    """
    Get overall system health status.
    """
    return {
        "success": True,
        "health": {
            "overall_status": "healthy",
            "services": {
                "api_server": {"status": "healthy", "latency_ms": 12},
                "ml_model": {"status": "healthy", "loaded": True},
                "database": {"status": "healthy", "connections": 5},
                "email_scanner": {"status": "healthy", "queue_size": 0}
            },
            "resources": {
                "cpu_usage": 23.5,
                "memory_usage": 45.2,
                "disk_usage": 38.7
            },
            "last_check": datetime.now(timezone.utc).isoformat()
        }
    }
