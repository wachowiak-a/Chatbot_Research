from itertools import permutations
import os
import dialogflow_v2

#set path to credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="C:/Users/wacho/OneDrive/Desktop/Chatbot_Research/httptesting-jqewut-6736957c571e.json"

conversation_items = []#holds each conversation item
responses = []#holds each response
training_phrases = {}#holds training phrases for each item
current_item = 0
permutation = []#
list_num_tphrases = [] #holds the number of training phrases that each intent has

#just for first intent
#list_of_phrases = []

#creates x many items as specified by the user
#will need to make an intent for item specific to it's permutation
number_of_items = int(input("Enter the number of conversation items you would like to create -->"))
for x in range(0, number_of_items):
    conversation_items.append(input("Name the item --> "))
    responses.append(input("What is the response associated with that item --> "))
    number_of_training_phrases = int(input("Enter the number of training phrases--> "))
    list_num_tphrases.append(number_of_training_phrases)

    intent_training_phrases = [] #resets list so it can be used for each intent

        #adds each training phrase to the list intent training phrases- it is reset every item
    for x in range(0, number_of_training_phrases):
        tphrase = input("What are the training phrases-- >")
        intent_training_phrases.append(tphrase)
    #    list_of_phrases.append(tphrase)

        #creates a dictionary item with the corresponding
    for x in range(0, number_of_training_phrases):
            #creates a key for the current intent with the training phrases as its definition
        training_phrases[str(current_item)] = intent_training_phrases

    current_item = current_item + 1


for x in range(0,number_of_items):
    permutation.append(x)

#List of the permutations
perm = list(permutations(permutation))

#keeps track of branch in order to differentiate each intent's context
branch = 0

#number of intents for each branch would be equal to the length of one possible combination
number_of_intents = len(perm[0])

#counter that will keep track of which intent we are on for each branch
current_intent = 0

#keeps track of the total number of intents- currently not being used
total_intents = 0

#will keep track of which branch we are on
branch_number = 0

for x in perm:
#can use a single value for all of the lists because each item in each list corresponds to the items in the same spot in other lists
    item = x

