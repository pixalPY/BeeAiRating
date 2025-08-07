#!/usr/bin/env python3
"""
Google Gemini AI Client
Handles API calls to Google Gemini AI service
"""

import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for Google Gemini AI API"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        self.api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        self.max_tokens = int(os.getenv('GEMINI_MAX_TOKENS', 1000))
        self.temperature = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
        
        if not self.api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            logger.info(f"Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise
    
    def generate_text(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate text using Gemini AI
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters for generation
            
        Returns:
            Generated text or None if failed
        """
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}")
            return None
    
    def analyze_text(self, text: str, analysis_type: str = "general") -> Optional[Dict[str, Any]]:
        """
        Analyze text using Gemini AI
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (sentiment, summary, etc.)
            
        Returns:
            Analysis results or None if failed
        """
        try:
            if analysis_type == "sentiment":
                prompt = f"Analyze the sentiment of this text and return a JSON with 'sentiment' (positive/negative/neutral) and 'confidence' (0-1): {text}"
            elif analysis_type == "summary":
                prompt = f"Provide a concise summary of this text: {text}"
            else:
                prompt = f"Analyze this text: {text}"
            
            response = self.generate_text(prompt)
            return {"analysis": response, "type": analysis_type}
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate_text("Hello, this is a test message.")
            return response is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Example usage
if __name__ == "__main__":
    try:
        client = GeminiClient()
        if client.test_connection():
            print("✅ Gemini API connection successful!")
            
            # Test text generation
            response = client.generate_text("What is artificial intelligence?")
            if response:
                print(f"Generated text: {response[:100]}...")
        else:
            print("❌ Gemini API connection failed!")
    except Exception as e:
        print(f"❌ Error: {e}") 