import json
from django.utils.html import escape
from django.http import JsonResponse, Http404
import google.generativeai as genai
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
import os
import markdown
from lms.models import CourseAnnouncement

# Load dotenv
load_dotenv()

# /api/generate
def generate(request):
    if request.method == "POST":
        # Make sure user is logged in
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "message": "Not authenticated!"})
        
        request_body = json.loads(request.body)
        prompt = request_body.get('prompt')
        genai.configure(api_key=os.getenv("GEMINI_API"))
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        response = model.generate_content(escape(prompt))
        print(response)

        if (not response._done):
            return JsonResponse({"success": False})
        
        return JsonResponse({"success": True, "response": response.text})
    else:
        return JsonResponse({"success": False})

def generate_tldr(request):
    if request.method != "GET":
        return JsonResponse({"success": "Wrote protocol"})

    # Make sure user is logged in
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"success": False, "message": "Not authenticated!"})
    
    type = escape(request.GET.get('type', -1))
    id = escape(request.GET.get('id', -1))

    if type == '-1' or id == '-1':
        return JsonResponse({"success": False, "message": "Missing parameter(s)!"})
    
    # Set GenAI API
    genai.configure(api_key=os.getenv("GEMINI_API"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = "Unable to get TLDR."
    
    if type == "announce":
        # Check if announcement exist
        try:
            announcement = CourseAnnouncement.objects.get(id=id)
            
            # Generate tldr
            prompt = f"Can you generate a tldr of an announcement? title is '{announcement.title}' and content is: {announcement.content}"
            response = model.generate_content(prompt)
            print(response)
        except ObjectDoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid ID!"})
    else:
        return JsonResponse({"success": False, "message": "Missing type!"})

    if (not response._done):
        return JsonResponse({"success": False})

    return JsonResponse({"success": True, "tldr": markdown.markdown(response.text)})
