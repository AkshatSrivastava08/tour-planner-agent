# AI Operations Assistant (Tour Planner Agent)

A local, multi-agent AI system that plans travel itineraries using real-time data from Weather and Search APIs. Built with Python, Streamlit, and LLM reasoning.

## 🚀 Features

- **Multi-Agent Architecture**:
  - **Planner**: Breaks down natural language queries into executable steps.
  - **Executor**: dynamically calls tools (Weather, Search) to gather info.
  - **Verifier**: Synthesizes results into a final, verified response.
- **Real Tools**: Integrates OpenWeatherMap and Serper.dev.
- **Structured Output**: Uses JSON-based planning for reliability.
- **Streamlit UI**: Clean, interactive interface to visualize the agent workflow.

## 🛠️ Architecture

The system uses a sequential multi-agent flow:

1.  **User Input**: "Plan a 3-day trip to Tokyo..."
2.  **Planner Agent**: Generates a JSON plan:
    ```json
    {"steps": [{"tool": "WeatherTool", "args": {"city": "Tokyo"}}, ...]}
    ```
3.  **Executor Agent**: Iterates through steps, calls `WeatherTool` or `SerperTool`, and logs outputs.
4.  **Verifier Agent**: Reads the original query + execution logs to produce the final itinerary.

## 📦 Setup Instructions

1.  **Clone the Repository**

    ```bash
    git clone <your-repo-link>
    cd ai_ops_assistant
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```ini
    OPENWEATHER_API_KEY=your_key_here # generated from (https://home.openweathermap.org/api_keys)
    SERPER_API_KEY=your_key_here # serper-api key generated from (https://serper.dev/)
    LLM_API_KEY=your_key_here # llm-api key generated from groqcloud(https://console.groq.com/home)
    LLM_BASE_URL=https://api.groq.com/openai/v1  # For Groq
    LLM_MODEL=llama-3.3-70b-versatile          # For Groq
    ```

## 🏃 Running the Project

**Recommended (UI):**

```bash
streamlit run app.py
```

**Alternative (CLI):**

```bash
python ai_ops_assistant/main.py --query "Plan a 2-day trip to London"
```

## 🔌 Integrated APIs

1.  **OpenWeatherMap**: Real-time current weather data.
2.  **Serper.dev**: Google Search results for attractions, events, and facts.

## 🧪 Example Prompts

Try these in the UI:

1.  _Plan a 3-day trip to Tokyo involving culture and food._
2.  _Find me the best hiking spots near San Francisco and check the weather there._
3.  _What are the top 3 museums in Paris and is it raining there right now?_
4.  _Plan a weekend getaway to New York City with a focus on jazz clubs._
5.  _Compare the weather in London and Dubai and suggest activities for the warmer one._

## ⚠️ Limitations & Tradeoffs

- **Sequential Execution**: The Executor runs steps one by one. Parallel execution could speed this up.
- **Context Limit**: Very long plans might hit LLM token limits (though GPT-4o handles most well).
- **Error Handling**: Basic retry logic is implemented, but severe API outages might fail the specific step.
