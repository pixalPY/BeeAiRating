#!/usr/bin/env python3
"""
Website Analyzer
Analyzes websites and provides ratings based on content quality
"""

import requests
import logging
import time
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass
from gemini_client import GeminiClient
from enhanced_rating_model import EnhancedRatingModel, RatingResult

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class WebsiteAnalysis:
    """Data class for website analysis results"""
    url: str
    title: str
    description: str
    content_summary: str
    rating: float
    rating_explanation: str
    analysis_details: Dict[str, Any]
    enhanced_rating: Optional[RatingResult] = None

class WebsiteAnalyzer:
    """Analyzes websites and provides AI-powered ratings"""
    
    def __init__(self):
        """Initialize the website analyzer"""
        self.gemini_client = GeminiClient()
        self.enhanced_model = EnhancedRatingModel()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the URL is accessible and valid
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Parse URL
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
            
            # Test connection
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"URL validation failed for {url}: {e}")
            return False
    
    def measure_load_time(self, url: str) -> float:
        """
        Measure website load time
        
        Args:
            url: URL to measure
            
        Returns:
            Load time in seconds
        """
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            load_time = time.time() - start_time
            return round(load_time, 2)
        except Exception as e:
            logger.warning(f"Failed to measure load time for {url}: {e}")
            return 5.0  # Default load time
    
    def extract_website_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Extract content from website
        
        Args:
            url: URL to extract content from
            
        Returns:
            Dictionary with extracted content or None if failed
        """
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            # Extract main content (focus on article, main, or body)
            content_selectors = [
                'article', 'main', '[role="main"]', '.content', '.main-content',
                '#content', '#main', '.post-content', '.entry-content'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text(separator=' ', strip=True)
                    break
            
            # If no specific content area found, use body
            if not content_text:
                body = soup.find('body')
                if body:
                    # Remove script and style elements
                    for script in body(["script", "style"]):
                        script.decompose()
                    content_text = body.get_text(separator=' ', strip=True)
            
            # Clean up content
            content_text = re.sub(r'\s+', ' ', content_text)
            content_text = content_text[:5000]  # Limit content length
            
            # Measure load time
            load_time = self.measure_load_time(url)
            
            # Check mobile friendliness (simplified)
            mobile_friendly = 'viewport' in response.text.lower()
            
            return {
                'title': title_text,
                'description': description,
                'content': content_text,
                'url': url,
                'load_time': load_time,
                'mobile_friendly': mobile_friendly
            }
            
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {e}")
            return None
    
    def analyze_website_quality(self, content: Dict[str, str]) -> WebsiteAnalysis:
        """
        Analyze website quality using AI
        
        Args:
            content: Dictionary with website content
            
        Returns:
            WebsiteAnalysis object with rating and explanation
        """
        try:
            # Create analysis prompt
            prompt = f"""
            请分析以下网站的质量，并给出0-5分的评分（0分最差，5分最好）。

            网站信息：
            - 标题：{content['title']}
            - 描述：{content['description']}
            - 内容：{content['content'][:2000]}...

            请从以下维度进行分析：
            1. 内容质量（原创性、深度、准确性）
            2. 用户体验（可读性、结构、导航）
            3. 专业性（设计、技术实现、品牌形象）
            4. 价值性（对用户的价值、实用性）

            请返回JSON格式的分析结果：
            {{
                "rating": 分数(0-5),
                "rating_explanation": "评分解释",
                "content_quality": "内容质量分析",
                "user_experience": "用户体验分析", 
                "professionalism": "专业性分析",
                "value": "价值性分析",
                "summary": "总体评价"
            }}
            """
            
            # Get AI analysis
            response = self.gemini_client.generate_text(prompt)
            
            if not response:
                # Fallback analysis
                return self._fallback_analysis(content)
            
            # Try to parse JSON response
            try:
                import json
                analysis_data = json.loads(response)
                
                # Get enhanced rating
                enhanced_rating = self.enhanced_model.predict_rating(content)
                
                return WebsiteAnalysis(
                    url=content['url'],
                    title=content['title'],
                    description=content['description'],
                    content_summary=content['content'][:500] + "...",
                    rating=float(analysis_data.get('rating', 0)),
                    rating_explanation=analysis_data.get('rating_explanation', '分析失败'),
                    analysis_details={
                        'content_quality': analysis_data.get('content_quality', ''),
                        'user_experience': analysis_data.get('user_experience', ''),
                        'professionalism': analysis_data.get('professionalism', ''),
                        'value': analysis_data.get('value', ''),
                        'summary': analysis_data.get('summary', '')
                    },
                    enhanced_rating=enhanced_rating
                )
            except json.JSONDecodeError:
                # If JSON parsing fails, use fallback
                return self._fallback_analysis(content)
                
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(content)
    
    def _fallback_analysis(self, content: Dict[str, str]) -> WebsiteAnalysis:
        """
        Fallback analysis when AI analysis fails
        
        Args:
            content: Website content
            
        Returns:
            Basic WebsiteAnalysis object
        """
        # Simple heuristic-based analysis
        content_length = len(content['content'])
        title_length = len(content['title'])
        desc_length = len(content['description'])
        
        # Basic scoring
        score = 0
        if content_length > 1000:
            score += 1
        if title_length > 10:
            score += 1
        if desc_length > 50:
            score += 1
        if 'http' in content['url']:
            score += 1
        if content['title'] != "No title found":
            score += 1
        
        # Get enhanced rating
        enhanced_rating = self.enhanced_model.predict_rating(content)
        
        return WebsiteAnalysis(
            url=content['url'],
            title=content['title'],
            description=content['description'],
            content_summary=content['content'][:500] + "...",
            rating=float(score),
            rating_explanation="基于基础指标的自动评分",
            analysis_details={
                'content_quality': f"内容长度: {content_length} 字符",
                'user_experience': "基础用户体验评估",
                'professionalism': "基础专业性评估",
                'value': "基础价值评估",
                'summary': "AI分析失败，使用基础评分"
            },
            enhanced_rating=enhanced_rating
        )
    
    def rate_website(self, url: str) -> Optional[WebsiteAnalysis]:
        """
        Main method to rate a website
        
        Args:
            url: URL to rate
            
        Returns:
            WebsiteAnalysis object or None if failed
        """
        try:
            # Validate URL
            if not self.validate_url(url):
                logger.error(f"Invalid or inaccessible URL: {url}")
                return None
            
            # Extract content
            content = self.extract_website_content(url)
            if not content:
                logger.error(f"Failed to extract content from: {url}")
                return None
            
            # Analyze quality
            analysis = self.analyze_website_quality(content)
            
            logger.info(f"Successfully analyzed {url} with rating: {analysis.rating}/5")
            return analysis
            
        except Exception as e:
            logger.error(f"Website rating failed for {url}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    analyzer = WebsiteAnalyzer()
    
    # Test with a sample URL
    test_url = "https://www.example.com"
    result = analyzer.rate_website(test_url)
    
    if result:
        print(f"网站: {result.url}")
        print(f"标题: {result.title}")
        print(f"评分: {result.rating}/5")
        print(f"解释: {result.rating_explanation}")
        print(f"总结: {result.analysis_details['summary']}")
    else:
        print("分析失败") 