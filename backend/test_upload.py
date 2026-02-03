import requests

# URL of your Django API
url = "http://127.0.0.1:8000/api/upload/"

# Path to your sample CSV
file_path = "../sample_equipment_data.csv"

# Superuser credentials
username = "bhagyasri"
password = "bhagyasri"  # replace with the password you set

# Open the CSV file and send POST request
with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files, auth=(username, password))

# Print status and JSON response
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except:
    print("Response Text:", response.text)
