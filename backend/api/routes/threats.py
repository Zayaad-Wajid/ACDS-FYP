"""
Threat Detection API Routes
============================
API endpoints for email scanning and threat detection.
"""

import time
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

# Define local models
class EmailScanRequest(BaseModel):
    content: str
    sender: Optional[str] = None
    subject: Optional[str] = None
    recipient: Optional[str] = None

class EmailScanBatchRequest(BaseModel):
    emails: List[EmailScanRequest]

# Import services
try:
    from ml.phishing_service import get_phishing_service
    from agents.response_agent import ResponseAgent
except ImportError:
    try:
        from backend.ml.phishing_service import get_phishing_service
        from backend.agents.response_agent import ResponseAgent
    except ImportError:
        get_phishing_service = None
        ResponseAgent = None

router = APIRouter(prefix="/threats", tags=["Threat Detection"])

# Initialize services
response_agent = ResponseAgent() if ResponseAgent else None

# In-memory threat storage (would be database in production)
import random
_threats_db = {}


@router.get("/list")
async def list_threats(
    limit: int = Query(50, le=200),
    severity: Optional[str] = None,
    status: Optional[str] = None
):
    """
    List all detected threats.
    
    Returns paginated list of threats with optional filtering.
    """
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    threat_types = ["Phishing", "Spear Phishing", "BEC", "Credential Harvesting"]
    statuses = ["Active", "Resolved", "Investigating", "Quarantined"]
    
    threats = []
    for i in range(min(limit, 50)):
        threat_severity = severity or random.choice(severities)
        threat_status = status or random.choice(statuses)
        threats.append({
            "id": f"THR-{1000 + i}",
            "type": random.choice(threat_types),
            "severity": threat_severity,
            "confidence": round(random.uniform(75, 99), 1),
            "status": threat_status,
            "source": f"suspicious_{i}@phishing-domain.com",
            "subject": f"Urgent: Action Required #{i}",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 168))).isoformat(),
            "description": "Suspicious email with phishing indicators detected"
        })
    
    return {
        "success": True,
        "threats": threats,
        "total": len(threats)
    }


@router.get("/{threat_id}")
async def get_threat_details(threat_id: str):
    """
    Get detailed information about a specific threat.
    """
    # Mock threat details
    return {
        "success": True,
        "threat": {
            "id": threat_id,
            "type": "Phishing",
            "severity": "HIGH",
            "confidence": 94.5,
            "status": "Active",
            "source": "suspicious@phishing-domain.com",
            "subject": "Urgent: Verify Your Account Now",
            "recipient": "user@company.com",
            "detected_at": datetime.now(timezone.utc).isoformat(),
            "content_preview": "Dear Customer, Your account has been compromised...",
            "indicators": [
                {"type": "suspicious_link", "value": "http://fake-login.com", "risk": "HIGH"},
                {"type": "urgency_language", "value": "immediately", "risk": "MEDIUM"},
                {"type": "sender_mismatch", "value": "Header spoofing detected", "risk": "HIGH"}
            ],
            "actions_taken": [
                {"action": "quarantined", "timestamp": datetime.now(timezone.utc).isoformat()},
                {"action": "sender_blocked", "timestamp": datetime.now(timezone.utc).isoformat()}
            ],
            "recommendations": [
                "Do not click any links in this email",
                "Report to IT security team",
                "Change passwords if credentials were entered"
            ]
        }
    }


# Need timedelta import
from datetime import timedelta


@router.post("/scan")
async def scan_email(request: EmailScanRequest):
    """
    Scan an email for phishing indicators.
    
    Analyzes the email content using ML model and returns
    detection results with confidence scores and recommendations.
    """
    start_time = time.time()
    
    try:
        service = get_phishing_service()
        result = service.predict(request.content)
        
        # Add sender/subject context if provided
        if request.sender:
            result['sender'] = request.sender
        if request.subject:
            result['subject'] = request.subject
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "result": result,
            "processing_time_ms": round(processing_time, 2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan/batch")
async def scan_emails_batch(request: EmailScanBatchRequest):
    """
    Scan multiple emails in batch.
    
    Processes multiple emails efficiently and returns
    results for each email.
    """
    start_time = time.time()
    
    try:
        service = get_phishing_service()
        results = []
        
        for email in request.emails:
            result = service.predict(email.content)
            if email.sender:
                result['sender'] = email.sender
            results.append(result)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Summary statistics
        phishing_count = sum(1 for r in results if r.get('is_phishing'))
        
        return {
            "success": True,
            "total_scanned": len(results),
            "phishing_detected": phishing_count,
            "safe_detected": len(results) - phishing_count,
            "results": results,
            "processing_time_ms": round(processing_time, 2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan/respond")
async def scan_and_respond(request: EmailScanRequest):
    """
    Scan an email and automatically respond to threats.
    
    Combines detection with automated response actions
    based on threat severity.
    """
    start_time = time.time()
    
    try:
        # Run detection
        service = get_phishing_service()
        scan_result = service.predict(request.content)
        
        # Add context
        scan_result['sender'] = request.sender
        scan_result['file_path'] = None  # No file in API request
        
        # Execute response if threat detected
        response_result = None
        if scan_result.get('is_phishing'):
            response_result = response_agent.respond(scan_result)
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "scan_result": scan_result,
            "response_result": response_result,
            "processing_time_ms": round(processing_time, 2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_detection_stats():
    """
    Get detection service statistics.
    
    Returns metrics about scans performed, detection rates,
    and model performance.
    """
    try:
        service = get_phishing_service()
        stats = service.get_stats()
        
        response_stats = response_agent.get_stats()
        
        return {
            "success": True,
            "detection_stats": stats,
            "response_stats": response_stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/info")
async def get_model_info():
    """
    Get information about the loaded ML model.
    
    Returns model metadata, training statistics,
    and configuration.
    """
    try:
        service = get_phishing_service()
        return {
            "success": True,
            "model_info": service.get_model_info()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blocked-senders")
async def get_blocked_senders():
    """Get list of blocked email senders."""
    return {
        "success": True,
        "blocked_senders": response_agent.get_blocked_senders(),
        "count": len(response_agent.get_blocked_senders())
    }


@router.post("/blocked-senders")
async def block_sender(email: str, reason: Optional[str] = None):
    """Add a sender to the block list."""
    result = response_agent._block_sender(email, {
        'action': 'block_sender',
        'status': 'pending'
    })
    
    return {
        "success": result.get('executed', False),
        "result": result
    }


@router.delete("/blocked-senders/{email}")
async def unblock_sender(email: str):
    """Remove a sender from the block list."""
    success = response_agent.unblock_sender(email)
    
    return {
        "success": success,
        "message": f"Sender {email} {'unblocked' if success else 'not found'}"
    }


@router.get("/quarantine")
async def get_quarantined_files():
    """Get list of quarantined files."""
    files = response_agent.get_quarantined_files()
    
    return {
        "success": True,
        "files": files,
        "count": len(files)
    }


@router.post("/quarantine/restore")
async def restore_from_quarantine(filename: str, destination: str):
    """Restore a file from quarantine."""
    success = response_agent.restore_from_quarantine(filename, destination)
    
    if not success:
        raise HTTPException(status_code=404, detail="File not found in quarantine")
    
    return {
        "success": True,
        "message": f"File {filename} restored to {destination}"
    }


@router.get("/response-history")
async def get_response_history(limit: int = Query(50, le=200)):
    """Get history of automated responses."""
    history = response_agent.get_response_history(limit)
    
    return {
        "success": True,
        "history": history,
        "count": len(history)
    }
