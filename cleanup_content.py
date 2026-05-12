from datetime import datetime, timedelta
import re

EXPIRY_DAYS = 4

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

today = datetime.now()
removed = 0

# Find all com-cards with data-approved attribute
pattern = r'<div class="com-card" data-approved="(\d{4}-\d{2}-\d{2})".*?</div>\s*</div>\s*</div>'
matches = list(re.finditer(pattern, content, re.DOTALL))

for match in reversed(matches):
    date_str = match.group(1)
    approved = datetime.strptime(date_str, '%Y-%m-%d')
    age = (today - approved).days
    
    if age >= EXPIRY_DAYS:
        content = content[:match.start()] + content[match.end():]
        removed += 1
        print(f"Removido card com data {date_str} ({age} dias)")

# Also remove expired video cards from videosGrid
video_pattern = r'<div class="com-card" data-approved="(\d{4}-\d{2}-\d{2})" data-tipo="youtube".*?</div>\s*</div>\s*</div>'
video_matches = list(re.finditer(video_pattern, content, re.DOTALL))

for match in reversed(video_matches):
    date_str = match.group(1)
    approved = datetime.strptime(date_str, '%Y-%m-%d')
    age = (today - approved).days
    
    if age >= EXPIRY_DAYS:
        content = content[:match.start()] + content[match.end():]
        removed += 1
        print(f"Removido vídeo com data {date_str} ({age} dias)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

if removed > 0:
    print(f"Total removido: {removed} cards expirados")
else:
    print("Nenhum card expirado encontrado")
