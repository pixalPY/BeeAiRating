#!/usr/bin/env python3
"""
Enhanced AI Rating Model
Provides advanced rating algorithms with multiple dimensions
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class RatingFeatures:
    """Data class for rating features"""
    content_length: int
    title_length: int
    description_length: int
    has_ssl: bool
    load_time: float
    mobile_friendly: bool
    seo_score: float
    accessibility_score: float
    performance_score: float
    security_score: float
    user_engagement: float
    content_quality: float
    design_score: float
    functionality_score: float

@dataclass
class RatingResult:
    """Data class for rating results"""
    overall_rating: float
    content_rating: float
    technical_rating: float
    user_experience_rating: float
    seo_rating: float
    security_rating: float
    # New rating dimensions based on the rating guide
    interface_rating: float
    code_rating: float
    functionality_rating: float
    practicality_rating: float
    confidence_score: float
    feature_importance: Dict[str, float]
    recommendations: List[str]
    timestamp: str

class EnhancedRatingModel:
    """Enhanced AI rating model with multiple dimensions"""
    
    def __init__(self):
        """Initialize the enhanced rating model"""
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
        self.feature_names = [
            'content_length', 'title_length', 'description_length',
            'has_ssl', 'load_time', 'mobile_friendly', 'seo_score',
            'accessibility_score', 'performance_score', 'security_score',
            'user_engagement', 'content_quality', 'design_score', 'functionality_score'
        ]
        
        # Load pre-trained model if exists
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model from file"""
        model_path = 'models/enhanced_rating_model.pkl'
        if os.path.exists(model_path):
            try:
                loaded_data = joblib.load(model_path)
                self.model = loaded_data['model']
                self.scaler = loaded_data['scaler']
                self.is_trained = True
                logger.info("Loaded pre-trained enhanced rating model")
            except Exception as e:
                logger.warning(f"Failed to load pre-trained model: {e}")
    
    def _save_model(self):
        """Save trained model to file"""
        try:
            os.makedirs('models', exist_ok=True)
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'timestamp': datetime.now().isoformat()
            }
            joblib.dump(model_data, 'models/enhanced_rating_model.pkl')
            logger.info("Saved enhanced rating model")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def extract_features(self, website_data: Dict[str, Any]) -> RatingFeatures:
        """
        Extract comprehensive features from website data
        
        Args:
            website_data: Raw website data
            
        Returns:
            RatingFeatures object
        """
        try:
            # Basic content features
            content_length = len(website_data.get('content', ''))
            title_length = len(website_data.get('title', ''))
            description_length = len(website_data.get('description', ''))
            
            # Technical features
            has_ssl = website_data.get('url', '').startswith('https://')
            load_time = website_data.get('load_time', 5.0)  # Default 5 seconds
            mobile_friendly = website_data.get('mobile_friendly', True)
            
            # SEO features
            seo_score = self._calculate_seo_score(website_data)
            
            # Accessibility features
            accessibility_score = self._calculate_accessibility_score(website_data)
            
            # Performance features
            performance_score = self._calculate_performance_score(website_data)
            
            # Security features
            security_score = self._calculate_security_score(website_data)
            
            # User engagement features
            user_engagement = self._calculate_user_engagement(website_data)
            
            # Content quality features
            content_quality = self._calculate_content_quality(website_data)
            
            # Design features
            design_score = self._calculate_design_score(website_data)
            
            # Functionality features
            functionality_score = self._calculate_functionality_score(website_data)
            
            return RatingFeatures(
                content_length=content_length,
                title_length=title_length,
                description_length=description_length,
                has_ssl=has_ssl,
                load_time=load_time,
                mobile_friendly=mobile_friendly,
                seo_score=seo_score,
                accessibility_score=accessibility_score,
                performance_score=performance_score,
                security_score=security_score,
                user_engagement=user_engagement,
                content_quality=content_quality,
                design_score=design_score,
                functionality_score=functionality_score
            )
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            # Return default features
            return RatingFeatures(
                content_length=0, title_length=0, description_length=0,
                has_ssl=False, load_time=5.0, mobile_friendly=True,
                seo_score=0.5, accessibility_score=0.5, performance_score=0.5,
                security_score=0.5, user_engagement=0.5, content_quality=0.5,
                design_score=0.5, functionality_score=0.5
            )
    
    def _calculate_seo_score(self, data: Dict[str, Any]) -> float:
        """Calculate SEO score based on various factors"""
        score = 0.5  # Base score
        
        # Title optimization
        title = data.get('title', '')
        if 30 <= len(title) <= 60:
            score += 0.1
        
        # Description optimization
        description = data.get('description', '')
        if 120 <= len(description) <= 160:
            score += 0.1
        
        # Content length
        content_length = len(data.get('content', ''))
        if content_length > 1000:
            score += 0.1
        
        # SSL certificate
        if data.get('url', '').startswith('https://'):
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_accessibility_score(self, data: Dict[str, Any]) -> float:
        """Calculate accessibility score"""
        score = 0.5  # Base score
        
        # Check for alt text in images (simplified)
        content = data.get('content', '')
        if 'alt=' in content.lower():
            score += 0.1
        
        # Check for semantic HTML elements
        semantic_elements = ['<header>', '<nav>', '<main>', '<article>', '<section>', '<footer>']
        for element in semantic_elements:
            if element in content:
                score += 0.05
        
        return min(1.0, score)
    
    def _calculate_performance_score(self, data: Dict[str, Any]) -> float:
        """Calculate performance score"""
        load_time = data.get('load_time', 5.0)
        
        if load_time < 2.0:
            return 1.0
        elif load_time < 4.0:
            return 0.8
        elif load_time < 6.0:
            return 0.6
        else:
            return 0.4
    
    def _calculate_security_score(self, data: Dict[str, Any]) -> float:
        """Calculate security score"""
        score = 0.5  # Base score
        
        # HTTPS
        if data.get('url', '').startswith('https://'):
            score += 0.3
        
        # Content security policy (simplified check)
        content = data.get('content', '')
        if 'content-security-policy' in content.lower():
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_user_engagement(self, data: Dict[str, Any]) -> float:
        """Calculate user engagement score"""
        score = 0.5  # Base score
        
        # Content length (longer content = more engagement)
        content_length = len(data.get('content', ''))
        if content_length > 2000:
            score += 0.2
        elif content_length > 1000:
            score += 0.1
        
        # Interactive elements
        content = data.get('content', '')
        if any(element in content.lower() for element in ['button', 'form', 'input']):
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_content_quality(self, data: Dict[str, Any]) -> float:
        """Calculate content quality score"""
        score = 0.5  # Base score
        
        # Title quality
        title = data.get('title', '')
        if len(title) > 10 and not title.isupper():
            score += 0.1
        
        # Description quality
        description = data.get('description', '')
        if len(description) > 50:
            score += 0.1
        
        # Content structure
        content = data.get('content', '')
        if any(tag in content for tag in ['<h1>', '<h2>', '<h3>', '<p>']):
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_design_score(self, data: Dict[str, Any]) -> float:
        """Calculate design score"""
        score = 0.5  # Base score
        
        # CSS presence
        content = data.get('content', '')
        if 'css' in content.lower() or 'style' in content.lower():
            score += 0.2
        
        # Responsive design indicators
        if 'viewport' in content.lower():
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_functionality_score(self, data: Dict[str, Any]) -> float:
        """Calculate functionality score"""
        score = 0.5  # Base score
        
        # JavaScript presence
        content = data.get('content', '')
        if 'script' in content.lower():
            score += 0.2
        
        # Form elements
        if 'form' in content.lower():
            score += 0.1
        
        return min(1.0, score)
    
    def features_to_array(self, features: RatingFeatures) -> np.ndarray:
        """Convert RatingFeatures to numpy array"""
        feature_values = [
            features.content_length, features.title_length, features.description_length,
            float(features.has_ssl), features.load_time, float(features.mobile_friendly),
            features.seo_score, features.accessibility_score, features.performance_score,
            features.security_score, features.user_engagement, features.content_quality,
            features.design_score, features.functionality_score
        ]
        return np.array(feature_values).reshape(1, -1)
    
    def predict_rating(self, website_data: Dict[str, Any]) -> RatingResult:
        """
        Predict comprehensive rating for website
        
        Args:
            website_data: Website data dictionary
            
        Returns:
            RatingResult object with detailed ratings
        """
        try:
            # Extract features
            features = self.extract_features(website_data)
            feature_array = self.features_to_array(features)
            
            if self.is_trained:
                # Use trained model
                scaled_features = self.scaler.transform(feature_array)
                overall_rating = self.model.predict(scaled_features)[0]
                
                # Get feature importance
                feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            else:
                # Use rule-based scoring
                overall_rating = self._rule_based_scoring(features)
                feature_importance = {name: 1.0/len(self.feature_names) for name in self.feature_names}
            
            # Calculate individual dimension ratings based on the rating guide
            interface_rating = (features.design_score + features.accessibility_score + float(features.mobile_friendly)) / 3
            code_rating = (features.performance_score + features.functionality_score) / 2
            functionality_rating = (features.content_quality + features.user_engagement + features.seo_score) / 3
            practicality_rating = features.content_quality
            
            # Legacy ratings for backward compatibility
            content_rating = functionality_rating
            technical_rating = code_rating
            user_experience_rating = interface_rating
            seo_rating = features.seo_score
            security_rating = features.security_score
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(features)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(features, overall_rating)
            
            return RatingResult(
                overall_rating=float(overall_rating),
                content_rating=float(content_rating),
                technical_rating=float(technical_rating),
                user_experience_rating=float(user_experience_rating),
                seo_rating=float(seo_rating),
                security_rating=float(security_rating),
                interface_rating=float(interface_rating),
                code_rating=float(code_rating),
                functionality_rating=float(functionality_rating),
                practicality_rating=float(practicality_rating),
                confidence_score=float(confidence_score),
                feature_importance=feature_importance,
                recommendations=recommendations,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error predicting rating: {e}")
            # Return default result
            return RatingResult(
                overall_rating=0.0, content_rating=0.0, technical_rating=0.0,
                user_experience_rating=0.0, seo_rating=0.0, security_rating=0.0,
                interface_rating=0.0, code_rating=0.0, functionality_rating=0.0, practicality_rating=0.0,
                confidence_score=0.0, feature_importance={}, recommendations=["分析失败"],
                timestamp=datetime.now().isoformat()
            )
    
    def _rule_based_scoring(self, features: RatingFeatures) -> float:
        """Rule-based scoring when model is not trained"""
        score = 0.0
        
        # Interface (35% weight) - 界面评分
        interface_score = (features.design_score + features.accessibility_score + features.mobile_friendly) / 3
        score += interface_score * 0.35
        
        # Code (15% weight) - 代码质量评分
        code_score = (features.performance_score + features.functionality_score) / 2
        score += code_score * 0.15
        
        # Functionality (45% weight) - 功能评分
        functionality_score = (features.content_quality + features.user_engagement + features.seo_score) / 3
        score += functionality_score * 0.45
        
        # Practicality in daily life (5% weight) - 实用性评分
        practicality_score = features.content_quality  # 内容质量作为实用性指标
        score += practicality_score * 0.05
        
        return min(5.0, score * 5.0)  # Scale to 0-5
    
    def _calculate_confidence(self, features: RatingFeatures) -> float:
        """Calculate confidence score for the rating"""
        # Higher confidence for more complete data
        confidence = 0.5  # Base confidence
        
        if features.content_length > 1000:
            confidence += 0.1
        
        if features.title_length > 10:
            confidence += 0.1
        
        if features.description_length > 50:
            confidence += 0.1
        
        if features.has_ssl:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _generate_recommendations(self, features: RatingFeatures, overall_rating: float) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if features.content_quality < 0.7:
            recommendations.append("提高内容质量和原创性")
        
        if features.seo_score < 0.7:
            recommendations.append("优化SEO设置，包括标题和描述")
        
        if features.security_score < 0.8:
            recommendations.append("加强网站安全性，确保使用HTTPS")
        
        if features.performance_score < 0.7:
            recommendations.append("优化网站加载速度")
        
        if features.accessibility_score < 0.7:
            recommendations.append("改善网站可访问性")
        
        if overall_rating < 3.0:
            recommendations.append("建议进行全面网站优化")
        
        if not recommendations:
            recommendations.append("网站表现良好，继续保持")
        
        return recommendations
    
    def train_model(self, training_data: List[Tuple[Dict[str, Any], float]]):
        """
        Train the model with labeled data
        
        Args:
            training_data: List of (website_data, rating) tuples
        """
        try:
            X = []
            y = []
            
            for website_data, rating in training_data:
                features = self.extract_features(website_data)
                feature_array = self.features_to_array(features)
                X.append(feature_array.flatten())
                y.append(rating)
            
            X = np.array(X)
            y = np.array(y)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            # Save model
            self._save_model()
            
            logger.info(f"Model trained with {len(training_data)} samples")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize model
    model = EnhancedRatingModel()
    
    # Example website data
    sample_data = {
        'url': 'https://example.com',
        'title': 'Example Website',
        'description': 'This is an example website for testing',
        'content': 'This is the main content of the website...',
        'load_time': 2.5,
        'mobile_friendly': True
    }
    
    # Predict rating
    result = model.predict_rating(sample_data)
    
    print(f"Overall Rating: {result.overall_rating:.2f}/5")
    print(f"Content Rating: {result.content_rating:.2f}/5")
    print(f"Technical Rating: {result.technical_rating:.2f}/5")
    print(f"User Experience Rating: {result.user_experience_rating:.2f}/5")
    print(f"SEO Rating: {result.seo_rating:.2f}/5")
    print(f"Security Rating: {result.security_rating:.2f}/5")
    print(f"Confidence: {result.confidence_score:.2f}")
    print(f"Recommendations: {result.recommendations}") 