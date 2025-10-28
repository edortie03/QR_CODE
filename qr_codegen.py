import qrcode

def gen_qr(data, file_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="white", back_color="black")
    img.save(file_name)

    print(f"QR code generated and saved as {file_name}")

# Example usage
data = "https://whatsapp.com/channel/0029VbAbtmIF1YlOG6k0zy2i"
file_name = "channel.png"
gen_qr(data, file_name)
# This code generates a QR code for the given data and saves it as an image file.