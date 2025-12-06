# Risk-Reward VPS Deployment Guide

## Server Information
- **VPS IP:** 82.25.105.18
- **URL:** http://82.25.105.18/risk-reward/
- **Backend Port:** 8003
- **Deploy Location:** /var/www/risk-reward/

---

## STEP 1: LOCAL PREPARATION (Windows PowerShell)

### 1.1 Verify all files are committed
```powershell
cd "D:\Risk reward - Copy"
git status
git add .
git commit -m "Prepare for VPS deployment"
git push origin main
```

---

## STEP 2: VPS SETUP (SSH into Ubuntu)

### 2.1 Connect to VPS
```powershell
ssh root@82.25.105.18
```

### 2.2 Navigate to web directory
```bash
cd /var/www
```

### 2.3 Clone the repository
```bash
git clone https://github.com/Manideepgadi1/Risk-Reward.git risk-reward
cd risk-reward
```

### 2.4 Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.5 Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 2.6 Test the application locally
```bash
python app.py
# Press Ctrl+C to stop after verifying it works
```

---

## STEP 3: CREATE SYSTEMD SERVICE

### 3.1 Create service file
```bash
sudo nano /etc/systemd/system/risk-reward.service
```

### 3.2 Add this content:
```ini
[Unit]
Description=Risk-Reward Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/risk-reward
Environment="PATH=/var/www/risk-reward/venv/bin"
ExecStart=/var/www/risk-reward/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8003 wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3.3 Enable and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable risk-reward
sudo systemctl start risk-reward
sudo systemctl status risk-reward
```

---

## STEP 4: CONFIGURE NGINX

### 4.1 Backup current Nginx config
```bash
sudo cp /etc/nginx/sites-available/combined /etc/nginx/sites-available/combined.backup
```

### 4.2 Edit Nginx configuration
```bash
sudo nano /etc/nginx/sites-available/combined
```

### 4.3 Add this location block (before the closing server bracket)
```nginx
    # Risk-Reward Application
    location /risk-reward/ {
        proxy_pass http://127.0.0.1:8003/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
```

### 4.4 Test and reload Nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## STEP 5: UPDATE LANDING PAGE

### 5.1 Edit the landing page
```bash
sudo nano /var/www/html/index.html
```

### 5.2 Add this link in the appropriate section:
```html
<li><a href="/risk-reward/">Risk-Reward Analysis</a> - Financial metrics and heatmap visualization</li>
```

---

## STEP 6: VERIFY DEPLOYMENT

### 6.1 Check service status
```bash
sudo systemctl status risk-reward
```

### 6.2 Check logs if needed
```bash
sudo journalctl -u risk-reward -n 50 --no-pager
```

### 6.3 Test the application
Open browser: http://82.25.105.18/risk-reward/

---

## UPDATING THE APPLICATION

When you push updates to GitHub:

```bash
ssh root@82.25.105.18
cd /var/www/risk-reward
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # if dependencies changed
sudo systemctl restart risk-reward
```

---

## TROUBLESHOOTING

### Check if port 8003 is listening
```bash
sudo netstat -tlnp | grep 8003
```

### View real-time logs
```bash
sudo journalctl -u risk-reward -f
```

### Check Nginx error logs
```bash
sudo tail -f /var/nginx/error.log
```

### Restart all services
```bash
sudo systemctl restart risk-reward
sudo systemctl reload nginx
```
