
##
## Prompt Engineering Lab
## Platform for Education and Experimentation with Prompt NEngineering in Generative Intelligent Systems
## _pipeline.py :: Simulated GenAI Pipeline 
## 
#  
# Copyright (c) 2025 Dr. Fernando Koch, The Generative Intelligence Lab @ FAU
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Documentation and Getting Started:
#    https://github.com/GenILab-FAU/prompt-eng
#
# Disclaimer: 
# Generative AI has been used extensively while developing this package.
# 


from queue import Empty
from re import I
import requests
import json
import os
import time


def load_config():
    """
    Load config file looking into multiple locations
    """
    config_locations = [
        "./_config",
        "prompt-eng/_config",
        "../_config"
    ]
    
    # Find CONFIG
    config_path = None
    for location in config_locations:
        if os.path.exists(location):
            config_path = location
            break
    
    if not config_path:
        raise FileNotFoundError("Configuration file not found in any of the expected locations.")
    
    # Load CONFIG
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def create_payload(model, prompt, target="ollama", **kwargs):
    """
    Create the Request Payload in the format required byt the Model Server
    @NOTE: 
    Need to adjust here to support multiple target formats
    target can be only ('ollama' or 'open-webui')

    @TODO it should be able to self_discover the target Model Server
    [Issue 1](https://github.com/genilab-fau/prompt-eng/issues/1)
    """

    payload = None
    if target == "ollama":
        payload = {
            "model": model,
            "prompt": prompt, 
            "stream": False,
        }
        if kwargs:
            payload["options"] = {key: value for key, value in kwargs.items()}

    elif target == "open-webui":
        '''
        @TODO need to verify the format for 'parameters' for 'open-webui' is correct.
        [Issue 2](https://github.com/genilab-fau/prompt-eng/issues/2)
        '''
        payload = {
            "model": model,
            "messages": [ {"role" : "user", "content": prompt } ]
        }

        # @NOTE: Taking not of the syntaxes we tested before; none seems to work so far 
        #payload.update({key: value for key, value in kwargs.items()})
        #if kwargs:
        #   payload["options"] = {key: value for key, value in kwargs.items()}
        
    else:
        print(f'!!ERROR!! Unknown target: {target}')
    return payload


def model_req(payload=None):
    """
    Issue request to the Model Server
    """
        
    # CUT-SHORT Condition
#i commented out ************************ Ollama is on; tried indentation changes;files is accessible; so just added direct ref to URL in this py code file.
    # try:
    #     load_config()
    # except: 
    #     return -1, f"!!ERROR!! Problem loading prompt-eng/_config"


   # url = os.getenv('URL_GENERATE', None)
    api_key = os.getenv('API_KEY', None)
#*************************************
    url = 'http://localhost:11434/api/generate'
    delta = response = None

    headers = dict()
    headers["Content-Type"] = "application/json"
    if api_key: headers["Authorization"] = f"Bearer {api_key}"

    #print(url, headers)
    print(payload)

    # Send out request to Model Provider
    try:
        start_time = time.time()
        response = requests.post(url, data=json.dumps(payload) if payload else None, headers=headers)
        delta = time.time() - start_time
    except:
        return -1, f"!!ERROR!! Request failed! You need to adjust prompt-eng/config with URL({url})"

    # Checking the response and extracting the 'response' field
    if response is None:
        return -1, f"!!ERROR!! There was no response (?)"
    elif response.status_code == 200:

        ## @NOTE: Need to adjust here to support multiple response formats
        result = ""
        delta = round(delta, 3)

        response_json = response.json()
        if 'response' in response_json: ## ollama
            result = response_json['response']
        elif 'choices' in response_json: ## open-webui
            result = response_json['choices'][0]['message']['content']
        else:
            result = response_json 
        
        return delta, result
    elif response.status_code == 401:
        return -1, f"!!ERROR!! Authentication issue. You need to adjust prompt-eng/config with API_KEY ({url})"
    else:
        return -1, f"!!ERROR!! HTTP Response={response.status_code}, {response.text}"
    return


def new_func():
    return \

if __name__ == "__main__":
    from _pipeline import create_payload, model_req
   
  
    GeneralInfo = " I'm developing a web page and need to analyze requirements."
    TotalMenuTiles =  input("How many dashboard box titles per functional area? ") 
    WhichPrompt = input("Which Prompt would you like to use? [Please type one as shown here: Help Design, Few, Chain, Zero, Meta, Self, QuickConvert])")
    HowMuchCTX = input("How much context do you prefer? Keep it under 1000 if your machine has und 4.8 GB of RAM.")
    PredictionsAmount = input("What is your preferred prediction lenth? If only a single value is needed--choose 1.")
    
#### (2) Adjust the Prompt Engineering Technique to be applied, simulating Workflow Templates
    Help_Me_Design = \
    f"""
    Q:{GeneralInfo} There is a div element with width of 100%. I need to add {TotalMenuTiles} tables to fit within the div within the div?
    A:Make all boxes the same width and height. Add padding of 2% between each box. Convert the width of each box from percentage into pixels.
    """
    CALCULATESIZE = "Calculate 100 divided by " + TotalMenuTiles 
    
    Chain_of_Thought = \
    f"""The Number of Functional Areas will determine how many boxes are displayed on the web page.
    A:The total width of the page is {CALCULATESIZE} + 2% between each box.
    There should be a space of 2% between each box. 
    A. {CALCULATESIZE} + 2%. Provide only the answer. No explanation. Check {HowMuchCTX} and Predictions to {PredictionsAmount}. Each should be set to 1.
    """
    Zero_Shots = \
    f"""
    {CALCULATESIZE} - 2%. The 2% is for padding. Only a single value or a very short length 
    answer should be returned."""
    
    Meta_Prompting = \
    f"""
    First, research requirements for a web page with a width of 100%. Second, is it best to use percentage or pixels for the web page elements?
    Third, is it best to use div element or table element or CSS to create boxes on the web page? Fourth, give example {CALCULATESIZE}
    """
    
    Self_Consistency = \
    f"""Requirements include building web pages using HTML div element instead of the HTML table. Show example of building web page using {CALCULATESIZE} """
    
    Quick_Convert = \
    f"""    
    Web Page width is 100%. Convert Pecentage to pixels (({CALCULATESIZE})/100) x 1000
    """
       
    PROMPT = ""
 
    
    match WhichPrompt:
        case "Few":
                PROMPT = GeneralInfo + '\n' + CALCULATESIZE
        case "Help Design":
                PROMPT = Help_Me_Design
        case "Chain":
                PROMPT = Chain_of_Thought
        case "Zero":
                PROMPT = Zero_Shots
        case "Meta":
                PROMPT = Meta_Prompting 
        case "Self":
                PROMPT = Self_Consistency
        case "QuickConvert":
                PROMPT = Quick_Convert
        case _:
                PROMPT = Help_Me_Design 
                
    payload = create_payload(
                         target="ollama",   
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                         num_ctx= (int(HowMuchCTX)), 
                         num_predict= (int(PredictionsAmount))
                         )

    time, response = model_req(payload=payload)  ###can create a chain of thought responses here, need to allow user to input
    #print('20')

    print(response)

    if time: print(f'Time taken: {time}s')
    
   