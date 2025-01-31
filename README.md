# 📜 Log Analyzer

A powerful and user-friendly web application built with Streamlit for analyzing various types of log files. This tool supports multiple log formats and provides interactive filtering and visualization capabilities.

## 🌟 Features

- 📁 Support for multiple log file formats:
  - Java logs
  - Apache/Nginx logs
  - Docker logs
  - System logs
  - Python logs
  - Custom format logs
  - JSON logs
- 🔍 Interactive log filtering by:
  - Log level (INFO, WARNING, ERROR, DEBUG, CRITICAL)
  - Custom search keywords
- 📊 Real-time log analysis
- 📥 Export filtered logs to .log files
- 💡 Automatic log format detection
- 🎯 Support for multiple file uploads (up to 15MB per file)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hadzicni/Log-Analyser.git
cd Log-Analyser
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run log_analyzer.py
```

The application will open in your default web browser.

## 💻 Usage

1. Open the application in your web browser
2. Drag and drop your log files (supported formats: .log, .txt, .json)
3. The application will automatically detect the log format
4. Use the filters to analyze specific log levels or search for keywords
5. Export filtered logs using the download button

## 🛠️ Supported Log Formats

### Java
```
2024-01-31 10:15:30,123 INFO com.example.Class Message
```

### Apache/Nginx
```
192.168.1.1 - - [31/Jan/2024:10:15:30 +0000] "GET /path HTTP/1.1" 200 1234
```

### Docker
```
2024-01-31T10:15:30.123Z INFO N Message
```

### System
```
Jan 31 10:15:30 hostname service[123]: Message
```

### Python
```
2024-01-31 10:15:30,123 - module - INFO - Message
```

### Custom
```
LEVEL | 2024-01-31 10:15:30 | Message
```

### JSON
```json
{"timestamp": "2024-01-31T10:15:30.123Z", "level": "INFO", "message": "Log message"}
```

## 📋 Dependencies

- streamlit
- pandas
- matplotlib
- python-dateutil

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Nikola Hadzic
