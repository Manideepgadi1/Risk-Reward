#!/bin/bash
# Deployment script for Risk-Reward project update

echo "Starting deployment process..."

# Navigate to project directory
cd /root/Risk-Reward || cd /var/www/Risk-Reward || cd ~/Risk-Reward

echo "Current directory: $(pwd)"

# Pull latest code from GitHub
echo "Pulling latest code from GitHub..."
git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Restart the service
echo "Restarting service..."
if systemctl list-units --full -all | grep -q "risk-reward.service"; then
    systemctl restart risk-reward.service
    echo "Restarted risk-reward.service"
elif systemctl list-units --full -all | grep -q "riskapp.service"; then
    systemctl restart riskapp.service
    echo "Restarted riskapp.service"
else
    # Try restarting gunicorn directly
    pkill -f gunicorn
    sleep 2
    gunicorn --config gunicorn.conf.py wsgi:app &
    echo "Restarted gunicorn directly"
fi

# Check service status
echo "Checking service status..."
systemctl status risk-reward.service || systemctl status riskapp.service || echo "Service status check completed"

echo "Deployment completed! Check http://82.25.105.18/risk-reward/"
