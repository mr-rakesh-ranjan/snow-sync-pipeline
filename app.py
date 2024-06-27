from servicenowrag import chat_engine

while(True):
    query=input("\nEnter a query: ")
    if query == "exit":
        break
    #Print the result
    print("\n\n> Question:")
    print (query)
    answer = chat_engine.chat(query)
    print (answer.response)