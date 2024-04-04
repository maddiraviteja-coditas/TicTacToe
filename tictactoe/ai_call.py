import os
from dotenv import load_dotenv
import openai
import json
from tictactoe.utils import print_matrix, update_matrix
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


data = [
    {
  "name": "extract_info",
  "description": "generate the next possible move position",
  "parameters": {
    "type": "object",
    "properties": {
      "position": {
        "type": "integer",
        "enum": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9
        ],
        "description": "The move position made."
      },
      "is_completed": {
        "type": "boolean",
        "description": "did anyone win the game return True or False?"
      },
      "who_won": {
        "type": "string",
        "enum": [
          "user",
          "ai"
        ],
        "description": "Who won the game?"
      }
    },
    "required": [
      "position",
      "is_completed"
    ]
  }
}
]
prompt = """
Instruction : play tic tac toe game, return a value where you need to place your move and for one time only make one move, 
do not replace the moves already made, the positions only lie between 1 and 9 strictly. follow all the rules of the tic tac toe game.
inform when the game is over. The game ends when one player(Ai or User) successfully places three of their marks in a row. 
That player is declared the winner (user or ai). predict for the next one move

Context: User move is represented with "X" and Ai's move is represented with "O". based on the moves make your next move intelligently.
Objective: The goal is to get three of your marks in a row horizontally, vertically, or diagonally. The row can be on the board or along the edges.
Choose the next move intelligently.
Note: Think step by step and analyse do the move defends the user and make the move.follow the rules of tic tac toe.

Q:These are the moves made until now, now it's your turn to make a move based on the matrix make a move intelligently against the X  
[[X,2,3],
[4,5,6]
[7,8,9]]
next move.
A: make a move at 5, as it blocks user to complete the game in diagonal.And the game is in progress.
Q:These are the moves made until now, now it's your turn to make a move based on the matrix make a move intelligently against the X  
[[X,2,3],
[4,O,6]
[X,8,9]]
next move.
A: make a move at 4, as it blocks user to complete the game in vertical.The game is in progress.
Q: These are the moves made until now, now it's your turn to make a move based on the matrix make a move intelligently think of the move made 
"""


def play_game_ai(final_prompt):
    # first api call to make move 
    play = openai.chat.completions.create(
        model = "gpt-3.5-turbo",  # gpt-4 works fine here.
        messages= [
            {"role" : "system", "content" : "You are an intelligent tic tac toe player. playing against the human user."},
            {"role" : "user", "content" : final_prompt}
        ],
        temperature=1.5, # it needs to think creative to make next move.
        top_p = 1
    )

    # second api call to extract the required data of the above prompts output or response.
    extract_data = openai.chat.completions.create(
    model = "gpt-3.5-turbo", # the gpt-3.5-turbo model works fine here instead of gpt-4
    messages= [
        {"role" : "system", "content" : "You are an intelligent model to extract the required data from the given data."},
        {"role" : "user", "content" :"Extract the position, and is the game completed , who won the game " + str(play.choices[0].message.content)}
    ],
    functions = data, # the required data format is passed to openai.
    temperature=0.5, # the temperature is set low as it needs to only seperate the data instead of generation
    top_p = 1
    )

    # converting the extracted data into the json format i.e., we can use it as a dictionary.
    extracted_data = json.loads(extract_data.choices[0].message.function_call.arguments)
    return extracted_data

input_matrix = [
     [1,2,3],
     [4,5,6],
     [7,8,9]
]

# The game starts here, This method is responsible for calling other methods that which help to call the api
# This method is also responsible for handling the data sent from the views.py and sending the data to the views.py 
def play(position = 0, reset = False):
        global input_matrix
        # checking if the user is trying to reset the board.
        # if the user posses to reset the input_matrix i.e., the board is set with its intial values.
        if reset:
             input_matrix = [[1,2,3],[4,5,6],[7,8,9]]
             return input_matrix
        
         # updating the initial matrix by the users input.
        input_matrix = update_matrix(input_matrix, position, "user") 

        #The final prompt by adding the current state of the board and the prompt
        final_prompt = prompt + str(input_matrix) + "\nnext move \nA: " 

        # here the play_game_ai is responsible for all the api calls and returning the data.
        data_extract = play_game_ai(final_prompt) 

        # Here the exception may raise as thethe position fetched may somtimes be inaccurate or any exception from api call.
        try : 
            # the initial matrix i.e., board is being updated by the response from the ai.
            input_matrix = update_matrix(input_matrix, data_extract["position"],"ai") 
        except Exception:
            print("Caught an exception...")

        # returning the updated board and the data that seperated from the ai's output like is_completed and the who_won the game and the position
        return [input_matrix, data_extract]