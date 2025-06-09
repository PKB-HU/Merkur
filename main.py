import ollama

import scan_for_devices

import json

with open("devices.json", "r") as f:
    devices = json.load(f)


scan_for_devices.start_periodic_scan()
print("Started network scanning")


old_system_prompt ="""
        You are an assistant that used to call functions. 
        You must only use the function 'add_two_numbers' with integer arguments 'a' and 'b'.  
        Do NOT use or invent any other functions.  
        
        When answering, respond ONLY with a valid JSON array of objects.  
        Each object must have exactly two keys:  
        - "function" (a string, always "add_two_numbers")  
        - "args" (an object with keys "a" and "b", integer values).  
        
        Do NOT output anything else, no explanations, no Python code, no raw function calls.  
        
        For example:  
        [
          {"function": "add_two_numbers", "args": {"a": 3, "b": 2}},  
          {"function": "add_two_numbers", "args": {"a": 5, "b": 5}}  
        ]
        
        When you need to use the result of a previous function call as an argument, use the placeholder "<result_N>" where N is the zero-based index of the previous call. For example:

        [
          {"function": "add_two_numbers", "args": {"a": 2, "b": 3}},
          {"function": "add_two_numbers", "args": {"a": "<result_0>", "b": 4}}
        ]


        """

system_message = {
    "role": "system",
    "content": (
        f"""
        You are an assistant responsible for controlling IoT devices. The list of currently connected devices is:

        {json.dumps(devices, indent=4)}

        Instructions:

        - You must only use the function: "comms.send_message(message, ip)".
        - Do NOT use or invent any other functions.
        - If no IoT devices are connected, respond with an empty list: [].

        Response format:

        You must respond with a JSON array. Each element in the array must be an object with exactly two keys:

        1. "function" — Always the string "comms.send_message"
        2. "args" — An object with two string keys:
           - "message" — The message to send (e.g., "turn on", "quit")
           - "ip" — The IP address of the target device

        Example:

        [
          {{
            "function": "comms.send_message",
            "args": {{
              "message": "turn on",
              "ip": "192.168.1.1"
            }}
          }}
        ]

        If no suitable devices are found or the command does not match any known actions, respond with:

        []

        Do not include any explanations, Python code, or raw function calls — only valid JSON as shown.
        """

)
}

print(system_message)

user_message = {"role": "user", "content": input("> ")}

messages = [system_message, user_message]

response = ollama.chat(
    model='llama3.1:8b', # llama3.2:3b
    messages=messages,
)

print(response.message.content)
