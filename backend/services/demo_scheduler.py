"""
Demo Scheduler Service
=======================
Automatically processes sample emails every 5 minutes for demonstration purposes.
This service simulates real-world email scanning by feeding sample data through
the detection pipeline.
"""

import asyncio
import random
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import threading
import json

# Sample phishing and legitimate email templates for demo
SAMPLE_EMAILS = {
    "phishing": [
        {
            "subject": "URGENT: Your account has been compromised",
            "sender": "security-alert@bankofamerica-verify.com",
            "content": "Dear Customer, We have detected suspicious activity on your account. Your account has been temporarily suspended. Please click the link below to verify your identity immediately or your account will be permanently closed within 24 hours. Verify Now: http://secure-bankofamerica-login.com/verify",
        },
        {
            "subject": "Your PayPal account is limited",
            "sender": "service@paypa1-secure.com",
            "content": "We noticed unusual login activity on your PayPal account. To restore full access, please confirm your information by clicking here: http://paypal-verify.xyz/confirm. Failure to verify within 48 hours will result in account suspension.",
        },
        {
            "subject": "Microsoft 365: Password Expiration Notice",
            "sender": "admin@microsoft365-support.net",
            "content": "Your Microsoft 365 password will expire in 24 hours. To avoid service interruption, please update your password immediately: http://microsoft365-update.com/password. This is an automated message from IT Security.",
        },
        {
            "subject": "Amazon: Confirm your order #AMZ-9847261",
            "sender": "orders@amazon-shipping.info",
            "content": "We couldn't process your recent order due to payment issues. Please update your payment method within 12 hours to avoid order cancellation: http://amazon-verify-payment.com/update",
        },
        {
            "subject": "IRS Tax Refund Notification",
            "sender": "refunds@irs-taxrefund.gov.com",
            "content": "You are eligible for a tax refund of $3,847.00. To claim your refund, please submit your banking information through our secure portal: http://irs-refund-claim.com/submit",
        },
        {
            "subject": "Netflix: Payment Failed - Action Required",
            "sender": "billing@netflix-payments.co",
            "content": "We were unable to process your monthly payment. Your subscription will be cancelled unless you update your payment details within 24 hours: http://netflix-billing-update.com",
        },
        {
            "subject": "Apple ID: Unusual Sign-in Detected",
            "sender": "noreply@apple-id-security.com",
            "content": "Someone tried to sign into your Apple ID from a new device. If this wasn't you, please secure your account immediately: http://apple-id-verify.net/secure",
        },
        {
            "subject": "LinkedIn: You have 5 pending connection requests",
            "sender": "connections@linkedin-network.co",
            "content": "You have pending connection requests from industry leaders. Log in to accept: http://linkedin-connections.info/login",
        },
        {
            "subject": "FedEx: Delivery Problem - Package Held",
            "sender": "delivery@fedex-tracking.info",
            "content": "Your package could not be delivered due to an incorrect address. Please confirm your delivery details: http://fedex-delivery-confirm.com/update",
        },
        {
            "subject": "Google Drive: Storage Full - Files at Risk",
            "sender": "storage@google-drive-alert.com",
            "content": "Your Google Drive storage is full. Files will be deleted in 48 hours. Upgrade now to prevent data loss: http://google-storage-upgrade.net",
        },
    ],
    "legitimate": [
        {
            "subject": "Your weekly project update",
            "sender": "manager@company.com",
            "content": "Hi team, Here's our weekly progress update. We completed 3 major milestones this week. Please review the attached report and let me know if you have questions. Best regards, John",
        },
        {
            "subject": "Meeting notes from yesterday's call",
            "sender": "colleague@company.com",
            "content": "Hi, As discussed in yesterday's meeting, here are the action items: 1. Complete the quarterly report by Friday 2. Schedule follow-up with the client 3. Review the budget proposal. Let me know if anything needs clarification.",
        },
        {
            "subject": "Your Amazon.com order has shipped",
            "sender": "ship-confirm@amazon.com",
            "content": "Your order #123-4567890-1234567 has shipped and is on its way. Track your package at amazon.com/orders. Estimated delivery: December 16, 2025.",
        },
        {
            "subject": "Monthly newsletter - December Edition",
            "sender": "newsletter@techcompany.com",
            "content": "Welcome to our December newsletter! This month we're featuring: New product announcements, customer success stories, and upcoming webinars. Click to read more on our website.",
        },
        {
            "subject": "Your subscription renewal confirmation",
            "sender": "billing@spotify.com",
            "content": "Your Spotify Premium subscription has been renewed. Your next billing date is January 14, 2026. Thank you for being a Premium member!",
        },
    ],
}

