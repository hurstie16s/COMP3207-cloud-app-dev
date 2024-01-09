#System Imports
import unittest
import requests
import uuid
import json
#Azure Imports
#Code base Imports
import AzureData
from chatGPTReview import send_interview_to_ai

class TestChatGPT(unittest.TestCase):
  
    # Test One: Expecting a non-empty response from chatGPT
    # Normal question and transcript input
    def test_easy_question(self):
        example_question = "Tell me about your hobbies."
        example_transcript = "Of course! I'm passionate about photography, capturing moments that tell awesome stories. \
                             Running keeps me active and refreshed. Reading diverse literature broadens my perspectives. \
                             All of these activities enhance my well-rounded approach to life and work."
        
        chatGPTResponse = send_interview_to_ai(example_question, example_transcript)

        if chatGPTResponse:
            self.assertTrue(chatGPTResponse)

    # Test Two: ValueError from an empty question string
    def test_empty_question(self):
        example_question = ""
        example_transcript = "I am very good in my cloud skills \
                             They include indepth skills regarding Azure and Google App Engine. \
                             In my spare time I create my own projects using them."
        with self.assertRaises(ValueError) as context:
            send_interview_to_ai(example_question, example_transcript)

        self.assertEqual(str(context.exception), "Question cannot be empty.")

    # Test Three: ValueError from an empty transcript string
    def test_empty_transcript(self):
        example_question = "What are your Azure skills like?"
        example_transcript = ""

        with self.assertRaises(ValueError) as context:
            send_interview_to_ai(example_question, example_transcript)

        self.assertEqual(str(context.exception), "Transcript cannot be empty.")