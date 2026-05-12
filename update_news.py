import feedparser
import requests
import re
import json
from datetime import datetime

STEAM_RSS = "https://store.steampowered.com/feeds/news/app/376210/"
HTML_FILE = "index.html"

# Tags para identificar tipo de update
def get_tag(title):
    t = title.lower()
    if 'devblog' in t: return 'DevBlog'
    if 'patch' in t or 'hotfix' in t or 'update' in t: return 'Patch Notes'
    if 'hordetest' in t: return 'HordeTest'
    if 'announcement' in t or 'anuncio' in t: return 'Anúncio'
    return 'Notícia'

def format_date(entry):
    try:
        dt = datetime(*entry.published_parsed[:6])
        months = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        return f"{dt.day:02d} {months[dt.month-1]} {dt.year}"
    except:
        return 'Recente'

def clean_html(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Limit to 220 chars
    if len(text) > 220:
        text = text[:220].rsplit(' ', 1)[0] + '...'
    return text

def build_card(entry, delay_class=""):
    title = entry.get('title', 'Sem título')
    link = entry.get('link', 'https://store.steampowered.com/news/app/376210')
    tag = get_tag(title)
    date = format_date(entry)
    
    # Get summary
    summary = entry.get('summary', '')
    excerpt = clean_html(summary) if summary else 'Confira a atualização completa no Steam.'
    
    return f'''      <div class="update-card reveal{delay_class}">
        <div class="update-date">{date}</div>
        <div class="update-title">{title}</div>
        <div class="update-excerpt">{excerpt}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:18px">
          <span class="update-tag">{tag}</span>
          <a href="{link}" target="_blank" style="font-family:'Cinzel',serif;font-size:.55rem;letter-spacing:.12em;text-transform:uppercase;color:var(--acid);text-decoration:none;opacity:.7">Ver no Steam →</a>
        </div>
      </div>'''

def main():
    print("Buscando feed RSS da Steam...")
    
    try:
        feed = feedparser.parse(STEAM_RSS)
        entries = feed.entries[:10]  # Pegar as 10 mais recentes
        print(f"Encontradas {len(entries)} notícias")
    except Exception as e:
        print(f"Erro ao buscar feed: {e}")
        return

    if not entries:
        print("Nenhuma notícia encontrada.")
        return

    # Montar os cards HTML
    delays = ["", " reveal-delay-1", " reveal-delay-2", " reveal-delay-3", " reveal-delay-4",
              "", " reveal-delay-1", " reveal-delay-2", " reveal-delay-3", " reveal-delay-4"]
    
    cards_html = "\n".join(build_card(e, delays[i]) for i, e in enumerate(entries))

    # Ler o HTML atual
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar a div updates-grid e substituir o conteúdo
    pattern = r'(<div class="updates-grid" id="updatesGrid">)\s*</div>'
    
    # O grid é preenchido por JS, então precisamos atualizar o array updates no JS
    # Montar array JS
    js_entries = []
    for entry in entries:
        title = entry.get('title', '').replace("'", "\\'")
        link = entry.get('link', 'https://store.steampowered.com/news/app/376210')
        tag = get_tag(entry.get('title', ''))
        date = format_date(entry)
        summary = entry.get('summary', '')
        excerpt = clean_html(summary).replace("'", "\\'")
        
        js_entries.append(
            f"  {{date:'{date}',type:'{tag.lower().replace(' ','')}',tag:'{tag}',"
            f"title:'{title}',"
            f"excerpt:'{excerpt[:200]}',"
            f"link:'{link}'}}"
        )

    new_updates_js = "const updates=[\n" + ",\n".join(js_entries) + "\n];"

    # Substituir o array updates no JS
    pattern_js = r'const updates=\[[\s\S]*?\];'
    if re.search(pattern_js, content):
        new_content = re.sub(pattern_js, new_updates_js, content)
        
        if new_content != content:
            with open(HTML_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Site atualizado com {len(entries)} notícias!")
        else:
            print("ℹ️ Nenhuma mudança necessária.")
    else:
        print("❌ Padrão não encontrado no HTML.")

if __name__ == "__main__":
    main()
