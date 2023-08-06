import openai
# openai.api_key = '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'
class OpenAi:
    def __init__(self, api_key):
        api_key = api_key[1:-1]
        self.api_key = api_key
        openai.api_key = api_key
    def finish_prompt(self, text):
        response = openai.Completion.create(
        model="ada",
        prompt=text,
        temperature=0.5,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        print(response)
        return response