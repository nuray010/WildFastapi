from fastapi import FastAPI
from mysite.api import  user,category,product,product_image,review,subcategory,auth
import uvicorn
from mysite.admin.setup import setup_admin


online_shop = FastAPI(title="Online Shop")
online_shop.include_router(user.user_router)
online_shop.include_router(category.category_router)
online_shop.include_router(product.product_router)
online_shop.include_router(product_image.product_image_router)
online_shop.include_router(review.review_router)
online_shop.include_router(subcategory.sub_category_router)
online_shop.include_router(auth.auth_router)
setup_admin(online_shop)

if __name__ == "__main__":
    uvicorn.run(online_shop, host="127.0.0.1", port=8003)


