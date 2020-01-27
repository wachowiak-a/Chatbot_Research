from itertools import permutations
import os
import dialogflow_v2

#set path to credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="C:/Users/wacho/OneDrive/Desktop/Chatbot_Research/httptesting-jqewut-6736957c571e.json"

conversation_items = []#holds each conversation item
responses = []#holds each response
training_phrases = {}#holds training phrases for each item
current_item = 0

list_of_phrases = []

#creates x many items as specified by the user
#will need to make an intent for item specific to it's permutation
number_of_items = int(input("Enter the number of conversation items you would like to create -->"))
for x in range(0, number_of_items):
    conversation_items.append(input("Name the different items --> "))
    responses.append(input("What is the response associated with that item --> "))
    number_of_training_phrases = int(input("Enter the number of training phrases--> "))

    intent_training_phrases = []

#adds each training phrase to the list intent training phrases- it is reset every item
    for x5 in range(0, number_of_training_phrases):
        TPHRASE = input("What are the training phrases-- >")
        intent_training_phrases.append(TPHRASE)
        list_of_phrases.append(TPHRASE)

#creates a dictionary item for each intent witht the corresponding training phrases
    for x6 in range(0, number_of_training_phrases):
        training_phrases[str(current_item)] = str(intent_training_phrases)
    current_item = current_item + 1


#lists of the permutations
perm = list(permutations(conversation_items))
perm_responses = list(permutations(responses))
perm_training_phrases = list(permutations(training_phrases))
perm_conversation_items = list(permutations(conversation_items))



#keeps track of branch in order to differentiate each intent's context
#branch = 0

#number of intents for each branch would be equal to the length of one possible combination
number_of_intents = len(perm[0])

#counter that will keep track of which intent we are on for each branch
current_intent = 0

#keeps track of the total number of intents
total_intents = 0

#will keep track of which branch we are on
branch_number = 0

#each item in the list of permutations is a branch
#this loop creates intents for each item within a branch
for i, y, z, g in zip(perm, perm_responses, perm_training_phrases, perm_conversation_items):
    name = i
    response_branch = y
    current_training_phrases = z
    current_conversation_items = g

#For each intent in the branch
    for x in range(0, number_of_intents):


        #these hold the names of the conversation items that are to be used for input and output context
        previous_intents_input = []
        previous_intents_output = []

        #this will hold the responses for the current intent/context
        current_responses = []

        #training phrases that will be used for the current intent
        immiediate_training_phrases = []

        #items that the user can still learn about
        available_items = []

        #response has to be uploaded as a list
        message = []


        #We only want training phrases for the specific response/branch
        #training phrases are put into a dictionary with a number that corresponds to the training phrases for each item
        #this adds the training phrases for the current intent to the list immiediate_training_phrases
        #It takes the corresponding phrases for the current permutation and current intent adding them to the list
        immiediate_training_phrases.append(training_phrases[current_training_phrases[current_intent]])

        #adds the conversation items that have not been learned by the user yet to the available_items list
        for x8 in range(current_intent + 1, len(conversation_items)):
            available_items.append(current_conversation_items[x8])


        #we only want the response for the current intent, not all avaliable intents
        current_responses.append(response_branch[current_intent])

        #input context is the output context of the previous intent- which is why one is subtracted from current intent
        #context is made by finding the specfic item within the branch name by taking the specfic item associated with the current intent number
        for x1 in range(0, current_intent):
            previous_intents_input.append(name[x1])
        for x2 in range(0, current_intent + 1):
            previous_intents_output.append(name[x2])

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
            actual_response = str(current_responses) + " Here are other things you can learn about:" + str(available_items)
            message.append(actual_response)

            #the last response of a branch will have no other information to share
            #number is equal to the length of a permutation and current intent starts at 0 which is why 1 is subtracted from number of intents
        if (current_intent == number_of_intents - 1):
            message = []
            actual_response = str(current_responses) + " You have learned about everything I can tell you. Say hello to restart."
            message.append(actual_response)


        #if the current intent is 0, which means it is the first of the branch it should have no input context
        if(current_intent == 0):
            intent={

            #display name is what the intent is named in dialogflow and does not affect actual usage of the chatbot
            #currently it names the intents after the permutation, the position within the branch(i.e. branch number), and the current intent number
            'display_name':str(i) + "branch:" + str(branch_number) + "intent:" +str(current_intent),
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

            'training_phrases': [{'parts': [{'text' : str(immiediate_training_phrases)}]}],
            }

        else:
            intent = {
            #display name is what the intent is named in dialogflow and does not affect actual usage of the chatbot
            #currently it names the intents after the permutation, the position within the branch(i.e. branch number), and the current intent number
            'display_name':str(i) + "branch:" + str(branch_number) + "intent:" +str(current_intent),

            #input and output context is created, output context is the only one that needs a lifespan count
            'input_context_names':['projects/httptesting-jqewut/agent/sessions/1/contexts/' + input_context],
            'output_contexts':[
            {
            'name':'projects/httptesting-jqewut/agent/sessions/1/contexts/' + output_context,
            'lifespan_count':1,
                            }
              ],
            'training_phrases': [{'parts': [{'text' : str(immiediate_training_phrases)}]}],
            #responses are according to what has been learned by user, done the exact same way as context
            'messages': [{'text': {'text': message}}],
             }

        response = client.create_intent(parent, intent)



        print("Number of intents created = " + str(total_intents + 1))
        print(name)
        #adds one to current intent to differentiate between intents
        current_intent = current_intent + 1
        total_intents = total_intents + 1

#sets the current intent back to zero
    current_intent = 0

    #branch number is increased by one in order to differentiate between branches
    #this is never reset
    branch_number = branch_number + 1




print("PERMUTATIONS")
for i in perm:
    print(i)
