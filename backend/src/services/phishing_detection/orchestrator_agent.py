import logging
from typing import Dict, Any, Optional

from .models import Email, Incident, IncidentStatus
from .detection_agent import DetectionAgent, get_detection_agent
from .incident_manager import IncidentManager, get_incident_manager
from .explainability_agent import ExplainabilityAgent, get_explainability_agent
from .orchestration_trigger import OrchestrationTrigger, get_orchestration_trigger
from .response_agent import ResponseAgent, get_response_agent
from .report_generator import ReportGenerator, get_report_generator
from .database import IncidentDatabase # New import

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    """
    Orchestrates the end-to-end phishing incident handling workflow for a single email.
    """
    def __init__(self, 
                 detection_agent: DetectionAgent, 
                 incident_manager: IncidentManager, 
                 explainability_agent: ExplainabilityAgent,
                 orchestration_trigger: OrchestrationTrigger,
                 response_agent: ResponseAgent,
                 report_generator: ReportGenerator # New agent
                ):
        self.detection_agent = detection_agent
        self.incident_manager = incident_manager
        self.explainability_agent = explainability_agent
        self.orchestration_trigger = orchestration_trigger
        self.response_agent = response_agent
        self.report_generator = report_generator # Assign new agent
        logger.info("OrchestratorAgent initialized.")

    async def process_email_workflow(self, email: Email) -> Optional[Incident]:
        """
        Executes the full phishing incident handling workflow for a given email.
        
        EMAIL INPUT    ↓
        DETECTION AGENT    (phishing?)    ↓
        INCIDENT CREATED IN DB    ↓
        EXPLAINABILITY AGENT    (why phishing?)    ↓
        ORCHESTRATION AGENT    (what should we do?)    ↓
        RESPONSE AGENT    (block sender? report?)    ↓
        UPDATE INCIDENT + TIMELINE    ↓
        REPORT GENERATOR (not part of orchestration, but follows it)
        """
        
        logger.info(f"Orchestrator: Starting workflow for email ID: {email.id}")

        # 1. DETECTION AGENT
        detection_results = self.detection_agent.detect_phishing(email)
        logger.info(f"Orchestrator: Detection Agent results for {email.id}: {detection_results['is_phishing']}")

        if not detection_results["is_phishing"]:
            logger.info(f"Orchestrator: Email {email.id} not identified as phishing. Ending workflow.")
            return None

        # 2. INCIDENT CREATED IN DB
        incident = await self.incident_manager.create_new_incident(email, detection_results)
        if not incident:
            logger.error(f"Orchestrator: Failed to create incident for email {email.id}. Ending workflow.")
            return None
        logger.info(f"Orchestrator: Incident {incident.id} created for email {email.id}.")

        # 3. EXPLAINABILITY AGENT
        explanation = self.explainability_agent.generate_explanation(incident)
        logger.info(f"Orchestrator: Explanation generated for incident {incident.id}.")
        # Update incident with explanation details
        await self.incident_manager.add_timeline_entry(
            incident.id, 
            "Explanation Generated", 
            {"explanation_summary": explanation.get("summary"), "explanation_details": explanation.get("details")}
        )
        
        # 4. ORCHESTRATION TRIGGER
        orchestration_success = await self.orchestration_trigger.trigger_orchestration(incident)
        logger.info(f"Orchestrator: Orchestration triggered for incident {incident.id}: {orchestration_success}")
        await self.incident_manager.add_timeline_entry(
            incident.id, 
            "Orchestration Triggered", 
            {"status": orchestration_success}
        )
        
        # 5. RESPONSE AGENT
        response_actions = await self.response_agent.execute_response(incident)
        logger.info(f"Orchestrator: Response actions for incident {incident.id}: {response_actions.get('summary')}")
        await self.incident_manager.add_timeline_entry(
            incident.id, 
            "Response Actions Executed", 
            {"actions_summary": response_actions.get("summary"), "details": response_actions.get("status_details")}
        )

        # 6. UPDATE INCIDENT (Status and Timeline are handled by IncidentManager calls above)
        # Update incident status based on automated actions if any, or to a final review state
        updated_incident = await self.incident_manager.update_incident_status(
            incident.id, IncidentStatus.CONFIRMED_PHISHING, analyst_id="Automated_Orchestrator"
        )
        if updated_incident:
            logger.info(f"Orchestrator: Incident {updated_incident.id} status updated to {updated_incident.status.value}.")
            incident = updated_incident # Keep the latest state of the incident
            
            # Generate PDF Report
            pdf_output_path = f"reports/incident_report_{incident.id}.pdf"
            await self.report_generator.generate_incident_report_pdf(incident, email, explanation, pdf_output_path)
            logger.info(f"Orchestrator: PDF report generated for incident {incident.id} at {pdf_output_path}")
        else:
            logger.error(f"Orchestrator: Failed to update final incident status for {incident.id}.")
            
        return incident

async def get_orchestrator_agent(incident_db: IncidentDatabase) -> OrchestratorAgent:
    """Returns a singleton-like instance of the OrchestratorAgent."""
    detection_agent = get_detection_agent()
    incident_manager = await get_incident_manager()
    explainability_agent = get_explainability_agent()
    orchestration_trigger = get_orchestration_trigger()
    response_agent = get_response_agent()
    report_generator = await get_report_generator(incident_db) # Initialize ReportGenerator with incident_db
    return OrchestratorAgent(detection_agent, incident_manager, explainability_agent, orchestration_trigger, response_agent, report_generator)
