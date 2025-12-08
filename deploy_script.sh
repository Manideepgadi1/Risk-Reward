cd /var/www/risk-reward 2>/dev/null || cd /var/www/html/risk-reward 2>/dev/null || cd /root/risk-reward 2>/dev/null || cd /opt/risk-reward 2>/dev/null
echo "Current directory: $(pwd)"
echo "Pulling latest code from GitHub..."
git pull origin main
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo "Restarting service..."
systemctl restart risk-reward.service 2>/dev/null || systemctl restart riskapp.service 2>/dev/null
echo "Checking service status..."
systemctl status risk-reward.service --no-pager 2>/dev/null || systemctl status riskapp.service --no-pager 2>/dev/null
echo "Deployment completed!"
exit
