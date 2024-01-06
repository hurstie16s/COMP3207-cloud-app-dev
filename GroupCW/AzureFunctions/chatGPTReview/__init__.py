import openai
from openai import OpenAI

client = OpenAI(
    # API key linking to Alyssa's account
    api_key="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",
    # 60 seconds (default is 10 minutes)
    timeout=60.0,
)

# Prompt parts
start_for_interview = "Based on this interview question: "
evaluation_for_interview = "Evaluate this interview transcript for this question: "
bullet_points_for_interview = "Give 2 bullet points about the good points and 2 points on what could be improved."
format_for_bullet_points_for_interview = "Force this format please: Good Points: -'point 1' -'point 2' Improvement Points: -'point 1' -'point 2' "


def send_interview_to_ai(question, transcript):
    try:
        chat_completion = client.with_options(max_retries=0).chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": start_for_interview + question + evaluation_for_interview + transcript + bullet_points_for_interview + format_for_bullet_points_for_interview,
                }
            ],
            model="gpt-3.5-turbo",
        )
        reply = chat_completion.choices[0].message.content
        return reply
    except openai.APIConnectionError as error:
        print("The server could not be reached.")
        print(error.__cause__)
    except openai.RateLimitError as error:
        print(str(error.status_code) + " status code received.")
    except openai.AuthenticationError as error:
        print("Authentication Error: " + str(error.status_code) + " status code.")
    except openai.APIStatusError as error:
        print("Non-200 status code received.")
        print("Error response: " + str(error.response))
    # Returns None
    return

start_for_question = "Give me a list of 10 bullet points of general advice not specific to an industry on how to answer this interview question: "
bullet_points_for_question = "Give it in a programmatic list format with each point in single quotes, seperated by commas and surrounded by square brackets "
example_for_bullet_points_for_question = "Force this format please: ['advice 1', 'advice 2'] please don't add any \\n."

def send_question_to_ai(question):
    try:
        chat_completion = client.with_options(max_retries=0).chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": start_for_question + question + bullet_points_for_question + example_for_bullet_points_for_question,
                }
            ],
            model="gpt-3.5-turbo",
        )
        reply = chat_completion.choices[0].message.content
        return reply
    except openai.APIConnectionError as error:
        print("The server could not be reached.")
        print(error.__cause__)
    except openai.RateLimitError as error:
        print(str(error.status_code) + " status code received.")
    except openai.AuthenticationError as error:
        print("Authentication Error: " + str(error.status_code) + " status code.")
    except openai.APIStatusError as error:
        print("Non-200 status code received.")
        print("Error response: " + str(error.response))
    # Returns None
    return


"""
# These will be from the 'blob'
example_question = "What programming skills do you have? "
# Example bad interview transcript (AI generated)
example_transcript = "I'm 16 and kinda know Python. I've done some basic stuff with it, " \
                     "made simple programs and all. I guess I'm okay with solving basic problems. "  \
                     "I've heard of Flask for web development but haven't really used it. "  \
                     "Web development, algorithms, and databases sound cool, but I'm just " \
                     "starting to get the hang of things. I'm not like a pro or anything, " \
                     "just trying to figure stuff out. I like learning, but there's still " \
                     "a lot I don't know. So, I've got some Python basics, basic problem-solving "  \
                     "skills, and I'm curious about other coding things. "

print(send_to_ai(example_question, example_transcript))
"""
