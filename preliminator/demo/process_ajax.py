@csrf_exempt
def ajax_view(request):
    response = []
    #Here you have to enter code here
    #to receive the data (datastring) you send here by POST
    #Do the operations you need with the form information
    #Add the data you need to send back to a list/dictionary like response
    #And return it to the JQuery function `enter code here`(simplejson.dumps is to convert to JSON)
    return HttpResponse(simplejson.dumps(response))
