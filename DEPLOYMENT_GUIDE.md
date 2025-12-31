# Risk-Reward - Complete Deployment Guide

**Application:** Risk-Reward Analysis Tool  
**Type:** Flask Backend Application  
**Port:** 5000  
**Framework:** Flask + Gunicorn  
**Purpose:** Risk-reward ratio analysis for investment decisions

---

## 🎯 Overview

Risk-Reward is a Flask-based analysis tool that helps users:
- Calculate risk-reward ratios
- Analyze investment opportunities
- Make data-driven decisions
- Evaluate portfolio risk profiles

**Access URLs:**
- Direct: http://82.25.105.18:5000
- Via Main Site: http://82.25.105.18/risk-reward/

---

## 📋 Prerequisites

1. ✅ SSH access to VPS (82.25.105.18)
2. ✅ Python 3.x installed
3. ✅ PM2 installed (for process management)
4. ✅ Nginx installed and running
5. ✅ Risk-Reward source code

---

## 📁 Required Application Structure

```
Risk-Reward/
├── app.py                # Main Flask application (required)
├── requirements.txt      # Python dependencies
├── venv/                # Virtual environment (created during deployment)
├── data.csv             # Historical price data
├── heatmap values.xlsx  # V1 percentile values
├── index_name_mapping.py # Column name to full name mappings
├── static/              # Static files (CSS, JS, images)
│   ├── styles.css
│   ├── script.js
│   └── heatmap.js
├── templates/           # HTML templates
│   ├── index.html
│   └── heatmap.html
├── riskapp/            # Core metrics module
│   ├── __init__.py
│   └── metrics.py
└── README.md           # Documentation
```

**Minimum Required Files:**
- `app.py` - Flask application entry point
- `requirements.txt` - Dependencies list
- `data.csv` - Historical price data
- `heatmap values.xlsx` - V1 percentile values
- `index_name_mapping.py` - Name mappings
- `templates/index.html` - Main page

---

## 🚀 Quick Deployment (Recommended)

### Step 1: Pull Latest Code from GitHub

```bash
# SSH to VPS
ssh root@82.25.105.18

# Navigate to application directory
cd /var/www/vsfintech

# If Risk-Reward directory doesn't exist, clone it
git clone https://github.com/Manideepgadi1/Risk-Reward.git

# If it exists, pull latest changes
cd Risk-Reward
git pull origin main
```

### Step 2: Run Deployment Script

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
sudo ./deploy.sh
```

The script will automatically:
- ✅ Check prerequisites (Python, PM2)
- ✅ Create Python virtual environment
- ✅ Install dependencies
- ✅ Configure PM2 process manager
- ✅ Set up Nginx reverse proxy
- ✅ Set correct permissions
- ✅ Test the deployment

---

## 🔧 Manual Deployment Steps

### Step 1: Pull Code from GitHub

```bash
ssh root@82.25.105.18
cd /var/www/vsfintech/Risk-Reward
git pull origin main
```

### Step 2: Set Up Python Virtual Environment

```bash
cd /var/www/vsfintech/Risk-Reward

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

**Required Dependencies (requirements.txt):**
```txt
Flask==3.0.0
gunicorn==21.2.0
flask-cors==4.0.0
pandas==2.1.3
numpy==1.26.2
openpyxl==3.1.2
```

### Step 4: Verify Application Files

Ensure these files exist:
```bash
ls -la data.csv
ls -la "heatmap values.xlsx"
ls -la index_name_mapping.py
ls -la app.py
```

### Step 5: Test Flask Application

```bash
# Still in virtual environment
python app.py

# In another terminal, test:
curl http://localhost:5000/
curl http://localhost:5000/api/metrics?duration=3years
```

Press `Ctrl+C` to stop the test server.

### Step 6: Configure PM2 Process Manager

```bash
# Deactivate virtual environment first
deactivate

# Remove old PM2 process if exists
pm2 stop risk-reward 2>/dev/null || true
pm2 delete risk-reward 2>/dev/null || true

# Start with PM2 using gunicorn
pm2 start /var/www/vsfintech/Risk-Reward/venv/bin/gunicorn \
    --name risk-reward \
    --cwd /var/www/vsfintech/Risk-Reward \
    --interpreter none \
    -- -w 2 -b 0.0.0.0:5000 app:app

# Save PM2 configuration
pm2 save

# Enable PM2 to start on boot
pm2 startup systemd
```

### Step 7: Configure Nginx Reverse Proxy

