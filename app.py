#!/usr/bin/env python3
"""
BeeAiRating - AI-powered rating system
Main application file with Flask web server
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, render_template, request, jsonify, send_from_directory
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging() -> None:
    """Setup logging configuration for the application"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Setup file handler
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Setup root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

class AiRatingEngine:
    """AI-powered rating engine for data analysis"""
    
    def __init__(self):
        """Initialize the AI rating engine"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing AI Rating Engine")
        
    def analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input data and return AI rating
        
        Args:
            data: Input data dictionary containing features to analyze
            
        Returns:
            Dictionary containing analysis results and rating
        """
        try:
            self.logger.info(f"Analyzing data with {len(data)} features")
            
            # Extract features from input data
            features = self._extract_features(data)
            
            # Calculate AI rating using machine learning model
            rating = self._calculate_rating(features)
            
            # Generate analysis report
            analysis = self._generate_analysis(features, rating)
            
            result = {
                'rating': rating,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat(),
                'confidence': self._calculate_confidence(features)
            }
            
            self.logger.info(f"Analysis completed. Rating: {rating}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during data analysis: {str(e)}")
            raise
    
    def _extract_features(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Extract numerical features from input data
        
        Args:
            data: Raw input data
            
        Returns:
            Numpy array of extracted features
        """
        # Convert data to numerical features
        # This is a simplified example - in real implementation,
        # you would have more sophisticated feature extraction
        features = []
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, str):
                # Simple string encoding (hash-based)
                features.append(hash(value) % 1000)
            else:
                features.append(0.0)
        
        return np.array(features)
    
    def _calculate_rating(self, features: np.ndarray) -> float:
        """
        Calculate AI rating based on features
        
        Args:
            features: Extracted numerical features
            
        Returns:
            Rating score between 0 and 100
        """
        # Simple weighted average as placeholder
        # In real implementation, this would be a trained ML model
        weights = np.ones(len(features)) / len(features)
        rating = np.dot(features, weights)
        
        # Normalize to 0-100 scale
        rating = max(0, min(100, rating))
        
        return round(rating, 2)
    
    def _generate_analysis(self, features: np.ndarray, rating: float) -> Dict[str, Any]:
        """
        Generate detailed analysis report
        
        Args:
            features: Extracted features
            rating: Calculated rating
            
        Returns:
            Analysis report dictionary
        """
        analysis = {
            'feature_count': len(features),
            'feature_summary': {
                'mean': float(np.mean(features)),
                'std': float(np.std(features)),
                'min': float(np.min(features)),
                'max': float(np.max(features))
            },
            'rating_category': self._categorize_rating(rating),
            'recommendations': self._generate_recommendations(rating)
        }
        
        return analysis
    
    def _categorize_rating(self, rating: float) -> str:
        """Categorize rating into performance levels"""
        if rating >= 90:
            return "Excellent"
        elif rating >= 80:
            return "Very Good"
        elif rating >= 70:
            return "Good"
        elif rating >= 60:
            return "Average"
        elif rating >= 50:
            return "Below Average"
        else:
            return "Poor"
    
    def _generate_recommendations(self, rating: float) -> list:
        """Generate improvement recommendations based on rating"""
        recommendations = []
        
        if rating < 70:
            recommendations.append("Consider improving data quality")
            recommendations.append("Review input parameters")
        
        if rating < 50:
            recommendations.append("Immediate attention required")
            recommendations.append("Consider expert consultation")
        
        return recommendations
    
    def _calculate_confidence(self, features: np.ndarray) -> float:
        """Calculate confidence score for the rating"""
        # Simple confidence calculation based on feature variance
        # Lower variance = higher confidence
        variance = np.var(features)
        confidence = max(0.5, 1.0 - (variance / 1000))
        return round(confidence, 2)

# Initialize AI rating engine
ai_engine = AiRatingEngine()

@app.route('/')
def index():
    """Serve the main application page"""
    logger.info("Serving main page")
    return send_from_directory('.', 'index.html')

@app.route('/api/rate', methods=['POST'])
def rate_data():
    """
    API endpoint for AI rating analysis
    
    Expected JSON format:
    {
        "data": {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    }
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            logger.warning("Invalid request data received")
            return jsonify({'error': 'Invalid request format'}), 400
        
        # Extract data for analysis
        data = request_data['data']
        logger.info(f"Received rating request with {len(data)} data points")
        
        # Perform AI analysis
        result = ai_engine.analyze_data(data)
        
        logger.info(f"Rating analysis completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in rating endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main application entry point"""
    try:
        # Get configuration from environment
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info(f"Starting BeeAiRating application on {host}:{port}")
        logger.info(f"Debug mode: {debug}")
        
        # Start Flask application
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == '__main__':
    main() 