# Implementation Plan - Trinity AI Personal Organization System

This plan outlines the steps to build a local AI-driven file organization system that monitors an `Inbox` folder and routes files to specific categories using Mistral, Grok, and OpenRouter APIs, while logging all actions to Notion.

## User Review Required

> [!IMPORTANT]
> The folder names will be created exactly as requested (e.g., `Kaggel takmicenj/` with spaces). If you prefer underscores (e.g., `Kaggel_takmicenj/`), please let me know.
> The system will use `~/Kiza/desktop` as the base directory. Please ensure this path is accessible.
> API keys from `.env` will be used. Ensure yours are updated.

## Proposed Changes

### Configuration
- Update variable names to match `main.py` and the prompt requirements (`MISTRAL_API_KEY`, `GROK_API_KEY`, `OPENROUTER_API_KEY`, `NOTION_API_KEY`, `NOTION_DATABASE_ID`).
- Add Arize credentials: `ARIZE_SPACE_ID`, `ARIZE_API_KEY`.

#### [MODIFY] [requirements.txt](file:///home/kizabgd/Desktop/Istrazivanje/trinity_organizer/requirements.txt)
- Ensure all dependencies are listed: `watchdog`, `requests`, `python-dotenv`, `arize-otel`, `openinference-semantic-conventions`.

### Core Logic
#### [MODIFY] [main.py](file:///home/kizabgd/Desktop/Istrazivanje/trinity_organizer/main.py)
- **Folder Initialization**: Implement a function to create the required folder structure in `~/Kiza/desktop` if it doesn't exist.
- **Mistral Integration**: Implement `call_mistral` to use the Mistral API (via `requests`) to extract text/metadata and provide a theme/category.
- **Grok Integration**: Implement `call_grok` to use the x.ai API for files identified as Kaggle or programming related.
- **OpenRouter Integration**: Implement `call_openrouter` using `meta-llama/llama-3-8b-instruct:free` to make the final routing decision.
- **Notion Integration**: Complete `log_to_notion` to write to the specified database with all required columns.
- **Dual Trigger**: 
    - Keep `watchdog` for event-driven processing.
    - Add a background thread or a periodic loop that scans the `Inbox` every 5 hours as a fallback.
- **Arize Tracing Integration**:
    - Use `arize.otel.register` to initialize tracing.
    - Manually instrument `call_mistral`, `call_grok`, and `call_openrouter_decision` with `openinference` semantic attributes (model name, prompt, completion tokens, etc.).
    - Wrap the overall `process_file` logic in a parent span.
- **Robustness**: Wrap API calls and file operations in `try-except` blocks with descriptive error logging and exception recording in spans.

## Verification Plan

### Automated Tests
- No specific unit tests are requested, but I will include print statements for each step of the pipeline.
- I will run `python main.py` and monitor the console output.

### Manual Verification
1. **Initial Run**: Start the script and verify that the 7 core folders are created in `~/Kiza/desktop`.
2. **File Processing**: Drop a sample text file (e.g., `kaggle_test.txt`) into `Inbox/` and verify:
    - Console output shows Mistral, Grok, and OpenRouter being called.
    - The file is moved to the correct folder (e.g., `Kaggel takmicenj/`).
    - A new entry appears in the Notion database with the correct metadata.
3. **API Errors**: Temporarily invalidate an API key and verify that the script catches the error and doesn't crash.
