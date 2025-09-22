from django.shortcuts import render
import io
from django.shortcuts import render, redirect
from django.http import JsonResponse
from contacts.models import Contact
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract
import re

def Scanner(request):
    return render(request, 'scanner.html')

import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import pytesseract

@csrf_exempt
@require_POST
def scan_business_card(request):
    file = request.FILES.get("card")
    if not file:
        return JsonResponse({"success": False, "error": "No file uploaded"})

    # Save temporarily
    path = default_storage.save("tmp/" + file.name, ContentFile(file.read()))
    full_path = default_storage.path(path)

    try:
        # Run OCR
        text = pytesseract.image_to_string(Image.open(full_path))

        # Extract fields with simple regex
        email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        phone = re.search(r"(\+?\d[\d\-\s]{7,}\d)", text)

        # You might want to improve name/company extraction later
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        name = lines[0] if lines else ""
        company = lines[1] if len(lines) > 1 else ""

        return JsonResponse({
            "success": True,
            "contact": {
                "full_name": name,
                "email": email.group(0) if email else "",
                "phone": phone.group(0) if phone else "",
                "company": company,
            }
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

