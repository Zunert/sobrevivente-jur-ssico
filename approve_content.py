import os
import re
from datetime import datetime

nome = os.environ.get('NOME', '')
tipo = os.environ.get('TIPO', '')
link = os.environ.get('LINK', '')
descricao = os.environ.get('DESCRICAO', '')
video_id = os.environ.get('VIDEO_ID', '')

print(f"Processando: {nome} ({tipo})")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

approved_date = datetime.now().strftime('%Y-%m-%d')

badge_map = {
    'YouTube':     ('com-badge-youtube', '📺 YouTube',  'youtube'),
    'LiveYouTube': ('com-badge-live',    '🔴 Live YT',  'youtube'),
    'Twitch':      ('com-badge-twitch',  '🎮 Twitch',   'twitch'),
    'LiveTwitch':  ('com-badge-live',    '🔴 Live',     'twitch'),
    'TikTok':      ('com-badge-tiktok',  '🎵 TikTok',   'tiktok'),
    'Discord':     ('com-badge-discord', '💬 Discord',  'discord'),
    'Video':       ('com-badge-video',   '▶ Vídeo',     'youtube'),
    'Outro':       ('com-badge-video',   '🔗 Link',     'outro'),
}
badge_class, badge_label, dir_tipo = badge_map.get(tipo, ('com-badge-video', '🔗 Link', 'outro'))

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

icon_map = {'youtube': '📺', 'twitch': '🎮', 'tiktok': '🎵', 'discord': '💬', 'outro': '🔗'}
dir_icon = icon_map.get(dir_tipo, '🔗')

is_video = tipo in ('Video', 'YouTube', 'LiveYouTube')

new_card = f'''
      <div class="com-card" data-approved="{approved_date}" data-tipo="{dir_tipo}">
        <div class="com-badge {badge_class}">{badge_label}</div>
        <div class="com-thumb">{thumb_html}</div>
        <div class="com-info">
          <div class="com-title">{nome}</div>
          <div class="com-desc">{descricao}</div>
          <a class="com-link" href="{link}" target="_blank" rel="noopener">Acessar →</a>
        </div>
      </div>'''

dir_card = f'''
      <div class="dir-card" data-tipo="{dir_tipo}">
        <div class="dir-icon">{dir_icon}</div>
        <div class="dir-info">
          <div class="dir-name">{nome}</div>
          <div class="dir-type">{badge_label}</div>
        </div>
        <a href="{link}" target="_blank" rel="noopener" class="dir-link">Visitar →</a>
      </div>'''

if is_video:
    target = '<div class="videos-grid reveal reveal-delay-2" id="videosGrid">'
    if target in content:
        content = content.replace(target, target + new_card)
        print("OK: adicionado em videosGrid")
else:
    target = '<div class="com-grid reveal reveal-delay-2" id="comGrid">'
    if target in content:
        content = content.replace(target, target + new_card)
        print("OK: adicionado em comGrid")
    dir_target = '<div class="dir-grid reveal reveal-delay-3" id="dirGrid">'
    if dir_target in content:
        content = content.replace(dir_target, dir_target + dir_card)
        print("OK: adicionado em dirGrid")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html atualizado!")
