import os

def vulnerable_function(user_input):
    # Intentional SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    print(f"Executing: {query}")
    
    # Intentional hardcoded secret
    api_key = "12345-ABCDE-SECRET"
    
    # Intentional style issue (unused variable)
    unused_var = 10
    
    return query
