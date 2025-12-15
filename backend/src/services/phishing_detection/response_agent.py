import logging
from typing import Dict, Any, Optional

from .models import Incident, Email, IncidentStatus

logger = logging.getLogger(__name__)

class ResponseAgent:
    """
    Agent responsible for executing response actions based on phishing incidents.
    This is a placeholder for actual integration with security tools.
    """
    def __init__(self):
        logger.info("ResponseAgent initialized.")

    async def execute_response(self, incident: Incident) -> Dict[str, Any]:
        """
        Simulates executing response actions for a detected phishing incident.
        
        Args:
            incident: The Incident object for which to execute responses.
            
        Returns:
            A dictionary detailing the executed response actions and their status.
        """
        response_actions = []
        action_status = {}

        logger.info(f"ResponseAgent: Processing incident {incident.id} for response actions.")

        # Example: Simple rule-based response
        if incident.status == IncidentStatus.CONFIRMED_PHISHING:
            # Simulate blocking the sender
            sender_to_block = incident.email_id # In a real system, this would be incident.email.sender
            logger.info(f"Simulating blocking sender {sender_to_block} for incident {incident.id}.")
            response_actions.append(f"Blocked sender (simulated): {sender_to_block}")
            action_status["blocked_sender"] = "simulated_success"

            # Simulate reporting the incident
            logger.info(f"Simulating reporting incident {incident.id} to security team.")
            response_actions.append(f"Reported incident (simulated): {incident.id}")
            action_status["reported_incident"] = "simulated_success"
        else:
            logger.info(f"No specific response actions for incident {incident.id} due to status {incident.status.value}.")
            response_actions.append("No automated response actions taken.")
            action_status["status"] = "no_action_needed"
            
        return {
            "summary": "Automated response actions simulated.",
            "actions": response_actions,
            "status_details": action_status
        }

def get_response_agent() -> ResponseAgent:
    """Returns a singleton-like instance of the ResponseAgent."""
    return ResponseAgent()
