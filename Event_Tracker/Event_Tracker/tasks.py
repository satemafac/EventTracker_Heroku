from __future__ import absolute_import, unicode_literals
from celery import shared_task
from openai import OpenAI
import requests
import os
import logging  # Import the logging module

@shared_task(bind=True)
def generate_flyer_task(self, data):
    # Simple test task
    return {'result': 2 + 2}

# @shared_task(bind=True)
# def generate_flyer_task(self, data):
#     # Extract data
#     event_name = data.get('event_name')
#     location = data.get('event_location')
#     organization = data.get('event_org')
#     description = data.get('about_event')
#     start_time = data.get('event_start_date')
#     end_time = data.get('event_end_date')

#     # Set OpenAI API key
#     # openai.api_key = os.getenv('OPENAI_API_KEY')

#     client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

#     print(client)


#     # Generate flyer prompt
#     prompt = f"""
#     Give me a prompt to generate a beautiful and engaging flyer for this event.

#     Event Name: {event_name}
#     Location: {location}
#     Organization: {organization}
#     Description: {description}
#     Start Time: {start_time}
#     End Time: {end_time}

#     The flyer should have a modern and elegant design, matching the theme of the event, and should include the provided details in a clear and attractive manner.
#     """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a creative assistant skilled in designing event flyers. Keep the prompts concise and to the point of creating an event flyer with no extra jargons."},
#                 {"role": "user", "content": prompt},
#             ],
#         )
#         flyer_prompt = response.choices[0].message.content.strip()
#     except Exception as e:
#         raise self.retry(exc=e, countdown=10, max_retries=3)

#     # Call Ideogram API
#     ideogram_api_url = "https://api.ideogram.ai/generate"
#     ideogram_payload = {
#         "image_request": {
#             "model": "V_2",
#             "magic_prompt_option": "AUTO",
#             "prompt": f"{flyer_prompt}"
#         }
#     }

#     ideogram_ai = os.getenv('IDEOGRAM_AI')
#     print(ideogram_ai)
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "Api-Key": f"{ideogram_ai}"
#     }

#     logger = logging.getLogger(__name__)

#     # Before making the API call
#     logger.info(f"Making Ideogram API call with headers: {headers}")
#     logger.info(f"Ideogram payload: {ideogram_payload}")


#     try:
#         ideogram_response = requests.post(
#             ideogram_api_url,
#             json=ideogram_payload,
#             headers=headers
#         )
#         ideogram_response.raise_for_status()
#     except Exception as e:
#         logger.error(f"Ideogram API call failed: {e}")
#         logger.error(f"Response content: {ideogram_response.text if ideogram_response else 'No response'}")
#         raise self.retry(exc=e, countdown=10, max_retries=3)

#     image_data = ideogram_response.json()

#     # Return the result
#     return {
#         'flyer_prompt': flyer_prompt,
#         'image_data': image_data
#     }