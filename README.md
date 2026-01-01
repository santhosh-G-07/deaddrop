# DeadDrop

> A lightweight, password-protected text collaboration board for asynchronous note sharing.

## What It Is

A minimalist, stealth-mode message board that looks like a system status page. Behind a simple access code lies a shared notepad where anyone with the code can read and append messages. No usernames, no chat bubbles, no timestamps — just clean text lines organized by date.

## Features

- 🖤 **Ultra-minimal black design** - Looks like a boring system monitor
- 🚪 **Multi-room support** - Each code creates a separate private room
- 🔒 **Infinite private rooms** - Use different codes for different conversations
- 📝 **Asynchronous messaging** - Not a chat, just a shared notepad
- 📅 **Daily organization** - Messages grouped by today's date
- 👻 **No user tracking** - No names, no metadata, just text
- 🔄 **Manual refresh** - Press F5 to see updates (no WebSockets)

## Tech Stack

- **Backend**: Django 5.0.1
- **Database**: SQLite
- **Frontend**: Vanilla HTML/CSS/JS
- **Styling**: Pure CSS (no frameworks)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and customize:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ACCESS_CODE=2203
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 5. Start Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000`

## Usage

1. **Landing Page**: You'll see a black page with "SYSTEM STATUS: OK" and a tiny green dot
2. **Access**: Click the dot, enter ANY code (minimum 4 characters)
3. **Room Created**: Your code creates/accesses a private room
4. **Board**: View today's messages in that room
5. **Post**: Type in the bottom input area, press Enter to send
6. **Refresh**: Press F5 to see new messages from others in the same room
7. **Switch Rooms**: Logout and enter a different code to access another room

## How Multi-Room Works

**Each code creates a completely separate, private room.**

### Examples:

- **Code `2203`** → Private room for you + girlfriend
- **Code `1234`** → Different room for you + friend
- **Code `work99`** → Another room for work team
- **Code `secret`** → Yet another isolated space

### Key Points:

✅ **No pre-configuration needed** - Just enter any code (min 4 characters)  
✅ **First use creates the room** - The first person to use a code creates that room  
✅ **Complete isolation** - Messages in room `2203` are invisible to room `1234`  
✅ **Unlimited rooms** - Create as many as you want with different codes  
✅ **Same code = same room** - Anyone with code `2203` sees the same messages

### Usage Example:

```
You + GF:
  1. Both enter code: 2203
  2. Chat privately in that room
  3. Only people with "2203" can see these messages

You + Friend:
  1. Both enter code: 1234
  2. Completely different conversation
  3. Your GF can't see this (she doesn't have "1234")

You + Work Team:
  1. All enter code: team2026
  2. Separate workspace
  3. Isolated from your other rooms
```

**Think of each code as a key to a different room. No key = no access.**

## Deployment

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn deaddrop.wsgi:application`
5. Add environment variables from `.env`

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Environment Variables for Production

```
SECRET_KEY=<generate-a-strong-secret-key>
DEBUG=False
ACCESS_CODE=<your-access-code>
ALLOWED_HOSTS=yourdomain.com
```

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use a strong, unique access code
- Consider using HTTPS (automatic on Railway/Render/Fly.io)
- This is NOT end-to-end encrypted
- Messages are stored in plain text in the database

## Project Structure

```
deaddrop/
├── board/                  # Main app
│   ├── models.py          # Message model
│   ├── views.py           # Landing, validation, board views
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin interface
│   └── templates/
│       └── board/
│           ├── landing.html   # Black landing page
│           └── board.html     # Message board
├── deaddrop/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .env                   # Your config (not in git)
└── .env.example          # Template
```

## Design Philosophy

**Stealth**: Looks like a system status page or monitoring tool  
**Minimal**: No frameworks, no bloat, just HTML/CSS/JS  
**Multi-Room**: Infinite private spaces, one code per room  
**Asynchronous**: Not real-time chat, just a shared notepad  
**Anonymous**: No user accounts, no tracking  
**Simple**: Enter a code, get a room, share with others

## Legal Notice

This is a legitimate collaboration tool. Use responsibly and in accordance with your organization's policies. The developers are not responsible for misuse.

## License

MIT License - Use at your own risk

---

**Built for simplicity. Designed for silence.**
