import streamlit as st
import requests

# Function to authenticate with access token
def authenticate_with_token(access_token):
    session = requests.Session()
    jar = requests.cookies.RequestsCookieJar()
    jar.set("access_token", access_token)
    session.cookies = jar
    return session

# Function to fetch data from API in batches
def fetch_data(access_token, user_id):
    offset = 0
    limit = 500
    data = []

    session = authenticate_with_token(access_token)

    while True:
        response = session.get(f"https://api.yodayo.com/v1/users/{user_id}/likes",
                               params={"offset": offset, "limit": limit, "width": 600, "include_nsfw": True})
        batch_data = response.json()
        if not batch_data:
            break
        data.extend(batch_data)
        offset += limit

    return data

# Function to count liked posts for each user
def count_likes(data):
    like_counts = {}
    for item in data:
        user_uuid = item['user_uuid']
        if user_uuid in like_counts:
            like_counts[user_uuid] += 1
        else:
            like_counts[user_uuid] = 1
    return like_counts

# Streamlit app
def main():
    st.title("Liked Posts Analysis")

    access_token = st.text_input("Enter Access Token:")
    user_id = st.text_input("Enter User ID:")

    if st.button("Fetch and Analyze Data"):
        if access_token and user_id:
            st.text("Fetching data...")
            data = fetch_data(access_token, user_id)
            st.text("Analyzing data...")
            like_counts = count_likes(data)

            st.text("Results:")
            for user_uuid, count in like_counts.items():
                st.write(f"User UUID: {user_uuid}, Liked Posts Count: {count}")
        else:
            st.warning("Please enter Access Token and User ID.")

if __name__ == "__main__":
    main()
