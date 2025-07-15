import aiohttp
import json
from datetime import datetime
import os
import sys
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from project.loggs.logger_config import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.crud import insert_product
from database.database import SessionLocal

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(5),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
async def fetch_with_retry(session, url, cookies, headers, params, file_prefix):
    try:
        async with session.post(url, cookies=cookies, headers=headers, params=params, timeout=20) as response:
            if response.status != 200:
                raise Exception(f"❌ Status code {response.status} for {file_prefix}")
            return await response.json()
    except Exception as e:
        logger.warning(f"⚠️ Attempt failed for {file_prefix}: {e}")
        raise

async def get_products(session, cookies, headers, params, file_prefix="output", brand="", max_count=0):
    url = 'https://us.shein.com/bff-api/category/real_category_goods_list'
    logger.info(f"✅ Starting task for {file_prefix} at {datetime.now().time()}")

    try:
        data = await fetch_with_retry(session, url, cookies, headers, params, file_prefix)
    except Exception as e:
        logger.error(f"❌ Failed to fetch data for {file_prefix} after retries: {e}")
        return []

    info = data.get("info", {})
    products = info.get("products", [])
    category_name = info.get("category_name", "")
    cat_name_url = category_name.lower().replace(" ", "-")
    category_id = params.get("cat_id", "")

    if not isinstance(products, list):
        logger.warning(f"⚠️ Unexpected products format in {file_prefix}")
        return []

    if brand:
        original_count = len(products)
        products = [p for p in products if p.get("premiumFlagNew", {}).get("brandName", "").lower() == brand.lower()]
        logger.info(f"✅ Filtered {original_count} → {len(products)} for brand: {brand}")

    if max_count > 0:
        products = products[:max_count]
        logger.info(f"✅ Truncated to max_count={max_count}")

    db = SessionLocal()
    product_list = []
    try:
        for p in products:
            item = {
                "Product ID": p.get("goods_id", ""),
                "Product Name": p.get("goods_name", ""),
                "Discounted Price": p.get("salePrice", {}).get("amount", ""),
                "Price": p.get("retailPrice", {}).get("amount", ""),
                "Brand": p.get("premiumFlagNew", {}).get("brandName", ""),
                "Image URL": p.get("goods_img", ""),
                "Product URL": f"https://us.shein.com/{p.get('goods_url_name', '')}-p-{p.get('goods_id', '')}.html",
                "Category Name": category_name,
                "Category URL": f"http://us.shein.com/{cat_name_url}-c-{category_id}.html"
            }
            product_list.append(item)
            insert_product(db, item)
    finally:
        db.close()

    os.makedirs("output_jsons", exist_ok=True)
    json_filename = f"output_jsons/{file_prefix}_products.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(product_list, f, indent=4, ensure_ascii=False)

    logger.info(f"✅ {file_prefix}: {len(product_list)} products saved and inserted")
    return product_list
