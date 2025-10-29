"""
Visualizer Module
Creates interactive visualizations for predictions
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List


class Visualizer:
    """Create visualizations for prediction results"""
    
    def __init__(self):
        """Initialize Visualizer"""
        self.colors = {
            'ALLOW': '#28a745',
            'MONITOR': '#ffc107',
            'BLOCK': '#dc3545',
            'Normal': '#17a2b8',
            'Anomaly': '#fd7e14'
        }
    
    def create_action_distribution_chart(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create pie chart showing action distribution
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Plotly figure
        """
        action_counts = results_df['action'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=action_counts.index,
            values=action_counts.values,
            hole=0.4,
            marker=dict(colors=[self.colors.get(a, '#999') for a in action_counts.index]),
            textinfo='label+percent',
            textfont_size=14
        )])
        
        fig.update_layout(
            title='Action Distribution',
            title_font_size=18,
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_trust_score_distribution(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create histogram of trust scores
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=results_df['trust_score'],
            nbinsx=30,
            name='Trust Score',
            marker_color='#1f77b4',
            opacity=0.7
        ))
        
        # Add threshold lines
        fig.add_vline(x=33, line_dash="dash", line_color="red", 
                     annotation_text="Low/Medium", annotation_position="top")
        fig.add_vline(x=66, line_dash="dash", line_color="green",
                     annotation_text="Medium/High", annotation_position="top")
        
        fig.update_layout(
            title='Trust Score Distribution',
            title_font_size=18,
            xaxis_title='Trust Score',
            yaxis_title='Count',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_trust_score_by_prediction(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create box plot of trust scores by prediction
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for pred_type in results_df['prediction'].unique():
            subset = results_df[results_df['prediction'] == pred_type]
            fig.add_trace(go.Box(
                y=subset['trust_score'],
                name=pred_type,
                marker_color=self.colors.get(pred_type, '#999'),
                boxmean='sd'
            ))
        
        fig.update_layout(
            title='Trust Scores by Prediction Type',
            title_font_size=18,
            yaxis_title='Trust Score',
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_confidence_distribution(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create histogram of confidence scores
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Plotly figure
        """
        fig = px.histogram(
            results_df,
            x='confidence',
            color='prediction',
            nbins=30,
            title='Confidence Distribution by Prediction',
            color_discrete_map=self.colors
        )
        
        fig.update_layout(
            title_font_size=18,
            xaxis_title='Confidence',
            yaxis_title='Count',
            height=400
        )
        
        return fig
    
    def create_trust_meter(self, trust_score: float) -> go.Figure:
        """
        Create gauge chart for trust score
        
        Args:
            trust_score: Trust score (0-100)
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=trust_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Trust Score", 'font': {'size': 24}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 33], 'color': '#ffcccc'},
                    {'range': [33, 66], 'color': '#fff8cc'},
                    {'range': [66, 100], 'color': '#ccffcc'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig
    
    def create_confusion_matrix_heatmap(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create confusion matrix heatmap (if true labels available)
        
        Args:
            results_df: DataFrame with prediction results and true labels
            
        Returns:
            Plotly figure or None
        """
        if 'true_class' not in results_df.columns:
            return None
        
        from sklearn.metrics import confusion_matrix
        
        # Create confusion matrix
        cm = confusion_matrix(
            results_df['true_class'],
            results_df['prediction'],
            labels=['Normal', 'Anomaly']
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Normal', 'Anomaly'],
            y=['Normal', 'Anomaly'],
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 16},
            colorscale='Blues',
            showscale=True
        ))
        
        fig.update_layout(
            title='Confusion Matrix',
            title_font_size=18,
            xaxis_title='Predicted',
            yaxis_title='Actual',
            height=400
        )
        
        return fig
    
    def create_summary_table(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create summary statistics table
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Summary DataFrame
        """
        summary = {
            'Metric': [
                'Total Predictions',
                'Normal Predictions',
                'Anomaly Predictions',
                'High Trust (Allow)',
                'Medium Trust (Monitor)',
                'Low Trust (Block)',
                'Avg Trust Score',
                'Avg Confidence'
            ],
            'Value': [
                len(results_df),
                len(results_df[results_df['prediction'] == 'Normal']),
                len(results_df[results_df['prediction'] == 'Anomaly']),
                len(results_df[results_df['action'] == 'ALLOW']),
                len(results_df[results_df['action'] == 'MONITOR']),
                len(results_df[results_df['action'] == 'BLOCK']),
                f"{results_df['trust_score'].mean():.2f}",
                f"{results_df['confidence'].mean():.4f}"
            ]
        }
        
        # Add accuracy if true labels available
        if 'true_class' in results_df.columns:
            accuracy = (results_df['correct'].sum() / len(results_df)) * 100
            summary['Metric'].append('Accuracy')
            summary['Value'].append(f"{accuracy:.2f}%")
        
        return pd.DataFrame(summary)
    
    def create_scatter_trust_vs_confidence(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Create scatter plot of trust score vs confidence
        
        Args:
            results_df: DataFrame with prediction results
            
        Returns:
            Plotly figure
        """
        fig = px.scatter(
            results_df,
            x='confidence',
            y='trust_score',
            color='action',
            title='Trust Score vs Confidence',
            labels={'confidence': 'Confidence', 'trust_score': 'Trust Score'},
            color_discrete_map=self.colors,
            opacity=0.6
        )
        
        fig.update_layout(
            title_font_size=18,
            height=400
        )
        
        return fig
