from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated
from sqlalchemy.orm import Session
from project.database.database import get_db
from project.database import crud
from project.database.schemas import BrandOut, BrandCountOut, ProductOut, ImageContentIn, ImageContentOut
from project.image_processor.image_processor import image_url_to_base64
from project.database.database import engine, Base
from project.loggs.logger_config import logger
import asyncio
from project.crawler.shein_crawler import crawl_all_products
from project.loggs.logger_config import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SHEIN")

is_crawling = False
crawl_task = None


@app.get("/brands", response_model=list[BrandOut])
def get_brands(db: Annotated[Session, Depends(get_db)]):
    return crud.get_brands(db)

@app.get("/brands/{brand}/count", response_model=BrandCountOut)
def brand_count(brand: str, db: Annotated[Session, Depends(get_db)]):
    count = crud.count_products_for_brand(db, brand)
    return {"brand": brand, "count": count}

@app.get("/products/filter", response_model=list[ProductOut])
def filter_products(
    db: Annotated[Session, Depends(get_db)],
    min: float = Query(20), 
    max: float = Query()
):
    products = crud.filter_products_by_price(db, min, max)
    return [
        {
            "id": p.id,
            "title": p.title,
            "url" : p.url,
            "img_url": p.image_urls,
            "category": p.category.name if p.category else None,
            "price": p.price,
            "discounted_price": p.discounted_price,
        } for p in products
    ]


@app.post("/crawl/start")
async def start_crawl():
    global crawl_task
    if crawl_task and not crawl_task.done():
        return {"message": "✅ A crawl task is already running."}
    
    logger.info("✅ Crawling started")
    crawl_task = asyncio.create_task(crawl_all_products())
    return {"message": "✅ Crawl task started"}

    
@app.post("/crawl/stop")
async def stop_crawl():
    global crawl_task
    if not crawl_task:
        return {"message": "⚠️ No crawl task has been started yet."}
    if crawl_task.done():
        return {"message": "✅ Crawl task already completed."}

    crawl_task.cancel()
    try:
        await crawl_task
    except asyncio.CancelledError:
        logger.info("❌ Crawl task was cancelled successfully.")
        return {"message": "❌ Crawl task cancelled."}
    except Exception as e:
        logger.error(f"❌ Error during cancellation: {e}")
        return {"message": f"❌ Failed to cancel task: {e}"}

    return {"message": "❌ Crawl task cancelled cleanly."}
    


@app.post("/content/", response_model=ImageContentOut)
def get_image_content(item: ImageContentIn):
    try:
        base64str = image_url_to_base64(item.url)
        return {"base64": base64str}
    except Exception as e:
        logger.error(f"❌ Image conversion error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

async def crawl_all_products_wrapper():
    global is_crawling
    await crawl_all_products(is_crawling_ref=lambda: is_crawling)
    is_crawling = False




