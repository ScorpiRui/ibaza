# Google Sheets Price Management Guide

## Overview
The iBaza bot now uses Google Sheets for managing iPhone models and prices. This allows for easy price updates without needing to modify code.

## Google Sheets URL
🔗 **Sheet URL:** https://docs.google.com/spreadsheets/d/1Rw3MW613RW6_4zKgtBWWkPg9bEoyvG68OLTCFbkgTAg/edit?gid=0#gid=0

## Current Models Available
The sheet has been pre-populated with all iPhone models from iPhone 11 to iPhone 16 (excluding mini versions), organized chronologically:

### iPhone 11 Series (2019)
- iPhone 11 Pro Max (64GB, 256GB, 512GB)
- iPhone 11 Pro (64GB, 256GB, 512GB)
- iPhone 11 (64GB, 128GB, 256GB)

### iPhone 12 Series (2020)
- iPhone 12 Pro Max (128GB, 256GB, 512GB)
- iPhone 12 Pro (128GB, 256GB, 512GB)
- iPhone 12 (64GB, 128GB, 256GB)

### iPhone 13 Series (2021)
- iPhone 13 Pro Max (128GB, 256GB, 512GB, 1TB)
- iPhone 13 Pro (128GB, 256GB, 512GB, 1TB)
- iPhone 13 (128GB, 256GB, 512GB)

### iPhone 14 Series (2022)
- iPhone 14 Pro Max (128GB, 256GB, 512GB, 1TB)
- iPhone 14 Pro (128GB, 256GB, 512GB, 1TB)
- iPhone 14 Plus (128GB, 256GB, 512GB)
- iPhone 14 (128GB, 256GB, 512GB)

### iPhone 15 Series (2023)
- iPhone 15 Pro Max (256GB, 512GB, 1TB)
- iPhone 15 Pro (128GB, 256GB, 512GB, 1TB)
- iPhone 15 Plus (128GB, 256GB, 512GB)
- iPhone 15 (128GB, 256GB, 512GB)

### iPhone 16 Series (2024) - Placeholder
- iPhone 16 Pro Max (256GB, 512GB, 1TB)
- iPhone 16 Pro (128GB, 256GB, 512GB, 1TB)
- iPhone 16 Plus (128GB, 256GB, 512GB)
- iPhone 16 (128GB, 256GB, 512GB)

## Sheet Structure
The sheet has the following columns:
- **Model**: iPhone model name
- **Memory (GB)**: Storage capacity (64, 128, 256, 512, 1024 for 1TB)
- **Ideal($)**: Price for excellent condition (95%+ battery, no scratches)
- **Yaxshi($)**: Price for good condition (85-95% battery, some scratches)
- **Ortacha($)**: Price for fair condition (<85% battery, visible scratches)
- **Notes**: Additional notes (optional)

## How to Update Prices

### Step 1: Access the Sheet
1. Click the "📊 Google Sheets da narxlarni boshqarish" button in the admin panel
2. Or directly visit: https://docs.google.com/spreadsheets/d/1Rw3MW613RW6_4zKgtBWWkPg9bEoyvG68OLTCFbkgTAg/edit?gid=0#gid=0

### Step 2: Edit Prices
1. Find the model and memory combination you want to update
2. Enter the prices in USD for each condition:
   - **Ideal**: Excellent condition phones
   - **Yaxshi**: Good condition phones  
   - **Ortacha**: Fair condition phones

### Step 3: Save Changes
1. Changes are automatically saved in Google Sheets
2. Return to the bot admin panel
3. Click "🔄 Narxlarni yangilash" to sync changes to the bot

## Price Guidelines
- All prices should be in USD
- Prices should reflect current market conditions
- Consider factors like:
  - Phone age and generation
  - Storage capacity
  - Market demand
  - Local competition

## Adding New Models (iPhone 17+)
When new iPhone models are released:

1. Add new rows at the bottom of the sheet
2. Follow the existing naming pattern: "iPhone 17 Pro Max", "iPhone 17 Pro", etc.
3. Enter memory capacities (typically 128GB, 256GB, 512GB, 1TB for Pro models)
4. Set initial prices to 0 in columns C, D, E
5. Update the prices based on market research
6. Click "🔄 Narxlarni yangilash" in the bot

### Example for iPhone 17:
```
iPhone 17 Pro Max | 256 | 0 | 0 | 0 |
iPhone 17 Pro Max | 512 | 0 | 0 | 0 |
iPhone 17 Pro Max | 1024 | 0 | 0 | 0 |
iPhone 17 Pro | 128 | 0 | 0 | 0 |
iPhone 17 Pro | 256 | 0 | 0 | 0 |
iPhone 17 Pro | 512 | 0 | 0 | 0 |
iPhone 17 Pro | 1024 | 0 | 0 | 0 |
iPhone 17 Plus | 128 | 0 | 0 | 0 |
iPhone 17 Plus | 256 | 0 | 0 | 0 |
iPhone 17 Plus | 512 | 0 | 0 | 0 |
iPhone 17 | 128 | 0 | 0 | 0 |
iPhone 17 | 256 | 0 | 0 | 0 |
iPhone 17 | 512 | 0 | 0 | 0 |
```

## Important Notes
- ✅ All prices are currently set to $0 - you need to fill them in manually
- ✅ The bot will automatically sync with the sheet when you click "Refresh Prices"
- ✅ Changes are immediate after refreshing
- ✅ The sheet supports iPhone 11-16 series with placeholders for future models
- ✅ Mini versions are excluded as requested
- ✅ Models are organized chronologically for easy management
- ✅ Template is ready for iPhone 17+ models to be added easily

## Troubleshooting
- If prices don't update, try clicking "🔄 Narxlarni yangilash" again
- If you can't access the sheet, check your internet connection
- If the bot shows no models, ensure the sheet has the correct format
- For new models, ensure the naming follows the exact pattern (e.g., "iPhone 17 Pro Max")

## Support
For technical issues, contact the development team.
For price-related questions, use your business judgment based on market conditions. 