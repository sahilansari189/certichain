import base64
from io import BytesIO

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
    import qrcode
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


