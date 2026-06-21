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
    total_cells = 53 * 7
    time_per_cell = fly_duration / total_cells
    
    dragon_base64 = get_dragon_base64()
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #0d1117;">
    <style>
        .grid {{
            fill: #161b22;
        }}
        .contrib {{
            animation: burn {anim_duration}s linear infinite;
            transform-origin: center;
            transform-box: fill-box;
        }}
        @keyframes burn {{
            0% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
            1% {{ fill: #ff9900; transform: scale(1.2); opacity: 1; }}
            2% {{ fill: #ff4d4d; transform: scale(0.8); opacity: 0.8; }}
            3% {{ fill: #1a1a1a; transform: scale(0.2); opacity: 0.2; }}
            80% {{ fill: #1a1a1a; transform: scale(0.2); opacity: 0.2; }}
            90% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
            100% {{ fill: var(--base-color); transform: scale(1); opacity: 1; }}
        }}
        .dragon {{
            animation: fly {anim_duration}s linear infinite;
        }}
        @keyframes fly {{
            0% {{ transform: translate(-150px, -20px); }}
            {fly_duration / anim_duration * 100}% {{ transform: translate({svg_width + 50}px, -20px); }}
            100% {{ transform: translate({svg_width + 50}px, -20px); }}
        }}
        .fire {{
            animation: breathe {anim_duration}s linear infinite;
            fill: #ff9900;
            opacity: 0;
            transform-origin: left center;
        }}
        @keyframes breathe {{
            0% {{ opacity: 0; transform: translate(-100px, 60px) scaleX(0); }}
            1% {{ opacity: 0.8; transform: translate(-80px, 60px) scaleX(1); }}
            {fly_duration / anim_duration * 100}% {{ opacity: 0.8; transform: translate({svg_width + 70}px, 60px) scaleX(1); }}
            {(fly_duration / anim_duration * 100) + 1}% {{ opacity: 0; transform: translate({svg_width + 80}px, 60px) scaleX(0); }}
            100% {{ opacity: 0; }}
        }}
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
            
            # Snake index logic: down even columns, up odd columns
            if c % 2 == 0:
                snake_idx = c * 7 + r
            else:
                snake_idx = c * 7 + (6 - r)
                
            delay = snake_idx * time_per_cell
            
            svg += f'        <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" rx="2" class="contrib grid" style="--base-color: {color}; fill: {color}; animation-delay: {delay}s;" />\n'
            
    svg += '    </g>\n'
    
    # Fire breath connecting dragon to the burning square
    svg += f'''
    <g class="fire">
        <path d="M 0,40 Q 60,20 120,40 Q 60,60 0,40 Z" fill="#ff9900" opacity="0.6"/>
        <path d="M 0,40 Q 40,30 80,40 Q 40,50 0,40 Z" fill="#ffcc00" opacity="0.8"/>
    </g>
    '''
    
    # Insert Dragon Image
    if dragon_base64:
        svg += f'''
    <g class="dragon">
        <image href="{dragon_base64}" x="0" y="0" width="160" height="160" preserveAspectRatio="xMidYMid slice"/>
    </g>
    '''
    else:
        # Fallback dragon if image missing
        svg += '''
    <g class="dragon">
        <path d="M46.7,26.4c0,0-15.5-8.5-22.5-3.5c-7,5,0,26.1,0,26.1s-10-8.8-11.5-6.8c-1.5,2,4,21.6,4,21.6s-18.1-15.1-18.1-12c0,3.1,16.6,26.6,16.6,26.6s-18.6-1.5-17.6,1.5c1,3,27.1,19.1,27.1,19.1s-15.1,14.6-12.6,16.6c2.5,2,19.6-12.6,19.6-12.6s2.5,24.1,5.5,23.1c3-1,5-24.1,5-24.1s14.6,16.6,17.6,14.6c3-2-8.5-23.1-8.5-23.1s27.1,8.5,28.1,5.5c1-3-12.6-19.1-12.6-19.1s24.1-3.5,23.1-6.5c-1-3-22.1-1.5-22.1-1.5s15.6-21.6,13.6-24.1C80.3,45,61.7,59.5,61.7,59.5S66.3,37.4,63.2,36C60.2,34.5,46.7,26.4,46.7,26.4z" fill="#00ff00" transform="translate(40, 60) scale(1.5)" />
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
