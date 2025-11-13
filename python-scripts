import cloudscraper
import json
import yaml
import time
import random

class LuoguFriendLinkSpider:
    def __init__(self):
        self.base_url = "https://www.luogu.com.cn/api/user/followings"
        self.user_id = "1062508"
        
        self.cookies = {
            '__client_id': '19fcee76ca7dda5f6903570c91a4cc6993bd2312',
            '_uid': '1848124',
            'C3VK': '0eef12'
        }
        
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        self.friend_links = []

    def crawl_followings(self, max_pages=20):
        for page in range(1, max_pages + 1):
            try:
                print(f"Crawling page {page}...")
                url = f"{self.base_url}?user={self.user_id}&page={page}"
                
                response = self.scraper.get(
                    url, 
                    timeout=30,
                    cookies=self.cookies
                )
                
                if response.status_code != 200:
                    print(f"Page {page} request failed, status code: {response.status_code}")
                    print(f"Response text: {response.text[:500]}")
                    
                    if response.status_code == 403:
                        print("Access forbidden. Cookies might be expired.")
                    
                    break
                
                data = response.json()
                
                if 'users' not in data or 'result' not in data['users']:
                    print(f"No data structure on page {page}, stopping")
                    break
                
                users = data['users']['result']
                if not users:
                    print(f"Empty user list on page {page}, stopping")
                    break
                
                for user in users:
                    self.process_user(user)
                
                print(f"Page {page} completed, got {len(users)} users")
                time.sleep(random.uniform(2, 4))
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error on page {page}: {e}")
                print(f"Response text: {response.text[:500]}")
                break
            except Exception as e:
                print(f"Exception on page {page}: {e}")
                break

    def process_user(self, user):
        try:
            name = user.get('name', '')
            avatar = user.get('avatar', '')
            slogan = user.get('slogan', '')
            uid = user.get('uid', '')
            link = f"https://www.luogu.com.cn/user/{uid}"
            friend_info = {
                'name': name,
                'link': link,
                'avatar': avatar,
                'descr': slogan or 'This user is too lazy to write anything'
            }
            if name and name != 'null':
                self.friend_links.append(friend_info)
                print(f"Added user: {name}")
        except Exception as e:
            print(f"Error processing user info: {e}")

    def generate_yaml(self, filename='luogu-links.yml'):
        luogu_section = [
            {
                'class_name': 'Luogu Friends',
                'class_desc': 'Automatically generated from Luogu followings',
                'link_list': self.friend_links
            }
        ]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(luogu_section, f, allow_unicode=True, indent=2, sort_keys=False)
            print(f"Luogu friend links file generated: {filename}")
            print(f"Total Luogu friends obtained: {len(self.friend_links)}")
        except Exception as e:
            print(f"Error generating YAML file: {e}")

    def run(self):
        print("Starting Luogu following list crawl...")
        print(f"Using cookies: {list(self.cookies.keys())}")
        self.crawl_followings()
        if self.friend_links:
            self.generate_yaml()
            print("\n=== Crawl Statistics ===")
            print(f"Total Luogu friend links: {len(self.friend_links)}")
            print("\n=== First 5 Friend Links Example ===")
            for i, friend in enumerate(self.friend_links[:5], 1):
                print(f"{i}. {friend['name']} - {friend['link']}")
        else:
            print("No friend links obtained")

if __name__ == "__main__":
    spider = LuoguFriendLinkSpider()
    spider.run()
