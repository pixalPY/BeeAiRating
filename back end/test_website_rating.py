#!/usr/bin/env python3
"""
Test script for website rating functionality
"""

import requests
import json
import time
from website_analyzer import WebsiteAnalyzer

def test_website_analyzer():
    """Test the website analyzer directly"""
    print("🧪 Testing Website Analyzer...")
    
    analyzer = WebsiteAnalyzer()
    
    # Test URLs
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.example.com"
    ]
    
    for url in test_urls:
        print(f"\n📊 Testing: {url}")
        try:
            result = analyzer.rate_website(url)
            if result:
                print(f"✅ 成功分析")
                print(f"   标题: {result.title}")
                print(f"   评分: {result.rating}/5")
                print(f"   解释: {result.rating_explanation}")
            else:
                print(f"❌ 分析失败")
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        time.sleep(2)  # Avoid rate limiting

def test_api_endpoint():
    """Test the API endpoint"""
    print("\n🌐 Testing API Endpoint...")
    
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
            print("✅ API 测试成功")
            print(f"   状态: {data.get('status')}")
            print(f"   评分: {data.get('rating')}/5")
            print(f"   标题: {data.get('title')}")
        else:
            print(f"❌ API 测试失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ API 测试错误: {e}")

def test_invalid_urls():
    """Test with invalid URLs"""
    print("\n🚫 Testing Invalid URLs...")
    
    analyzer = WebsiteAnalyzer()
    
    invalid_urls = [
        "not-a-url",
        "http://invalid-domain-that-does-not-exist-12345.com",
        "",
        "ftp://example.com"
    ]
    
    for url in invalid_urls:
        print(f"\n📊 Testing invalid URL: {url}")
        result = analyzer.rate_website(url)
        if result is None:
            print("✅ 正确处理了无效URL")
        else:
            print("❌ 应该返回None但得到了结果")

if __name__ == "__main__":
    print("🚀 Starting Website Rating Tests...")
    
    # Test 1: Direct analyzer testing
    test_website_analyzer()
    
    # Test 2: Invalid URL handling
    test_invalid_urls()
    
    # Test 3: API endpoint testing
    test_api_endpoint()
    
    print("\n✨ 测试完成!") 