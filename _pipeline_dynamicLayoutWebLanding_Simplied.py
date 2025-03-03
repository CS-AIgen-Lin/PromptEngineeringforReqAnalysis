
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
#L.T. Changed the use of the config file for the url and added it directly. There was an issue accessing it; director/file are set for read/write. It could be an indention issue.
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
#L.T. created new prompt method, Help Me Design, for web page layout design. Phase 1. There is a more complex propmpt on _pipeline_dynamicWebLandingPage.py included in this project.
   
    TotalMenuTiles =  input("How many dashboard box titles per functional area? ")

#### (2) Adjust the Prompt Engineering Technique to be applied, simulating Workflow Templates
    Help_Me_Design = \
    f"""
    Q:I'm developing a web page and need to analyze requirements. There is a div element with width of 100%. I need to add {TotalMenuTiles} tables to fit within the div within the div?
    A:Make all boxes the same width. Add padding of 2% between each box. Convert the width of each box from percentage into pixels.
    Q:How can I add names to each box?
    A:Add the name: CFA to one box, Add the name: HR to another box, Add the name: EXR to another box. If there is an extra box add the name Placeholder.
    """


    PROMPT = Help_Me_Design

  
    payload = create_payload(
                         target="ollama",   
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                        num_ctx=100, 
                        num_predict=100
                         )

    time, response = model_req(payload=payload)  ###can create a chain of thought responses here, need to allow user to input
    #print('20')

    print(response)

    if time: print(f'Time taken: {time}s')
    
    checkResponse = response.find("<table>")
    if checkResponse == -1:
        print ("A div element can easily be used.")
        betterElement = "An HTML div element can be better than a table element."
    else:
        print("Instead of using a table, a div element can be easily used.")    
        betterElement = "Use HTML div element instead of the table element."
        

    PROMPT = betterElement

  
    payload = create_payload(
                         target="ollama",   
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                        num_ctx=200, 
                        num_predict=200
                         )

    time, response = model_req(payload=payload)  ###can create a chain of thought responses here, need to allow user to input
    #print('20')

    print(response)
   
    if time: print(f'Time taken: {time}s')
    
 





