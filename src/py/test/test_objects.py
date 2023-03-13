df = pd.DataFrame()

assert(type(df).__name__ == 'DataFrame') # Success Example
assert(type(df).__name__ == type([]).__name__) # Fail Example