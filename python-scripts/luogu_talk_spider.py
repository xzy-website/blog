import cloudscraper
import json
import yaml
import time
import random
import os

USER_ID = "1062508"
BASE_URL = "https://www.luogu.com.cn/api/feed/list"

def main():
    cookie = os.environ.get('cookie')
    csrf_token = os.environ.get('CSRF_TOKEN')

    headers = {}
    if csrf_token:
        headers['X-CSRF-TOKEN'] = csrf_token

    cookies = {
        '__client_id': cookie,
        '_uid': '1848124',
        'C3VK': '0eef12'
    }

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    if headers:
        scraper.headers.update(headers)

    all_feeds = []
    page = 1
    max_pages = 50
    retry_count = 0
    max_retries = 5

    while page <= max_pages:
        try:
            url = f"{BASE_URL}?user={USER_ID}&page={page}"
            print(f"Fetching talk page {page}...")
            response = scraper.get(url, timeout=30, cookies=cookies)

            if response.status_code in [403, 429] or 'FrequentRequestException' in response.text or '请求频繁' in response.text:
                if response.status_code == 403 and 'FrequentRequestException' not in response.text and '请求频繁' not in response.text:
                    print("403 Forbidden without rate-limit hint. Cookies may be invalid.")
                    print(f"Response: {response.text[:200]}")
                    break
                wait_time = (2 ** retry_count) + random.uniform(2, 6)
                print(f"Rate limit detected, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                retry_count += 1
                if retry_count > max_retries:
                    print("Max retries exceeded.")
                    break
                continue

            if response.status_code != 200:
                print(f"Unexpected status {response.status_code}, stopping.")
                break

            data = response.json()
            if 'feeds' not in data or 'result' not in data['feeds']:
                print("No feeds result structure, stopping.")
                break

            feeds = data['feeds']['result']
            if not feeds:
                print("No more feeds, stopping.")
                break

            all_feeds.extend(feeds)
            print(f"Page {page} got {len(feeds)} feeds, total {len(all_feeds)}")
            page += 1
            retry_count = 0

            delay = random.uniform(3, 6)
            print(f"Waiting {delay:.1f}s before next page...")
            time.sleep(delay)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text[:500]}")
            break
        except Exception as e:
            print(f"Exception: {e}")
            break

    talk_list = []
    for feed in all_feeds:
        content = feed.get('content', '')
        timestamp = feed.get('time')
        if timestamp is None:
            continue
        try:
            ts = int(timestamp)
        except:
            continue
        talk_list.append({'content': content, 'timestamp': ts})

    output_dir = 'source/_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'talk.yml')

    def represent_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)

    yaml.add_representer(str, represent_str)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(talk_list, f, allow_unicode=True, indent=2, sort_keys=False, default_flow_style=False)

    print(f"Written {len(talk_list)} talks to {output_file}")

if __name__ == "__main__":
    main()