Edit the main Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/vsfintech.conf
```

Add this location block inside the server block:

```nginx
# Risk-Reward Flask App
location /risk-reward {
    proxy_pass http://localhost:5000/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Timeout settings
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

Test and reload Nginx:

```bash
# Test configuration
sudo nginx -t

# If successful, reload
sudo systemctl reload nginx
```

### Step 8: Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/vsfintech/Risk-Reward
sudo chmod -R 755 /var/www/vsfintech/Risk-Reward
```

### Step 9: Test Deployment

```bash
# Test backend directly
curl http://localhost:5000/
curl http://localhost:5000/api/metrics?duration=3years

# Test through Nginx proxy
curl http://localhost/risk-reward/
curl http://82.25.105.18/risk-reward/

# Check PM2 status
pm2 status

# View logs
pm2 logs risk-reward --lines 50
```

---

## 🔍 Verification & Testing

### Check Service Status

```bash
# PM2 process status
pm2 status

# Expected output:
# │ risk-reward │ online │ 0 │ none │ ...
```

### Check Application Logs

```bash
# View live logs
pm2 logs risk-reward

# View last 100 lines
pm2 logs risk-reward --lines 100

# View error logs only
pm2 logs risk-reward --err
```

### Test HTTP Endpoints

```bash
# Test home page
curl -I http://localhost:5000/

# Test API endpoint
curl http://localhost:5000/api/metrics?duration=3years

# Test through Nginx
curl -I http://82.25.105.18/risk-reward/

# Test with full response
curl http://82.25.105.18/risk-reward/api/metrics?duration=3years | jq '.'
```

### Check Port Availability

```bash
# Verify port 5000 is listening
sudo netstat -tulpn | grep 5000

# Expected output:
# tcp  0  0  0.0.0.0:5000  0.0.0.0:*  LISTEN  <PID>/gunicorn
```

---

## 🔧 Troubleshooting

### Issue: Port 5000 Already in Use

```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill the process
sudo kill -9 <PID>

# Restart PM2 service
pm2 restart risk-reward
```

### Issue: Module Not Found Error

```bash
# Reinstall dependencies
cd /var/www/vsfintech/Risk-Reward
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
deactivate

# Restart service
pm2 restart risk-reward
```

### Issue: 502 Bad Gateway

This means Nginx can't connect to the backend:

```bash
# Check if backend is running
pm2 status

# Check backend logs
pm2 logs risk-reward

# Restart backend
pm2 restart risk-reward

# Wait a few seconds and test
sleep 5
curl http://localhost:5000/
```

### Issue: File Not Found (data.csv, heatmap values.xlsx)

```bash
# Check if files exist
cd /var/www/vsfintech/Risk-Reward
ls -la data.csv
ls -la "heatmap values.xlsx"
ls -la index_name_mapping.py

# If missing, pull from git again
git pull origin main
```

---

## 📊 Monitoring & Maintenance

### View Real-time Logs

```bash
# PM2 logs
pm2 logs risk-reward --lines 100

# Nginx access logs
sudo tail -f /var/log/nginx/access.log | grep risk-reward

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Check Resource Usage

```bash
# PM2 monitoring dashboard
pm2 monit

# Memory and CPU usage
pm2 status
```

### Restart Service

```bash
# Restart PM2 service
pm2 restart risk-reward

# Restart with zero downtime
pm2 reload risk-reward

# Stop service
pm2 stop risk-reward

# Start service
pm2 start risk-reward
```

### Update Application

```bash
# Pull latest changes from GitHub
cd /var/www/vsfintech/Risk-Reward
git pull origin main

# Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt --upgrade
deactivate

# Restart service
pm2 restart risk-reward
```

---

## ✅ Deployment Checklist

- [ ] Code pulled from GitHub to `/var/www/vsfintech/Risk-Reward/`
- [ ] `app.py`, `data.csv`, `heatmap values.xlsx`, `index_name_mapping.py` present
- [ ] Python virtual environment created (`venv/`)
- [ ] Dependencies installed successfully
- [ ] Flask application tested locally
- [ ] PM2 process `risk-reward` running on port 5000
- [ ] Nginx configuration added for `/risk-reward` location
- [ ] Nginx config tested (`nginx -t`)
- [ ] Nginx reloaded successfully
- [ ] File permissions set correctly (www-data:www-data, 755)
- [ ] Port 5000 responding to requests
- [ ] Nginx proxy working at `/risk-reward/`
- [ ] API endpoints functional
- [ ] PM2 saved and set to auto-start
- [ ] Logs checked for errors

---

## 🎯 Quick Reference Commands

```bash
# Status
pm2 status
pm2 info risk-reward

# Logs
pm2 logs risk-reward
pm2 logs risk-reward --lines 100

# Control
pm2 restart risk-reward
pm2 stop risk-reward
pm2 start risk-reward
pm2 reload risk-reward  # Zero-downtime restart

# Monitoring
pm2 monit

# Nginx
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl status nginx

# Test
curl http://localhost:5000/
curl http://localhost:5000/api/metrics?duration=3years
curl http://82.25.105.18/risk-reward/

# Check port
sudo netstat -tulpn | grep 5000
sudo lsof -i :5000

# Update from Git
cd /var/www/vsfintech/Risk-Reward
git pull origin main
pm2 restart risk-reward
```

---

## 📞 Support & Next Steps

**Deployment Status:** Ready for deployment  
**Expected Result:** Risk-Reward accessible at http://82.25.105.18/risk-reward/

**GitHub Repository:** https://github.com/Manideepgadi1/Risk-Reward

**Next Steps:**
1. SSH to VPS: `ssh root@82.25.105.18`
2. Pull latest code: `cd /var/www/vsfintech/Risk-Reward && git pull origin main`
3. Run deployment script: `sudo ./deploy.sh`
4. Verify endpoints are working
5. Test integration with main platform

---

**Ready to deploy!** Run the automated script or follow the manual deployment steps.
