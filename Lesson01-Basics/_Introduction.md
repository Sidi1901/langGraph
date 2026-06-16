#### Task 1:

Install langchain and confirm installaton.



LangChain is designed to automatically look for specific environment variable keys. For the Google GenAI integration, it checks for GOOGLE_API_KEY first (and uses GEMINI_API_KEY as a fallback).

Otherwise the Direct Argument Way for Quick Testing

```
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key="AIzaSyYourActualKeyHere...",  # Your key goes here
    temperature=0.3
)
```