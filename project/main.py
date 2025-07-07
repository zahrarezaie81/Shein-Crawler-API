from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from project.database.database import get_db
from project.database import crud
from project.database.schemas import BrandOut, BrandCountOut, ProductOut, ImageContentIn, ImageContentOut, StatusOut
from project.image_processor.image_processor import image_url_to_base64

app = FastAPI(title="SHEIN")

# =========== 1. GET /brands ===========
@app.get("/brands", response_model=list[BrandOut])
def get_brands(db: Session = Depends(get_db)):
    return crud.get_brands(db)

# =========== 2. GET /brands/{brand}/count ===========
@app.get("/brands/{brand}/count", response_model=BrandCountOut)
def brand_count(brand: str, db: Session = Depends(get_db)):
    count = crud.count_products_for_brand(db, brand)
    return {"brand": brand, "count": count}

@app.get("/products/filter", response_model=list[ProductOut])
def filter_products(
    min: float = Query(0), 
    max: float = Query(100000), 
    db: Session = Depends(get_db)
):
    products = crud.filter_products_by_price(db, min, max)
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "title": p.title,
            "brand": {"id": p.brand.id, "name": p.brand.name} if p.brand else None,
            "category": p.category.name if p.category else None,  # فقط اسم دسته‌بندی
            "price": p.price,
            "discounted_price": p.discounted_price,
        })
    return result


# # =========== 4. POST /crawl/start ===========
# is_crawling = False

# def fake_crawler():
#     import time
#     global is_crawling
#     is_crawling = True
#     for i in range(10):
#         if not is_crawling:
#             break
#         print(f"Crawling... {i+1}/10")
#         time.sleep(1)
#     is_crawling = False

# @app.post("/crawl/start", response_model=StatusOut)
# def start_crawl(background_tasks: BackgroundTasks):
#     global is_crawling
#     if is_crawling:
#         return {"status": "Already running"}
#     background_tasks.add_task(fake_crawler)
#     return {"status": "Started"}

# # =========== 5. POST /crawl/stop ===========
# @app.post("/crawl/stop", response_model=StatusOut)
# def stop_crawl():
#     global is_crawling
#     if not is_crawling:
#         return {"status": "No crawler running"}
#     is_crawling = False
#     return {"status": "Stopped"}

# =========== 6. POST /content/ ===========
@app.post("/content/", response_model=ImageContentOut)
def get_image_content(item: ImageContentIn):
    try:
        base64str = image_url_to_base64(item.url)
        return {"base64": base64str}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
