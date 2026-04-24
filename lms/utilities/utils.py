import qrcode
import base64
from io import BytesIO
from PIL import Image, ImageDraw

def generate_certificate_linkedin_url(certi,certificate_url):
    base_url = f"https://www.linkedin.com/profile/add?startTask=Course Completion"
    cert_name = certi.course.title
    org_id = "103012446"  
    issue_year = certi.created_at.year
    issue_month = certi.created_at.month
    exp_year = ""
    exp_month = ""
    cert_url = certificate_url
    cert_id = certi.uid

    linkedin_url = f"{base_url}&name={cert_name}&organizationId={org_id}" \
                   f"&issueYear={issue_year}&issueMonth={issue_month}" \
                   f"&expirationYear={exp_year}&expirationMonth={exp_month}" \
                   f"&certUrl={cert_url}&certId={cert_id}"

    return linkedin_url


def generate_qr_code_base64(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

def generate_qr_code_base64_with_img(data, logo_path='static/images/logo.png'):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")

        qr_width, qr_height = img.size
        logo_size = qr_width // 5  # 20% of QR code size
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # White background box
        draw = ImageDraw.Draw(img)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        box_coords = [
            pos[0] - 10, pos[1] - 10,  # padding
            pos[0] + logo_size + 10, pos[1] + logo_size + 10
        ]
        draw.rectangle(box_coords, fill="white")

        # Paste logo on white box
        img.paste(logo, pos, mask=logo)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return img_base64

