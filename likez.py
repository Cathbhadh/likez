import streamlit as st
import requests

def fetch_data(user_id, access_token, offset=0, limit=500, include_nsfw=True):
    url = f"https://api.yodayo.com/v1/users/{user_id}/likes?offset={offset}&limit={limit}&width=600&include_nsfw={include_nsfw}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return []

def count_liked_posts(data):
    liked_posts = {}
    for post_data in data:
        if post_data:
            post = eval(post_data)
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
    access_token = st.text_input("Enter access token:")

    if user_id and access_token:
        offset = 0
        all_data = []
        while True:
            data = fetch_data(user_id, access_token, offset=offset, limit=500)
            if not data:
                break
            posts = eval(data)  # assuming the response is a valid Python list of dictionaries
            all_data.extend([str(post) for post in posts])
            offset += 500

        liked_posts = count_liked_posts(all_data)
        st.subheader("Liked Posts Count")
        for user_uuid, info in liked_posts.items():
            st.write(f"{info['name']}: {info['count']}")

if __name__ == "__main__":
    main()
