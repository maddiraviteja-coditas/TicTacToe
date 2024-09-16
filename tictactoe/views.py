from django.shortcuts import render, redirect
from django.http import request
from tictactoe.ai_call import play
# Create your views here.

def game(request):
    print(request.method)
    if request.method == "POST":
        req = request.POST
        do_reset = req.get("reset")

        # print(do_reset) # Just for debugging

        if do_reset == "True":
            ai_response = play(reset = True)
            return render(request,"index.html", {"ai_response" : ai_response[0]})
        
        position = req.get("cell")
        # print(position)  #Just for debugging
        ai_response = play(int(position))
        if ai_response[1]["is_completed"] == True:
            play(reset = True)
            return render(request, 'winner.html', {"ai_response" : ai_response[1]["who_won"]})
        
        print(ai_response[1])
        return render(request, 'index.html',{"ai_response":ai_response[0],"additional_data" : ai_response[1]})
    else:
        ai_response = [1,2,3]
        return render(request,'index.html',{"ai_response" :ai_response})


