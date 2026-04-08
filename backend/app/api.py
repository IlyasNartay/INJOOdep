from fastapi import FastAPI

from app.routers import address, admin_stats, admin_users, auth, menu, order, sitemap


def register_routers(app: FastAPI) -> None:
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(menu.router, prefix="/menu", tags=["Menu"])
    app.include_router(order.router, prefix="/orders", tags=["Orders"])
    app.include_router(address.router, prefix="/addresses", tags=["Addresses"])
    app.include_router(admin_stats.router, prefix="/admin", tags=["Admin Stats"])
    app.include_router(admin_users.router, prefix="/admin", tags=["Admin Users"])
    app.include_router(sitemap.router)
