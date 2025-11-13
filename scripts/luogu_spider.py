import requests
import json
import yaml
import time

class LuoguFriendLinkSpider:
    def __init__(self):
        self.base_url = "https://www.luogu.com.cn/api/user/followings"
        self.user_id = "1062508"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.luogu.com.cn',
            'Referer': f'https://www.luogu.com.cn/user/{self.user_id}',
        }
        self.friend_links = []

    def crawl_followings(self, max_pages=20):
        for page in range(1, max_pages + 1):
            try:
                print(f"Crawling page {page}...")
                url = f"{self.base_url}?user={self.user_id}&page={page}"
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code != 200:
                    print(f"Page {page} request failed, status code: {response.status_code}")
                    break
                data = response.json()
                if 'users' not in data or 'result' not in data['users']:
                    print(f"No data on page {page}, stopping")
                    break
                users = data['users']['result']
                if not users:
                    print(f"Empty user list on page {page}, stopping")
                    break
                for user in users:
                    self.process_user(user)
                print(f"Page {page} completed, got {len(users)} users")
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                print(f"Request exception on page {page}: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"JSON decode error on page {page}: {e}")
                break
            except Exception as e:
                print(f"Unknown exception on page {page}: {e}")
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