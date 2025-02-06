import os
from pathlib import Path
from typing import Union, List
import tomllib
import anthropic
from merge_files import merge_files_to_string

def main():
    # Example usage
    toml_path = Path("C:/Users/AkshayGulabrao/Desktop/secrets.toml")
    with open(toml_path, "rb") as f:
        secrets = tomllib.load(f)
    client = anthropic.Anthropic(api_key=secrets["llms"]["ANTHROPIC_API_KEY"])
    try:
        # Mixed mode
        paths = [
            Path(".venv/Lib/site-packages/gitlab/v4/objects"),  # Directory
            # Path("akshay-trading-5/main.py")   # Another individual file
        ]
        # merged_string = merge_files_to_string(paths)
        # with open("gitlab.txt", "w",encoding='utf-8') as f:
        #     f.write(merged_string) 

        llm_chat(client, "gitlab python sdk project get commit cnt",None)

    except Exception as e:
        print(f"Error: {str(e)}")

def llm_chat(client,query, ctx: str | None = None):
    message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": query}
            ]
        )
    with open("output.md", "w") as f:
        f.write(message.content[0].text)

if __name__ == "__main__":
    main()