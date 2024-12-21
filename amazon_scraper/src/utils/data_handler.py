import os
import json
import pandas as pd
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DataHandler:
    def __init__(self):
        self.data_dir = self._create_data_directory()
        
    def _create_data_directory(self):
        """Create directory structure for data storage"""
        base_dir = os.path.join(os.getcwd(), 'data')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_dir = os.path.join(base_dir, f'scrape_{timestamp}')
        
        # Create directories if they don't exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(os.path.join(data_dir, 'json'), exist_ok=True)
        os.makedirs(os.path.join(data_dir, 'csv'), exist_ok=True)
        
        return data_dir
        
    def save_data(self, data, category, format='both'):
        """Save scraped data in specified format(s)"""
        try:
            if not data:
                logger.warning(f"No data to save for category: {category}")
                return
                
            # Clean category name for filename
            category_clean = category.lower().replace(' ', '_')
            
            if format in ['csv', 'both']:
                csv_path = os.path.join(self.data_dir, 'csv', f'{category_clean}.csv')
                df = pd.DataFrame(data)
                df.to_csv(csv_path, index=False)
                logger.info(f"Data saved to CSV: {csv_path}")
                
            if format in ['json', 'both']:
                json_path = os.path.join(self.data_dir, 'json', f'{category_clean}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                logger.info(f"Data saved to JSON: {json_path}")
                
        except Exception as e:
            logger.error(f"Error saving data for {category}: {str(e)}") 