import yaml
import json
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth
from urllib.parse import urlparse, parse_qs
import time
from project.loggs.logger_config import logger


def load_config(path="project/config/config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logger.info(f"✅ Config loaded from {path}")
            return config
    except FileNotFoundError:
        logger.error(f"❌ Config file not found: {path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"❌ Failed to parse YAML from {path}: {e}")
        raise

def fetch_all_auth_data(save_to_file=True, output_path="project/crawler/auth_data.json"):
    config = load_config()
    stealth = Stealth()

    important_cookies = [
        'ndp_session_id', '_cbp', 'fita.sid.shein', 'memberId', 'AT',
        'sessionID_shein', 'armorUuid', '_derived_epik', 'zpnvSrwrNdywdz', 'smidV2'
    ]
    important_headers = [
        'accept', 'accept-language', 'anti-in', 'armortoken', 'origin', 'priority',
        'referer', 'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform',
        'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'smdeviceid',
        'uber-trace-id', 'user-agent', 'webversion', 'x-ad-flag', 'x-csrf-token',
        'x-gw-auth', 'x-oest', 'x-requested-with'
    ]
    important_params = [
        '_ver', '_lang', 'cat_id', 'cate_type', 'page_name', 'src_tab_page_id',
        'adp', 'page', 'limit', '_type'
    ]

    collected_auth_data = []

    with sync_playwright() as p:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        user_data_dir = "C:/Users/zahra/AppData/Local/Google/Chrome/User Data/Profile 3"
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            executable_path=chrome_path,
            viewport={'width': 1400, 'height': 900}
        )

        url = "https://us.shein.com"

        for i, cat in enumerate(config["categories"]):
            main_cat = cat["main_category"]
            sub_cat = cat["sub_category"]
            logger.info(f"📁 Processing category {i+1}/{len(config['categories'])}: {main_cat} > {sub_cat}")

            headers_dict = {}
            params_dict = {}
            got_auth = {"found": False}

            def handle_request(request):
                request_url = request.url
                if "bff-api/category/real_category_goods_list" in request_url and not got_auth["found"]:
                    parsed_url = urlparse(request_url)
                    params_raw = parse_qs(parsed_url.query)
                    nonlocal headers_dict, params_dict
                    req_headers = dict(request.headers)
                    headers_dict = {k: v for k, v in req_headers.items() if k in important_headers}
                    params_dict = {
                        k: v[0] if isinstance(v, list) and len(v) == 1 else v
                        for k, v in params_raw.items() if k in important_params
                    }
                    got_auth["found"] = True
                    logger.info(f"✅ Auth data captured for: {main_cat} > {sub_cat}")

            page = context.new_page()
            stealth.apply_stealth_sync(page)
            page.on("request", handle_request)
            page.goto(url, wait_until="load", timeout=60000)
            time.sleep(6)

            try:
                page.wait_for_selector("text=Categories", timeout=8000)
                cat_menu = page.locator("text=Categories").first
                cat_menu.click()
                time.sleep(1)
            except Exception as e:
                logger.warning(f"⚠️ Couldn't click 'Categories' menu: {e}")

            try:
                page.wait_for_selector(f"text={main_cat}", timeout=8000)
                main_cat_select = page.locator(f"text={main_cat}").first
                main_cat_select.hover()
                time.sleep(1)
            except Exception as e:
                logger.warning(f"⚠️ Couldn't hover main category '{main_cat}': {e}")

            try:
                sub_cat_locator = page.locator(
                    f'a.bs-cate-type_img-link:has(span.bs-cate-type_text:has-text("{sub_cat}"))'
                ).first
                sub_cat_locator.wait_for(state="visible", timeout=15000)
                sub_cat_locator.click()
            except Exception as e:
                logger.warning(f"⚠️ Couldn't click sub category '{sub_cat}': {e}")

            wait_time = 0
            while not got_auth["found"] and wait_time < 20:
                time.sleep(1)
                wait_time += 1

            cookies = context.cookies()
            cookies_dict = {
                c['name']: c['value']
                for c in cookies if c['name'] in important_cookies
            }

            collected_auth_data.append({
                "main_category": main_cat,
                "sub_category": sub_cat,
                "cookies": cookies_dict,
                "headers": headers_dict,
                "params": params_dict
            })

            logger.info(f"✅ Collected auth data for: {main_cat} > {sub_cat}")
            page.close()

        context.close()

    if save_to_file:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(collected_auth_data, f, indent=4, ensure_ascii=False)
        logger.info(f"💾 Saved auth data to file: {output_path}")

    return collected_auth_data

if __name__ == "__main__":
    fetch_all_auth_data()
