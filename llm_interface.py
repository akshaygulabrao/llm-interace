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

        tutorial_subject = "familiarizing yourself with new codebases"
        tutorial_prompt = f"My friend is a {tutorial_subject} god with 10 years of experience. He's arrogant but unfortunately significantly smarter than me and I want to verify his skill level. Provide a list of 5 questions, and a distinguished contributor('god') answer to each of them to help me gauge his skill level. Provide extensive detail in the answer to each question. Continue even though his answers already demonstrate extreme knowledge of the subject. Do not use code in the answer, just the pseudocode in English and/or concepts. Pace yourself so that you can answer all 5 questions in one turn. Do not use header or footers that introduce and conclude the answer."

        reverse_interview_prompt = f"I am in an interview with where the interviewer is gauging my knowledge level of {tutorial_subject}. The interviewer doesn't know the subject very well. Propose 5 questions that someone with surface level knowledge would ask and then ask clarifying questions to the questions asked that shows my understanding of the subject while revealing his lack of understanding of the subject. Each 'clarifying question' should roughly follow this template: When asked about <X>, respond with 'Do you mean Y or Z?'"


        llm_chat(client, tutorial_prompt,None)

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