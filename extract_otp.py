import json
from base64 import b32encode, b64decode
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image
from pyzbar.pyzbar import decode

from google_auth_pb import google_auth_pb2


def main():
  input_dir = Path('./inputs')
  output_dir = Path('./outputs')

  if not input_dir.exists():
    print("Input directory missing!")
    exit(1)

  if not output_dir.exists():
    output_dir.mkdir(exist_ok=True)

  for path in input_dir.glob("**/*"):
    # Read the image.
    image = Image.open(path)

    # Get the URL from the QR image.
    decoded_qr_data = decode(image)
    decoded_url = decoded_qr_data[0].data.decode('ascii')
    parsed_url = urlparse(decoded_url)

    # Parse the data field of the params to get the secret.
    params = parse_qs(parsed_url.query, strict_parsing=True)
    data_base64 = params['data'][0]
    data_base64_fixed = data_base64.replace(' ', '+')
    data = b64decode(data_base64_fixed, validate=True)
    payload = google_auth_pb2.MigrationPayload()
    payload.ParseFromString(data)

    # Decode the secret and process data.
    output = []
    for otp_data in payload.otp_parameters:
      decoded_secret = str(b32encode(otp_data.secret), 'utf-8')
      output.append({
        'secret': decoded_secret,
        'issuer': otp_data.issuer,
        'name': otp_data.name
      })

    # Write to file.
    output_path = (output_dir / path.name).with_suffix('.json')
    with output_path.open('w') as f:
      json.dump(output, f, indent=2)

if __name__ == "__main__":
  main()