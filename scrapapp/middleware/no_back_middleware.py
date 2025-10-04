from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_cache_control

class DisableBackButtonMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Apply no-cache headers
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True)
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        
   
        
