import requests
import json
import time


def get_all_reviews(api_url, initial_payload, headers):
    all_reviews = []
    page_number = 1

    while True:
        print(f"Fetching page {page_number}")
        try:
            response = requests.post(
                # Add timeout here
                api_url, headers=headers, data=json.dumps(initial_payload), timeout=10
            )
        except requests.exceptions.Timeout:
            print(f"Request timed out for page {page_number}.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Request failed for page {page_number} with error: {e}")
            break

        if response.status_code != 200:
            print(
                f"Failed to fetch page {page_number}, status code: {response.status_code}")
            break

        data = response.json()

        if 'errors' in data:
            print(f"API returned errors: {data['errors']}")
            break

        if 'data' in data and 'getReviews' in data['data']:
            reviews = data['data']['getReviews']['edges']
            all_reviews.extend(reviews)
            total_count = data['data']['getReviews']['totalCount']
            page_info = data['data']['getReviews']['pageInfo']
            next_page_token = page_info.get('nextPageToken')

            if next_page_token:
                initial_payload['variables']['pagination'] = {
                    "after": next_page_token, "limit": 30
                }
                page_number += 1
                time.sleep(1)
                print(f"Got {len(all_reviews)} reviews")
            else:
                break
        else:
            print(f"No more data available or error in data structure.")
            break

    return all_reviews


# API endpoint URL
api_url = "https://kxbwmqov6jgg3daaamb744ycu4.appsync-api.us-east-1.amazonaws.com/graphql"

# Initial payload for the API request
initial_payload = {
    "operationName": "getReviews",
    "query": """
        query getReviews($filters: BookReviewsFilterInput!, $pagination: PaginationInput) {
          getReviews(filters: $filters, pagination: $pagination) {
            totalCount
            edges {
              node {
                id
                creator {
                  name
                  imageUrlSquare
                }
                text
                rating
                createdAt
                updatedAt
              }
            }
            pageInfo {
              nextPageToken
            }
          }
        }
    """,
    "variables": {
        "filters": {
            "resourceType": "WORK",
            "resourceId": "kca://work/amzn1.gr.work.v1.4TDi1WBhgl0QMST5ez9_Fg"
        },
        "pagination": {
            "limit": 30
        }
    }
}

# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": "da2-xpgsdydkbregjhpr6ejzqdhuwy"
}

# Get all reviews
all_reviews = get_all_reviews(api_url, initial_payload, headers)

# Output the total number of reviews retrieved
print(f"Total number of reviews retrieved: {len(all_reviews)}")

# Write reviews to file
with open('TheAwakeningOutput.txt', 'w', encoding='utf-8') as f:
    for review in all_reviews:
        f.write(review['node']['text'] + '\n')

print("Reviews saved to TheAwakeningOutput.txt")
