import os
import requests
import json

class SerperTool:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.url = "https://google.serper.dev/search"

    def search(self, query: str):
        """
        Performs a google search using Serper.dev
        """
        if not self.api_key:
            return {"error": "Missing SERPER_API_KEY"}

        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request("POST", self.url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract organic results
            organic = data.get("organic", [])
            snippet = []
            for item in organic[:3]: # Top 3 results
                snippet.append(f"Title: {item.get('title')}\nLink: {item.get('link')}\nSnippet: {item.get('snippet')}")
            
            return {
                "query": query,
                "results": "\n\n".join(snippet) if snippet else "No results found.",
                "raw_data": data
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

if __name__ == "__main__":
    tool = SerperTool()
    if tool.api_key:
        print(tool.search("Top tourist attractions in Paris"))
    else:
        print("Skipping serper test, no key.")
