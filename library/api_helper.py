import time
import requests


class APIHelper:
     @staticmethod
     # Helper function to send requests with connection handling
     def send_post_request(base_url, payload):
         with requests.Session() as session:
             start_time = time.time()
             response = session.post(base_url, json=payload)
             response_time = time.time() - start_time
         return response, response_time
