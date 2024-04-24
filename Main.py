from Scrape import scrapeCars
from Clean import cleaning
import os
import pandas as pd




dirtyData = scrapeCars()
cleanData = cleaning(dirtyData)





