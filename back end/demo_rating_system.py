#!/usr/bin/env python3
"""
Demo script for the new rating system based on the rating guide
"""

from enhanced_rating_model import EnhancedRatingModel

def demo_rating_system():
    """Demonstrate the new rating system"""
    print("🚀 BeeAiRating 评分系统演示")
    print("=" * 60)
    print("📊 评分标准 (按图片指南):")
    print("   • 界面 (Interface): 35%")
    print("   • 代码 (Code): 15%")
    print("   • 功能 (Functionality): 45%")
    print("   • 实用性 (Practicality): 5%")
    print()
    print("⭐ 星级标准:")
    print("   • 5星: 80-100%")
    print("   • 4星: 60-80%")
    print("   • 3星: 40-60%")
    print("   • 2星: 20-40%")
    print("   • 1星: 0-20%")
    print("=" * 60)
    
    model = EnhancedRatingModel()
    
    # Test cases
    test_cases = [
        {
            'name': '优秀网站 (GitHub)',
            'data': {
                'url': 'https://www.github.com',
                'title': 'GitHub: Let\'s build from here',
                'description': 'GitHub is where over 100 million developers shape the future of software, together.',
                'content': 'GitHub is a web-based platform for version control and collaboration that lets developers work together on projects from anywhere.',
                'load_time': 1.5,
                'mobile_friendly': True
            }
        },
        {
            'name': '基础网站',
            'data': {
                'url': 'http://basic-site.com',
                'title': 'Basic Website',
                'description': 'A simple website',
                'content': 'This is a basic website with minimal content.',
                'load_time': 4.0,
                'mobile_friendly': False
            }
        },
        {
            'name': '中等质量网站',
            'data': {
                'url': 'https://medium-site.com',
                'title': 'Medium Quality Website',
                'description': 'A website with decent content and features',
                'content': 'This website has good content with proper structure and some interactive elements.',
                'load_time': 2.5,
                'mobile_friendly': True
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 测试案例 {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            result = model.predict_rating(test_case['data'])
            
            # Calculate percentage
            percentage = (result.overall_rating / 5.0) * 100
            
            # Determine star rating
            if percentage >= 80:
                stars = "⭐⭐⭐⭐⭐"
                star_text = "5星 (优秀)"
            elif percentage >= 60:
                stars = "⭐⭐⭐⭐☆"
                star_text = "4星 (良好)"
            elif percentage >= 40:
                stars = "⭐⭐⭐☆☆"
                star_text = "3星 (一般)"
            elif percentage >= 20:
                stars = "⭐⭐☆☆☆"
                star_text = "2星 (较差)"
            else:
                stars = "⭐☆☆☆☆"
                star_text = "1星 (很差)"
            
            print(f"总体评分: {result.overall_rating:.2f}/5 ({percentage:.1f}%)")
            print(f"星级: {stars} {star_text}")
            print(f"置信度: {result.confidence_score:.2f}")
            
            print("\n📈 详细评分分解:")
            print(f"   • 界面评分: {result.interface_rating:.2f}/5 (权重: 35%)")
            print(f"   • 代码评分: {result.code_rating:.2f}/5 (权重: 15%)")
            print(f"   • 功能评分: {result.functionality_rating:.2f}/5 (权重: 45%)")
            print(f"   • 实用性评分: {result.practicality_rating:.2f}/5 (权重: 5%)")
            
            # Calculate weighted scores
            interface_weighted = result.interface_rating * 0.35
            code_weighted = result.code_rating * 0.15
            functionality_weighted = result.functionality_rating * 0.45
            practicality_weighted = result.practicality_rating * 0.05
            
            print(f"\n⚖️ 加权评分:")
            print(f"   • 界面加权: {interface_weighted:.3f}")
            print(f"   • 代码加权: {code_weighted:.3f}")
            print(f"   • 功能加权: {functionality_weighted:.3f}")
            print(f"   • 实用性加权: {practicality_weighted:.3f}")
            print(f"   • 总计: {interface_weighted + code_weighted + functionality_weighted + practicality_weighted:.3f}")
            
            print(f"\n💡 改进建议:")
            for rec in result.recommendations:
                print(f"   • {rec}")
                
        except Exception as e:
            print(f"❌ 评分失败: {e}")
        
        print()

def demo_feature_importance():
    """Demonstrate feature importance analysis"""
    print("\n🎯 特征重要性分析演示")
    print("=" * 60)
    
    model = EnhancedRatingModel()
    
    # Sample data
    sample_data = {
        'url': 'https://www.example.com',
        'title': 'Example Website',
        'description': 'This is an example website for demonstration',
        'content': 'This website contains various features and content for testing purposes.',
        'load_time': 2.0,
        'mobile_friendly': True
    }
    
    try:
        result = model.predict_rating(sample_data)
        
        print("📊 特征重要性排序:")
        sorted_features = sorted(result.feature_importance.items(), 
                               key=lambda x: x[1], reverse=True)
        
        for i, (feature, importance) in enumerate(sorted_features[:10], 1):
            feature_name = {
                'content_length': '内容长度',
                'title_length': '标题长度',
                'description_length': '描述长度',
                'has_ssl': 'SSL证书',
                'load_time': '加载时间',
                'mobile_friendly': '移动友好',
                'seo_score': 'SEO评分',
                'accessibility_score': '可访问性',
                'performance_score': '性能评分',
                'security_score': '安全评分',
                'user_engagement': '用户参与',
                'content_quality': '内容质量',
                'design_score': '设计评分',
                'functionality_score': '功能评分'
            }.get(feature, feature)
            
            print(f"   {i:2d}. {feature_name}: {importance:.3f}")
            
    except Exception as e:
        print(f"❌ 特征分析失败: {e}")

if __name__ == "__main__":
    demo_rating_system()
    demo_feature_importance()
    print("\n✨ 演示完成!") 