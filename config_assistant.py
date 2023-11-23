from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def show_assistant(assistant_id):
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    return my_assistant

def modify_assistant(assistant_id):
    my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    # instructions="",
    # name="",
    tools=[{
    "type": "function",
    "function": {
        "name": "get_current_time_and_date",
        "description": "Get the current time and date to validate if the check-in and check-out is a after date.",
        "parameters": {
        "type": "object",
        "properties": {},
        "required": []
        },
        "response": {
        "type": "object",
        "properties": {
            "currentTimeAndDate": {"type": "string"}
        }
        }
    }
    },
    {
    "type": "function",
    "function": {
      "name": "get_hotels_info",
      "description": "Get informations about available hotels.",
      "parameters": {
        "type": "object",
        "properties": {
          "check_in": {"type": "string", "description": "The date of check-in user."},
          "check_out": {"type": "string", "description": "The date of check-out user."},
          "adults": {"type": "string", "description": "The quantity of adults who will travel considering the user."},
          "children_ages": {"type": "string", "description": "The ages of all the children who will travel."},
          "city": {"type": "string", "description": "the name of the city the user wants to travel to."},
        },
        "required": ["check_in", "check_out", "adults", "children_ages", "city"]
      }
    } 
    }]
    # model="",
    # file_ids=["file-abc123", "file-abc456"],
    )
    return my_updated_assistant



if __name__ == "__main__":
    # assistant_id = 'asst_dt5eWgjY8vQqz1Oo6skWvk3D'
    complete_hotelina_assistant_id = 'asst_qayuVh8i6bSMF0lYy1UxkBG6'
    assistant = show_assistant(complete_hotelina_assistant_id)
    updated = modify_assistant(complete_hotelina_assistant_id)
    print(assistant)
