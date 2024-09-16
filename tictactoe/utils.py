import openai

# method to update the value in the matrix based on the position
# it takes 3 arguments the matrix or the board in 2d and the value to be replaced i.e., the position and who is going to modify the value.
def update_matrix(matrix, replace_value, player):
    for data_list in matrix:  # Iterating the 2d matrix 
        if replace_value in data_list:  # checking if the passed value is in the 1d list 
            index = data_list.index(replace_value)    # getting the index of the element
            if player.lower() == "ai":                # if replace made by ai it to "O"
                data_list[index] = "O"
            else:
                data_list[index] = "X"                 # if the replace is made by user it need to be "X"
    return matrix                                      # 

# method to print the matric to the console.
def print_matrix(matrix):
    for data in matrix:
        print(data)


