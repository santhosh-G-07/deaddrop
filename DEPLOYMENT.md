# DeadDrop - Render Deployment Guide

## 🚀 Deploy to Render (FREE)

Follow these steps to deploy your DeadDrop application to Render.com for free.

---

## Prerequisites

1. **GitHub Account** (free)
2. **Render Account** (free) - Sign up at [render.com](https://render.com)
3. **Git installed** on your computer

---

## Step 1: Push Code to GitHub

### 1.1 Initialize Git Repository

```bash
cd e:\chat
git init
git add .
git commit -m "Initial commit - DeadDrop multi-room chat"
```

### 1.2 Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **"New repository"**
3. Name it: `deaddrop` (or any name you want)
4. **DO NOT** initialize with README (we already have code)
5. Click **"Create repository"**

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/deaddrop.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 2: Deploy on Render

### 2.1 Create New Web Service

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Select your `deaddrop` repository
5. Click **"Connect"**

### 2.2 Configure Web Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `deaddrop` (or any name) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn deaddrop.wsgi:application` |
| **Instance Type** | **Free** |

### 2.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `your-super-secret-key-change-this-now` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `PYTHON_VERSION` | `3.11.0` |

**IMPORTANT**: 
- Replace `your-app-name` with your actual Render app name
- Generate a strong SECRET_KEY (use a password generator)

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Render will:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

---

## Step 3: Access Your App

Once deployed, your app will be available at:

```
https://your-app-name.onrender.com
```

**Test it:**
1. Visit the URL
2. Click the green dot
3. Enter any code (e.g., `2203`)
4. Start using your multi-room chat!

---

## Step 4: Share with Others

### Option 1: Direct Link
Share: `https://your-app-name.onrender.com`

### Option 2: Custom Domain (Optional)
1. Buy a domain (e.g., `status-checker.xyz`)
2. In Render dashboard → **"Settings"** → **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed

---

## Important Notes

### Free Tier Limitations

✅ **What's Included:**
- Free hosting forever
- HTTPS automatically enabled
- Automatic deployments from GitHub
- 750 hours/month (enough for 24/7)

⚠️ **Limitations:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 512 MB RAM (plenty for this app)

### Keeping App Awake (Optional)

If you want instant access, upgrade to paid tier ($7/month) or use a ping service:
- [UptimeRobot](https://uptimerobot.com) - Free, pings your app every 5 minutes
- [Cron-job.org](https://cron-job.org) - Free scheduled pings

---

## Updating Your App

When you make changes:

```bash
git add .
git commit -m "Your update message"
git push
```

Render will automatically redeploy!

---

## Troubleshooting

### Build Failed

Check the build logs in Render dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Syntax errors in code
- Database migration issues

### App Not Loading

1. Check environment variables are set correctly
2. Verify `ALLOWED_HOSTS` includes your Render URL
3. Check logs in Render dashboard

### Database Issues

Render uses SQLite by default. For production, consider upgrading to PostgreSQL:
1. In Render, create a PostgreSQL database (free tier available)
2. Update `settings.py` to use PostgreSQL
3. Add `psycopg2-binary` to `requirements.txt`

---

## Security Recommendations

### For Production Use:

1. **Strong SECRET_KEY**: Use a 50+ character random string
2. **Unique Room Codes**: Use long, random codes (e.g., `gf_secret_2026_xyz`)
3. **HTTPS Only**: Render provides this automatically
4. **Regular Updates**: Keep Django and dependencies updated
5. **Backup Database**: Download SQLite file regularly from Render

---

## Cost Summary

| Service | Cost |
|---------|------|
| Render Free Tier | **$0/month** |
| GitHub (public repo) | **$0/month** |
| Domain (optional) | ~$10/year |
| **Total (minimum)** | **$0/month** |

---

## Alternative Deployment Options

If Render doesn't work for you:

### Railway.app
- Similar to Render
- Free tier: 500 hours/month
- Deploy: `railway up`

### Fly.io
- Free tier: 3 VMs
- Global edge network
- Deploy: `fly launch`

### PythonAnywhere
- Free tier available
- Good for beginners
- Manual setup required

---

## Support

If you encounter issues:

1. Check Render logs: Dashboard → Your Service → Logs
2. Review Django errors in logs
3. Verify environment variables
4. Test locally first: `python manage.py runserver`

---

## Next Steps After Deployment

1. ✅ Test all room codes work
2. ✅ Share URL with trusted people only
3. ✅ Create different room codes for different groups
4. ✅ Set up UptimeRobot to keep app awake (optional)
5. ✅ Consider custom domain for stealth (optional)

---

**Your DeadDrop is now live and accessible worldwide! 🎉**

Share room codes privately and enjoy your stealth multi-room chat system.
