# DuckDuckGoSearchRun doesn't use an API key because DuckDuckGo offers a free, public search interface that doesn't require authentication.
# Under the hood, it uses the duckduckgo-searchPython package, which makes HTTP requests directly to DuckDuckGo's search endpoint — essentially the same as a browser doing a search, but in code

from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

results = search_tool.invoke("India news")

print(results)