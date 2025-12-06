#!/bin/bash
# Quick Deployment Script for Risk-Reward on VPS
# Run this on your Ubuntu VPS after cloning the repo

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "Risk-Reward Deployment Script"
echo "════════════════════════════════════════════════════════════"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Clone repository
echo -e "${BLUE}Step 1: Cloning repository...${NC}"
cd /var/www
if [ -d "risk-reward" ]; then
    echo "Directory exists, pulling latest changes..."
    cd risk-reward
    git pull origin main
else
    git clone https://github.com/Manideepgadi1/Risk-Reward.git risk-reward
    cd risk-reward
fi

# Step 2: Setup Python environment
echo -e "${BLUE}Step 2: Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Step 3: Create systemd service
echo -e "${BLUE}Step 3: Creating systemd service...${NC}"
sudo cp risk-reward.service /etc/systemd/system/risk-reward.service
sudo systemctl daemon-reload
sudo systemctl enable risk-reward
sudo systemctl start risk-reward

# Step 4: Check service status
echo -e "${BLUE}Step 4: Checking service status...${NC}"
sudo systemctl status risk-reward --no-pager

# Step 5: Display next steps
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. Add Nginx configuration:"
echo "   sudo nano /etc/nginx/sites-available/combined"
echo ""
echo "2. Add this block before the closing server bracket:"
echo "   (See nginx-config-addition.conf in the repo)"
echo ""
echo "3. Test and reload Nginx:"
echo "   sudo nginx -t"
echo "   sudo systemctl reload nginx"
echo ""
echo "4. Update landing page:"
echo "   sudo nano /var/www/html/index.html"
echo "   Add: <li><a href=\"/risk-reward/\">Risk-Reward Analysis</a></li>"
echo ""
echo "5. Access your app at: http://82.25.105.18/risk-reward/"
echo ""
echo "View logs: sudo journalctl -u risk-reward -f"
