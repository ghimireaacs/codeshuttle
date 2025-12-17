# CodeShuttle 🚀

**CodeShuttle** is a minimalistic pastebin and file-sharing web app built with Flask.  
It supports text snippets, logs, and file attachments, with a modern brutalist-inspired UI and dark/light mode toggle.

---

## Features

- Paste text or upload files
- Copy text to clipboard with one click
- Dark/Light theme toggle (stored in browser)
- Responsive brutalist-inspired UI
- File attachments with download links
- SQLite backend for easy local deployment
- Dockerized for quick deployment


---

## Screenshot

![CodeShuttle Screenshot](static/screenshot.gif)

---

## Quick Start (Docker)

### **Option 1: Run from GHCR (Recommended)**

You have a pre-built image hosted on GitHub Container Registry:

```bash
docker pull ghcr.io/ghimireaacs/codeshuttle:latest
docker run -d -p 5000:8000 \
  -v /home/ghost/ghostsilo/20_Temporary/:/app/data \
  --name codeshuttle \
  ghcr.io/ghimireaacs/codeshuttle:latest
````

* Access the app: [http://localhost:5000](http://localhost:5000)

---

### **Option 2: Build Locally**

```bash
git clone https://github.com/ghimireaacs/codeshuttle.git
cd codeshuttle

docker build -t codeshuttle:latest .
docker run -d -p 5000:8000 \
  -v /home/ghost/ghostsilo/20_Temporary/:/app/data \
  --name codeshuttle \
  codeshuttle:latest
```

---

## Folder Structure

```
.
├── app.py               # Flask application
├── requirements.txt
├── Dockerfile
├── docker-compose.yml   # Optional
├── templates/
│   └── index.html
├── static/
│   └── (CSS/JS optional)
├── data/
│   └── uploads/         # Uploaded files
├── icon.png             # App icon
└── screenshot.png       # App screenshot
```

---

## License

MIT License © ghimireaacs
