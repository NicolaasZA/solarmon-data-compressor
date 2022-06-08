import requests

# python -m pip install requests

url = 'http://data.klausius.co.za/okahandja/endpoint.php'


def uploadFile(path: str) -> str:
    files = {'fileToUpload': open(path, 'rb')}
    data = {'date': '2022-05-26'}

    r = requests.post(url, files=files, data=data)
    return r.text


print(uploadFile('FILE_NAME_HERE'))
