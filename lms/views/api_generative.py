import json
from django.utils.html import escape
from django.http import JsonResponse, Http404
import google.generativeai as genai
from dotenv import load_dotenv
import os

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
