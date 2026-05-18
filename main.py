from fastapi import FastAPI

from routers.users import router as user_router
from routers.books import router as book_router
from routers.purchases import router as purchase_router
from routers.sales import router as sale_router
from routers.bills import router as bill_router

app = FastAPI(title="图书销售管理系统")

app.include_router(user_router)
app.include_router(book_router)
app.include_router(purchase_router)
app.include_router(sale_router)
app.include_router(bill_router)


@app.get("/")
async def root():
    return {"message": "图书销售管理系统"}
