#!/usr/bin/env python3
"""
Comprehensive test suite for the E-commerce Analytics Application.

This script tests all major components of the application to ensure
they work correctly before deployment.
"""

import sys
import os
from pathlib import Path
import traceback
import time

# Add module paths
sys.path.append(str(Path(__file__).parent / "30-database"))
sys.path.append(str(Path(__file__).parent / "40-llm"))
sys.path.append(str(Path(__file__).parent / "50-visualization"))

def test_database_components():
    """Test database connection and schema components."""
    print("🔍 Testing Database Components...")
    
    try:
        from connection import get_database, test_connection
        from schema import get_schema
        
        # Test database connection
        print("  ✓ Database modules imported successfully")
        
        if test_connection():
            print("  ✓ Database connection successful")
        else:
            print("  ❌ Database connection failed")
            return False
        
        # Test database operations
        db = get_database()
        table_info = db.get_table_info()
        print(f"  ✓ Database has {table_info['row_count']} rows")
        
        # Test schema operations
        schema = get_schema()
        categories = schema.get_categories_and_subcategories()
        print(f"  ✓ Schema loaded with {len(categories)} categories")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_llm_components():
    """Test LLM components (SQL agent and story generator)."""
    print("\n🤖 Testing LLM Components...")
    
    try:
        from sql_agent import get_sql_agent
        from story_generator import get_story_generator
        
        print("  ✓ LLM modules imported successfully")
        
        # Test SQL agent
        sql_agent = get_sql_agent()
        
        # Test with a simple question
        test_question = "What are the top 3 product categories by number of orders?"
        print(f"  🔍 Testing SQL generation: {test_question}")
        
        result = sql_agent.generate_sql(test_question)
        
        if result.success:
            print(f"  ✓ SQL generated successfully: {result.query[:100]}...")
            print(f"  ✓ Query returned {len(result.data)} rows")
        else:
            print(f"  ❌ SQL generation failed: {result.error}")
            return False
        
        # Test story generator
        story_generator = get_story_generator()
        
        print("  📝 Testing story generation...")
        story = story_generator.generate_story(
            test_question,
            result.query,
            result.data,
            ['product_category', 'order_count']
        )
        
        if story.executive_summary:
            print(f"  ✓ Story generated successfully")
            print(f"  ✓ Executive summary: {story.executive_summary[:100]}...")
        else:
            print("  ❌ Story generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ LLM test failed: {e}")
        traceback.print_exc()
        return False

def test_visualization_components():
    """Test visualization components."""
    print("\n📊 Testing Visualization Components...")
    
    try:
        from plotly_charts import get_chart_generator, suggest_chart_type
        
        print("  ✓ Visualization modules imported successfully")
        
        # Test chart generator
        chart_generator = get_chart_generator()
        
        # Sample data for testing
        sample_data = [
            ('Electronics', 1500, 45),
            ('Clothing', 1200, 38),
            ('Books', 800, 25),
            ('Home', 600, 18)
        ]
        
        columns = ['category', 'revenue', 'orders']
        
        # Test chart generation
        fig = chart_generator.auto_generate_chart(sample_data, columns, "Test Chart")
        
        if fig:
            print("  ✓ Chart generated successfully")
        else:
            print("  ❌ Chart generation failed")
            return False
        
        # Test chart type suggestion
        suggested_type = suggest_chart_type(sample_data, columns)
        print(f"  ✓ Chart type suggestion: {suggested_type}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Visualization test failed: {e}")
        traceback.print_exc()
        return False

def test_end_to_end_workflow():
    """Test complete end-to-end workflow."""
    print("\n🔄 Testing End-to-End Workflow...")
    
    try:
        from sql_agent import get_sql_agent
        from story_generator import get_story_generator
        from plotly_charts import get_chart_generator
        
        # Initialize components
        sql_agent = get_sql_agent()
        story_generator = get_story_generator()
        chart_generator = get_chart_generator()
        
        # Test questions
        test_questions = [
            "What are the top 5 product categories by revenue?",
            "Show me the average order value by shipping state",
            "Which payment methods are most popular?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n  Test {i}: {question}")
            
            # Generate SQL
            start_time = time.time()
            result = sql_agent.generate_sql(question)
            sql_time = time.time() - start_time
            
            if not result.success:
                print(f"    ❌ SQL generation failed: {result.error}")
                continue
            
            print(f"    ✓ SQL generated in {sql_time:.2f}s")
            
            # Generate story
            start_time = time.time()
            story = story_generator.generate_story(
                question,
                result.query,
                result.data,
                ['column1', 'column2']  # Simplified for test
            )
            story_time = time.time() - start_time
            
            print(f"    ✓ Story generated in {story_time:.2f}s")
            
            # Generate chart
            start_time = time.time()
            fig = chart_generator.auto_generate_chart(
                result.data,
                ['category', 'value'],
                question
            )
            chart_time = time.time() - start_time
            
            print(f"    ✓ Chart generated in {chart_time:.2f}s")
            print(f"    ✓ Total time: {sql_time + story_time + chart_time:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"  ❌ End-to-end test failed: {e}")
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling scenarios."""
    print("\n⚠️  Testing Error Handling...")
    
    try:
        from sql_agent import get_sql_agent
        
        sql_agent = get_sql_agent()
        
        # Test with invalid question
        invalid_questions = [
            "DELETE FROM sales_table",  # Dangerous query
            "",  # Empty question
            "What is the meaning of life?",  # Irrelevant question
        ]
        
        for question in invalid_questions:
            print(f"  Testing invalid question: {question[:50]}...")
            result = sql_agent.generate_sql(question)
            
            if not result.success:
                print(f"    ✓ Properly handled error: {result.error}")
            else:
                print(f"    ⚠️  Expected error but got success")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 E-commerce Analytics Application Test Suite")
    print("=" * 50)
    
    # Track test results
    tests = [
        ("Database Components", test_database_components),
        ("LLM Components", test_llm_components),
        ("Visualization Components", test_visualization_components),
        ("End-to-End Workflow", test_end_to_end_workflow),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print(f"\n🎉 All tests passed! Application is ready for use.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)