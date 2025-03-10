import subprocess

from django.conf import settings
from django.http import JsonResponse
from django.views import View


class UpdateView(View):
    def get(self, request):
        expected_header_key = "X-SECRET-KEY"
        expected_header_value = settings.DEPLOY_SECRET_KEY
        received_header_value = request.headers.get(expected_header_key)

        if received_header_value != expected_header_value:
            return JsonResponse(
                {"status": "error", "message": "Unauthorized access"}, status=403
            )

        try:
            script_path = "/home/pravat/kot/deploy.sh"
            subprocess.Popen(
                ["bash", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return JsonResponse(
                {"status": "started deployment", "message": "Running in background"}
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
