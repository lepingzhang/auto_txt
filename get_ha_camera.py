import os
import sys
import requests

hass_url = "http://ip:8123"
access_token = "长期访问令牌"

headers = {
    "Authorization": f"Bearer {access_token}",
    "content-type": "application/json",
}

camera_snapshot_url = f"{hass_url}/api/camera_proxy/camera.yangtai"

response = requests.get(camera_snapshot_url, headers=headers)

if response.status_code == 200:
    image_data = response.content

    file_path = '你的快照保存路径\\camera_snapshot.jpg'
    
    with open(file_path, 'wb') as file:
        file.write(image_data)
    print("成功保存截图")
else:
    print(f"获取摄像头快照失败，状态码：{response.status_code}")
    sys.exit(1)
