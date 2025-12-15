import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, Response # Added Response
import uvicorn
import logging

from backend.src.services.phishing_detection.database import get_incident_db, IncidentDatabase
from backend.src.services.phishing_detection.orchestrator_agent import get_orchestrator_agent
from backend.src.services.phishing_detection.data_loader import get_email_data_loader
from backend.src.services.phishing_detection.models import Email, Incident, IncidentStatus # Added IncidentStatus
from backend.src.services.phishing_detection.report_generator import get_report_generator # Added get_report_generator
from typing import Dict, Any, Optional # Added for get_all_incidents endpoint response_model
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ACDS Phishing Detection Module",
    description="API for automated phishing detection, incident management, and reporting.",
    version="1.0.0"
)

# Root endpoint
@app.get("/", response_class=HTMLResponse, summary="Root endpoint")
async def read_root():
    return """
    <html>
        <head>
            <title>ACDS Phishing Detection Module</title>
        </head>
        <body>
            <h1>ACDS Phishing Detection Module API</h1>
            <p>Visit /docs for API documentation.</p>
        </body>
    </html>
    """

# Example of an endpoint for batch processing (internal/testing)
@app.post("/api/v1/phishing-detection/process-emails", summary="Initiate batch email processing for phishing detection")
async def process_emails_batch(
    dataset_name: str = "zefang-liu/phishing-email-dataset",
    split: str = "train",
    raw_text_column: str = "Email Text",
    incident_db: IncidentDatabase = Depends(get_incident_db)
):
    logger.info(f"Received request to process emails from dataset: {dataset_name}, split: {split}")
    
    data_loader = get_email_data_loader(dataset_name, split, raw_text_column)
    emails_to_process = data_loader.load_emails_from_hf_dataset()

    if not emails_to_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No emails found in the specified dataset."
        )
    
    orchestrator = await get_orchestrator_agent(incident_db)
    processed_count = 0
    incidents_created = 0

    for email in emails_to_process:
        incident = await orchestrator.process_email_workflow(email)
        processed_count += 1
        if incident:
            incidents_created += 1
            
    return {
        "message": f"Successfully processed {processed_count} emails. Created {incidents_created} incidents.",
        "processed_emails": processed_count,
        "incidents_created": incidents_created
    }

@app.get("/api/v1/phishing-detection/incidents/{incident_id}", response_model=Incident, summary="Retrieve a specific phishing incident by ID")
async def get_incident_by_id(
    incident_id: str,
    incident_db: IncidentDatabase = Depends(get_incident_db)
):
    incident = await incident_db.get_incident(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found."
        )
    return incident

@app.get("/api/v1/phishing-detection/incidents", response_model=Dict[str, Any], summary="Retrieve a list of all phishing incidents")
async def get_all_incidents(
    status: Optional[IncidentStatus] = None,
    limit: int = 100,
    offset: int = 0,
    incident_db: IncidentDatabase = Depends(get_incident_db)
):
    query = {}
    if status:
        query["status"] = status.value

    incidents = await incident_db.find_incidents(query, limit, offset)
    total_count = await incident_db.count_incidents(query)

    return {
        "total": total_count,
        "incidents": incidents
    }

@app.get("/api/v1/phishing-detection/incidents/{incident_id}/report/pdf", summary="Generate and retrieve a PDF report for a specific phishing incident")
async def get_incident_pdf_report(
    incident_id: str,
    incident_db: IncidentDatabase = Depends(get_incident_db)
):
    incident = await incident_db.get_incident(incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found."
        )
    
    # In a real scenario, you'd fetch the original email associated with the incident
    # For now, we'll need to mock or fetch a dummy email for report generation if not stored with incident
    # For now, just generate a dummy email for the report
    dummy_email = Email(
        raw_content="Dummy email content for report generation.",
        sender="dummy@example.com",
        recipients=["analyst@example.com"],
        subject=f"Report for Incident {incident_id}",
        body="This is a dummy body for the report generation.",
        attachments=[]
    )

    report_generator = await get_report_generator(incident_db)
    
    # Define a temporary path for the PDF
    pdf_output_path = f"reports/temp_incident_report_{incident_id}.pdf"
    
    try:
        explanation = incident.explanation_details.model_dump() if incident.explanation_details else {}
        await report_generator.generate_incident_report_pdf(incident, dummy_email, explanation, pdf_output_path)
        
        with open(pdf_output_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()
        
        # Clean up the temporary PDF file
        os.remove(pdf_output_path)

        return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=incident_report_{incident_id}.pdf"})
    except Exception as e:
        logger.error(f"Error generating or serving PDF report for incident {incident_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF report."
        )

# Startup event for database connection
@app.on_event("startup")
async def startup_db_client():
    logger.info("Connecting to MongoDB on startup...")
    try:
        await get_incident_db() # This will connect the singleton incident_db
        logger.info("MongoDB connection established successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB on startup: {e}")
        # Optionally, re-raise or handle more gracefully depending on desired behavior
        # For now, let's allow startup to complete but log error
        pass

# Shutdown event for database disconnection
@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Disconnecting from MongoDB on shutdown...")
    incident_db = await get_incident_db()
    await incident_db.disconnect()
    logger.info("MongoDB connection closed.")

if __name__ == "__main__":
    # Ensure uvicorn runs the app from the correct module
    # 'backend.main:app' refers to the 'app' object in 'backend/main.py'
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)