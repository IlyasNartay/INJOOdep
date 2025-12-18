from fastapi import APIRouter, Response
from datetime import datetime
from app.database import SessionLocal
from app import services, schemas

router = APIRouter(tags=["SEO"])


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    db = SessionLocal()
    try:
        # Получаем все блюда через сервис
        dishes = services.dish_service.get_all_dishes(db)

        # Формируем XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
'''

        # Статические страницы
        pages = [
            ("https://injoo.kz/", "1.0"),
            ("https://injoo.kz/menu", "0.9"),
        ]

        for loc, priority in pages:
            xml += f'''
<url>
    <loc>{loc}</loc>
    <changefreq>daily</changefreq>
    <priority>{priority}</priority>
</url>
'''

        # Динамические страницы (блюда)
        for dish in dishes:
            dish_serialized = schemas.DishRead.model_validate(dish)
            lastmod = dish_serialized.updated_at.strftime(
                "%Y-%m-%d") if dish_serialized.updated_at else datetime.utcnow().strftime("%Y-%m-%d")
            xml += f'''
<url>
    <loc>https://injoo.kz/dish/{dish_serialized.id}</loc>
    <lastmod>{lastmod}</lastmod>
    <priority>0.8</priority>
    <image:image>
        <image:loc>{dish_serialized.image_url}</image:loc>
        <image:title>{dish_serialized.name}</image:title>
    </image:image>
</url>
'''

        xml += '</urlset>'
        return Response(content=xml, media_type="application/xml")
    finally:
        db.close()
