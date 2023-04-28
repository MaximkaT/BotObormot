import replicate

client = replicate.Client(api_token='r8_72jMqputQrrnVQeSxgaciiSW2XgxseE4MHaAR')

output = client.run(
    "ai-forever/kandinsky-2:601eea49d49003e6ea75a11527209c4f510a93e2112c969d548fbb45b9c4f19f",
    input={"prompt": "red cat, 4k photo"}
)
print(output)