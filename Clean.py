import pandas as pd
import re
import os

dirtyData = pd.read_excel("dirty_car_data.xlsx")

def cleaning(dirtyData):
    dirtyData = dirtyData.drop(columns=['Co2'])

    # Drop duplicates and rows with NaN as it is only a handful of rows so no need to impute
    dirtyData = dirtyData.drop_duplicates().dropna()

    # Removing 'dage' from 'DageTilSalg' and converting to integer
    dirtyData['DageTilSalg'] = dirtyData['DageTilSalg'].str.extract('(\d+)').astype(int)


    # Extracting the year from 'Årstal'
    dirtyData['Årstal'] = dirtyData['Årstal'].str.extract('(\d{4})').astype(int)
    
    # Removing 'km' from 'Kilometertal' and converting to integer
    dirtyData['Kilometertal'] = dirtyData['Kilometertal'].str.replace('.', '').str.extract('(\d+)').astype(int)

    # Extracting Hæstekræfter
    dirtyData['Hestekræfter'] = dirtyData['Hestekræfter'].str.extract('(\d+) HK')


    # Replace 'El/Benzin' with 'Hybrid' in the 'Motor' column
    dirtyData['Brændstof'] = dirtyData['Motor'].str.replace('El/Benzin', 'Hybrid', regex=True)

    # Splitting 'Motor' into 'Motorstørrelse' and 'Brændstof'
    dirtyData['Motorstørrelse'] = dirtyData['Motor'].str.extract('(\d+\.\d+|\d+)L').astype(float)
    dirtyData['Brændstof'] = dirtyData['Motor'].str.extract('(Diesel|Benzin|El|Hybrid)', flags=re.IGNORECASE)
    # Filter out rows where 'Brændstof' is 'El'
    dirtyData = dirtyData[dirtyData['Brændstof'] != 'El']

    # Removing 'Km/L' from 'Km/L' and converting to float
    dirtyData['Km/L'] = dirtyData['Km/L'].str.replace(',', '.').str.extract('(\d+\.\d+)').astype(float)

    # Removing 'kr.' and converting 'Pris' to float
    dirtyData['Pris'] = dirtyData['Pris'].str.replace('kr.', '').str.replace('.', '').astype(float)
    total_nan_count = dirtyData.isna().sum()
    print("Step 8 Total number of NaN values in the DataFrame:", total_nan_count.sum())

    # You can drop the old 'Motor' column if it's no longer needed
    dirtyData = dirtyData.drop(columns=['Motor'])

    return dirtyData

file_name = "clean_car_data.xlsx"
current_directory = os.getcwd()
path = current_directory
file_path = os.path.join(path, file_name)

cleanData = cleaning(dirtyData)
cleanData.to_excel(file_path, index=False)
print(f"Excel file saved to: {file_path}")
