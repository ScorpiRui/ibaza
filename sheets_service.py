import os
import logging
from typing import List, Dict, Any, Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logger = logging.getLogger(__name__)

# Google Sheets API configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'ibaza-sheet-api-0455687921f7.json'
SPREADSHEET_ID = '1Rw3MW613RW6_4zKgtBWWkPg9bEoyvG68OLTCFbkgTAg'

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets service"""
        try:
            self.creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=self.creds)
            self.sheet = self.service.spreadsheets()
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            raise
    
    def create_template(self) -> bool:
        """Create the initial template in Google Sheets"""
        try:
            # Define the template structure with all iPhone models from iPhone 11 to iPhone 16 (excluding mini versions)
            template_data = [
                ['Model', 'Memory (GB)', 'Ideal($)', 'Yaxshi($)', 'Ortacha($)', 'Notes'],
                # iPhone 11 series (2019)
                ['iPhone 11 Pro Max', '64', '0', '0', '0', ''],
                ['iPhone 11 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 11 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 11 Pro', '64', '0', '0', '0', ''],
                ['iPhone 11 Pro', '256', '0', '0', '0', ''],
                ['iPhone 11 Pro', '512', '0', '0', '0', ''],
                ['iPhone 11', '64', '0', '0', '0', ''],
                ['iPhone 11', '128', '0', '0', '0', ''],
                ['iPhone 11', '256', '0', '0', '0', ''],
                # iPhone 12 series (2020)
                ['iPhone 12 Pro Max', '128', '0', '0', '0', ''],
                ['iPhone 12 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 12 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 12 Pro', '128', '0', '0', '0', ''],
                ['iPhone 12 Pro', '256', '0', '0', '0', ''],
                ['iPhone 12 Pro', '512', '0', '0', '0', ''],
                ['iPhone 12', '64', '0', '0', '0', ''],
                ['iPhone 12', '128', '0', '0', '0', ''],
                ['iPhone 12', '256', '0', '0', '0', ''],
                # iPhone 13 series (2021)
                ['iPhone 13 Pro Max', '128', '0', '0', '0', ''],
                ['iPhone 13 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 13 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 13 Pro Max', '1024', '0', '0', '0', ''],
                ['iPhone 13 Pro', '128', '0', '0', '0', ''],
                ['iPhone 13 Pro', '256', '0', '0', '0', ''],
                ['iPhone 13 Pro', '512', '0', '0', '0', ''],
                ['iPhone 13 Pro', '1024', '0', '0', '0', ''],
                ['iPhone 13', '128', '0', '0', '0', ''],
                ['iPhone 13', '256', '0', '0', '0', ''],
                ['iPhone 13', '512', '0', '0', '0', ''],
                # iPhone 14 series (2022)
                ['iPhone 14 Pro Max', '128', '0', '0', '0', ''],
                ['iPhone 14 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 14 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 14 Pro Max', '1024', '0', '0', '0', ''],
                ['iPhone 14 Pro', '128', '0', '0', '0', ''],
                ['iPhone 14 Pro', '256', '0', '0', '0', ''],
                ['iPhone 14 Pro', '512', '0', '0', '0', ''],
                ['iPhone 14 Pro', '1024', '0', '0', '0', ''],
                ['iPhone 14 Plus', '128', '0', '0', '0', ''],
                ['iPhone 14 Plus', '256', '0', '0', '0', ''],
                ['iPhone 14 Plus', '512', '0', '0', '0', ''],
                ['iPhone 14', '128', '0', '0', '0', ''],
                ['iPhone 14', '256', '0', '0', '0', ''],
                ['iPhone 14', '512', '0', '0', '0', ''],
                # iPhone 15 series (2023)
                ['iPhone 15 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 15 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 15 Pro Max', '1024', '0', '0', '0', ''],
                ['iPhone 15 Pro', '128', '0', '0', '0', ''],
                ['iPhone 15 Pro', '256', '0', '0', '0', ''],
                ['iPhone 15 Pro', '512', '0', '0', '0', ''],
                ['iPhone 15 Pro', '1024', '0', '0', '0', ''],
                ['iPhone 15 Plus', '128', '0', '0', '0', ''],
                ['iPhone 15 Plus', '256', '0', '0', '0', ''],
                ['iPhone 15 Plus', '512', '0', '0', '0', ''],
                ['iPhone 15', '128', '0', '0', '0', ''],
                ['iPhone 15', '256', '0', '0', '0', ''],
                ['iPhone 15', '512', '0', '0', '0', ''],
                # iPhone 16 series (2024) - Placeholder for future models
                ['iPhone 16 Pro Max', '256', '0', '0', '0', ''],
                ['iPhone 16 Pro Max', '512', '0', '0', '0', ''],
                ['iPhone 16 Pro Max', '1024', '0', '0', '0', ''],
                ['iPhone 16 Pro', '128', '0', '0', '0', ''],
                ['iPhone 16 Pro', '256', '0', '0', '0', ''],
                ['iPhone 16 Pro', '512', '0', '0', '0', ''],
                ['iPhone 16 Pro', '1024', '0', '0', '0', ''],
                ['iPhone 16 Plus', '128', '0', '0', '0', ''],
                ['iPhone 16 Plus', '256', '0', '0', '0', ''],
                ['iPhone 16 Plus', '512', '0', '0', '0', ''],
                ['iPhone 16', '128', '0', '0', '0', ''],
                ['iPhone 16', '256', '0', '0', '0', ''],
                ['iPhone 16', '512', '0', '0', '0', '']
            ]
            
            # Clear existing data and write template
            range_name = 'A1:F150'  # Increased range to accommodate all models
            self.sheet.values().clear(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            # Write template data
            body = {
                'values': template_data
            }
            
            result = self.sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Template created successfully: {result.get('updatedCells')} cells updated")
            return True
            
        except HttpError as error:
            logger.error(f"Failed to create template: {error}")
            return False
    
    def get_all_models(self) -> List[Dict[str, Any]]:
        """Get all models from Google Sheets"""
        try:
            range_name = 'A2:F150'  # Increased range to accommodate all models
            result = self.sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            models = {}
            
            for row in values:
                if len(row) >= 5 and row[0] and row[1]:  # Ensure model and memory exist
                    model_name = row[0].strip()
                    memory = row[1].strip()
                    
                    # Convert memory to integer (handle 1TB = 1024GB)
                    try:
                        if memory.lower() == '1tb':
                            memory_int = 1024
                        else:
                            memory_int = int(memory)
                    except ValueError:
                        continue
                    
                    # Parse prices
                    try:
                        new_price = int(row[2]) if row[2] else 0
                        good_price = int(row[3]) if row[3] else 0
                        fair_price = int(row[4]) if row[4] else 0
                    except ValueError:
                        continue
                    
                    # Group by model name
                    if model_name not in models:
                        models[model_name] = {
                            'name': model_name,
                            'memories': [],
                            'prices': {}
                        }
                    
                    # Add memory if not already present
                    if memory_int not in models[model_name]['memories']:
                        models[model_name]['memories'].append(memory_int)
                    
                    # Add prices
                    models[model_name]['prices'][str(memory_int)] = {
                        'new': new_price,
                        'good': good_price,
                        'fair': fair_price
                    }
            
            # Convert to list and sort memories
            models_list = []
            for model_name, model_data in models.items():
                model_data['memories'].sort()
                models_list.append(model_data)
            
            logger.info(f"Retrieved {len(models_list)} models from Google Sheets")
            return models_list
            
        except HttpError as error:
            logger.error(f"Failed to get models from Google Sheets: {error}")
            return []
    
    def add_model(self, model_name: str, memory: int, new_price: int, good_price: int, fair_price: int) -> bool:
        """Add a new model row to Google Sheets"""
        try:
            # Convert memory to display format
            memory_display = '1TB' if memory == 1024 else f'{memory}'
            
            # Prepare row data
            row_data = [
                model_name,
                memory_display,
                str(new_price),
                str(good_price),
                str(fair_price),
                ''  # Notes column
            ]
            
            # Find the next empty row
            range_name = 'A:A'
            result = self.sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            next_row = len(values) + 1
            
            # Append the new row
            range_name = f'A{next_row}'
            body = {
                'values': [row_data]
            }
            
            result = self.sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Model added successfully: {model_name} {memory_display}")
            return True
            
        except HttpError as error:
            logger.error(f"Failed to add model: {error}")
            return False
    
    def update_model_price(self, model_name: str, memory: int, new_price: int, good_price: int, fair_price: int) -> bool:
        """Update price for existing model"""
        try:
            # Convert memory to display format
            memory_display = '1TB' if memory == 1024 else f'{memory}'
            
            # Find the row with this model and memory
            range_name = 'A2:F100'
            result = self.sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            for i, row in enumerate(values):
                if len(row) >= 2 and row[0].strip() == model_name and row[1].strip() == memory_display:
                    # Found the row, update prices
                    row_index = i + 2  # +2 because we start from A2 and i is 0-based
                    
                    # Update prices
                    range_name = f'C{row_index}:E{row_index}'
                    body = {
                        'values': [[str(new_price), str(good_price), str(fair_price)]]
                    }
                    
                    result = self.sheet.values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=range_name,
                        valueInputOption='RAW',
                        body=body
                    ).execute()
                    
                    logger.info(f"Model price updated successfully: {model_name} {memory_display}")
                    return True
            
            logger.warning(f"Model not found: {model_name} {memory_display}")
            return False
            
        except HttpError as error:
            logger.error(f"Failed to update model price: {error}")
            return False
    
    def delete_model(self, model_name: str, memory: int) -> bool:
        """Delete a model row from Google Sheets"""
        try:
            # Convert memory to display format
            memory_display = '1TB' if memory == 1024 else f'{memory}'
            
            # Find the row with this model and memory
            range_name = 'A2:F100'
            result = self.sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            for i, row in enumerate(values):
                if len(row) >= 2 and row[0].strip() == model_name and row[1].strip() == memory_display:
                    # Found the row, delete it
                    row_index = i + 2  # +2 because we start from A2 and i is 0-based
                    
                    # Delete the row
                    request = {
                        'deleteDimension': {
                            'range': {
                                'sheetId': 0,  # Assuming first sheet
                                'dimension': 'ROWS',
                                'startIndex': row_index - 1,  # 0-based index
                                'endIndex': row_index
                            }
                        }
                    }
                    
                    self.sheet.batchUpdate(
                        spreadsheetId=SPREADSHEET_ID,
                        body={'requests': [request]}
                    ).execute()
                    
                    logger.info(f"Model deleted successfully: {model_name} {memory_display}")
                    return True
            
            logger.warning(f"Model not found: {model_name} {memory_display}")
            return False
            
        except HttpError as error:
            logger.error(f"Failed to delete model: {error}")
            return False

# Global instance
sheets_service = None

def get_sheets_service() -> GoogleSheetsService:
    """Get or create Google Sheets service instance"""
    global sheets_service
    if sheets_service is None:
        sheets_service = GoogleSheetsService()
    return sheets_service 