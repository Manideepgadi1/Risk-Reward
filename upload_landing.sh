#!/bin/bash
cat > /tmp/landing.html << 'EOFMARKER'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Projects Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 60px; animation: fadeInDown 0.8s ease; }
        .header h1 { font-size: 3rem; font-weight: 700; margin-bottom: 15px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .header p { font-size: 1.2rem; opacity: 0.95; font-weight: 300; }
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; margin-bottom: 40px; }
        .project-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: all 0.3s ease; cursor: pointer; position: relative; overflow: hidden; animation: fadeInUp 0.8s ease; }
        .project-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); }
        .project-card:hover { transform: translateY(-10px); box-shadow: 0 15px 40px rgba(0,0,0,0.3); }
        .project-icon { width: 60px; height: 60px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; font-size: 28px; }
        .project-title { font-size: 1.5rem; font-weight: 600; color: #2d3748; margin-bottom: 12px; }
        .project-description { color: #718096; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px; }
        .project-tag { display: inline-block; background: #e6f2ff; color: #667eea; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin-right: 8px; margin-bottom: 8px; }
        .project-link { display: inline-flex; align-items: center; color: #667eea; text-decoration: none; font-weight: 600; margin-top: 15px; transition: color 0.3s ease; }
        .project-link:hover { color: #764ba2; }
        .project-link svg { margin-left: 8px; transition: transform 0.3s ease; }
        .project-link:hover svg { transform: translateX(5px); }
        .footer { text-align: center; color: white; margin-top: 60px; opacity: 0.9; animation: fadeIn 1s ease 0.5s both; }
        .footer p { font-size: 0.95rem; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media (max-width: 768px) { .header h1 { font-size: 2rem; } .header p { font-size: 1rem; } .projects-grid { grid-template-columns: 1fr; gap: 20px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>My Projects Dashboard</h1>
            <p>Explore interactive financial analysis and visualization tools</p>
        </div>
        <div class="projects-grid">
            <div class="project-card" onclick="window.location.href='/Sector-Heatmap/'">
                <div class="project-icon">📊</div>
                <h2 class="project-title">Sector Heatmap</h2>
                <p class="project-description">Interactive heatmap visualization for sector performance analysis with real-time data updates and color-coded indicators.</p>
                <div><span class="project-tag">FastAPI</span><span class="project-tag">Visualization</span><span class="project-tag">Real-time</span></div>
                <a href="/Sector-Heatmap/" class="project-link" onclick="event.stopPropagation()">Launch App<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
            </div>
            <div class="project-card" onclick="window.location.href='/multi-charts/'">
                <div class="project-icon">📈</div>
                <h2 class="project-title">Multi-charts</h2>
                <p class="project-description">Comprehensive charting solution with multiple visualization types, technical indicators, and customizable views.</p>
                <div><span class="project-tag">Charts</span><span class="project-tag">Analytics</span><span class="project-tag">Dashboard</span></div>
                <a href="/multi-charts/" class="project-link" onclick="event.stopPropagation()">Launch App<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
            </div>
            <div class="project-card" onclick="window.location.href='/RightTime/'">
                <div class="project-icon">⏰</div>
                <h2 class="project-title">RightTime</h2>
                <p class="project-description">Time-series analysis tool for optimal market timing with bar-line charts and predictive indicators.</p>
                <div><span class="project-tag">Time-series</span><span class="project-tag">Prediction</span><span class="project-tag">FastAPI</span></div>
                <a href="/RightTime/" class="project-link" onclick="event.stopPropagation()">Launch App<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
            </div>
            <div class="project-card" onclick="window.location.href='/RightSector/'">
                <div class="project-icon">🎯</div>
                <h2 class="project-title">RightSector</h2>
                <p class="project-description">Sector rotation analysis and recommendation engine to identify high-potential market sectors.</p>
                <div><span class="project-tag">Sector Analysis</span><span class="project-tag">Recommendations</span><span class="project-tag">Static</span></div>
                <a href="/RightSector/" class="project-link" onclick="event.stopPropagation()">Launch App<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
            </div>
            <div class="project-card" onclick="window.location.href='/risk-reward/'">
                <div class="project-icon">⚖️</div>
                <h2 class="project-title">Risk-Reward Analysis</h2>
                <p class="project-description">Calculate and visualize risk-adjusted returns, volatility metrics, and momentum indicators for indices.</p>
                <div><span class="project-tag">Flask</span><span class="project-tag">Risk Metrics</span><span class="project-tag">Heatmaps</span></div>
                <a href="/risk-reward/" class="project-link" onclick="event.stopPropagation()">Launch App<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
            </div>
        </div>
        <div class="footer"><p>&copy; 2025 Financial Analytics Suite | All Rights Reserved</p></div>
    </div>
</body>
</html>
EOFMARKER

sudo mv /tmp/landing.html /var/www/html/index.html
echo "Landing page updated successfully!"
