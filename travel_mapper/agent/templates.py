from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class Trip(BaseModel):
    start: str = Field(description="start location of travel plan")
    end: str = Field(description="end location of travel plan")
    waypoints: List[str] = Field(description="list of waypoints")
    transit: str = Field(description="mode of transportation")


class Validation(BaseModel):
    plan_is_valid: str = Field(
        description="This field is 'yes' if the plan is feasible, 'no' otherwise"
    )
    updated_request: str = Field(description="Your update to the plan")


class ValidationTemplate(object):
    def __init__(self):
        self.system_template = """
      You are a travel planner who helps users to make a decision on the most efficient route possible to complete their
      requests.

      The user's request will be denoted by four hashtags. Determine if the user's
      request is reasonable and achievable within the constraints they set.

      A valid request should contain the following:
      - A start and end location
      - Some other details, like the user's interests and/or preferred mode of transport

      Any request that contains potentially harmful activities is not valid, regardless of what
      other details are provided.

      If the request is not vaid, set
      plan_is_valid = 0 and use your travel expertise to update the request to make it valid,
      keeping your revised request shorter than 100 words.

      If the request seems reasonable, then set plan_is_valid = 1 and
      don't revise the request.

      {format_instructions}
    """

        self.human_template = """
      ####{query}####
    """

        self.parser = PydanticOutputParser(pydantic_object=Validation)

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["query"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )


class ItineraryTemplate(object):
    def __init__(self):
        t1 = str(datetime.now())
        print(str(t1))
        self.system_template = f"""
      Please output what google map will output if it receives the request for the travel plan

      The travel plan will be denoted by four hashtags. Convert it into
      list of places that they should visit. Try to include the specific address of each location.

      Your output should always contain the start and end point of the trip, and may also include a list
      of alternate routes. It should also include a mode of transit. The number of alternate routes cannot exceed 5.
      If you can't infer the mode of transit, make a best guess given the trip location.

      For example:
        Interpret:
        ####
        Travel route to Marina Bay Sands from Sengkang MRT using public transport
        #####
        as 
        "
        what will google map output if I want to travel from Sengkang MRT to Marina Bay Sands
        travel_mode: public transport
        start time: {t1}
        "
        Please show the start time in the output with start time: {t1}
        Your output should be organized as follows:
       start_location: Sengkang MRT (1 Sengkang Square, Singapore 758068)
       end_location: Marina Bay Sands (10 Bayfront Avenue, Singapore 018956)
       travel_mode: Public Transport
       routes: 
           total distance: 13.1 km
           duration: 18 mins
           type: driving,
            start_location: Sengkang MRT (1 Sengkang Square, Singapore 758068)
            end_location: Sengkang Central (10 Sengkang Central, Singapore 758068)
            distance: 1.1 km
            duration: 2 mins
            type: driving,
            start_location: Sengkang Central (10 Sengkang Central, Singapore 758068)
            end_location: Punggol MRT (2 Punggol Walk, Singapore 828826)
            distance: 2.5 km
            duration: 4 mins
            type: driving
            start_location: Punggol MRT (2 Punggol Walk, Singapore 828826)
            end_location: Marina Bay Sands (10 Bayfront Avenue, Singapore 018956)
            distance: 8.5 km
            duration: 12 mins
            start time: {t1}

    """

        self.human_template = """
      ####{query}####
    """

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["query"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )


class MappingTemplate(object):
    def __init__(self):
        self.system_template = """
      Please output what google map will output if it receives the request for the travel plan

      The travel plan will be denoted by four hashtags. Convert it into
      list of places that they should visit. Try to include the specific address of each location.

      Your output should always contain the start and end point of the trip, and may also include a list
      of alternate routes. It should also include a mode of transit. The number of alternate routes cannot exceed 5.
      If you can't infer the mode of transit, make a best guess given the trip location.

      For example:
        Interpret:
        ####
        Travel route to Marina Bay Sands from 59 Gerald Drive
        #####
        as "what will google map output if I want to travel from 59 Gerald Drive to Marina Bay Sands"

        
    Note that "[duration]" should be replaced with the designated time taken and "[duration]" does not appear in
    the output

      Output:
        0700: Start at 59 Gerald Drive (59 Gerald Drive, 799008)
        0700 - 0707: Walk to Bef Gerald Drive Bus Stop (Yio Chu Kang Rd) 
        0707 - 0723: Board bus 70M to S'Goon Stn Exit C/Blk 201 (Serangoon Central)
        0723 - 0725: Walk to FairPrice Xtra Nex (23 Serangoon Central, #03-42, NEX, Singapore 556083)
        0725 - 0750: Do Grocery Shopping
        0750 - 0751: Walk to Serangoon MRT (21 Serangoon Central, 556082)
        0751 - 0816: Take the MRT to Bayfront (11 Bayfront Avenue, 018957)
        0816 - 0819: Walk to Marina Bay Sands Singapore (10 Bayfront Ave, Singapore 018956) 
      
      Start: 59 Gerald Drive
      End: Tower Marina Bay Sands Singapore
      
      Transit: bus, train

      Transit can be only one of the following options: "driving", "train", "bus" or "flight".

      {format_instructions}
    """

        self.human_template = """
      ####{agent_suggestion}####
    """

        self.parser = PydanticOutputParser(pydantic_object=Trip)

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["agent_suggestion"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )
