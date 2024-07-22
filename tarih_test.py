import re
import dateparser
from datetime import datetime

def find_dates(text):
    dates = []
    current_year = datetime.now().year
    
    # Tarih formatlarını tanımlayan düzenli ifadeler
    date_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # 12/31/2020 veya 31/12/2020
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # 12-31-2020 veya 31-12-2020
        r'\b\d{1,2} \w+ \d{2,4}\b',      # 31 December 2020
        r'\b\w+ \d{1,2}, \d{2,4}\b',     # December 31, 2020
        r'\b\d{1,2} \w+\b',              # 2 Temmuz
        r'\b\w+ \d{1,2}\b',  # July 2
        r'\b\d{1,2}. \w+\b'  # 2. Juli
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Bulunan tarihi doğrulama ve normalleştirme
                date = dateparser.parse(match)
                
                # Eğer tarih geçmişse, bir yıl ekleyin
                if date and date < datetime.now():
                    date = date.replace(year=date.year + 1)
                
                if date:
                    dates.append(date)
            except ValueError:
                continue
    
    return dates


# Örnek kullanım
text = "Bugünün tarihi 12/31/2020 veya 4 Ağustos olabilir. Ayrıca, bir sonraki toplantı July 2'de veya 5. Juli veya 3 Temmuz 2024 yapılacaktır."
dates = find_dates(text)
print(datetime.now())
for date in dates:
    print(date.strftime('%Y-%m-%d'))