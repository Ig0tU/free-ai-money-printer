#!/usr/bin/env python3
import os
import sys
import json
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from ai_model_handler import AIModelHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pump_fun_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CryptoAnalyzer:
    def __init__(self):
        self.ai_handler = AIModelHandler()
        self.results_dir = Path("analysis_results")
        self.results_dir.mkdir(exist_ok=True)

    def analyze_token(self, token_data):
        """
        Analyze a token using AI model insights.
        
        Args:
            token_data (dict): Token information including metrics and social data
            
        Returns:
            dict: Analysis results including AI insights and risk assessment
        """
        try:
            # Prepare the analysis prompt
            prompt = self._create_analysis_prompt(token_data)
            
            # Get AI insights
            ai_response = self.ai_handler.call_model(prompt)
            
            # Process and structure the response
            analysis_result = self._process_ai_response(ai_response, token_data)
            
            # Save the analysis
            self._save_analysis(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Token analysis failed: {e}")
            raise

    def _create_analysis_prompt(self, token_data):
        """Create a detailed prompt for the AI model."""
        prompt = f"""
        Analyze the following cryptocurrency token data and provide insights:

        Token Information:
        - Name: {token_data.get('name', 'Unknown')}
        - Symbol: {token_data.get('symbol', 'Unknown')}
        - Current Price: {token_data.get('price', 'Unknown')}
        - Market Cap: {token_data.get('market_cap', 'Unknown')}
        - 24h Volume: {token_data.get('volume_24h', 'Unknown')}
        
        Social Metrics:
        - Twitter Mentions: {token_data.get('twitter_mentions', 'Unknown')}
        - Telegram Members: {token_data.get('telegram_members', 'Unknown')}
        - Reddit Subscribers: {token_data.get('reddit_subscribers', 'Unknown')}

        Please provide:
        1. Overall risk assessment (High/Medium/Low)
        2. Key technical indicators and their implications
        3. Social sentiment analysis
        4. Potential red flags or concerns
        5. Investment considerations and recommendations
        """
        return prompt

    def _process_ai_response(self, ai_response, token_data):
        """Process and structure the AI model's response."""
        # Extract the main content from the AI response
        if isinstance(ai_response, dict):
            analysis_text = ai_response.get('generated_text', '') or ai_response.get('text', '')
        else:
            analysis_text = str(ai_response)

        # Structure the result
        return {
            'timestamp': datetime.now().isoformat(),
            'token_data': token_data,
            'ai_analysis': analysis_text,
            'model_used': os.getenv('MODEL_TYPE', 'unknown')
        }

    def _save_analysis(self, analysis_result):
        """Save the analysis results to a JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.results_dir / f"analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        logger.info(f"Analysis saved to {filename}")

    def batch_analyze(self, tokens_list):
        """
        Analyze multiple tokens in batch.
        
        Args:
            tokens_list (list): List of token data dictionaries
            
        Returns:
            list: List of analysis results
        """
        results = []
        for token in tokens_list:
            try:
                result = self.analyze_token(token)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze token {token.get('symbol', 'Unknown')}: {e}")
                continue
        return results

def main():
    """Main execution function."""
    try:
        # Sample token data for testing
        sample_tokens = [
            {
                'name': 'Sample Token 1',
                'symbol': 'ST1',
                'price': '0.00123',
                'market_cap': '1000000',
                'volume_24h': '50000',
                'twitter_mentions': '1500',
                'telegram_members': '5000',
                'reddit_subscribers': '2000'
            },
            {
                'name': 'Sample Token 2',
                'symbol': 'ST2',
                'price': '0.05678',
                'market_cap': '5000000',
                'volume_24h': '250000',
                'twitter_mentions': '3000',
                'telegram_members': '10000',
                'reddit_subscribers': '4500'
            }
        ]

        # Initialize the analyzer
        analyzer = CryptoAnalyzer()
        
        # Run analysis
        logger.info("Starting batch analysis...")
        results = analyzer.batch_analyze(sample_tokens)
        
        # Print summary
        print("\nAnalysis Summary:")
        print("-" * 50)
        for result in results:
            print(f"\nToken: {result['token_data']['symbol']}")
            print(f"Analysis Timestamp: {result['timestamp']}")
            print("\nAI Analysis:")
            print(result['ai_analysis'])
            print("-" * 50)

    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
