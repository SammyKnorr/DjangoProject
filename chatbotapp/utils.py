import pandas as pd
import os
from django.conf import settings

def load_valid_symbols(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    df = pd.read_excel(file_path)
    return set(df['Symbol'].dropna().tolist())

# Load valid symbols once
valid_symbols = load_valid_symbols('validTags.xlsx')
