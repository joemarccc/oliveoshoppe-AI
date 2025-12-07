import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def chatbot_response(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'Message field is required'}, status=400)
        
        # OpenRouter API configuration
        api_key = "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"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare the conversation payload
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Olive, a friendly AI plant expert helping users care for and choose plants."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        
        # Make request to OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            api_response = response.json()
            bot_response = api_response['choices'][0]['message']['content']
            return JsonResponse({'response': bot_response})
        else:
            return JsonResponse(
                {'error': 'Failed to get response from AI service'}, 
                status=response.status_code
            )
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
