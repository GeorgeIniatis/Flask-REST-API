# Postman or other tools could also be used to do the same job

import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "Cat Video", "views": 1000, "likes": 10, },
    {"name": "Dog Video", "views": 2300, "likes": 84, },
    {"name": "Penguin Video", "views": 854, "likes": 33, },
    {"name": "Sloth Video", "views": 354845, "likes": 1000, }
]

# Insert some videos
index = 0
for video in data:
    response = requests.post(BASE + f"video/{index}", video)
    print(response.json())
    index += 1

# Retrieve a video
response = requests.get(BASE + "video/3")
print(response.json())

# Update a video
response = requests.patch(BASE + "video/3", {"name": "Giraffe Video", "likes": 1634})
print(response.json())

# Delete a video
response = requests.delete(BASE + "video/3")
print(response)

# Retrieve all videos
response = requests.get(BASE + "videos")
print(response.json())