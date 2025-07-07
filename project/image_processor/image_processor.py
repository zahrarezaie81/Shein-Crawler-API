import base64
import requests
url="//img.ltwebstatic.com/images3_pi/2025/03/06/85/1741234726d8861240454820e3030dd89e3d3cbc3e_thumbnail_405x552.jpg"
def image_url_to_base64(url):
    url = "https:" + url
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download image.")
    return base64.b64encode(response.content).decode('utf-8')

# if __name__ == "__main__":


#     test_url = "//img.ltwebstatic.com/images3_pi/2025/03/06/85/1741234726d8861240454820e3030dd89e3d3cbc3e_thumbnail_405x552.jpg"
#     try:
#         b64_url = image_url_to_base64(test_url)
#         print("result : ", b64_url, "...")
#     except Exception as e:
#         print("خطا در تبدیل url:", e)