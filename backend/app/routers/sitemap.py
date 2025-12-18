from fastapi import APIRouter
from fastapi.responses import Response
from datetime import datetime
from app.services.dishes import get_dishes_from_db

router = APIRouter(tags=["SEO"])

@router.get("/sitemap.xml", include_in_schema=False)
def sitemap():
    dishes = get_dishes_from_db()

    xml = """<?xml version="1.0" encoding="UTF-8"?>"""
    xml += """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
    """

    # статические страницы
    pages = [
        ("https://injoo.kz/", "1.0"),
        ("https://injoo.kz/menu", "0.9"),
        ("https://injoo.kz/about", "0.6"),
    ]

    for loc, priority in pages:
        xml += f"""
        <url>
            <loc>{loc}</loc>
            <changefreq>daily</changefreq>
            <priority>{priority}</priority>
        </url>
        """

    # динамика
    for dish in dishes:
        xml += f"""
        <url>
            <loc>https://injoo.kz/dish/{dish.id}</loc>
            <lastmod>{dish.updated_at.date()}</lastmod>
            <priority>0.8</priority>
            <image:image>
                <image:loc>{dish.image_url}</image:loc>
                <image:title>{dish.name}</image:title>
            </image:image>
        </url>
        """

    xml += "</urlset>"

    return Response(xml, media_type="application/xml")
