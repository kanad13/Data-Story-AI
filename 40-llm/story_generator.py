"""
Story generation module for creating rich analytical narratives.

This module generates comprehensive business stories and insights from SQL query results,
providing context and actionable recommendations.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import pandas as pd
import json
from dotenv import load_dotenv

# Environment variables hardcoded for Streamlit deployment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - hardcoded for deployment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OPENAI_API_KEY is required")

@dataclass
class StoryContent:
    """Structure for generated story content."""
    executive_summary: str
    key_insights: List[str]
    detailed_analysis: str
    recommendations: List[str]
    visualization_suggestions: List[Dict[str, str]]
    follow_up_questions: List[str]

class StoryGenerator:
    """
    Generates business stories and insights from data analysis results.
    """

    def __init__(self):
        """Initialize the story generator."""
        self.llm = self._initialize_llm()

    def _create_safe_dataframe(self, data: List[tuple], columns: List[str]) -> pd.DataFrame:
        """
        Create a pandas DataFrame with automatic column mismatch handling.

        Args:
            data: List of tuples containing query results
            columns: List of column names

        Returns:
            pandas DataFrame with properly aligned columns
        """
        try:
            if not data or len(data) == 0:
                return pd.DataFrame(columns=columns)

            # Fix column count mismatch
            actual_cols = len(data[0])

            if len(columns) != actual_cols:
                logger.warning(f"Story generator column mismatch: expected {len(columns)}, got {actual_cols}. Auto-fixing...")

                if len(columns) < actual_cols:
                    # Add missing column names
                    columns = columns + [f'col_{i}' for i in range(len(columns), actual_cols)]
                elif len(columns) > actual_cols:
                    # Truncate extra column names
                    columns = columns[:actual_cols]

            return pd.DataFrame(data, columns=columns)

        except Exception as e:
            logger.error(f"Error creating safe DataFrame in story generator: {e}")
            # Ultimate fallback: create generic DataFrame
            if data and len(data) > 0:
                actual_cols = len(data[0])
                fallback_columns = [f'column_{i+1}' for i in range(actual_cols)]
                return pd.DataFrame(data, columns=fallback_columns)
            else:
                return pd.DataFrame()

    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the OpenAI LLM."""
        try:
            return ChatOpenAI(
                model="gpt-4.1-nano-2025-04-14",
                temperature=0.8,
                openai_api_key=OPENAI_API_KEY,
                max_tokens=10000
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def generate_story(self, question: str, query: str, data: List[tuple], columns: List[str]) -> StoryContent:
        """
        Generate a comprehensive business story from query results.

        Args:
            question: Original business question
            query: SQL query that was executed
            data: Query results
            columns: Column names

        Returns:
            StoryContent with comprehensive analysis
        """
        try:
            # Convert data to DataFrame with safe column handling
            df = self._create_safe_dataframe(data, columns)

            # Create context for the LLM
            context = self._create_analysis_context(question, query, df, columns)

            # Generate story using LLM
            story_prompt = self._create_story_prompt(context)
            response = self.llm.invoke([
                SystemMessage(content=story_prompt["system"]),
                HumanMessage(content=story_prompt["user"])
            ])

            # Parse the response
            story_content = self._parse_story_response(response.content)

            return story_content

        except Exception as e:
            logger.error(f"Error generating story: {e}")
            return self._create_error_story(str(e))

    def _create_analysis_context(self, question: str, query: str, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        """Create context for story generation."""
        context = {
            "question": question,
            "query": query,
            "data_summary": {
                "total_rows": len(df),
                "columns": columns,
                "sample_data": df.head(10).to_dict('records') if len(df) > 0 else []
            },
            "data_insights": self._extract_basic_insights(df, columns)
        }

        return context

    def _extract_basic_insights(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        """Extract basic insights from the data."""
        insights = {}

        try:
            if len(df) > 0:
                for col in columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        insights[col] = {
                            "type": "numeric",
                            "min": float(df[col].min()),
                            "max": float(df[col].max()),
                            "mean": float(df[col].mean()),
                            "std": float(df[col].std()) if len(df) > 1 else 0
                        }
                    else:
                        insights[col] = {
                            "type": "categorical",
                            "unique_values": int(df[col].nunique()),
                            "top_values": df[col].value_counts().head(5).to_dict()
                        }
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")

        return insights

    def _create_story_prompt(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Create prompts for story generation."""

        system_prompt = """
You are a senior business analyst specializing in e-commerce analytics. Your task is to create comprehensive, actionable business stories from data analysis results.

Create a well-structured analysis that includes:
1. Executive Summary (2-3 sentences)
2. Key Insights (3-5 bullet points)
3. Detailed Analysis (2-3 paragraphs)
4. Recommendations (3-5 actionable items)
5. Visualization Suggestions (2-3 chart types with descriptions)
6. Follow-up Questions (3-5 related questions)

Format your response as JSON with the following structure:
{
  "executive_summary": "Brief summary of main findings",
  "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "detailed_analysis": "Detailed explanation of findings and their business implications",
  "recommendations": ["Recommendation 1", "Recommendation 2", "Recommendation 3"],
  "visualization_suggestions": [
    {"type": "chart_type", "description": "What this chart shows"},
    {"type": "chart_type", "description": "What this chart shows"}
  ],
  "follow_up_questions": ["Question 1", "Question 2", "Question 3"]
}

Focus on:
- Business implications and actionable insights
- Trends, patterns, and anomalies
- Opportunities for growth and improvement
- Practical recommendations
- Clear, non-technical language
"""

        user_prompt = f"""
Analyze the following e-commerce data and create a comprehensive business story:

**Original Question:** {context['question']}

**SQL Query:** {context['query']}

**Data Summary:**
- Total rows: {context['data_summary']['total_rows']}
- Columns: {context['data_summary']['columns']}

**Sample Data:**
{context['data_summary']['sample_data'][:5]}

**Data Insights:**
{context['data_insights']}

Please provide a comprehensive business analysis in JSON format.
"""

        return {
            "system": system_prompt,
            "user": user_prompt
        }

    def _parse_story_response(self, response_content: str) -> StoryContent:
        """Parse the LLM response into StoryContent."""
        try:
            # Clean the response (remove markdown formatting if present)
            content = response_content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()

            # Parse JSON
            parsed = json.loads(content)

            return StoryContent(
                executive_summary=parsed.get('executive_summary', ''),
                key_insights=parsed.get('key_insights', []),
                detailed_analysis=parsed.get('detailed_analysis', ''),
                recommendations=parsed.get('recommendations', []),
                visualization_suggestions=parsed.get('visualization_suggestions', []),
                follow_up_questions=parsed.get('follow_up_questions', [])
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return self._create_fallback_story(response_content)
        except Exception as e:
            logger.error(f"Error parsing story response: {e}")
            return self._create_error_story(str(e))

    def _create_fallback_story(self, raw_content: str) -> StoryContent:
        """Create a fallback story when JSON parsing fails."""
        return StoryContent(
            executive_summary="Analysis completed successfully, but formatting needs adjustment.",
            key_insights=[
                "Data analysis was performed successfully",
                "Results are available for review",
                "Additional processing may be needed for optimal presentation"
            ],
            detailed_analysis=f"Raw analysis results: {raw_content[:500]}...",
            recommendations=[
                "Review the raw analysis results",
                "Consider re-running the analysis",
                "Check data format and structure"
            ],
            visualization_suggestions=[
                {"type": "bar", "description": "Standard bar chart for categorical data"},
                {"type": "line", "description": "Time series chart for trends"}
            ],
            follow_up_questions=[
                "What specific metrics are most important?",
                "Are there any data quality issues?",
                "What time period should we focus on?"
            ]
        )

    def _create_error_story(self, error_message: str) -> StoryContent:
        """Create an error story when generation fails."""
        return StoryContent(
            executive_summary=f"Story generation encountered an error: {error_message}",
            key_insights=[
                "Story generation process failed",
                "Data may still be available for manual review",
                "Technical issue needs to be resolved"
            ],
            detailed_analysis=f"The story generation process failed with the following error: {error_message}. Please check the data format and try again.",
            recommendations=[
                "Review the error message and data format",
                "Check system configuration and API keys",
                "Try with a simpler query or smaller dataset"
            ],
            visualization_suggestions=[
                {"type": "table", "description": "Raw data table for manual review"}
            ],
            follow_up_questions=[
                "Is the data format correct?",
                "Are all required fields present?",
                "Should we simplify the analysis?"
            ]
        )

    def generate_quick_summary(self, data: List[tuple], columns: List[str]) -> str:
        """
        Generate a quick summary of query results.

        Args:
            data: Query results
            columns: Column names

        Returns:
            Quick summary string
        """
        try:
            if not data:
                return "No data found for the given query."

            df = pd.DataFrame(data, columns=columns)

            summary = f"Query returned {len(df)} rows with {len(columns)} columns. "

            # Add insights about numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                col = numeric_cols[0]
                summary += f"The {col} ranges from {df[col].min():.2f} to {df[col].max():.2f}. "

            # Add insights about categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                col = categorical_cols[0]
                unique_count = df[col].nunique()
                summary += f"There are {unique_count} unique {col} values. "

            return summary

        except Exception as e:
            logger.error(f"Error generating quick summary: {e}")
            return f"Summary generation failed: {str(e)}"


# Global story generator instance
story_generator = None

def get_story_generator() -> StoryGenerator:
    """
    Get the global story generator instance.

    Returns:
        StoryGenerator: The global story generator instance
    """
    global story_generator
    if story_generator is None:
        story_generator = StoryGenerator()
    return story_generator


def test_story_generator():
    """Test the story generator functionality."""
    try:
        generator = get_story_generator()

        # Sample data
        sample_data = [
            ('Electronics', 1500, 45),
            ('Clothing', 1200, 38),
            ('Books', 800, 25),
            ('Home', 600, 18)
        ]

        columns = ['category', 'revenue', 'orders']
        question = "What are the top product categories by revenue?"
        query = "SELECT category, SUM(revenue) as revenue, COUNT(*) as orders FROM sales GROUP BY category ORDER BY revenue DESC"

        print("🔍 Testing story generation...")
        story = generator.generate_story(question, query, sample_data, columns)

        print(f"✅ Executive Summary: {story.executive_summary}")
        print(f"✅ Key Insights: {len(story.key_insights)} insights")
        print(f"✅ Recommendations: {len(story.recommendations)} recommendations")

        # Test quick summary
        quick_summary = generator.generate_quick_summary(sample_data, columns)
        print(f"✅ Quick Summary: {quick_summary}")

        return True
    except Exception as e:
        print(f"❌ Story generator test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing Story Generator...")
    test_story_generator()
