import yaml
import os

def merge_links():
    luogu_links = []
    if os.path.exists('luogu-links.yml'):
        with open('luogu-links.yml', 'r', encoding='utf-8') as f:
            luogu_links = yaml.safe_load(f)
        print(f"Loaded {len(luogu_links[0]['link_list'])} Luogu friend links")
    else:
        print("Luogu links file not found")
    fixed_links = []
    if os.path.exists('links-fixed.yml'):
        with open('links-fixed.yml', 'r', encoding='utf-8') as f:
            fixed_links = yaml.safe_load(f)
        print(f"Loaded {len(fixed_links)} fixed friend categories")
    else:
        print("Fixed links file not found")
    merged_links = luogu_links + fixed_links
    with open('links.yml', 'w', encoding='utf-8') as f:
        yaml.dump(merged_links, f, allow_unicode=True, indent=2, sort_keys=False)
    print(f"Merged {len(merged_links)} friend categories into links.yml")
    if os.path.exists('luogu-links.yml'):
        os.remove('luogu-links.yml')
        print("Cleaned up temporary luogu-links.yml")

if __name__ == "__main__":
    merge_links()