import requests

response = requests.get('http://127.0.0.1:8000/api/notifications/2')

print("RESULT OF THE GET REQ:", '\n', response.text, '\n')

requests.post('http://127.0.0.1:8000/api/notifications', 
data={
"type":"FAIL",
"title":"TEST_FAIL",
"content":"TEST_FAIL_CONTENT"
})