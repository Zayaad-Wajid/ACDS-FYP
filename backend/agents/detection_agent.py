import os
import joblib
import logging
from typing import Dict, Any, Optional

# Attempt to import from project structure, handle potential import errors gracefully during dev
try:
    from backend.core.logger import get_logger
except ImportError:
    # Fallback logger if backend.core.logger is not yet created
    logging.basicConfig(level=logging.INFO)
    def get_logger(name):
        return logging.getLogger(name)

try:
    from backend.ml.preprocess import preprocess_file
except ImportError:
    # Fallback/Mock if backend.ml.preprocess is not yet created
    def preprocess_file(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

class DetectionAgent:
    """
    Agent responsible for detecting phishing attempts in files using a pre-trained ML model.
    """

    def __init__(self, model_path: str = "backend/models/phishing_model.pkl"):
        """
        Initialize the Detection Agent.

        Args:
            model_path (str): Path to the pickled ML model.
        """
        self.logger = get_logger(__name__)
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self) -> Any:
        """
        Load the machine learning model from disk.

        Returns:
            The loaded model object or None if loading fails.
        """
        if not os.path.exists(self.model_path):
            self.logger.warning(f"Model file not found at {self.model_path}. Detection will run in dummy mode.")
            return None

        try:
            model = joblib.load(self.model_path)
            self.logger.info(f"Successfully loaded ML model from {self.model_path}")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load ML model: {str(e)}")
            return None

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a file to detect phishing content.

        Args:
            file_path (str): Absolute or relative path to the file.

        Returns:
            dict: A dictionary containing filename, phishing status, and confidence score.
        """
        filename = os.path.basename(file_path)
        
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return {
                "filename": filename,
                "is_phishing": False,
                "confidence": 0.0,
                "error": "File not found"
            }

        try:
            self.logger.info(f"Processing file: {filename}")

            # 1. Preprocess the file content
            # Assuming preprocess_file returns a format suitable for the model (e.g., vector or string)
            processed_data = preprocess_file(file_path)

            # 2. Predict using the model
            if self.model:
                # Assuming model.predict returns [0] or [1] and predict_proba returns [[prob_0, prob_1]]
                # Adjust indexing based on actual model structure (sklearn style assumed)
                
                # Note: In a real scenario, we might need to vectorize the text if the model expects vectors
                # and the pipeline isn't included in the pkl. 
                # For this agent, we assume the model pipeline handles it or processed_data is ready.
                
                # Check if model supports probability
                if hasattr(self.model, "predict_proba"):
                    prediction_probs = self.model.predict_proba([processed_data])
                    confidence = float(prediction_probs[0][1]) # Probability of class 1 (Phishing)
                    is_phishing = confidence > 0.5
                else:
                    prediction = self.model.predict([processed_data])
                    is_phishing = bool(prediction[0])
                    confidence = 1.0 if is_phishing else 0.0
            else:
                # Dummy logic if model is not loaded (for testing/fallback)
                self.logger.warning("Model not loaded. Using keyword-based fallback detection.")
                content_lower = str(processed_data).lower()
                phishing_keywords = ['urgent', 'verify your account', 'password expiration', 'bank']
                is_phishing = any(keyword in content_lower for keyword in phishing_keywords)
                confidence = 0.85 if is_phishing else 0.1

            result = {
                "filename": filename,
                "is_phishing": is_phishing,
                "confidence": round(confidence, 4)
            }

            log_level = logging.WARNING if is_phishing else logging.INFO
            self.logger.log(log_level, f"Detection result for {filename}: Phishing={is_phishing}, Confidence={confidence}")

            return result

        except Exception as e:
            self.logger.error(f"Error processing file {filename}: {str(e)}")
            return {
                "filename": filename,
                "is_phishing": False,
                "confidence": 0.0,
                "error": str(e)
            }
