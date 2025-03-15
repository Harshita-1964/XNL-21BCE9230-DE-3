import pyotp  # For MFA (One-Time Password)
import cv2  # For biometric verification using facial recognition

# MFA with Google Authenticator (or similar)
def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    print(f"Generated OTP: {otp}")
    return otp

def verify_otp(otp, secret):
    totp = pyotp.TOTP(secret)
    if totp.verify(otp):
        print("OTP verified successfully!")
        return True
    else:
        print("Invalid OTP.")
        return False

def verify_face():
    
    cap = cv2.VideoCapture(0)

    
    ret, frame = cap.read()

    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)

    if len(faces) > 0:
        print("Face recognized.")
        return True
    else:
        print("Face not recognized.")
        return False

    cap.release()


secret = "JBSWY3DPEHPK3PXP"
otp = generate_otp(secret)
verify_otp(otp, secret)

if verify_face():
    print("User verified successfully.")
else:
    print("Biometric verification failed.")
