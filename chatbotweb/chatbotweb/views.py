from django.http import HttpResponse
from django.shortcuts import render


def chatbot(request):
    #return HttpResponse('chatbot')
    template = loader.get_template('templates/chatbotweb.html')
    context ={
        'latest_question_list': "test",
    }
    return render(request, 'chatbot.html')
