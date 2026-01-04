import json
import base64
import uuid
import qrcode
import cloudinary
import cloudinary.uploader
from io import BytesIO

cloudinary.config(
    cloud_name="dztntkuwn",
    api_key="658259493959287",
    api_secret="lVkJN4C8L7OxTAOyyejs80Nr-7E"
)

def handler(event, context):
    body = json.loads(event["body"])
    file_base64 = body["file"]
    filename = f"{uuid.uuid4()}.pdf"

    pdf_bytes = base64.b64decode(file_base64)

    upload = cloudinary.uploader.upload(
        BytesIO(pdf_bytes),
        resource_type="raw",
        public_id=filename
    )

    pdf_url = upload["secure_url"]

    qr = qrcode.make(pdf_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "pdf_url": pdf_url,
            "qr": qr_base64
        })
    }
