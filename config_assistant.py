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
        "name": "validate_dates",
        "description": "Use this function to validate check-in and check-out dates.",
        "parameters": {
        "type": "object",
        "properties": {
          "check_in": {"type": "string", "description": "The user's check-in date in the format DD/MM/YYYY."},
          "check_out": {"type": "string", "description": "The user's check-out date in the format DD/MM/YYYY."},
        },
        "required": ["check_in", "check_out"]
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
          "adults": {"type": "string", "description": "The quantity of adults who will travel considering the user."},
          "children_ages": {"type": "string", "description": "The ages of all the children who will travel. For example: three children aged 2, 4 and 7, the porperty will be '2,4,7'"},
          "city": {"type": "string", "description": "the name of the city the user wants to travel to."},
          "email": {"type": "string", "description": "the e-mail of the user."},
        },
        "required": ["adults", "children_ages", "city", "email"]
      }
    } 
    },
    {
    "type": "function",
    "function": {
      "name": "get_hotel_info",
      "description": "Get a complete description about a especific hotel.",
      "parameters": {
        "type": "object",
        "properties": {
          "hotel_name": {"type": "string", "description": "The name of the hotel that the user wants to know more information about."},
        },
        "required": ["hotel_name"]
      }
    } 
    },
    {
    "type": "function",
    "function": {
      "name": "get_rooms_info",
      "description": "Get a general overview about the rooms in a especific hotel.",
      "parameters": {
        "type": "object",
        "properties": {
          "hotel_name": {"type": "string", "description": "The name of the hotel that the user wants to know more rooms information about."},
        },
        "required": ["hotel_name"]
      }
    } 
    },
    {
    "type": "function",
    "function": {
      "name": "get_room_info",
      "description": "Get a complete description and a photograph about a especific room.",
      "parameters": {
        "type": "object",
        "properties": {
          "room_name": {"type": "string", "description": "The name of the room that the user wants to know more information about."},
        },
        "required": ["room_name"]
      }
    } 
    },
    {
    "type": "function",
    "function": {
      "name": "get_current_date",
      "description": "Use this function when you need to get the current date.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    } 
    },
    {
    "type": "function",
    "function": {
      "name": "summarize_booking",
      "description": "Use this function to summarize and confirm the reservation before end the conversation.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    } 
    },
    ]
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
