from Scrape import scrapeCars
from Clean import cleaning
import os
import pandas as pd




dirtyData = scrapeCars()
print(len(dirtyData))
cleanData = cleaning(dirtyData)


### TIL EXCEL ###

# Specify the file name and location on the desktop
file_name = "car_data.xlsx"
desktop_path = "/Users/jeppeandersson/Desktop"
file_path = os.path.join(desktop_path, file_name)

# Save the DataFrame to an Excel file
cleanData.to_excel(file_path, index=False)
print(f"Excel file saved to: {file_path}")


