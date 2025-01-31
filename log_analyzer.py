import streamlit as st
import pandas as pd
import re
import json
import matplotlib.pyplot as plt
import io
import datetime

# Streamlit App
st.title("📜 Log Analyzer")

# Datei-Upload mit Drag & Drop, Limit: 15MB pro Datei
uploaded_files = st.file_uploader(
    "📂 Drag and Drop files here (max. 15MB per file)",
    type=["log", "txt", "json"],
    accept_multiple_files=True
)

# Max. Dateigröße pro Datei: 15MB
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB in Bytes

# Standardisiere `filtered_df`, um Fehler zu vermeiden
filtered_df = pd.DataFrame(columns=["Timestamp", "Level", "Message"])

if uploaded_files:
    logs = []
    detected_formats = {}

    for uploaded_file in uploaded_files:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"❌ Datei {
                     uploaded_file.name} ist zu groß! Bitte laden Sie eine Datei unter 15MB hoch.")
            st.stop()

        stringio = io.StringIO(
            uploaded_file.getvalue().decode(errors="ignore"))
        file_lines = list(stringio.readlines())
        logs.extend(file_lines)

        # Reguläre Ausdrücke für verschiedene Log-Formate
        log_patterns = {
            "Java": re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\w+) ([\w\.\[\]]+) (.+)"),
            "Apache/Nginx": re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.+)\] "(\w+) (.+?)" (\d{3}) (\d+)'),
            "Docker": re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z) (\w+) (\w) (.+)"),
            "System": re.compile(r'([A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2}) (\S+) (\S+)\[\d+\]: (.+)'),
            "Python": re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\S+) - (\w+) - (.+)"),
            "Custom": re.compile(r"(\w+) \| (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| (.+)")
        }

        # JSON Log-Parser
        def parse_json_log(line):
            try:
                log_entry = json.loads(line)
                return "JSON Logs"
            except json.JSONDecodeError:
                return None

        # Format für die Datei bestimmen
        detected_format = "Unbekannt"
        for line in file_lines:
            if parse_json_log(line):
                detected_format = "JSON Logs"
                break
            for format_name, pattern in log_patterns.items():
                if pattern.match(line):
                    detected_format = format_name
                    break
            if detected_format != "Unbekannt":
                break

        detected_formats[uploaded_file.name] = detected_format

    # Zeige die erkannten Log-Formate
    st.subheader("📑 Erkannte Log-Formate")
    for file_name, log_format in detected_formats.items():
        st.write(f"✅ **{file_name}** → {log_format}")

    log_data = []
    log_levels = {"INFO": 0, "WARNING": 0,
                  "ERROR": 0, "DEBUG": 0, "CRITICAL": 0}

    for line in logs:
        parsed = None

        # JSON-Parsing versuchen
        json_log = parse_json_log(line)
        if json_log:
            parsed = {"Timestamp": "Unbekannt",
                      "Level": "INFO", "Message": line}
        else:
            # Teste reguläre Ausdrücke
            for pattern in log_patterns.values():
                match = pattern.match(line)
                if match:
                    parsed = match.groups()
                    break

        if parsed:
            if isinstance(parsed, dict):
                log_data.append(parsed)
            else:
                timestamp = parsed[0] if len(parsed) > 0 else "Unbekannt"
                level = parsed[1].upper() if len(parsed) > 1 else "INFO"
                message = parsed[-1] if len(
                    parsed) > 2 else "Unbekannte Nachricht"

                if level not in log_levels:
                    level = "INFO"

                log_data.append(
                    {"Timestamp": timestamp, "Level": level, "Message": message})
                log_levels[level] += 1

    df = pd.DataFrame(log_data)

    if not df.empty:
        st.subheader("📜 Letzte Log-Einträge")
        st.dataframe(df.tail(20))

        # Filter nach Log-Level oder Suchbegriff
        st.subheader("🔎 Logs durchsuchen")
        log_level_filter = st.selectbox(
            "Filtern nach Log-Level", ["Alle"] + list(log_levels.keys()))
        search_query = st.text_input(
            "🔍 Nach Schlüsselwörtern filtern (z. B. 'Fehler, Database')")

        filtered_df = df
        if log_level_filter != "Alle":
            filtered_df = filtered_df[filtered_df["Level"] == log_level_filter]

        if search_query:
            search_terms = [term.strip() for term in search_query.split(",")]
            regex_pattern = "|".join(search_terms)
            filtered_df = filtered_df[filtered_df["Message"].str.contains(
                regex_pattern, case=False, na=False)]

        num_logs = st.slider(
            "Anzahl der anzuzeigenden letzten Einträge", 5, 100, 20)
        st.dataframe(filtered_df.tail(num_logs))

        # Export als `.log` Datei
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"logs_{timestamp}.log"

        # Konvertiere gefilterte Logs in Textformat
        log_content = "\n".join(filtered_df.apply(
            lambda row: f"{row['Timestamp']} - {row['Level']} - {row['Message']}", axis=1
        ))

        # Erstelle die Datei als Download
        log_bytes = log_content.encode("utf-8")
        st.download_button("📥 Gefilterte Logs herunterladen",
                           log_bytes, log_filename, "text/plain")

else:
    st.info("Bitte laden Sie mindestens eine Log-Datei hoch, um die Analyse zu starten.")
