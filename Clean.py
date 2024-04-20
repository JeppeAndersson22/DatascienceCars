import pandas as pd
import re
######################
####### CLEANING #####
######################


def cleaning(dirtyData):

    # Removing 'dage' from 'DageTilSalg' and converting to integer
    dirtyData['DageTilSalg'] = dirtyData['DageTilSalg'].str.extract('(\d+)').astype(int)

    # Extracting the year from 'Årstal'
    dirtyData['Årstal'] = dirtyData['Årstal'].str.extract('(\d{4})').astype(int)

    # Removing 'km' from 'Kilometertal' and converting to integer
    dirtyData['Kilometertal'] = dirtyData['Kilometertal'].str.replace('.', '').str.extract('(\d+)').astype(int)

    # Extracting Hæstekræfter
    dirtyData['Hestekræfter'] = dirtyData['Hestekræfter'].str.extract('(\d+) HK').astype(int)

    # Replace 'El/Benzin' with 'Hybrid' in the 'Motor' column
    dirtyData['Brændstof'] = dirtyData['Motor'].str.replace('El/Benzin', 'Hybrid', regex=True)

    # Splitting 'Motor' into 'Motorstørrelse' and 'Brændstof'
    dirtyData['Motorstørrelse'] = dirtyData['Motor'].str.extract('(\d+\.\d+|\d+)L').astype(float)
    dirtyData['Brændstof'] = dirtyData['Motor'].str.extract('(Diesel|Benzin|El|Hybrid)',flags=re.IGNORECASE)

    # Removing 'Km/L' from 'Km/L' and converting to float
    dirtyData['Km/L'] = dirtyData['Km/L'].str.replace(',', '.').str.extract('(\d+\.\d+)').astype(float)

    # Removing 'kr.' and converting 'Pris' to float
    dirtyData['Pris'] = dirtyData['Pris'].str.replace('kr.', '').str.replace('.', '').astype(float)

    # You can drop the old 'Motor' column if it's no longer needed
    dirtyData = dirtyData.drop(columns=['Motor'])
    dirtyData = dirtyData.drop(columns=['Co2'])

    #Drop dupes and rows with NaN as it is only a handfull of rows so no need to impute
    dirtyData = dirtyData.drop_duplicates()
    dirtyData = dirtyData.dropna()

    return dirtyData