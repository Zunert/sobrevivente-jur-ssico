import os
import re

nome = os.environ.get('NOME', '')
tipo = os.environ.get('TIPO', '')
link = os.environ.get('LINK', '')
descricao = os.environ.get('DESCRICAO', '')
video_id = os.environ.get('VIDEO_ID', '')

print(f"Processando: {nome} ({tipo})")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── Definir badge e ícone por tipo ──
badge_map = {
    'YouTube':     ('com-badge-youtube', '📺 YouTube'),
    'LiveYouTube': ('com-badge-live',    '🔴 Live YT'),
    'Twitch':      ('com-badge-twitch',  '🎮 Twitch'),
    'LiveTwitch':  ('com-badge-live',    '🔴 Live Twitch'),
    'TikTok':      ('com-badge-tiktok',  '🎵 TikTok'),
    'Discord':     ('com-badge-discord', '💬 Discord'),
    'Video':       ('com-badge-video',   '▶ Vídeo'),
    'Outro':       ('com-badge-video',   '🔗 Link'),
}

badge_class, badge_label = badge_map.get(tipo, ('com-badge-video', '🔗 Link'))

# ── Thumb ──
if tipo in ('YouTube', 'LiveYouTube', 'Video') and video_id:
    thumb_html = f'<img class="com-thumb" src="https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" alt="{nome}" style="width:100%;height:100%;object-fit:cover">'
elif tipo in ('Twitch', 'LiveTwitch'):
    channel = link.rstrip('/').split('/')[-1]
    thumb_html = f'<img class="com-thumb" src="https://static-cdn.jtvnw.net/previews-ttv/live_user_{channel}-320x180.jpg" alt="{nome}" style="width:100%;height:100%;object-fit:cover">'
elif tipo == 'TikTok':
    thumb_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#010101,#1a1a1a);font-size:2.5rem">🎵</div>'
elif tipo == 'Discord':
    thumb_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a2a,#12124a);font-size:2.5rem">💬</div>'
else:
    thumb_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a,#1a1a1a);font-size:2.5rem">🔗</div>'

# ── Novo card ──
new_card = f'''
      <div class="com-card">
        <div class="com-badge {badge_class}">{badge_label}</div>
        <div class="com-thumb">{thumb_html}</div>
        <div class="com-info">
          <div class="com-title">{nome}</div>
          <div class="com-desc">{descricao}</div>
          <a class="com-link" href="{link}" target="_blank" rel="noopener">Acessar →</a>
        </div>
      </div>'''

# ── Inserir na seção correta ──
# Vídeos vão para videosGrid, o resto para comGrid
if tipo in ('Video', 'YouTube', 'LiveYouTube'):
    # Adicionar na seção de vídeos
    target = '<div class="videos-grid reveal reveal-delay-2" id="videosGrid">'
    
    if target in content:
        content = content.replace(target, target + new_card)
        print(f"✅ Adicionado em videosGrid")
    else:
        print("❌ videosGrid não encontrado")
else:
    # Adicionar na seção de comunidade
    target = '<div class="com-grid reveal reveal-delay-2" id="comGrid">'
    
    if target in content:
        content = content.replace(target, target + new_card)
        print(f"✅ Adicionado em comGrid")
    else:
        print("❌ comGrid não encontrado")

# ── Para Twitch ao vivo, adicionar também na barra de lives ──
if tipo in ('LiveTwitch', 'LiveYouTube'):
    channel = link.rstrip('/').split('/')[-1]
    if tipo == 'LiveTwitch':
        thumb_url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{channel}-320x180.jpg"
    else:
        thumb_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""
    
    platform = '📺 YouTube' if 'YouTube' in tipo else '🎮 Twitch'
    
    live_entry = f"  {{ name: '{nome}', platform: '{platform}', thumb: '{thumb_url}', url: '{link}' }},"
    
    target_lives = 'const youtubeLives = ['
    if target_lives in content:
        content = content.replace(target_lives, target_lives + '\n' + live_entry)
        print(f"✅ Adicionado em lives")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ index.html atualizado com sucesso!")
