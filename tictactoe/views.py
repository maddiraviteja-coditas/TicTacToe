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
            data = play(reset = True)
            return render(request,"index.html", {"data" : data[0]})
        
        position = req.get("cell")
        # print(position)  #Just for debugging
        data = play(int(position))
        if data[1]["is_completed"] == True:
            play(reset = True)
            return render(request, 'winner.html', {"data" : data[1]["who_won"]})
        
        print(data[1])
        return render(request, 'index.html',{"data":data[0],"additional_data" : data[1]})
    else:
        data = [1,2,3]
        return render(request,'index.html',{"data" :data})


