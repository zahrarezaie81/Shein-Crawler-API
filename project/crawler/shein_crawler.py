import asyncio
import json
import yaml
import aiohttp

from project.crawler.product_fetch import get_products
from project.loggs.logger_config import logger

def load_auth_and_config(auth_path="project/crawler/auth_data.json", config_path="project/config/config.yaml"):
    try:
        with open(auth_path, "r", encoding="utf-8") as f:
            auth_data = json.load(f)
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logger.info(f"✅ Loaded auth data and config: {len(auth_data)} entries")
        return auth_data, config.get("categories", [])
    except Exception as e:
        logger.error(f"❌ Failed to load auth/config files: {e}")
        return [], []

async def crawl_all_products():
    auth_data_list, categories = load_auth_and_config()
    if len(auth_data_list) != len(categories):
        logger.error("❌ auth_data.json and config.yaml count mismatch")
        return

    all_products = []

    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for cat, auth in zip(categories, auth_data_list):
                file_prefix = f"{cat['main_category'].replace(' ', '_')}_{cat['sub_category'].replace(' ', '_')}"
                logger.info(f"✅ Crawling category: {file_prefix}")

                task = get_products(
                    session=session,
                    cookies=auth["cookies"],
                    headers=auth["headers"],
                    params=auth["params"],
                    file_prefix=file_prefix,
                    brand=cat.get("brand", ""),
                    max_count=cat.get("max_count", 0)
                )
                tasks.append(task)

            try:
                results = await asyncio.gather(*tasks)
            except asyncio.CancelledError:
                logger.warning("⚠️ Crawl task was cancelled mid-way.")
                return


        for result in results:
            all_products.extend(result)

        logger.info(f"✅ Crawling finished: {len(all_products)} total products inserted")

    except Exception as e:
        logger.error(f"❌ Crawling process failed: {e}")
