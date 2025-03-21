import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from starlette.config import Config

config = Config('.env')
def send_email_with_inline_qr(to_email, qr_data):
    # 1. QR 코드 생성
    qr = qrcode.make(qr_data)

    # 2. 이미지를 메모리에 저장
    img_io = BytesIO()
    qr.save(img_io, format='PNG')
    img_io.seek(0)

    # 3. 이메일 메시지 생성 (MIME 멀티파트)
    msg = MIMEMultipart('related')
    msg['Subject'] = 'OTP 인증용 메일 입니다'
    msg['From'] = config("EMAIL")
    msg['To'] = to_email

    # 4. HTML 본문 작성 (이미지를 cid로 삽입)
    html = f"""
    <html>
      <body>
        <p>안녕하세요,<br>
           아래 QR 코드를 확인해주세요:<br>
           <img src="cid:qrcode_image">
           QR코드 스캔이 어려우다면 아래 코드를 입력해주세요.
           <br>
           {qr_data}
        </p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    # 5. QR 코드 이미지 추가 (Content-ID를 'qrcode_image'로 지정)
    img = MIMEImage(img_io.read(), _subtype='png')
    img.add_header('Content-ID', '<qrcode_image>')
    img.add_header('Content-Disposition', 'inline', filename='qrcode.png')
    msg.attach(img)

    # 6. SMTP로 전송
    with smtplib.SMTP_SSL('smtp.naver.com', 465) as smtp:
        smtp.login(config("EMAIL_ID"), config("EMAIL_PASSWORD"))  # 앱 비밀번호 사용
        smtp.send_message(msg)