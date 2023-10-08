import llm

question = llm.Question('Is the player doing something morally questionable?', ['yes', 'no', 'maybe'])
print(question.ask('The player has caught the bank robber.'))

question = llm.Question("What is the tone of the player's response?", ['threatening', 'friendly', 'unknown'])
print(question.ask('Player: "Excuse me?"'))