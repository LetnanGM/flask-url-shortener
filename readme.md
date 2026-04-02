# Flask URL Shortener With Custom Library

## Table of Contents

- [OverView](#overview)
- [About](#about)
- [Features](#-features)
- [Philosophy](#philosophy)
- [TechStack](#️-tech-stack)
- [Installtion](#installing)
- [Usage](#usage)
- [knownIssue](#️-known-issues)
- [Begginer?](#-who-is-this-for)
- [Contributing](CONTRIBUTING.md)
- [LICENSE](LICENSE.md)

## 🚀 Project Overview <a name="overview"></a>

This project is designed as a learning-focused backend system, helping developers understand how core features like authentication, session handling, and URL redirection work internally.

Unlike most Flask projects, this repository intentionally avoids external authentication plugins to keep everything transparent and easy to follow.

## About <a name = "about"></a>

ShortenerURL as like urlshort, s(.)id or something like them, make long or UGLY URL into short and beautiful, no need write long URL, just short it and share.

## ✨ Features <a name="features"></a>

URL shortening system

- Custom authentication system (no Flask-Login, no Flask-Session)
- Session handling using manual implementation
- Modular backend architecture
- Simple and readable codebase
- Designed for learning and contribution

## 🧠 Project Philosophy <a name="philosophy"></a>

This project follows a "build it yourself" approach.

We intentionally avoid external Flask authentication/session plugins such as:

- Flask-Login

- Flask-Session

# Why?

- To understand how authentication systems work internally

- To avoid hidden abstractions

- To keep the code beginner-friendly and transparent

Contributions that align with this philosophy are highly appreciated.

## 🛠️ Tech Stack <a name="techStack"></a>

- Python

- Flask

- Pydantic

- Argon2 (for password hashing)

### Installing <a name="installation"></a>

A step by step how to clone this repo and place it to your machine.

clone this repo

```
git clone https://github.com/LetnanGM/flask-url-shortener.git
```

change directory to workspace.

```
cd flask-url-shortener
```

run app or open it on your IDE

```run app
python app.py
```

## 📌 Usage <a name = "usage"></a>

- Access web interface via `/login`, `/register`, `/dashboard`

- Use API endpoints under `/api/\*`

- Shortened URLs are accessed via `/`<slug>

## ⚠️ Known Issues <a name="knownIssue"></a>

- Some endpoints lack input validation

- Authentication system is still evolving

- No rate limiting yet

- Session system is basic (no expiration handling)
- Protection Custom PLUGIN is still evolving

## 🎯 Who Is This For? <a name="whoIsThisFor"></a>

- Beginners learning Flask backend development

- Developers exploring how authentication works internally

- Contributors looking for a real-world beginner-friendly project

## 🤝 Contributing <a name="Contributing"></a>

Contributions are welcome! Please read the guidelines in CONTRIBUTING.md before submitting.

## 📄 License

This project is open-source and available under the MIT License.
