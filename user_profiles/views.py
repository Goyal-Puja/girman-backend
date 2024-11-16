# //from django.shortcuts import render

import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# View to fetch user data based on search query
@csrf_exempt
def get_user_data(request):
    # Define the path to the JSON file
    json_file_path = os.path.join(settings.BASE_DIR, 'data','users.json')
    
    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as file:
            user_data = json.load(file)
        
        # If search parameters are provided, filter data
        search_term = request.GET.get('search', '').lower()
        if search_term:
            user_data = [
                user for user in user_data if search_term in user['first_name'].lower() or search_term in user['last_name'].lower()
            ]

        # Return the data as a JSON response
        return JsonResponse(user_data, safe=False)
    
    except FileNotFoundError:
        return JsonResponse({'error': 'JSON file not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error parsing JSON file'}, status=400)
