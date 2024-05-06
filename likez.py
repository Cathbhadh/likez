import streamlit as st
import requests
import json

def fetch_data(user_id, offset=0, limit=500, include_nsfw=True):
    url = f"https://api.yodayo.com/v1/users/{user_id}/likes?offset={offset}&limit={limit}&width=600&include_nsfw={include_nsfw}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def count_liked_posts(data):
    liked_posts = {}
    for post in data:
        user_uuid = post['user_uuid']
        profile_name = post['profile']['name']
        if user_uuid in liked_posts:
            liked_posts[user_uuid]['count'] += 1
        else:
            liked_posts[user_uuid] = {'name': profile_name, 'count': 1}
    return liked_posts

def main():
    st.title("Liked Posts Analysis")
    user_id = st.text_input("Enter user ID:")

    if user_id:
        offset = 0
        all_data = []
        while True:
            data = fetch_data(user_id, offset=offset)
            if not data:
                break
            all_data.extend(data)
            offset += 500

        liked_posts = count_liked_posts(all_data)
        st.subheader("Liked Posts Count")
        for user_uuid, info in liked_posts.items():
            st.write(f"{info['name']}: {info['count']}")

if __name__ == "__main__":
    main()
