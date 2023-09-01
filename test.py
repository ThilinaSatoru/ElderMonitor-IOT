import requests

stream = ['bash', './bash_stream.sh']
API_URL = 'http://127.0.0.1:8090'
last_file = ''


def api_post_image(image):
    url = API_URL + '/img'
    file = {'file': open(image, 'rb')}
    req = requests.post(url=url, files=file)
    print(req.status_code)
    print(image)


if __name__ == '__main__':
    try:
        api_post_image('captures/cosmo-logo.png')

    except Exception as e:
        print("some error : " + str(e))
