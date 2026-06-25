from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from controller.storage import PER_PAGE, get_all_articles, get_article

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "dist"


def build_context(template_name: str, **extra: Any) -> dict[str, Any]:
    context: dict[str, Any] = {
        "csrf_token": lambda: "",
        "url_for": lambda endpoint, **values: "/static/" + values.get("filename", "").lstrip("/") if endpoint == "static" else "/",
        "current_user": SimpleNamespace(is_authenticated=False, is_admin=False),
    }
    context.update(extra)
    return context


def render_page(template_name: str, output_path: Path, **context: Any) -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    html = template.render(**build_context(template_name, **context))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def write_static_assets() -> None:
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static", dirs_exist_ok=True)


def build_site() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    articles = get_all_articles()
    articles_page = articles[:PER_PAGE]

    render_page(
        "home.html",
        OUTPUT_DIR / "index.html",
        articles=articles_page,
        page=1,
        total_pages=1,
        kategori=None,
        query="",
    )
    render_page(
        "home.html",
        OUTPUT_DIR / "home" / "index.html",
        articles=articles_page,
        page=1,
        total_pages=1,
        kategori=None,
        query="",
    )

    render_page(
        "contact.html",
        OUTPUT_DIR / "contact" / "index.html",
        success=False,
        error=None,
        is_contact=True,
    )

    for article in articles:
        article_data = get_article(int(article.get("id", 0))) or article
        render_page(
            "artikel.html",
            OUTPUT_DIR / "artikel" / str(article_data["id"]) / "index.html",
            article=article_data,
            comments=article_data.get("comments", []),
        )

    write_static_assets()


if __name__ == "__main__":
    build_site()
    print(f"Built static site to {OUTPUT_DIR}")
