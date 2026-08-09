import cloudscraper
import json
import yaml
import time
import random
import os

class LuoguFriendLinkSpider:
    def __init__(self):
        self.base_url = "https://www.luogu.com.cn/api/user/followings"
        self.user_id = "1062508"

        self.cookies = {
            '__client_id': os.environ.get('cookie'),
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
        page = 1
        retry_count = 0
        max_retries = 5

        while page <= max_pages:
            try:
                print(f"Crawling page {page}...")
                url = f"{self.base_url}?user={self.user_id}&page={page}"

                response = self.scraper.get(
                    url,
                    timeout=30,
                    cookies=self.cookies
                )

                is_rate_limited = (
                    response.status_code in [403, 429] or
                    '访问过于频繁' in response.text or
                    'too frequent' in response.text.lower()
                )

                if is_rate_limited:
                    if response.status_code == 403 and '访问过于频繁' not in response.text:
                        print("403 Forbidden without rate-limit hint. Cookies may be invalid.")
                        print(f"Response preview: {response.text[:200]}")
                        break

                    wait_time = (2 ** retry_count) + random.uniform(2, 6)
                    print(f"Rate limit detected. Waiting {wait_time:.1f} seconds before retry...")
                    time.sleep(wait_time)
                    retry_count += 1
                    if retry_count > max_retries:
                        print("Max retries exceeded. Aborting this page.")
                        break
                    continue

                if response.status_code != 200:
                    print(f"Unexpected status code {response.status_code}. Stopping.")
                    break

                data = response.json()

                if 'users' not in data or 'result' not in data['users']:
                    print("Unexpected data structure. Stopping.")
                    break

                users = data['users']['result']
                if not users:
                    print(f"No users found on page {page}. Stopping.")
                    break

                for user in users:
                    self.process_user(user)

                print(f"Page {page} completed. Fetched {len(users)} users.")
                retry_count = 0
                page += 1

                delay = random.uniform(8, 15)
                print(f"Waiting {delay:.1f} seconds before next request...")
                time.sleep(delay)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Response text: {response.text[:500]}")
                break
            except Exception as e:
                print(f"Exception occurred: {e}")
                break

    def process_user(self, user):
        try:
            name = user.get('name', '')
            avatar = user.get('avatar', '')
            slogan = user.get('slogan', '')
            uid = user.get('uid', '')
            link = f"https://www.luogu.com/user/{uid}"
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
            print(f"Error processing user: {e}")

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
            print(f"YAML file generated: {filename}")
            print(f"Total friends: {len(self.friend_links)}")
        except Exception as e:
            print(f"Error generating YAML: {e}")

    def run(self):
        print("Starting Luogu following list crawler...")
        print(f"Using cookies: {list(self.cookies.keys())}")
        self.crawl_followings()
        if self.friend_links:
            self.generate_yaml()
            print("\n=== Statistics ===")
            print(f"Total friends: {len(self.friend_links)}")
            print("\n=== First 5 friends ===")
            for i, friend in enumerate(self.friend_links[:5], 1):
                print(f"{i}. {friend['name']} - {friend['link']}")
        else:
            print("No friends fetched. Please check cookies or network.")

if __name__ == "__main__":
    spider = LuoguFriendLinkSpider()
    spider.run()
