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
from website_analyzer import WebsiteAnalyzer

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
        """Categorize rating into star levels based on percentage"""
        percentage = (rating / 5.0) * 100
        
        if percentage >= 80:
            return "5星 (Excellent)"
        elif percentage >= 60:
            return "4星 (Very Good)"
        elif percentage >= 40:
            return "3星 (Good)"
        elif percentage >= 20:
            return "2星 (Average)"
        else:
            return "1星 (Poor)"
    
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

# Initialize website analyzer
website_analyzer = WebsiteAnalyzer()

@app.route('/')
def index():
    """Serve the main application page"""
    logger.info("Serving main page")
    return send_from_directory('..', 'index.html')

@app.route('/website-rating')
def website_rating():
    """Serve the website rating page"""
    logger.info("Serving website rating page")
    return send_from_directory('..', 'website_rating.html')

@app.route('/enhanced-rating')
def enhanced_rating():
    """Serve the enhanced rating page"""
    logger.info("Serving enhanced rating page")
    return send_from_directory('..', 'enhanced_rating.html')

@app.route('/nav')
def navigation():
    """Serve the navigation page"""
    logger.info("Serving navigation page")
    return send_from_directory('..', 'navigation.html')

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

@app.route('/api/rate-website', methods=['POST'])
def rate_website():
    """
    API endpoint for website rating analysis
    
    Expected JSON format:
    {
        "url": "https://example.com"
    }
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data or 'url' not in request_data:
            logger.warning("Invalid website rating request - missing URL")
            return jsonify({'error': 'URL is required'}), 400
        
        url = request_data['url'].strip()
        if not url:
            logger.warning("Empty URL provided")
            return jsonify({'error': 'URL cannot be empty'}), 400
        
        logger.info(f"Received website rating request for: {url}")
        
        # Perform website analysis
        analysis = website_analyzer.rate_website(url)
        
        if not analysis:
            logger.error(f"Failed to analyze website: {url}")
            return jsonify({'error': 'Failed to analyze website. Please check the URL and try again.'}), 500
        
        # Format response
        result = {
            'url': analysis.url,
            'title': analysis.title,
            'description': analysis.description,
            'rating': analysis.rating,
            'rating_explanation': analysis.rating_explanation,
            'analysis_details': analysis.analysis_details,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        # Add enhanced rating data if available
        if analysis.enhanced_rating:
            result.update({
                'enhanced_rating': {
                    'overall_rating': analysis.enhanced_rating.overall_rating,
                    'content_rating': analysis.enhanced_rating.content_rating,
                    'technical_rating': analysis.enhanced_rating.technical_rating,
                    'user_experience_rating': analysis.enhanced_rating.user_experience_rating,
                    'seo_rating': analysis.enhanced_rating.seo_rating,
                    'security_rating': analysis.enhanced_rating.security_rating,
                    # New rating dimensions based on the rating guide
                    'interface_rating': analysis.enhanced_rating.interface_rating,
                    'code_rating': analysis.enhanced_rating.code_rating,
                    'functionality_rating': analysis.enhanced_rating.functionality_rating,
                    'practicality_rating': analysis.enhanced_rating.practicality_rating,
                    'confidence_score': analysis.enhanced_rating.confidence_score,
                    'feature_importance': analysis.enhanced_rating.feature_importance,
                    'recommendations': analysis.enhanced_rating.recommendations
                }
            })
        
        logger.info(f"Website rating completed for {url}: {analysis.rating}/5")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in website rating endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/rate-batch', methods=['POST'])
def rate_websites_batch():
    """
    API endpoint for batch website rating analysis
    
    Expected JSON format:
    {
        "urls": [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com"
        ]
    }
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data or 'urls' not in request_data:
            logger.warning("Invalid batch rating request - missing URLs")
            return jsonify({'error': 'URLs array is required'}), 400
        
        urls = request_data['urls']
        if not isinstance(urls, list) or len(urls) == 0:
            logger.warning("Invalid URLs array provided")
            return jsonify({'error': 'URLs must be a non-empty array'}), 400
        
        if len(urls) > 10:  # Limit batch size
            logger.warning(f"Batch size too large: {len(urls)}")
            return jsonify({'error': 'Maximum 10 URLs allowed per batch'}), 400
        
        logger.info(f"Received batch rating request for {len(urls)} URLs")
        
        results = []
        for i, url in enumerate(urls):
            try:
                url = url.strip()
                if not url:
                    results.append({
                        'url': url,
                        'error': 'Empty URL provided',
                        'status': 'failed'
                    })
                    continue
                
                logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")
                
                # Perform website analysis
                analysis = website_analyzer.rate_website(url)
                
                if not analysis:
                    results.append({
                        'url': url,
                        'error': 'Failed to analyze website',
                        'status': 'failed'
                    })
                    continue
                
                # Format result
                result = {
                    'url': analysis.url,
                    'title': analysis.title,
                    'description': analysis.description,
                    'rating': analysis.rating,
                    'rating_explanation': analysis.rating_explanation,
                    'analysis_details': analysis.analysis_details,
                    'status': 'success'
                }
                
                # Add enhanced rating data if available
                if analysis.enhanced_rating:
                    result.update({
                        'enhanced_rating': {
                            'overall_rating': analysis.enhanced_rating.overall_rating,
                            'content_rating': analysis.enhanced_rating.content_rating,
                            'technical_rating': analysis.enhanced_rating.technical_rating,
                            'user_experience_rating': analysis.enhanced_rating.user_experience_rating,
                            'seo_rating': analysis.enhanced_rating.seo_rating,
                            'security_rating': analysis.enhanced_rating.security_rating,
                            # New rating dimensions based on the rating guide
                            'interface_rating': analysis.enhanced_rating.interface_rating,
                            'code_rating': analysis.enhanced_rating.code_rating,
                            'functionality_rating': analysis.enhanced_rating.functionality_rating,
                            'practicality_rating': analysis.enhanced_rating.practicality_rating,
                            'confidence_score': analysis.enhanced_rating.confidence_score,
                            'feature_importance': analysis.enhanced_rating.feature_importance,
                            'recommendations': analysis.enhanced_rating.recommendations
                        }
                    })
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                results.append({
                    'url': url,
                    'error': f'Processing error: {str(e)}',
                    'status': 'failed'
                })
        
        # Calculate batch statistics
        successful_results = [r for r in results if r['status'] == 'success']
        failed_results = [r for r in results if r['status'] == 'failed']
        
        batch_summary = {
            'total_urls': len(urls),
            'successful': len(successful_results),
            'failed': len(failed_results),
            'average_rating': 0.0
        }
        
        if successful_results:
            total_rating = sum(r['rating'] for r in successful_results)
            batch_summary['average_rating'] = round(total_rating / len(successful_results), 2)
        
        response_data = {
            'results': results,
            'summary': batch_summary,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Batch rating completed: {batch_summary['successful']}/{batch_summary['total_urls']} successful")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in batch rating endpoint: {str(e)}")
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