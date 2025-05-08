#!/usr/bin/env python3
import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
MODEL_TYPE = os.getenv("MODEL_TYPE", "google")
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

class AIModelHandler:
    def __init__(self):
        self.model_type = MODEL_TYPE.lower()
        self.history_file = Path("analysis_history.json")
        self._initialize_history()

    def _initialize_history(self):
        """Initialize or load analysis history."""
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps({"analyses": []}))

    def _save_to_history(self, prompt, response, model_used):
        """Save analysis results to history."""
        try:
            history = json.loads(self.history_file.read_text())
            history["analyses"].append({
                "timestamp": datetime.now().isoformat(),
                "model_used": model_used,
                "prompt": prompt,
                "response": response
            })
            self.history_file.write_text(json.dumps(history, indent=2))
        except Exception as e:
            logger.error(f"Failed to save to history: {e}")

    def call_model(self, prompt):
        """
        Main method to call the appropriate AI model based on configuration.
        
        Args:
            prompt (str): The analysis prompt to send to the model
            
        Returns:
            dict: The processed response from the model
        """
        try:
            if self.model_type == "google":
                response = self._call_google_gemini(prompt)
            elif self.model_type == "huggingface":
                response = self._call_huggingface(prompt)
            elif self.model_type == "local":
                response = self._call_local_model(prompt)
            else:
                raise ValueError(f"Unsupported MODEL_TYPE: {self.model_type}")

            # Save successful analysis to history
            self._save_to_history(prompt, response, self.model_type)
            return response

        except Exception as e:
            logger.error(f"Error during model call: {e}")
            # Try fallback to local model if not already using it
            if self.model_type != "local":
                logger.info("Attempting fallback to local model...")
                try:
                    response = self._call_local_model(prompt)
                    self._save_to_history(prompt, response, "local_fallback")
                    return response
                except Exception as fallback_error:
                    logger.error(f"Fallback failed: {fallback_error}")
                    raise fallback_error
            raise e

    def _call_google_gemini(self, prompt):
        """Call Google's Gemini API."""
        if not GOOGLE_GEMINI_API_KEY:
            raise ValueError("Google Gemini API key not found in environment variables")

        try:
            # Note: Update the API endpoint when Gemini's API is publicly available
            api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"
            headers = {
                "Authorization": f"Bearer {GOOGLE_GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": {
                    "text": prompt
                },
                "temperature": 0.7,
                "maxOutputTokens": 1024
            }

            response = requests.post(
                api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Google Gemini API request failed: {e}")
            raise

    def _call_huggingface(self, prompt):
        """Call Hugging Face's Inference API."""
        if not HUGGINGFACE_API_KEY:
            raise ValueError("Hugging Face API key not found in environment variables")

        try:
            # Using a general text generation model - update model_id as needed
            model_id = "gpt2"  # You can change this to any preferred model
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            payload = {"inputs": prompt}

            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Hugging Face API request failed: {e}")
            raise

    def _call_local_model(self, prompt):
        """Use a local model for inference."""
        try:
            from transformers import pipeline

            # Initialize the model pipeline
            generator = pipeline(
                "text-generation",
                model="gpt2",  # You can change this to any locally available model
                device=-1  # Use CPU. Set to 0 for GPU if available
            )

            # Generate response
            result = generator(
                prompt,
                max_length=1024,
                num_return_sequences=1,
                temperature=0.7
            )

            return {
                "generated_text": result[0]["generated_text"],
                "model": "local_gpt2"
            }

        except Exception as e:
            logger.error(f"Local model inference failed: {e}")
            raise

    def get_analysis_history(self):
        """Retrieve the analysis history."""
        try:
            return json.loads(self.history_file.read_text())
        except Exception as e:
            logger.error(f"Failed to read history: {e}")
            return {"analyses": []}

# Example usage
if __name__ == "__main__":
    handler = AIModelHandler()
    try:
        result = handler.call_model(
            "Analyze the following crypto token metrics: "
            "market cap trends, volume patterns, and social sentiment indicators"
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Analysis failed: {e}")
