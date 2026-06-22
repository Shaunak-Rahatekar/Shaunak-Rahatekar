import os
import urllib.request
import json
import base64
from datetime import datetime, timedelta
import random

def fetch_contributions(username, token):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }
    
    query = """
    query($userName:String!) {
      user(login: $userName){
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "userName": username
    }
    
    data = json.dumps({'query': query, 'variables': variables}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['data']['user']['contributionsCollection']['contributionCalendar']
            else:
                print(f"Failed to fetch data: {response.status}")
                return None
    except Exception as e:
        print(f"Error making request: {e}")
        return None

def generate_mock_data():
    weeks = []
    start_date = datetime.now() - timedelta(days=365)
    for w in range(53):
        days = []
        for d in range(7):
            date_str = (start_date + timedelta(days=w*7+d)).strftime("%Y-%m-%d")
            count = random.choices([0, 1, 3, 5, 8], weights=[50, 20, 15, 10, 5])[0]
            days.append({
                "contributionCount": count,
                "date": date_str
            })
        weeks.append({"contributionDays": days})
    return {"weeks": weeks, "totalContributions": sum(d['contributionCount'] for w in weeks for d in w['contributionDays'])}

def get_color(count):
    if count == 0:
        return "#161b22"
    elif count <= 2:
        return "#0e4429"
    elif count <= 4:
        return "#006d32"
    elif count <= 6:
        return "#26a641"
    else:
        return "#39d353"

def get_dragon_base64():
    image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'dragon.gif')
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/gif;base64,{encoded_string}"
    return ""

def generate_svg(calendar_data):
    svg_width = 800
    svg_height = 200
    
    square_size = 10
    gap = 4
    step = square_size + gap
    
    offset_x = (svg_width - (53 * step)) / 2
    offset_y = 60
    
    anim_duration = 10  # total loop duration in seconds
    fly_duration = 5    # time dragon takes to cross the screen
    
    dragon_base64 = get_dragon_base64()
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #0d1117;">
    <style>
        .grid {{
            fill: #161b22;
        }}
        .dragon {{
            animation: fly {anim_duration}s linear infinite;
        }}
        @keyframes fly {{
            0% {{ transform: translate(-130px, -10px); }}
            {fly_duration / anim_duration * 100}% {{ transform: translate({svg_width + 50}px, -10px); }}
            100% {{ transform: translate({svg_width + 50}px, -10px); }}
        }}
        /* Fire is nested inside dragon group — no separate animation needed */
        
        /* Live fire effects */
        .flame-outer {{ animation: flicker1 0.15s infinite alternate; transform-origin: 0 0; }}
        .flame-inner {{ animation: flicker2 0.12s infinite alternate; transform-origin: 0 0; }}
        .flame-core {{ animation: flicker1 0.1s infinite alternate; transform-origin: 0 0; }}
        .fireball-1 {{ animation: shoot1 0.3s infinite linear; }}
        .fireball-2 {{ animation: shoot2 0.25s infinite linear; }}
        .fireball-3 {{ animation: shoot3 0.35s infinite linear; }}
        
        @keyframes flicker1 {{
            0% {{ transform: scaleX(0.8) scaleY(0.9); opacity: 0.8; }}
            100% {{ transform: scaleX(1.1) scaleY(1.1); opacity: 1; }}
        }}
        @keyframes flicker2 {{
            0% {{ transform: scaleX(1.1) scaleY(0.8); opacity: 1; }}
            100% {{ transform: scaleX(0.9) scaleY(1.2); opacity: 0.9; }}
        }}
        @keyframes shoot1 {{
            0% {{ transform: translateX(0) scale(1); opacity: 1; }}
            100% {{ transform: translateX(60px) scale(0); opacity: 0; }}
        }}
        @keyframes shoot2 {{
            0% {{ transform: translateX(0) scale(1); opacity: 1; }}
            100% {{ transform: translateX(40px) scale(0); opacity: 0; }}
        }}
        @keyframes shoot3 {{
            0% {{ transform: translateX(0) scale(1); opacity: 1; }}
            100% {{ transform: translateX(50px) scale(0); opacity: 0; }}
        }}
    '''
    
    # Generate dynamic keyframes for each of the 371 cells
    total_cells = 53 * 7
    for i in range(total_cells):
        hit_pct = (i / total_cells) * (fly_duration / anim_duration * 100)
        svg += f'''
        @keyframes burn-{i} {{
            0% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
            {hit_pct:.2f}% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
            {min(hit_pct + 1, 95):.2f}% {{ fill: #ff9900; transform: scale(1.2); opacity: 1; }}
            {min(hit_pct + 2, 95):.2f}% {{ fill: #ff4d4d; transform: scale(0.8); opacity: 0.8; }}
            {min(hit_pct + 3, 95):.2f}% {{ fill: #1a1a1a; transform: scale(0.2); opacity: 0.2; }}
            95% {{ fill: #1a1a1a; transform: scale(0.2); opacity: 0.2; }}
            98% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
            100% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
        }}
        .contrib-{i} {{
            animation: burn-{i} {anim_duration}s linear infinite;
            transform-origin: center;
            transform-box: fill-box;
        }}
        '''

    svg += '''
    </style>
    
    <g id="grid">
    '''
    
    weeks = calendar_data['weeks']
    for c, week in enumerate(weeks):
        x = offset_x + c * step
        for r, day in enumerate(week['contributionDays']):
            y = offset_y + r * step
            count = day['contributionCount']
            color = get_color(count)
            
            if c % 2 == 0:
                snake_idx = c * 7 + r
            else:
                snake_idx = c * 7 + (6 - r)
                
            svg += f'        <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" rx="2" class="contrib-{snake_idx} grid" style="--base-color: {color}; fill: {color};" />\n'
            
    svg += '    </g>\n'
    
    # Dragon + Fire in ONE group so they share the same fly animation
    if dragon_base64:
        svg += f'''
    <g class="dragon">
        <!-- Dragon image, flipped to face right -->
        <g transform="scale(-1, 1) translate(-110, 0)">
            <image href="{dragon_base64}" x="0" y="0" width="110" height="110" preserveAspectRatio="xMidYMid slice"/>
        </g>
        <!-- Fire breath from mouth, nested inside dragon group for perfect alignment -->
        <g transform="translate(90, 25) rotate(40)">
            <g style="animation: flicker1 0.15s infinite alternate; transform-origin: 0 0;">
                <path d="M 0,-4 L 15,-8 L 30,-6 L 45,-12 L 60,-8 L 75,-14 L 85,-6 L 75,0 L 85,8 L 75,14 L 60,8 L 45,12 L 30,6 L 15,8 Z" fill="#ff4d00" opacity="0.95"/>
                <path d="M 0,-2 L 15,-5 L 30,-3 L 45,-7 L 55,-4 L 60,0 L 55,4 L 45,7 L 30,3 L 15,5 Z" fill="#ffcc00" opacity="1"/>
                <path d="M 0,-1 L 10,-3 L 20,0 L 10,3 Z" fill="#ffffff" opacity="0.9"/>
            </g>
        </g>
    </g>
    '''
    else:
        svg += '''
    <g class="dragon">
        <rect width="110" height="110" fill="red" />
    </g>
    '''
    
    svg += '</svg>'
    return svg

def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "Shaunak-Rahatekar")
    
    if token:
        print(f"Fetching data for {username}...")
        data = fetch_contributions(username, token)
        if not data:
            print("Failed to fetch real data, using mock data.")
            data = generate_mock_data()
    else:
        print("No GITHUB_TOKEN found, using mock data.")
        data = generate_mock_data()
        
    svg_content = generate_svg(data)
    
    os.makedirs("dist", exist_ok=True)
    with open("dist/github-dragon.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print("Successfully generated dist/github-dragon.svg")

if __name__ == "__main__":
    main()
