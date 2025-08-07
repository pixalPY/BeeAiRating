#!/usr/bin/env python3
"""
Test suite for BeeAiRating application
"""

import pytest
import json
import tempfile
import os
import numpy as np
from unittest.mock import patch, MagicMock
from app import app, AiRatingEngine

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return {
        "data": {
            "feature1": 85.5,
            "feature2": 92.0,
            "feature3": 78.5,
            "feature4": "test_string",
            "feature5": 88.0
        }
    }

class TestAiRatingEngine:
    """Test cases for AI Rating Engine"""
    
    def setup_method(self):
        """Setup method for each test"""
        self.engine = AiRatingEngine()
    
    def test_engine_initialization(self):
        """Test AI rating engine initialization"""
        assert self.engine is not None
        assert hasattr(self.engine, 'logger')
    
    def test_extract_features(self):
        """Test feature extraction from data"""
        test_data = {
            "numeric1": 100,
            "numeric2": 50.5,
            "string1": "test",
            "string2": "another_test"
        }
        
        features = self.engine._extract_features(test_data)
        
        assert len(features) == 4
        assert features[0] == 100.0
        assert features[1] == 50.5
        assert isinstance(features[2], float)  # hash value
        assert isinstance(features[3], float)  # hash value
    
    def test_calculate_rating(self):
        """Test rating calculation"""
        features = np.array([80.0, 90.0, 70.0, 85.0])
        rating = self.engine._calculate_rating(features)
        
        assert isinstance(rating, float)
        assert 0 <= rating <= 100
        assert rating == 81.25  # (80+90+70+85)/4
    
    def test_categorize_rating(self):
        """Test rating categorization"""
        assert self.engine._categorize_rating(95) == "Excellent"
        assert self.engine._categorize_rating(85) == "Very Good"
        assert self.engine._categorize_rating(75) == "Good"
        assert self.engine._categorize_rating(65) == "Average"
        assert self.engine._categorize_rating(55) == "Below Average"
        assert self.engine._categorize_rating(30) == "Poor"
    
    def test_generate_recommendations(self):
        """Test recommendation generation"""
        # High rating - no recommendations
        recs_high = self.engine._generate_recommendations(85)
        assert len(recs_high) == 0
        
        # Medium rating - some recommendations
        recs_medium = self.engine._generate_recommendations(65)
        assert len(recs_medium) == 2
        assert "Consider improving data quality" in recs_medium
        
        # Low rating - more recommendations
        recs_low = self.engine._generate_recommendations(30)
        assert len(recs_low) == 4
        assert "Immediate attention required" in recs_low
    
    def test_calculate_confidence(self):
        """Test confidence calculation"""
        # Low variance features - high confidence
        features_low_var = np.array([50.0, 51.0, 49.0, 50.5])
        confidence_low = self.engine._calculate_confidence(features_low_var)
        assert confidence_low > 0.8
        
        # High variance features - lower confidence
        features_high_var = np.array([10.0, 90.0, 5.0, 95.0])
        confidence_high = self.engine._calculate_confidence(features_high_var)
        assert confidence_high < confidence_low
    
    def test_analyze_data_complete(self):
        """Test complete data analysis workflow"""
        test_data = {
            "score1": 85,
            "score2": 92,
            "category": "premium"
        }
        
        result = self.engine.analyze_data(test_data)
        
        # Check result structure
        assert 'rating' in result
        assert 'analysis' in result
        assert 'timestamp' in result
        assert 'confidence' in result
        
        # Check rating value
        assert isinstance(result['rating'], float)
        assert 0 <= result['rating'] <= 100
        
        # Check analysis structure
        analysis = result['analysis']
        assert 'feature_count' in analysis
        assert 'feature_summary' in analysis
        assert 'rating_category' in analysis
        assert 'recommendations' in analysis
        
        # Check feature summary
        summary = analysis['feature_summary']
        assert 'mean' in summary
        assert 'std' in summary
        assert 'min' in summary
        assert 'max' in summary

class TestFlaskEndpoints:
    """Test cases for Flask API endpoints"""
    
    def test_index_route(self, client):
        """Test main page route"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['version'] == '1.0.0'
    
    def test_rate_data_valid(self, client, sample_data):
        """Test rating endpoint with valid data"""
        response = client.post('/api/rate',
                             data=json.dumps(sample_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'rating' in data
        assert 'analysis' in data
        assert 'timestamp' in data
        assert 'confidence' in data
    
    def test_rate_data_invalid_format(self, client):
        """Test rating endpoint with invalid data format"""
        # Missing 'data' key
        invalid_data = {"wrong_key": {"feature1": 100}}
        response = client.post('/api/rate',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid request format' in data['error']
    
    def test_rate_data_empty(self, client):
        """Test rating endpoint with empty data"""
        response = client.post('/api/rate',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_rate_data_malformed_json(self, client):
        """Test rating endpoint with malformed JSON"""
        response = client.post('/api/rate',
                             data="invalid json",
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Not found'

class TestLogging:
    """Test cases for logging functionality"""
    
    def test_logging_setup(self):
        """Test that logging is properly configured"""
        # Check if logs directory is created
        assert os.path.exists('logs')
        
        # Check if log file is created when app runs
        # This would be tested in integration tests
    
    @patch('app.logging.getLogger')
    def test_logging_in_ai_engine(self, mock_get_logger):
        """Test logging in AI rating engine"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        engine = AiRatingEngine()
        
        # Test that logger is called during initialization
        mock_logger.info.assert_called_with("Initializing AI Rating Engine")

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v']) 