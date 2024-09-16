import os
from dotenv import load_dotenv
import openai
import json
from tictactoe.utils import print_matrix, update_matrix
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


function_data = [
    {
  "name": "extract_info",
  "description": "generate the next possible move position",
  "parameters": {
    "type": "object",
    "properties": {
      "position": {
        "type": "integer",
        "enum": [1,2,3,4,5,6,7,8,9],
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
Instructions : 
1) play tic tac toe game.
2) return a value where the next move to be placed.
3) and for one time only make one move, do not replace the moves already made, the positions only lie between 1 and 9 strictly. 
4) follow all the rules of the tic tac toe game.
5) inform when the game is over. The game ends when one player(Ai or User) successfully places three of their marks in a line.
6) The line may be vertically or horizontally or diagonally. 

Context: 
1) User move is represented with "X" and Ai's move is represented with "O". 
2) based on the current board state make your next move strategically.
Caution: place the move where the empty cell is present.

Objective: The goal is to get three of your marks in a line.

Note: Think step by ste where your next move is strategical and is defending the opponent and setting a win win situation to "O" representation.

Examples:
Q:This is the current state of the board, Which has been made by X.  
[[X,2,3],
[4,5,6]
[7,8,9]]
next move.
A: make a move at 5, as it blocks user to complete the game in diagonal.And the game is in progress.
Q:This is the current state of the board, Which has been made by X.  
[[X,2,3],
[4,O,6]
[X,8,9]]
next move.
A: make a move at 4, as it blocks user to complete the game in vertical.The game is in progress.

Just consider these examples and make a more starategic move that helps to make a win win situation fo rO representation.
Now what would be your next representation of O make a strategic move that help O representation to win the game

Q: This is the current state of the board, Which has been made by X.
"""

def play_game_ai(final_prompt):
    try:
        play = openai.chat.completions.create(
            model = "gpt-3.5-turbo",  # gpt-4 works fine here.
            messages= [
                {"role" : "system", "content" : "An Intelligent tic tac toe game player playing against human user to win the game."},
                {"role" : "user", "content" : final_prompt}
            ],
            temperature=1.5, 
            top_p = 1
        )
        print(play.choices[0].message.content)
        extract_data = openai.chat.completions.create(
        model = "gpt-3.5-turbo", 
        messages= [
            {"role" : "system", "content" : "You are an intelligent model to extract the required data from the given data."},
            {"role" : "user", "content" :"Extract the position, and is the game completed , who won the game " + str(play.choices[0].message.content)}
        ],
        functions = function_data,
        temperature=0.5, 
        top_p = 1
        )
    except Exception:
        print("caught an  exception")

    print(extract_data.choices[0].message.function_call.arguments)

    extracted_data = json.loads(extract_data.choices[0].message.function_call.arguments)
    return extracted_data

input_matrix = [
     [1,2,3],
     [4,5,6],
     [7,8,9]
]

def play(position = 0, reset = False):
        global input_matrix
        if reset:
             input_matrix = [[1,2,3],[4,5,6],[7,8,9]]
             return input_matrix
        
        input_matrix = update_matrix(input_matrix, position, "user") 

        final_prompt = prompt + str(input_matrix) + "next move A:Let's think step by step for making a sucessful strategic move to win and defend " 

        openai_response = play_game_ai(final_prompt) 

        try : 
            input_matrix = update_matrix(input_matrix, openai_response["position"],"ai") 
        except Exception:
            print("Caught an exception...")

        
        return [input_matrix, openai_response]