class DemoScheduler:
    """
    Scheduler that automatically processes sample emails for demonstration.
    Runs every 5 minutes to simulate real-world email scanning.
    """
    
    def __init__(self):
        self.running = False
        self.interval_seconds = 300  # 5 minutes
        self._task: Optional[asyncio.Task] = None
        self._stats = {
            "total_processed": 0,
            "phishing_detected": 0,
            "legitimate_detected": 0,
            "last_run": None,
            "next_run": None,
            "sessions": []
        }
        
    @property
    def stats(self):
        return self._stats
    
    async def start(self):
        """Start the demo scheduler."""
        if self.running:
            return {"status": "already_running", "message": "Demo scheduler is already running"}
        
        self.running = True
        self._task = asyncio.create_task(self._run_loop())
        return {"status": "started", "message": f"Demo scheduler started. Will process emails every {self.interval_seconds} seconds"}
    
    async def stop(self):
        """Stop the demo scheduler."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        return {"status": "stopped", "message": "Demo scheduler stopped"}
    
    async def _run_loop(self):
        """Main loop that runs the demo at regular intervals."""
        while self.running:
            try:
                await self.process_batch()
                self._stats["last_run"] = datetime.now(timezone.utc).isoformat()
                self._stats["next_run"] = (datetime.now(timezone.utc).replace(microsecond=0) + 
                                          __import__('datetime').timedelta(seconds=self.interval_seconds)).isoformat()
                await asyncio.sleep(self.interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Demo scheduler error: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying
    
    async def process_batch(self, count: int = 5):
        """Process a batch of sample emails."""
        from database.connection import get_collection
        
        results = []
        session_id = f"DEMO-{uuid.uuid4().hex[:8].upper()}"
        
        # Mix of phishing and legitimate emails (70% phishing, 30% legitimate for demo)
        phishing_count = int(count * 0.7)
        legitimate_count = count - phishing_count
        
        emails_to_process = []
        
        # Select random phishing emails
        for _ in range(phishing_count):
            email = random.choice(SAMPLE_EMAILS["phishing"])
            emails_to_process.append({**email, "expected": "phishing"})
        
        # Select random legitimate emails
        for _ in range(legitimate_count):
            email = random.choice(SAMPLE_EMAILS["legitimate"])
            emails_to_process.append({**email, "expected": "legitimate"})
        
        # Shuffle the emails
        random.shuffle(emails_to_process)
        
        # Process each email
        for email_data in emails_to_process:
            result = await self._process_single_email(email_data, session_id)
            results.append(result)
            
            # Log activity
            await self._log_activity({
                "event": "email_scanned",
                "session_id": session_id,
                "email_subject": email_data["subject"][:50],
                "is_phishing": result.get("is_phishing", False),
                "confidence": result.get("confidence", 0),
                "timestamp": datetime.now(timezone.utc)
            })
        
        # Update stats
        phishing_found = sum(1 for r in results if r.get("is_phishing"))
        self._stats["total_processed"] += len(results)
        self._stats["phishing_detected"] += phishing_found
        self._stats["legitimate_detected"] += len(results) - phishing_found
        
        session_summary = {
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "emails_processed": len(results),
            "phishing_detected": phishing_found,
            "legitimate_detected": len(results) - phishing_found
        }
        self._stats["sessions"].append(session_summary)
        
        # Keep only last 10 sessions
        self._stats["sessions"] = self._stats["sessions"][-10:]
        
        # Log completion
        await self._log_activity({
            "event": "batch_completed",
            "session_id": session_id,
            "emails_processed": len(results),
            "phishing_detected": phishing_found,
            "timestamp": datetime.now(timezone.utc)
        })
        
        return {
            "success": True,
            "session_id": session_id,
            "results": results,
            "summary": session_summary
        }
    
    async def _process_single_email(self, email_data: dict, session_id: str) -> dict:
        """Process a single email through the detection pipeline."""
        try:
            # Import orchestrator
            from agents.orchestrator_agent import get_orchestrator_agent
            
            orchestrator = get_orchestrator_agent()
            
            if orchestrator:
                # Run through full pipeline
                result = await orchestrator.process_email(
                    content=email_data["content"],
                    sender=email_data.get("sender"),
                    subject=email_data.get("subject"),
                    recipient="demo@acds.local"
                )
                
                return {
                    "success": True,
                    "is_phishing": result.get("pipeline_results", {}).get("detection", {}).get("is_phishing", False),
                    "confidence": result.get("pipeline_results", {}).get("detection", {}).get("confidence", 0),
                    "severity": result.get("severity", "LOW"),
                    "threat_id": result.get("threat_id"),
                    "actions_taken": result.get("actions_taken", []),
                    "expected": email_data.get("expected", "unknown")
                }
            else:
                # Fallback - use direct ML service
                from ml.phishing_service import get_phishing_service
                
                service = get_phishing_service()
                if service:
                    result = service.predict(email_data["content"])
                    return {
                        "success": True,
                        "is_phishing": result.get("is_phishing", False),
                        "confidence": result.get("confidence", 0),
                        "severity": result.get("severity", "LOW"),
                        "expected": email_data.get("expected", "unknown")
                    }
                    
        except Exception as e:
            print(f"Error processing email: {e}")
        
        return {
            "success": False,
            "error": "Processing failed",
            "expected": email_data.get("expected", "unknown")
        }
    
    async def _log_activity(self, log_data: dict):
        """Log activity to database."""
        try:
            from database.connection import get_collection
            
            logs_col = get_collection("activity_logs")
            if logs_col is not None:
                log_data["_id"] = None  # Let MongoDB generate ID
                log_data["created_at"] = datetime.now(timezone.utc)
                logs_col.insert_one(log_data)
        except Exception as e:
            print(f"Failed to log activity: {e}")
    
    def set_interval(self, seconds: int):
        """Set the processing interval in seconds."""
        if seconds < 30:
            seconds = 30  # Minimum 30 seconds
        self.interval_seconds = seconds
        return {"status": "updated", "interval_seconds": self.interval_seconds}


# Global scheduler instance
_scheduler: Optional[DemoScheduler] = None


def get_demo_scheduler() -> DemoScheduler:
    """Get or create the demo scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = DemoScheduler()
    return _scheduler
