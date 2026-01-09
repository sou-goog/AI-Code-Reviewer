def calculate_total(items):
    # Bug: Doesn't handle empty list
    total = 0
    for item in items:
        total += item['price']
    
    # Security issue: Hardcoded API key
    api_key = "sk-1234567890abcdef"
    
    # Performance issue: Inefficient loop
    result = []
    for i in range(len(items)):
        result.append(items[i])
    
    return total
