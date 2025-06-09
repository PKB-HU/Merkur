import ollama

system_message = {
    "role": "system",
    "content": (
        """
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
    )
}


user_message = {"role": "user", "content": input("> ")}

messages = [system_message, user_message]

response = ollama.chat(
    model='llama3.2:3b',
    messages=messages,
)

print(response.message.content)
