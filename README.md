## About
This portfolio project showcases my ability to implement tool calling through a LangChain agent. I used the OpenWeather API and created a chat interface where the GPT-4o-mini LLM answers natural language queries about current weather and 5-day forecasts for any city name or zip code with country name. The functions to get weather using API are bound as tools to the GPT-4o-mini LLM through LangChain.

## How to run locally:
1. pip install -r requirements.txt
2. streamlit run weather_api_tool_agent.py
Create an .env file in the project directory and add:

* OPEN_WEATHER_API_KEY = '\<your-open-weather-api-key\>'
* OPENAI_API_KEY='\<your-open-api-key\>'

## References 
- https://blog.langchain.dev/tool-calling-with-langchain/
- https://python.langchain.com/docs/modules/model_io/chat/function_calling/?ref=blog.langchain.dev
- https://openweathermap.org/current
- https://openweathermap.org/forecast5

## Explanation
This AI assistant answers your natural language questions about the current weather and 5-day forecast for any city or zip code. Ask it anything - “Is it raining in London today?” or “What’s the forecast for Paris tomorrow?” - and get the info you need in a chat-like format.
This project combines LangChain’s agent capabilities with a powerful LLM for a user-friendly weather experience.