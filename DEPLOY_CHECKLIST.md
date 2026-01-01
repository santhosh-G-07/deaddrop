# 🚀 Quick Deployment Checklist

## Files Ready for Deployment ✅

Your DeadDrop project is now ready to deploy! Here's what was prepared:

### Configuration Files Created:
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `build.sh` - Build script for deployment
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Configured for production
- ✅ `.gitignore` - Prevents sensitive files from being committed

### Production Dependencies Added:
- ✅ `gunicorn` - Production web server
- ✅ `whitenoise` - Static file serving

---

## Next Steps (5 Minutes to Deploy):

### 1. Push to GitHub (2 minutes)
```bash
cd e:\chat
git init
git add .
git commit -m "DeadDrop - Multi-room stealth chat"
```

Then create a repo on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/deaddrop.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render (3 minutes)
1. Go to [render.com](https://render.com) and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn deaddrop.wsgi:application`
   - **Instance Type**: Free
5. Add environment variables:
   - `SECRET_KEY`: (generate a random string)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
6. Click "Create Web Service"

### 3. Wait for Deployment (5-10 minutes)
Render will automatically:
- Install dependencies
- Run database migrations
- Collect static files
- Start your app

### 4. Access Your App
Visit: `https://your-app-name.onrender.com`

---

## Environment Variables You'll Need:

Copy these to Render's environment variables section:

```
SECRET_KEY=CHANGE-THIS-TO-A-LONG-RANDOM-STRING-50-CHARS
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

**IMPORTANT**: Replace `your-app-name` with your actual Render app name!

---

## Testing After Deployment:

1. ✅ Visit your Render URL
2. ✅ Click the green dot
3. ✅ Enter code `2203`
4. ✅ Post a test message
5. ✅ Click top-left dot to switch rooms
6. ✅ Enter code `1234`
7. ✅ Verify it's a different room
8. ✅ Share codes with friends!

---

## Free Tier Details:

**What You Get FREE:**
- ✅ 750 hours/month (24/7 uptime)
- ✅ HTTPS automatically
- ✅ Automatic deployments
- ✅ Unlimited room codes
- ✅ Unlimited messages

**Limitations:**
- ⚠️ App sleeps after 15 min inactivity
- ⚠️ First request after sleep: ~30 sec wake time
- ⚠️ 512 MB RAM (plenty for this app)

---

## Alternative: One-Click Deploy

If you want even faster deployment, you can also use:

### Railway.app
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

### Fly.io
```bash
fly launch
fly deploy
```

---

## Need Help?

Read the full guide: `DEPLOYMENT.md`

---

**Your app is ready to go live! 🎉**

Total time to deploy: ~10 minutes
Total cost: $0/month