#For each intent in the branch
    for x in range(0, number_of_intents):

        #these hold the names of the conversation items that are to be used for input and output context
        previous_intents_input = []
        previous_intents_output = []

        #this will hold the responses for the current intent/context
        current_responses = []


        #items that the user can still learn about
        available_items = []

        #response has to be uploaded as a list
        message = []

    #    immiediate_training_phrases.append(training_phrases[item[current_intent]])

        #adds the conversation items that have not been learned by the user yet to the available_items list
        for x in range(current_intent + 1, len(conversation_items)):
            available_items.append(conversation_items[item[x]])


        #we only want the response for the current intent, not all avaliable intents
        current_responses.append(responses[item[current_intent]])

        #input context is the output context of the previous intent- which is why one is subtracted from current intent
        #context is made by finding the specfic item within the branch name by taking the specfic item associated with the current intent number
        for x in range(0, current_intent):
            previous_intents_input.append(conversation_items[item[x]])
        for x in range(0, current_intent + 1):
            previous_intents_output.append(conversation_items[item[x]])

        #formats both contexts to remove commas
        previous_intents_output = ('{}'*len(previous_intents_output)).format(*previous_intents_output)
        #output context is the known intents which are gotten from the for loop above
        output_context = "KnownItems_" + str(previous_intents_output) + "_and_intent" + str(current_intent)



        #input context only matters if the intent is not the first intent in the converstaion
        if(current_intent != 0):
            previous_intents_input = ('{}'*len(previous_intents_input)).format(*previous_intents_input)
            input_context = "KnownItems_" + str(previous_intents_input) + "_and_intent" + str(current_intent -1)

        client = dialogflow_v2.IntentsClient()
        parent = client.project_agent_path('httptesting-jqewut')


        if(current_intent != number_of_intents):
            actual_response = current_responses[0] + " Here are other things you can learn about:" + str(available_items)
            message.append(actual_response)

            #the last response of a branch will have no other information to share
            #number is equal to the length of a permutation and current intent starts at 0 which is why 1 is subtracted from number of intents
        if (current_intent == number_of_intents - 1):
            message = []
            actual_response = current_responses[0] + " You have learned about everything I can tell you. Say hello to restart."
            message.append(actual_response)

        if(current_intent == 0):
            intent={

            #display name is what the intent is named in dialogflow and does not affect actual usage of the chatbot
            #currently it names the intents after the permutation, the position within the branch(i.e. branch number), and the current intent number
            'display_name':str(conversation_items[item[x]]) + "branch:" + str(branch_number) + "intent:" +str(current_intent),
            #no input context

            #output context is added
            'output_contexts':[
            {
            'name':'projects/httptesting-jqewut/agent/sessions/1/contexts/' + output_context,
            #lifespan sets how long the context is active for
            'lifespan_count':1,
                }
              ],
            'messages': [{'text': {'text': message}}],
            'training_phrases': []
            }

        else:
            intent = {
            #display name is what the intent is named in dialogflow and does not affect actual usage of the chatbot
            #currently it names the intents after the permutation, the position within the branch(i.e. branch number), and the current intent number
            'display_name':str(conversation_items[item[x]]) + "|branch:" + str(branch_number) + "intent:" +str(current_intent),

            #input and output context is created, output context is the only one that needs a lifespan count
            'input_context_names':['projects/httptesting-jqewut/agent/sessions/1/contexts/' + input_context],
            'output_contexts':[
            {
            'name':'projects/httptesting-jqewut/agent/sessions/1/contexts/' + output_context,
            'lifespan_count':1,
                            }
              ],
                    #responses are according to what has been learned by user, done the exact same way as context
            'messages': [{'text': {'text': message}}],
            'training_phrases': []
            }
    #    for x in range(0, len(conversation_items)): #for each item
        for y in range(0, list_num_tphrases[item[x]]):#for each training phrase for that item
            print(current_intent)
            intent['training_phrases'].append({'parts': [{'text' : training_phrases[str(item[x])][y]}]})

        response = client.create_intent(parent, intent)

        current_intent = current_intent + 1
        total_intents = total_intents + 1

#sets the current intent back to zero
    current_intent = 0

    #branch number is increased by one in order to differentiate between branches
    #this is never reset
    branch_number = branch_number + 1

#CREATING WELCOME INTENT
#Response has to be a list?
#below doesn't work
#r = ["Hello! You can learn about " + str(conversation_items) +". Feel free to say hello to restart the converstaion."]
#^calling the specific object in the list for the message doesn't work, you have to just call the entire list I am not sure why
welcome_message = ["Hello! You can learn about " + str(conversation_items) +". Feel free to say hello to restart the converstaion."]

intent = {
'display_name':"WELCOME INTENT",

 # "events": ["Welcome"], ////currently welcome doesn't work? not sure why but it isn't critical

#responses are according to what has been learned by user, done the exact same way as context
'messages': [{'text': {'text': welcome_message}}],
'training_phrases': [
{'parts': [{'text' : "Hello"}]},
{'parts': [{'text' : "Hi"}]},
{'parts': [{'text' : "Howdy"}]},
{'parts': [{'text' : "How are you?"}]},
{'parts': [{'text' : "Hey"}]},
{'parts': [{'text' : "How's it going?"}]},
{'parts': [{'text' : "What's up?"}]},
{'parts': [{'text' : "Who are you?"}]},
{'parts': [{'text' : "What's going on?"}]},
{'parts': [{'text' : "Yo"}]},
]}
    #    for x in range(0, len(conversation_items)): #for each item

response = client.create_intent(parent, intent)



print(permutation)

for x, y in training_phrases.items():
  print(x, y)
