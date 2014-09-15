import subprocess
import os

def detect():
    #Detects qr code(s) from camera and returns a list that represents the code(s).

    subprocess.call(["raspistill -n -t 1 -w 512 -h 512 -o cam.png"],shell=True)
    out = subprocess.Popen(["zbarimg -D cam.png"], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True).communicate()[0] 
    qr_code = None

    # out looks like "QR-Code: Xuz213asdY...\n" so you need
    # to remove it and split into list 
    if len(out) > 8:
        out = out.replace('QR-code: ','')
        qr_code = out.replace('QR-Code:','').split()
    return qr_code
