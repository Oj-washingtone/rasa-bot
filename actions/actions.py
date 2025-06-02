from typing import Any, Dict, List, Text
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionFetchServiceProviders(Action):
    def name(self) -> Text:
        return "action_fetch_service_providers"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        
        service = tracker.get_slot("service")
        location = tracker.get_slot("location")


        if not service or not location:
            dispatcher.utter_message(text="I need both the service and location to find a provider.")
            
        try:
            url = "http://localhost:5000/api/search"
            params = {"serviceName": service, "location": location}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                providers = response.json()

                if not providers:
                    dispatcher.utter_message(text=f"Sorry, I couldn't find any {service} providers in {location}.")
                   
                
                messages = []

                for p in providers:
                    name = p.get("name", "Unknown")
                    phone = p.get("phone", "N/A")
                    desc = p.get("description", "")
                    owner = p.get("owner", {})
                    owner_name = f"{owner.get('firstName', '')} {owner.get('lastName', '')}".strip()

                    message = f"*{name}* ({owner_name})\n📞 {phone}\n {desc}"
                    messages.append(message)

                full_response = "\n\n".join(messages)
                dispatcher.utter_message(text=f"Here are some {service} providers in {location}:\n\n{full_response}")
            
            else:
                dispatcher.utter_message(text= f"There is no current listing of any {service}s around {location} ")


        except Exception as e:
            dispatcher.utter_message(text="An error occurred while contacting the service.")
            print(f"[ERROR]: {e}")






