
# 🔗 Flask URL Shortener

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-black?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)
[![Stars](https://img.shields.io/github/stars/LetnanGM/flask-url-shortener?style=social)](#)
[![Good First Issues](https://img.shields.io/badge/Good%20First%20Issues-Welcome%20👋-brightgreen)](#-good-first-issues)

> 🎓 **A beginner-friendly Flask project to learn web development by building a URL shortener service**

**Perfect for:**
- 👶 Learning Flask & Python backend
- 🔒 Understanding authentication from scratch
- 🤝 Your FIRST open-source contribution
- 📚 Real-world project experience

---

## 📋 Table of Contents

- [📖 Overview](#overview)
- [✨ Features](#features)
- [🧠 Why This Project?](#why-this-project)
- [🛠️ Tech Stack](#tech-stack)
- [⚡ Quick Start](#quick-start)
- [📚 Usage](#usage)
- [🤝 Contributing](#contributing)
- [🐛 Known Issues](#known-issues)
- [🎯 Beginner's Guide](#beginners-guide)
- [📄 License](#license)

---

## 📖 Overview {#overview}

A **learning-focused URL shortening service** built with Flask, designed to teach beginners how real web applications work.

This isn't just another URL shortener. It's built to **show you what's happening behind the scenes** - no magic, no hidden libraries, just pure Python.

### What You'll Learn

```
Long URL: https://example.com/very/long/path/to/article?id=123&ref=twitter
    ↓ (ShortenerURL)
Short URL: https://yoursite.com/a7K9m
```

---

## ✨ Features

| Feature | Description | Learning Value |
|---------|-------------|-----------------|
| 🔐 **Custom Authentication** | Built from scratch (no Flask-Login) | See how security really works |
| 📊 **URL Shortening** | Convert long URLs to short codes | Database + Logic design |
| 👤 **User Management** | Register, login, manage your URLs | Session handling |
| 📈 **Analytics** | Track clicks and URL performance | Data tracking & statistics |
| 🎨 **Clean UI** | Simple, responsive web interface | Frontend + Backend integration |
| 🧩 **Modular Code** | Well-organized architecture | Professional code structure |

---

## 🧠 Why This Project?

### For Beginners

```
❌ Most projects use Flask-Login (hides the magic)
✅ This project builds auth from scratch (shows the magic)

❌ You wonder: "How does session handling work?"
✅ You'll SEE it in the code!

❌ Other projects are too complex
✅ This one is beginner-friendly & real-world
```

### Philosophy: "Build It Yourself"

We intentionally avoid these libraries:
- ❌ Flask-Login
- ❌ Flask-Session
- ❌ Flask-SQLAlchemy (keeping it simple)

**Why?** Because understanding HOW something works is better than using it as a black box.

---

## 🛠️ Tech Stack

```
Frontend: HTML5 + CSS3 + JavaScript
Backend: Python + Flask
Database: SQLite (production-ready with PostgreSQL migration)
Security: Argon2 (password hashing)
Code Quality: Pydantic (data validation)
```

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/LetnanGM/flask-url-shortener.git
cd flask-url-shortener
```

### 2️⃣ Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings (optional for local development)
```

### 4️⃣ Run the Application

```bash
python main.py

# Visit: http://localhost:5000
# Done! 🎉
```

### ✅ Expected Output

```
 * Running on http://localhost:5000
 * Debug mode: on
```

---

## 📚 Usage

### For Users

1. **Register:** Create an account at `/register`
2. **Login:** Access your dashboard at `/login`
3. **Create Short URL:** Paste long URL, get short code
4. **Share:** Copy and share your shortened URL
5. **Track:** View analytics on your dashboard

### For Developers (API)

```bash
# Create shortened URL (POST)
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/very/long/path"}'

# Response:
{
  "short_url": "http://localhost:5000/a7K9m",
  "original_url": "https://example.com/very/long/path"
}
```

---

## 🤝 Contributing

### 🎯 We Need YOUR Help!

Even if you're a complete beginner, **you can contribute here!**

### ✅ Good First Issues

```bash
# Find beginner-friendly tasks:
# 1. Go to: Issues tab
# 2. Filter by label: "good-first-issue"
# 3. Pick one
# 4. Comment: "I want to work on this!"
```

### Examples of Contributions

✅ **Found a typo?** → Fix it!
✅ **Unclear documentation?** → Improve it!
✅ **Missing feature?** → Add it!
✅ **Better error messages?** → Write them!
✅ **UI improvement?** → Design it!

### 🛠️ How to Contribute

**1. Pick an issue**
```bash
# Look for issues labeled:
# - "good-first-issue" (perfect for beginners!)
# - "help-wanted"
# - "documentation"
```

**2. Fork & Clone**
```bash
git clone https://github.com/YOUR_USERNAME/flask-url-shortener.git
cd flask-url-shortener
```

**3. Create Feature Branch**
```bash
git checkout -b fix/issue-name
# Example: git checkout -b fix/add-password-validation
```

**4. Make Changes**
```bash
# Edit files
# Test locally
python main.py
```

**5. Commit & Push**
```bash
git add .
git commit -m "fix: Add password validation"
git push origin fix/issue-name
```

**6. Create Pull Request**
- Go to GitHub
- Click "Compare & Pull Request"
- Describe your changes
- Submit!

### 📖 Read First

Before contributing, please read:
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

## 🐛 Known Issues

| Issue | Status | Help Needed |
|-------|--------|-------------|
| ⚠️ Input validation incomplete | In progress | Fix: Form validation |
| ⚠️ Session expiration | Needs work | Add: Session timeout |
| ⚠️ Rate limiting | Planned | Add: Request throttling |
| ⚠️ Mobile UI refinement | Planned | Fix: Responsive design |
| ⚠️ Error messages unclear | Open | Improve: UX messages |

**See all issues:** [Issues tab](https://github.com/LetnanGM/flask-url-shortener/issues)

---

## 🎯 Beginner's Guide

### "I've never contributed to open source before..."

**No problem! Here's your step-by-step path:**

**Step 1: Fork (Make your copy)**
```
Go to: GitHub.com/LetnanGM/flask-url-shortener
Click: Fork (top right)
You now have your own copy!
```

**Step 2: Clone (Get it locally)**
```bash
git clone https://github.com/YOUR_USERNAME/flask-url-shortener.git
```

**Step 3: Pick an issue**
```
Go to: Issues tab
Filter by: "good-first-issue"
Pick one you like
Comment: "I'll work on this!"
```

**Step 4: Create a branch**
```bash
git checkout -b feature/your-feature-name
```

**Step 5: Make changes**
```bash
# Edit the code
# Test it locally
```

**Step 6: Commit**
```bash
git add .
git commit -m "Fix: Clear description of what you did"
```

**Step 7: Push to your fork**
```bash
git push origin feature/your-feature-name
```

**Step 8: Create Pull Request**
```
Go to GitHub
Click: "Compare & Pull Request"
Add description
Click: "Create Pull Request"
```

**Step 9: Wait for review**
```
We'll review your code
May ask for changes (that's normal!)
Once approved: MERGED! 🎉
```

### Common Questions

**Q: What if I make a mistake?**
A: No problem! That's how we learn. We'll guide you to fix it.

**Q: Do I need to be an expert?**
A: No! Beginners are welcome. We value contributions big and small.

**Q: What if I get stuck?**
A: Ask! Comment on your PR or issue. We're here to help.

---

## 🤖 Project Structure

```
flask-url-shortener/
│
├── application/          # Flask app & routes
│   ├── routes.py        # URL endpoints
│   ├── auth.py          # Authentication logic
│   └── models.py        # Data models
│
├── domain/              # Business logic
│   ├── shorten.py       # URL shortening logic
│   └── analytics.py     # Analytics calculations
│
├── infrastructure/      # Database & storage
│   ├── database.py      # Database connection
│   └── queries.py       # SQL queries
│
├── assets/              # Frontend files
│   ├── css/
│   └── js/
│
├── test/                # Tests
│   └── test_*.py
│
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── .env.example        # Config template
└── README.md           # This file!
```

---

## 📊 Project Stats

```
Language:    Python 🐍
Framework:   Flask ⚡
Size:        Beginner-friendly (learning project)
Status:      Active & Growing 📈
Contributors: WELCOME! 🤝
```

---

## ⭐ Stars & Community

If this project helped you learn, please give it a star! ⭐

**It helps:**
- 📈 More people discover the project
- 🤝 Build our community
- 💪 Motivate contributions

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

**In simple terms:** You can use this code for anything, just mention us. 😊

---

## 🙏 Acknowledgments

- 👥 All contributors
- 📚 Flask documentation
- 🎓 Open source community

---

## 📞 Contact & Questions

Have questions? 
- 💬 Comment on issues
- 📧 Check CONTRIBUTING.md
- 🤝 Join our discussions

---

## 🚀 What's Next?

Check out [Planned Features](CHANGELOG.md#unreleased) to see what we're working on!

Want to propose a feature? → Create an issue!

---

**Made with ❤️ for beginners, by developers who remember learning.**

```
       /\_/\
      ( o.o )
       > ^ <
      /|   |\
     (_|   |_)
```

Happy coding! ❤