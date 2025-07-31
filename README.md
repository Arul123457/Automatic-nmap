# Automatic-nmap

**Automatic NMAP Report & Screenshot Tool** is a powerful automation utility that:

- Parses Nmap XML output
- Extracts open ports per host
- Generates individual URLs (e.g., `http://ip:port`)
- Captures screenshots of each service using Selenium
- Filters unreachable or error pages
- Generates a professional Excel report with embedded screenshots

---

## 🖥 Setup Instructions

### ✅ Requirements

- Python 3.10+
- Google Chrome or Chromium
- ChromeDriver matching your browser version

---

### 💻 Windows Setup

1. **Install Python 3.10+**

   - [Download Python](https://www.python.org/downloads/windows/)
   - During installation, check ✅ `Add Python to PATH`

2. **Install Google Chrome**

   - [Download Chrome](https://www.google.com/chrome/)

3. **Install ChromeDriver**

   - Check your Chrome version:  
     Open `chrome://settings/help`
   - [Download matching ChromeDriver](https://chromedriver.chromium.org/downloads)
   - Extract and move `chromedriver.exe` to your project folder or add to PATH

4. **Run the Tool**

   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

5. **Open Browser**  
   Navigate to: [http://localhost:5000](http://localhost:5000)

---

### 🐧 Linux Setup (Ubuntu / Kali / Debian)

1. **Install Python 3.10+**

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

2. **Install Google Chrome**

   ```bash
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt install ./google-chrome-stable_current_amd64.deb
   ```

3. **Install ChromeDriver**

   - Check Chrome version:
     ```bash
     google-chrome --version
     ```
   - Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
   - Extract and move it:
     ```bash
     unzip chromedriver_linux64.zip
     sudo mv chromedriver /usr/local/bin/
     chmod +x /usr/local/bin/chromedriver
     ```

4. **Install Dependencies and Run**

   ```bash
   cd backend
   pip install -r requirements.txt
   python3 main.py
   ```

5. **Access the Tool**  
   Visit: [http://localhost:5000](http://localhost:5000)

---

### 🧪 Headless Server Mode (Linux-only)

If running on a headless server (no GUI), use `Xvfb`:

```bash
sudo apt install xvfb
xvfb-run -a python3 main.py
```

---

## 🤝 Contributing

We welcome contributions!  
- Fork the repo  
- Create a feature branch:  
  ```bash
  git checkout -b feature-name
  ```
- Commit your changes  
- Submit a Pull Request

If you have ideas or feature requests, feel free to open an [issue](https://github.com/Arul123457/Automatic-nmap/issues).