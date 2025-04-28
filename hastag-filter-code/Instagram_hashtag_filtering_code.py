import requests
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("instagram_fetcher.log"), logging.StreamHandler()]
)

# Load environment variables from .env file
load_dotenv()

class InstagramFetcher:
    """Class to fetch and filter Instagram posts by hashtags."""
    
    def __init__(self):
        # Load credentials from environment variables for security
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.user_id = os.getenv('INSTAGRAM_USER_ID')
        self.base_url = 'https://graph.instagram.com'
        self.api_version = 'v17.0'  # Updated to a more recent API version
        
        # Define relevant hashtags and keywords
        self.tech_hashtags = ['programming', 'coding', 'technology', 'python', 'javascript']
        self.exclude_keywords = ['love', 'breakup', 'relationship', 'social']
        
        # Validate credentials
        if not self.access_token or not self.user_id:
            raise ValueError("Missing Instagram credentials. Please set INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_USER_ID in .env file.")

    def fetch_hashtag_id(self, hashtag):
        """Fetch the ID for a given hashtag."""
        url = f"{self.base_url}/{self.api_version}/ig_hashtag_search"
        params = {
            'user_id': self.user_id,
            'q': hashtag,
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes
            
            data = response.json()
            if data.get('data'):
                return data['data'][0]['id']
            else:
                logging.warning(f"No hashtag ID found for #{hashtag}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching hashtag ID for #{hashtag}: {e}")
            return None

    def fetch_posts_by_hashtag_id(self, hashtag_id, limit=10):
        """Fetch recent media posts for a hashtag ID."""
        url = f"{self.base_url}/{self.api_version}/{hashtag_id}/recent_media"
        params = {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,username',
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('data', [])
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching posts for hashtag ID {hashtag_id}: {e}")
            return []
    
    def filter_posts(self, posts):
        """Filter posts based on exclude keywords and retain only tech-relevant content."""
        filtered_posts = []
        
        for post in posts:
            caption = post.get('caption', '').lower() if post.get('caption') else ''
            
            # Skip posts containing excluded keywords
            if any(keyword.lower() in caption for keyword in self.exclude_keywords):
                continue
                
            # Ensure the post has at least some tech-related content
            if any(tag.lower() in caption for tag in self.tech_hashtags):
                filtered_posts.append(post)
                
        return filtered_posts
    
    def format_post(self, post):
        """Format a post for readability."""
        caption = post.get('caption', 'No caption')
        username = post.get('username', 'Unknown user')
        timestamp = post.get('timestamp')
        if timestamp:
            # Convert ISO format to readable date
            date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            timestamp_formatted = date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_formatted = 'Unknown date'
            
        return {
            'username': username,
            'date': timestamp_formatted,
            'caption': caption[:100] + '...' if len(caption) > 100 else caption,
            'media_type': post.get('media_type', 'Unknown'),
            'permalink': post.get('permalink', '#'),
            'media_url': post.get('media_url', None)
        }
    
    def run(self, posts_per_hashtag=10):
        """Main method to fetch and display relevant posts."""
        all_posts = []
        
        logging.info(f"Starting to fetch posts for {len(self.tech_hashtags)} hashtags")
        
        # Fetch posts for each tech hashtag
        for hashtag in self.tech_hashtags:
            logging.info(f"Processing hashtag: #{hashtag}")
            
            # Get hashtag ID
            hashtag_id = self.fetch_hashtag_id(hashtag)
            if not hashtag_id:
                continue
                
            # Add rate limiting to avoid API limits
            time.sleep(1)
            
            # Get posts for this hashtag
            posts = self.fetch_posts_by_hashtag_id(hashtag_id, limit=posts_per_hashtag)
            logging.info(f"Found {len(posts)} posts for #{hashtag}")
            all_posts.extend(posts)
        
        # Filter posts to exclude irrelevant content
        filtered_posts = self.filter_posts(all_posts)
        logging.info(f"Filtered down to {len(filtered_posts)} relevant tech posts")
        
        # Process and return formatted posts
        return [self.format_post(post) for post in filtered_posts]

def main():
    """Run the Instagram tech content fetcher."""
    try:
        fetcher = InstagramFetcher()
        posts = fetcher.run()
        
        # Display filtered posts
        print(f"\n=== {len(posts)} Filtered Programming and Technology Posts ===\n")
        for i, post in enumerate(posts, 1):
            print(f"[{i}] Posted by {post['username']} on {post['date']}")
            print(f"Caption: {post['caption']}")
            print(f"Type: {post['media_type']}")
            print(f"Link: {post['permalink']}")
            print("-" * 70)
            
        return posts
        
    except Exception as e:
        logging.error(f"Application error: {e}")
        return []

if __name__ == "__main__":
    main()