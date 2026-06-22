import os

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="380" style="background-color: #0d1117; border-radius: 8px; border: 1px solid #30363d;">
    <style>
        .code { font-family: 'Fira Code', 'Courier New', monospace; font-size: 15px; fill: #c9d1d9; }
        .keyword { fill: #ff7b72; }
        .variable { fill: #79c0ff; }
        .string { fill: #a5d6ff; }
        .punctuation { fill: #c9d1d9; }
        .property { fill: #d2a8ff; }
        
        /* Mac window buttons */
        .btn-red { fill: #ff5f56; }
        .btn-yellow { fill: #ffbd2e; }
        .btn-green { fill: #27c93f; }

        .cursor { fill: #c9d1d9; animation: blink 1s step-end infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
    
    <defs>
        <clipPath id="c1"><rect x="0" y="-20" width="0" height="30"><animate attributeName="width" values="0;800" begin="0.0s" dur="0.4s" fill="freeze" /></rect></clipPath>
        <clipPath id="c2"><rect x="0" y="6" width="0" height="30"><animate attributeName="width" values="0;800" begin="0.6s" dur="0.8s" fill="freeze" /></rect></clipPath>
        <clipPath id="c3"><rect x="0" y="32" width="0" height="30"><animate attributeName="width" values="0;800" begin="1.6s" dur="1.2s" fill="freeze" /></rect></clipPath>
        <clipPath id="c4"><rect x="0" y="58" width="0" height="30"><animate attributeName="width" values="0;800" begin="3.0s" dur="1.0s" fill="freeze" /></rect></clipPath>
        <clipPath id="c5"><rect x="0" y="84" width="0" height="30"><animate attributeName="width" values="0;800" begin="4.2s" dur="0.3s" fill="freeze" /></rect></clipPath>
        <clipPath id="c6"><rect x="0" y="110" width="0" height="30"><animate attributeName="width" values="0;800" begin="4.6s" dur="0.8s" fill="freeze" /></rect></clipPath>
        <clipPath id="c7"><rect x="0" y="136" width="0" height="30"><animate attributeName="width" values="0;800" begin="5.5s" dur="0.8s" fill="freeze" /></rect></clipPath>
        <clipPath id="c8"><rect x="0" y="162" width="0" height="30"><animate attributeName="width" values="0;800" begin="6.4s" dur="0.9s" fill="freeze" /></rect></clipPath>
        <clipPath id="c9"><rect x="0" y="188" width="0" height="30"><animate attributeName="width" values="0;800" begin="7.5s" dur="0.2s" fill="freeze" /></rect></clipPath>
        <clipPath id="c10"><rect x="0" y="214" width="0" height="30"><animate attributeName="width" values="0;800" begin="7.8s" dur="1.2s" fill="freeze" /></rect></clipPath>
        <clipPath id="c11"><rect x="0" y="240" width="0" height="30"><animate attributeName="width" values="0;800" begin="9.2s" dur="0.2s" fill="freeze" /></rect></clipPath>
    </defs>
    
    <!-- Window controls -->
    <rect x="0" y="0" width="800" height="40" fill="#161b22" />
    <circle cx="20" cy="20" r="6" class="btn-red" />
    <circle cx="40" cy="20" r="6" class="btn-yellow" />
    <circle cx="60" cy="20" r="6" class="btn-green" />
    <text x="400" y="25" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="middle">shaunak.js</text>
    
    <g transform="translate(20, 80)" class="code">
        <text y="0" clip-path="url(#c1)"><tspan class="keyword">const</tspan> <tspan class="variable">shaunak</tspan> <tspan class="punctuation">=</tspan> <tspan class="punctuation">{</tspan></text>
        <text y="26" clip-path="url(#c2)" xml:space="preserve">    <tspan class="property">role</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"Student &amp; Aspiring Developer"</tspan><tspan class="punctuation">,</tspan></text>
        <text y="52" clip-path="url(#c3)" xml:space="preserve">    <tspan class="property">passions</tspan><tspan class="punctuation">:</tspan> <tspan class="punctuation">[</tspan><tspan class="string">"AI × Wellness"</tspan><tspan class="punctuation">, </tspan><tspan class="string">"Cross-Platform Apps"</tspan><tspan class="punctuation">, </tspan><tspan class="string">"Full-Stack Magic"</tspan><tspan class="punctuation">]</tspan><tspan class="punctuation">,</tspan></text>
        <text y="78" clip-path="url(#c4)" xml:space="preserve">    <tspan class="property">motto</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"I don't just write code — I craft experiences."</tspan><tspan class="punctuation">,</tspan></text>
        <text y="104" clip-path="url(#c5)" xml:space="preserve">    <tspan class="property">currently</tspan><tspan class="punctuation">:</tspan> <tspan class="punctuation">{</tspan></text>
        <text y="130" clip-path="url(#c6)" xml:space="preserve">        <tspan class="property">building</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"AI-powered apps that improve lives"</tspan><tspan class="punctuation">,</tspan></text>
        <text y="156" clip-path="url(#c7)" xml:space="preserve">        <tspan class="property">learning</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"ML pipelines &amp; cloud architecture"</tspan><tspan class="punctuation">,</tspan></text>
        <text y="182" clip-path="url(#c8)" xml:space="preserve">        <tspan class="property">exploring</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"the intersection of tech &amp; mindfulness"</tspan></text>
        <text y="208" clip-path="url(#c9)" xml:space="preserve">    <tspan class="punctuation">}</tspan><tspan class="punctuation">,</tspan></text>
        <text y="234" clip-path="url(#c10)" xml:space="preserve">    <tspan class="property">funFact</tspan><tspan class="punctuation">:</tspan> <tspan class="string">"I've built more yoga AI apps than yoga poses I can do 🧘"</tspan></text>
        <text y="260" clip-path="url(#c11)"><tspan class="punctuation">};</tspan> <tspan class="cursor">_</tspan></text>
    </g>
</svg>
"""

os.makedirs("dist", exist_ok=True)
with open("dist/typing-js.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Successfully generated dist/typing-js.svg")
