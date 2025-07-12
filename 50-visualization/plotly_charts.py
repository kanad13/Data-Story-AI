"""
Plotly chart generation utilities for data visualization.

This module provides functions to create various types of charts and visualizations
using Plotly based on SQL query results.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlotlyChartGenerator:
    """
    Generates Plotly charts from SQL query results.
    """
    
    def __init__(self):
        """Initialize the chart generator."""
        self.default_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        self.chart_config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
        }
    
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
                logger.warning(f"Column mismatch: expected {len(columns)}, got {actual_cols}. Auto-fixing...")
                
                if len(columns) < actual_cols:
                    # Add missing column names
                    columns = columns + [f'col_{i}' for i in range(len(columns), actual_cols)]
                elif len(columns) > actual_cols:
                    # Truncate extra column names  
                    columns = columns[:actual_cols]
            
            return pd.DataFrame(data, columns=columns)
            
        except Exception as e:
            logger.error(f"Error creating safe DataFrame: {e}")
            # Ultimate fallback: create generic DataFrame
            if data and len(data) > 0:
                actual_cols = len(data[0])
                fallback_columns = [f'column_{i+1}' for i in range(actual_cols)]
                return pd.DataFrame(data, columns=fallback_columns)
            else:
                return pd.DataFrame()
    
    def create_bar_chart(self, data: List[tuple], columns: List[str], title: str = "Bar Chart") -> go.Figure:
        """
        Create a bar chart from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Bar chart requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title(),
                showlegend=False
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return self._create_error_chart(f"Error creating bar chart: {e}")
    
    def create_line_chart(self, data: List[tuple], columns: List[str], title: str = "Line Chart") -> go.Figure:
        """
        Create a line chart from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Line chart requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.line(
                df, 
                x=x_col, 
                y=y_col,
                title=title,
                markers=True
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title()
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return self._create_error_chart(f"Error creating line chart: {e}")
    
    def create_pie_chart(self, data: List[tuple], columns: List[str], title: str = "Pie Chart") -> go.Figure:
        """
        Create a pie chart from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Pie chart requires at least 2 columns")
            
            names_col = df.columns[0]
            values_col = df.columns[1]
            
            fig = px.pie(
                df, 
                names=names_col, 
                values=values_col,
                title=title,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return fig
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            return self._create_error_chart(f"Error creating pie chart: {e}")
    
    def create_scatter_plot(self, data: List[tuple], columns: List[str], title: str = "Scatter Plot") -> go.Figure:
        """
        Create a scatter plot from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Scatter plot requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            # Use third column for color if available
            color_col = df.columns[2] if len(df.columns) > 2 else None
            
            fig = px.scatter(
                df, 
                x=x_col, 
                y=y_col,
                color=color_col,
                title=title,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title()
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            return self._create_error_chart(f"Error creating scatter plot: {e}")
    
    def create_histogram(self, data: List[tuple], columns: List[str], title: str = "Histogram") -> go.Figure:
        """
        Create a histogram from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = pd.DataFrame(data, columns=columns)
            
            if len(columns) < 1:
                raise ValueError("Histogram requires at least 1 column")
            
            x_col = columns[0]
            
            fig = px.histogram(
                df, 
                x=x_col,
                title=title,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title='Count'
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            return self._create_error_chart(f"Error creating histogram: {e}")
    
    def create_heatmap(self, data: List[tuple], columns: List[str], title: str = "Heatmap") -> go.Figure:
        """
        Create a heatmap from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = pd.DataFrame(data, columns=columns)
            
            if len(columns) < 3:
                raise ValueError("Heatmap requires at least 3 columns")
            
            # Pivot the data for heatmap
            pivot_df = df.pivot(index=columns[0], columns=columns[1], values=columns[2])
            
            fig = px.imshow(
                pivot_df,
                title=title,
                aspect="auto",
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                xaxis_title=columns[1].replace('_', ' ').title(),
                yaxis_title=columns[0].replace('_', ' ').title()
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return self._create_error_chart(f"Error creating heatmap: {e}")
    
    def create_violin_plot(self, data: List[tuple], columns: List[str], title: str = "Violin Plot") -> go.Figure:
        """
        Create a violin plot from query results for distribution analysis.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Violin plot requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.violin(
                df, 
                x=x_col, 
                y=y_col,
                title=title,
                box=True,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title()
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating violin plot: {e}")
            return self._create_error_chart(f"Error creating violin plot: {e}")
    
    def create_funnel_chart(self, data: List[tuple], columns: List[str], title: str = "Funnel Chart") -> go.Figure:
        """
        Create a funnel chart for conversion analysis.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Funnel chart requires at least 2 columns")
            
            names_col = df.columns[0]
            values_col = df.columns[1]
            
            fig = go.Figure(go.Funnel(
                y=df[names_col],
                x=df[values_col],
                textinfo="value+percent initial"
            ))
            
            fig.update_layout(
                title=title,
                font_size=12
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating funnel chart: {e}")
            return self._create_error_chart(f"Error creating funnel chart: {e}")
    
    def create_waterfall_chart(self, data: List[tuple], columns: List[str], title: str = "Waterfall Chart") -> go.Figure:
        """
        Create a waterfall chart for breakdown analysis.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Waterfall chart requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = go.Figure(go.Waterfall(
                name="",
                orientation="v",
                measure=["relative"] * (len(df) - 1) + ["total"],
                x=df[x_col],
                y=df[y_col],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title=title,
                showlegend=False
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating waterfall chart: {e}")
            return self._create_error_chart(f"Error creating waterfall chart: {e}")
    
    def create_statistical_summary_chart(self, data: List[tuple], columns: List[str], title: str = "Statistical Summary") -> go.Figure:
        """
        Create a statistical summary visualization with multiple metrics.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = pd.DataFrame(data, columns=columns)
            
            # Create subplots for multiple statistical views
            from plotly.subplots import make_subplots
            
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=("Distribution", "Box Plot", "Summary Stats", "Outliers"),
                specs=[[{"type": "scatter"}, {"type": "scatter"}],
                       [{"type": "table"}, {"type": "scatter"}]]
            )
            
            # Assume first numeric column for analysis
            numeric_col = None
            for col in columns:
                if df[col].dtype in ['int64', 'float64']:
                    numeric_col = col
                    break
            
            if numeric_col:
                values = df[numeric_col]
                
                # Distribution histogram
                fig.add_trace(
                    go.Histogram(x=values, name="Distribution"),
                    row=1, col=1
                )
                
                # Box plot
                fig.add_trace(
                    go.Box(y=values, name="Box Plot"),
                    row=1, col=2
                )
                
                # Summary statistics table
                stats = {
                    'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q1', 'Q3'],
                    'Value': [
                        f"{values.mean():.2f}",
                        f"{values.median():.2f}",
                        f"{values.std():.2f}",
                        f"{values.min():.2f}",
                        f"{values.max():.2f}",
                        f"{values.quantile(0.25):.2f}",
                        f"{values.quantile(0.75):.2f}"
                    ]
                }
                
                fig.add_trace(
                    go.Table(
                        header=dict(values=list(stats.keys())),
                        cells=dict(values=list(stats.values()))
                    ),
                    row=2, col=1
                )
                
                # Outliers scatter plot
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                outliers = values[(values < Q1 - 1.5*IQR) | (values > Q3 + 1.5*IQR)]
                
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(outliers))),
                        y=outliers,
                        mode='markers',
                        name="Outliers",
                        marker=dict(color='red', size=8)
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(title=title, height=600)
            return fig
            
        except Exception as e:
            logger.error(f"Error creating statistical summary: {e}")
            return self._create_error_chart(f"Error creating statistical summary: {e}")

    def create_box_plot(self, data: List[tuple], columns: List[str], title: str = "Box Plot") -> go.Figure:
        """
        Create a box plot from query results.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = self._create_safe_dataframe(data, columns)
            
            if len(df.columns) < 2:
                raise ValueError("Box plot requires at least 2 columns")
            
            x_col = df.columns[0]
            y_col = df.columns[1]
            
            fig = px.box(
                df, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.default_colors
            )
            
            fig.update_layout(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title()
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating box plot: {e}")
            return self._create_error_chart(f"Error creating box plot: {e}")
    
    def auto_generate_chart(self, data: List[tuple], columns: List[str], title: str = "Auto Chart") -> go.Figure:
        """
        Automatically generate the most appropriate chart based on data characteristics and query context.
        
        Args:
            data: List of tuples containing query results
            columns: List of column names
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        try:
            df = pd.DataFrame(data, columns=columns)
            
            # Analyze title and column names for statistical indicators
            title_lower = title.lower()
            columns_lower = [col.lower() for col in columns]
            
            # Check for statistical analysis keywords
            statistical_keywords = ['standard deviation', 'std dev', 'variance', 'coefficient', 'percentile', 
                                 'quartile', 'distribution', 'outlier', 'correlation', 'volatility']
            conversion_keywords = ['conversion', 'funnel', 'pipeline', 'flow']
            breakdown_keywords = ['breakdown', 'waterfall', 'contribution', 'decomposition']
            
            is_statistical = any(keyword in title_lower for keyword in statistical_keywords)
            is_conversion = any(keyword in title_lower for keyword in conversion_keywords)
            is_breakdown = any(keyword in title_lower for keyword in breakdown_keywords)
            
            # Statistical analysis - use advanced visualizations
            if is_statistical and len(columns) >= 2:
                # Check if we have statistical measures in column names
                stat_cols = [col for col in columns_lower if any(stat in col for stat in ['std', 'deviation', 'variance', 'coefficient'])]
                if stat_cols or 'distribution' in title_lower:
                    return self.create_statistical_summary_chart(data, columns, title)
                elif 'percentile' in title_lower or 'quartile' in title_lower:
                    return self.create_box_plot(data, columns, title)
                else:
                    return self.create_violin_plot(data, columns, title)
            
            # Conversion analysis
            elif is_conversion and len(columns) >= 2:
                return self.create_funnel_chart(data, columns, title)
            
            # Breakdown analysis
            elif is_breakdown and len(columns) >= 2:
                return self.create_waterfall_chart(data, columns, title)
            
            # Standard logic for non-statistical queries
            elif len(columns) == 1:
                # Single column - histogram
                return self.create_histogram(data, columns, title)
            elif len(columns) == 2:
                # Two columns - determine best chart type
                col1_dtype = df[columns[0]].dtype
                col2_dtype = df[columns[1]].dtype
                
                # If first column is categorical and second is numeric
                if col1_dtype == 'object' and pd.api.types.is_numeric_dtype(col2_dtype):
                    # Check if we have few categories (good for pie chart)
                    if len(df[columns[0]].unique()) <= 8:
                        return self.create_pie_chart(data, columns, title)
                    else:
                        return self.create_bar_chart(data, columns, title)
                
                # If both are numeric
                elif pd.api.types.is_numeric_dtype(col1_dtype) and pd.api.types.is_numeric_dtype(col2_dtype):
                    return self.create_scatter_plot(data, columns, title)
                
                # If first column looks like dates
                elif 'date' in columns[0].lower() or 'time' in columns[0].lower():
                    return self.create_line_chart(data, columns, title)
                
                # Default to bar chart
                else:
                    return self.create_bar_chart(data, columns, title)
            
            # Multiple columns with specific patterns
            elif len(columns) >= 3:
                # Check for heatmap patterns (3+ columns with categorical x numeric)
                if (df[columns[0]].dtype == 'object' and 
                    df[columns[1]].dtype == 'object' and 
                    pd.api.types.is_numeric_dtype(df[columns[2]].dtype)):
                    return self.create_heatmap(data, columns, title)
                else:
                    # Default to bar chart with first two columns
                    return self.create_bar_chart(data, columns[:2], title)
            
            else:
                # Fallback to bar chart
                return self.create_bar_chart(data, columns[:2], title)
                
        except Exception as e:
            logger.error(f"Error auto-generating chart: {e}")
            return self._create_error_chart(f"Error auto-generating chart: {e}")
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """
        Create an error chart to display when chart generation fails.
        
        Args:
            error_message: Error message to display
            
        Returns:
            Plotly Figure object with error message
        """
        fig = go.Figure()
        fig.add_annotation(
            text=f"❌ {error_message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Chart Generation Error",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    def create_dashboard(self, data_sets: List[Dict[str, Any]], title: str = "Dashboard") -> go.Figure:
        """
        Create a dashboard with multiple charts.
        
        Args:
            data_sets: List of datasets, each with 'data', 'columns', 'title', and 'chart_type'
            title: Dashboard title
            
        Returns:
            Plotly Figure object with subplots
        """
        try:
            num_charts = len(data_sets)
            if num_charts == 0:
                return self._create_error_chart("No data provided for dashboard")
            
            # Calculate subplot layout
            if num_charts == 1:
                rows, cols = 1, 1
            elif num_charts == 2:
                rows, cols = 1, 2
            elif num_charts <= 4:
                rows, cols = 2, 2
            else:
                rows, cols = 3, 2
                
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=[ds.get('title', f'Chart {i+1}') for i, ds in enumerate(data_sets[:rows*cols])]
            )
            
            for i, ds in enumerate(data_sets[:rows*cols]):
                row = i // cols + 1
                col = i % cols + 1
                
                # Create individual chart
                chart_type = ds.get('chart_type', 'bar')
                data = ds.get('data', [])
                columns = ds.get('columns', [])
                
                if chart_type == 'bar' and len(columns) >= 2:
                    df = pd.DataFrame(data, columns=columns)
                    fig.add_trace(
                        go.Bar(x=df[columns[0]], y=df[columns[1]], name=ds.get('title', f'Chart {i+1}')),
                        row=row, col=col
                    )
                elif chart_type == 'line' and len(columns) >= 2:
                    df = pd.DataFrame(data, columns=columns)
                    fig.add_trace(
                        go.Scatter(x=df[columns[0]], y=df[columns[1]], mode='lines+markers', name=ds.get('title', f'Chart {i+1}')),
                        row=row, col=col
                    )
                elif chart_type == 'pie' and len(columns) >= 2:
                    df = pd.DataFrame(data, columns=columns)
                    fig.add_trace(
                        go.Pie(labels=df[columns[0]], values=df[columns[1]], name=ds.get('title', f'Chart {i+1}')),
                        row=row, col=col
                    )
            
            fig.update_layout(
                title=title,
                showlegend=False,
                height=600 if rows > 1 else 400
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            return self._create_error_chart(f"Error creating dashboard: {e}")


# Global chart generator instance
chart_generator = PlotlyChartGenerator()

def get_chart_generator() -> PlotlyChartGenerator:
    """
    Get the global chart generator instance.
    
    Returns:
        PlotlyChartGenerator: The global chart generator instance
    """
    return chart_generator


def suggest_chart_type(data: List[tuple], columns: List[str]) -> str:
    """
    Suggest the best chart type for given data.
    
    Args:
        data: List of tuples containing query results
        columns: List of column names
        
    Returns:
        Suggested chart type
    """
    try:
        if not data or not columns:
            return "bar"
        
        df = pd.DataFrame(data, columns=columns)
        
        if len(columns) == 1:
            return "histogram"
        elif len(columns) == 2:
            col1_dtype = df[columns[0]].dtype
            col2_dtype = df[columns[1]].dtype
            
            if col1_dtype == 'object' and pd.api.types.is_numeric_dtype(col2_dtype):
                if len(df[columns[0]].unique()) <= 8:
                    return "pie"
                else:
                    return "bar"
            elif pd.api.types.is_numeric_dtype(col1_dtype) and pd.api.types.is_numeric_dtype(col2_dtype):
                return "scatter"
            elif 'date' in columns[0].lower() or 'time' in columns[0].lower():
                return "line"
            else:
                return "bar"
        else:
            return "bar"
    except Exception as e:
        logger.error(f"Error suggesting chart type: {e}")
        return "bar"


if __name__ == "__main__":
    # Test the chart generator
    print("Testing Plotly Chart Generator...")
    
    # Sample data
    sample_data = [
        ('Electronics', 1500, 45),
        ('Clothing', 1200, 38),
        ('Books', 800, 25),
        ('Home', 600, 18)
    ]
    
    columns = ['category', 'revenue', 'orders']
    
    generator = get_chart_generator()
    
    # Test different chart types
    fig = generator.auto_generate_chart(sample_data, columns, "Sample Chart")
    print(f"✅ Auto-generated chart type: {type(fig)}")
    
    suggested_type = suggest_chart_type(sample_data, columns)
    print(f"✅ Suggested chart type: {suggested_type}")
    
    print("✅ Chart generator tests completed")