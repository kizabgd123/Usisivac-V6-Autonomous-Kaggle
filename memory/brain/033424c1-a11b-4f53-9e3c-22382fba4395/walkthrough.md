# Walkthrough - Trinity AI Personal Organization System

I have successfully implemented your local "Trinity AI Personal Organization System". Below is a guide on how to get it running and what it does.

## 🚀 Setup Instructions

1. **Install Dependencies**:
   Run the following command in your terminal within the project directory:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   Open `.env.example`, fill in your actual API keys, and rename it to `.env`:
   ```bash
   mv .env.example .env
   ```

3. **Run the System**:
   Start the organizer with:
   ```bash
   python main.py
   ```

## 📂 Folder Structure
The system has automatically created (or verified) the following structure in `~/Kiza/desktop`:
- `Inbox/` (Drop your files here)
- `Kaggel takmicenj/`
- `Work i work log/`
- `Learning/`
- `Archive/`
- `Teme diskusije/`
- `razno/`

## 🧠 Intelligence Pipeline
When a file enters the `Inbox`:
1. **Mistral**: Extracts text/metadata and performs initial categorization.
2. **Grok**: If the file is related to Kaggle or programming, Grok extracts hyper-parameters or strategic insights.
3. **OpenRouter (Llama 3 8B Free)**: Reviews the data from Mistral and Grok to make the final decision on the destination folder.
4. **Notion**: Logs the move, including the file name, category, summary, Grok insight, date, and local path.

## 🔍 Observability (Arize Tracing)
The system is now instrumented with **OpenTelemetry** and sends traces to **Arize**. This allows you to:
- Monitor the latency of each AI provider (Mistral, Grok, OpenRouter).
- Audit prompt and completion tokens used.
- Visualize the decision-making chain for every file in your `Inbox`.

**Setup for Tracing**:
1. Ensure `ARIZE_SPACE_ID` and `ARIZE_API_KEY` are set in your `.env` file.
2. Traces will automatically appear in your Arize project named `trinity-organizer`.

## ⚙️ Trigger Mechanisms
- **Real-time (Watchdog)**: Processes files the instant they are added to the `Inbox`.
- **Periodic Fallback**: Scans the `Inbox` every 5 hours to ensure no files are missed due to system downtime or missed events.

## ✅ Validation Results
- **Folder Initialization**: Verified that `~/Kiza/desktop` and its sub-folders are correctly created.
- **Code Integrity**: `main.py` has been checked for syntax errors and is ready for use.
- **Robustness**: API calls are wrapped in `try-except` blocks to prevent the system from crashing if one service is down.
