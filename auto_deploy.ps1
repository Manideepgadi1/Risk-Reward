# Automated deployment script for Risk-Reward project
# This script will connect via SSH and update the project

$sshHost = "root@82.25.105.18"
$password = "Satish@23121982"

# Commands to execute on the remote server
$commands = @"
cd /var/www/risk-reward 2>/dev/null || cd /var/www/html/risk-reward 2>/dev/null || cd /root/risk-reward 2>/dev/null || cd /opt/risk-reward 2>/dev/null
echo "Current directory: `$(pwd)"
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
"@

# Create temporary script file
$commands | Out-File -FilePath ".\deploy_script.sh" -Encoding UTF8

# Use plink (PuTTY's command line tool) or ssh with password
Write-Host "Connecting to server and executing deployment commands..."
Write-Host "Note: You may need to enter the password when prompted: Satish@23121982"

# Execute via SSH
ssh $sshHost "cd /var/www/risk-reward 2>/dev/null || cd /var/www/html/risk-reward 2>/dev/null || cd /root/risk-reward 2>/dev/null || cd /opt/risk-reward 2>/dev/null; pwd; git pull origin main; pip3 install -r requirements.txt; systemctl restart risk-reward.service 2>/dev/null || systemctl restart riskapp.service 2>/dev/null; systemctl status risk-reward.service --no-pager 2>/dev/null || systemctl status riskapp.service --no-pager 2>/dev/null"
