# Deployment Guide for Hostinger VPS

## Prerequisites
- Hostinger VPS plan (KVM 1 or higher)
- A domain name (optional, can use IP address)

---

## Step 1: Purchase Hostinger VPS

1. Go to https://www.hostinger.com/vps-hosting
2. Choose **KVM 1** plan (~$5.99/month) or higher
3. During setup, select **Ubuntu 22.04** as OS
4. Set a strong root password
5. Note down your **VPS IP address** after purchase

---

## Step 2: Connect to Your VPS

### On Windows (PowerShell):
```powershell
ssh root@YOUR_VPS_IP
```
Enter your root password when prompted.

### If SSH is blocked, use Hostinger's web terminal:
1. Go to Hostinger hPanel
2. Click on your VPS
3. Click "Terminal" or "Console"

---

## Step 3: Set Up Server (Run on VPS)

Copy and paste these commands one by one:

```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install python3 python3-pip python3-venv nginx -y

# Create app directory
mkdir -p /var/www/riskapp

# Set permissions
chown -R www-data:www-data /var/www/riskapp
```

---

## Step 4: Upload Your Files

### Option A: Using SCP (from your Windows PowerShell)
```powershell
cd "D:\Risk reward - Copy"
scp -r * root@YOUR_VPS_IP:/var/www/riskapp/
```

### Option B: Using FileZilla (SFTP)
1. Download FileZilla: https://filezilla-project.org/
2. Connect using:
   - Host: sftp://YOUR_VPS_IP
   - Username: root
   - Password: your_root_password
   - Port: 22
3. Navigate to /var/www/riskapp/ on the server
4. Upload all files from "D:\Risk reward - Copy\"

---

## Step 5: Install Python Dependencies (Run on VPS)

```bash
cd /var/www/riskapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask pandas numpy gunicorn
```

---

## Step 6: Set Up Systemd Service (Run on VPS)

```bash
# Copy service file
cp /var/www/riskapp/riskapp.service /etc/systemd/system/

# Set permissions
chown -R www-data:www-data /var/www/riskapp

# Reload systemd
systemctl daemon-reload

# Enable and start the service
systemctl enable riskapp
systemctl start riskapp

# Check if it's running
systemctl status riskapp
```

---

## Step 7: Configure Nginx (Run on VPS)

```bash
# Edit nginx config - replace YOUR_DOMAIN_OR_IP in the file
nano /var/www/riskapp/nginx.conf
```

Replace `YOUR_DOMAIN_OR_IP` with your actual domain or VPS IP address, then:

```bash
# Copy to nginx sites
cp /var/www/riskapp/nginx.conf /etc/nginx/sites-available/riskapp

# Enable the site
ln -s /etc/nginx/sites-available/riskapp /etc/nginx/sites-enabled/

# Remove default site
rm /etc/nginx/sites-enabled/default

# Test nginx config
nginx -t

# Restart nginx
systemctl restart nginx
```

---

## Step 8: Open Firewall Ports (Run on VPS)

```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
```

---

## Step 9: Access Your App!

Open your browser and go to:
```
http://YOUR_VPS_IP
```

Or if you have a domain:
```
http://yourdomain.com
```

---

## Optional: Add SSL (HTTPS)

```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate (replace with your domain)
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
```

---

## Troubleshooting

### Check if app is running:
```bash
systemctl status riskapp
```

### View app logs:
```bash
journalctl -u riskapp -f
```

### Restart app after making changes:
```bash
systemctl restart riskapp
```

### Check nginx logs:
```bash
tail -f /var/log/nginx/error.log
```

---

## Updating Your App

1. Upload new files via SCP or FileZilla
2. Restart the service:
```bash
systemctl restart riskapp
```

---

## Monthly Cost Estimate
- Hostinger VPS KVM 1: ~$5.99/month
- Domain (optional): ~$10-15/year

