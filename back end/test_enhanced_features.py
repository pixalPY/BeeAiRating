#!/usr/bin/env python3
"""
Test script for enhanced AI rating features
"""

import requests
import json
import time
from enhanced_rating_model import EnhancedRatingModel

def test_enhanced_model():
    """Test the enhanced rating model directly"""
    print("🧪 Testing Enhanced Rating Model...")
    
    model = EnhancedRatingModel()
    
    # Test website data
    test_data = {
        'url': 'https://www.github.com',
        'title': 'GitHub: Let\'s build from here',
        'description': 'GitHub is where over 100 million developers shape the future of software, together. Contribute to the open source community, manage your Git repositories, review code like a pro, track bugs and features, power your CI/CD and DevOps workflows, and secure code before you commit it.',
        'content': 'GitHub is a web-based platform for version control and collaboration that lets developers work together on projects from anywhere. It provides a distributed version control system that allows multiple people to work on the same project simultaneously.',
        'load_time': 2.1,
        'mobile_friendly': True
    }
    
    print(f"\n📊 Testing enhanced model with sample data")
    try:
        result = model.predict_rating(test_data)
        print(f"✅ 增强模型测试成功")
        print(f"   总体评分: {result.overall_rating:.2f}/5")
        print(f"   内容评分: {result.content_rating:.2f}/5")
        print(f"   技术评分: {result.technical_rating:.2f}/5")
        print(f"   用户体验评分: {result.user_experience_rating:.2f}/5")
        print(f"   SEO评分: {result.seo_rating:.2f}/5")
        print(f"   安全评分: {result.security_rating:.2f}/5")
        print(f"   置信度: {result.confidence_score:.2f}")
        print(f"   建议数量: {len(result.recommendations)}")
        print(f"   特征重要性: {len(result.feature_importance)} 个特征")
    except Exception as e:
        print(f"❌ 增强模型测试失败: {e}")

def test_enhanced_api():
    """Test the enhanced API endpoint"""
    print("\n🌐 Testing Enhanced API Endpoint...")
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_data = {
        "url": "https://www.github.com"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/rate-website",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 增强API测试成功")
            print(f"   基础评分: {data.get('rating')}/5")
            
            if 'enhanced_rating' in data:
                enhanced = data['enhanced_rating']
                print(f"   增强总体评分: {enhanced.get('overall_rating', 0):.2f}/5")
                print(f"   内容评分: {enhanced.get('content_rating', 0):.2f}/5")
                print(f"   技术评分: {enhanced.get('technical_rating', 0):.2f}/5")
                print(f"   用户体验评分: {enhanced.get('user_experience_rating', 0):.2f}/5")
                print(f"   SEO评分: {enhanced.get('seo_rating', 0):.2f}/5")
                print(f"   安全评分: {enhanced.get('security_rating', 0):.2f}/5")
                print(f"   置信度: {enhanced.get('confidence_score', 0):.2f}")
                print(f"   建议: {len(enhanced.get('recommendations', []))} 条")
            else:
                print("   ⚠️ 未返回增强评分数据")
        else:
            print(f"❌ 增强API测试失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 增强API测试错误: {e}")

def test_batch_api():
    """Test the batch rating API endpoint"""
    print("\n📦 Testing Batch Rating API...")
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_data = {
        "urls": [
            "https://www.github.com",
            "https://www.google.com",
            "https://www.example.com"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/rate-batch",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 批量API测试成功")
            print(f"   总网站数: {data['summary']['total_urls']}")
            print(f"   成功评测: {data['summary']['successful']}")
            print(f"   评测失败: {data['summary']['failed']}")
            print(f"   平均评分: {data['summary']['average_rating']}")
            
            # Show individual results
            for i, result in enumerate(data['results']):
                print(f"   {i+1}. {result['url']}: {result.get('rating', 'N/A')}/5 ({result['status']})")
        else:
            print(f"❌ 批量API测试失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 批量API测试错误: {e}")

def test_feature_extraction():
    """Test feature extraction functionality"""
    print("\n🔍 Testing Feature Extraction...")
    
    model = EnhancedRatingModel()
    
    # Test different types of website data
    test_cases = [
        {
            'name': 'High Quality Website',
            'data': {
                'url': 'https://www.example.com',
                'title': 'Professional Website with Great Content',
                'description': 'This is a comprehensive description that provides detailed information about the website and its services.',
                'content': 'This website contains extensive content with proper structure, including headers, paragraphs, and interactive elements. The content is well-organized and provides valuable information to users.',
                'load_time': 1.5,
                'mobile_friendly': True
            }
        },
        {
            'name': 'Basic Website',
            'data': {
                'url': 'http://basic-site.com',
                'title': 'Basic Site',
                'description': 'Basic description',
                'content': 'Minimal content',
                'load_time': 5.0,
                'mobile_friendly': False
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        try:
            features = model.extract_features(test_case['data'])
            print(f"   内容长度: {features.content_length}")
            print(f"   标题长度: {features.title_length}")
            print(f"   描述长度: {features.description_length}")
            print(f"   SSL证书: {features.has_ssl}")
            print(f"   加载时间: {features.load_time}s")
            print(f"   移动友好: {features.mobile_friendly}")
            print(f"   SEO评分: {features.seo_score:.2f}")
            print(f"   可访问性: {features.accessibility_score:.2f}")
            print(f"   性能评分: {features.performance_score:.2f}")
            print(f"   安全评分: {features.security_score:.2f}")
        except Exception as e:
            print(f"   ❌ 特征提取失败: {e}")

def test_model_training():
    """Test model training functionality"""
    print("\n🎓 Testing Model Training...")
    
    model = EnhancedRatingModel()
    
    # Create sample training data
    training_data = [
        ({
            'url': 'https://excellent-site.com',
            'title': 'Excellent Website',
            'description': 'A comprehensive description',
            'content': 'High-quality content with proper structure',
            'load_time': 1.0,
            'mobile_friendly': True
        }, 4.5),
        ({
            'url': 'https://good-site.com',
            'title': 'Good Website',
            'description': 'A good description',
            'content': 'Good content with some structure',
            'load_time': 2.0,
            'mobile_friendly': True
        }, 3.5),
        ({
            'url': 'http://basic-site.com',
            'title': 'Basic Site',
            'description': 'Basic description',
            'content': 'Minimal content',
            'load_time': 5.0,
            'mobile_friendly': False
        }, 2.0)
    ]
    
    try:
        model.train_model(training_data)
        print("✅ 模型训练成功")
        print(f"   训练样本数: {len(training_data)}")
        print(f"   模型已保存: {model.is_trained}")
    except Exception as e:
        print(f"❌ 模型训练失败: {e}")

if __name__ == "__main__":
    print("🚀 Starting Enhanced Features Tests...")
    print("=" * 60)
    
    # Test 1: Enhanced model functionality
    test_enhanced_model()
    
    # Test 2: Feature extraction
    test_feature_extraction()
    
    # Test 3: Model training
    test_model_training()
    
    # Test 4: Enhanced API endpoint
    test_enhanced_api()
    
    # Test 5: Batch API endpoint
    test_batch_api()
    
    print("\n" + "=" * 60)
    print("✨ 增强功能测试完成!") 