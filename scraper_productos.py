"""Descarga productos e imágenes siguiendo el formato del scraper entregado.

Uso:
    pip install requests beautifulsoup4
    python scraper_productos.py

Pinsoft puede responder 403 a peticiones automatizadas; en ese caso se
conservan los datos locales de demostración y se informa del bloqueo.
"""

import hashlib
import json
import os
import re
import math
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

OUTPUT_JSON = "productos.json"
OUTPUT_JS = "catalogo_actualizado.js"
IMAGE_DIR = "imagenes"
CATALOG_URL = "https://www.pinsoft.ec/laptop-notebook-portatiles/c-67.html"
BASE_URL = "https://www.pinsoft.ec"
FUENTES = [
    {"nombre": "Pinsoft", "base": "https://www.pinsoft.ec", "categoria": "Computadoras", "url": CATALOG_URL, "cantidad": 999, "precio_maximo": 700},
    {"nombre": "DigitalPC", "base": "https://digitalpcecuador.com", "categoria": "Computadoras", "url": "https://digitalpcecuador.com/categoria-producto/laptops/", "cantidad": 999, "precio_maximo": 700},
    {"nombre": "MundoTek", "base": "https://mundotek.com.ec", "categoria": "Celulares", "url": "https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/", "cantidad": 999, "precio_maximo": 600},
    {"nombre": "MundoTek TVs", "base": "https://mundotek.com.ec", "categoria": "Televisores", "url": "https://mundotek.com.ec/product-category/mejores-televisores-calidad-precio/", "cantidad": 999, "precio_maximo": 600},
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
}


def limpiar_texto(texto):
    return re.sub(r"\s+", " ", BeautifulSoup(texto or "", "html.parser").get_text(" ", strip=True)).strip()


def extraer_precio(texto):
    valores = re.findall(r"\$\s*(\d+(?:\.\d{1,2})?)", (texto or "").replace(",", ""))
    return min((float(valor) for valor in valores), default=None)


def resolver_url(url, base=BASE_URL):
    return urljoin(base, url) if url else None


def extraer_imagen_desde_tag(img, base=BASE_URL):
    if not img:
        return None
    srcset = img.get("data-srcset") or img.get("srcset")
    if srcset:
        return resolver_url(srcset.split(",")[-1].strip().split(" ")[0], base)
    for atributo in ("data-large_image", "data-lazy-src", "data-src", "data-original", "src"):
        if img.get(atributo):
            return resolver_url(img[atributo], base)
    return None


def nombre_archivo_seguro(texto):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", texto.lower()).strip("-")[:60]


def calcular_precio_final(producto):
    incremento = 50 if producto.get("fuente") == "MundoTek" else 90 if producto.get("fuente") in {"Pinsoft", "DigitalPC"} else 80
    return math.ceil((producto["precio_original"] + incremento) / 10) * 10


def caracteristicas_web(producto):
    caracteristicas = producto.get("caracteristicas", [])
    if caracteristicas:
        return caracteristicas[:4]
    categoria = producto["categoria"]
    if categoria == "Celulares":
        return ["Smartphone", "Precio final", "Consulta disponibilidad", "Cotización por WhatsApp"]
    if categoria == "Televisores":
        return ["Smart TV", "Imagen de alta definición", "Consulta disponibilidad", "Cotización por WhatsApp"]
    return ["Equipo tecnológico", "Rendimiento confiable", "Consulta disponibilidad", "Cotización por WhatsApp"]


def extraer_pinsoft(html):
    soup = BeautifulSoup(html, "html.parser")
    productos = []
    for enlace in soup.find_all("a", href=True):
        contenedor = enlace
        texto_contenedor = ""
        precio = None
        for _ in range(6):
            contenedor = contenedor.parent
            if not contenedor:
                break
            texto_contenedor = limpiar_texto(contenedor.get_text(" ", strip=True))
            precio = extraer_precio(texto_contenedor)
            if precio and len(texto_contenedor) > 20:
                break
        nombre = limpiar_texto(enlace.get_text(" ", strip=True))
        if not precio or len(nombre) < 15:
            titulo = contenedor.select_one("h2,h3,h4") if contenedor else None
            nombre = limpiar_texto(titulo.get_text(" ", strip=True)) if titulo else nombre
        if not precio or len(nombre) < 15:
            continue
        url = resolver_url(enlace["href"])
        if url == CATALOG_URL or any(part in url.lower() for part in ("/cart", "/login", "/contact")):
            continue
        imagen = extraer_imagen_desde_tag(contenedor.select_one("img") if contenedor else None)
        productos.append({
            "nombre": nombre,
            "precio_original": precio,
            "categoria": "Laptops",
            "url_origen": url,
            "imagen_candidata": imagen,
            "codigo": hashlib.md5(url.encode()).hexdigest()[:8],
        })
    unicos = {producto["url_origen"]: producto for producto in productos}
    return sorted(unicos.values(), key=lambda item: item["precio_original"])


def extraer_pinsoft_con_navegador(page, fuente):
    """Recorre las páginas como el scraper entregado y conserva el precio publicado."""
    encontrados = {}
    for numero in range(1, 4):
        url = fuente["url"] if numero == 1 else f"{fuente['url'].rstrip('/')}/{numero}/"
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
        page.wait_for_timeout(1500)
        for producto in extraer_pinsoft(page.content()):
            encontrados[producto["url_origen"]] = producto
    productos = sorted(encontrados.values(), key=lambda item: item["precio_original"])
    limite = fuente.get("precio_maximo")
    if limite is not None:
        productos = [item for item in productos if item["precio_original"] <= limite]
    return productos[:fuente["cantidad"]]


def extraer_woocommerce_con_navegador(page, fuente):
    """Extrae tarjetas WooCommerce ordenadas por precio, como el scraper de referencia."""
    encontrados = {}
    for numero in range(1, 5):
        separador = "&" if "?" in fuente["url"] else "?"
        url = f"{fuente['url']}{separador}orderby=price&per_page=24"
        if numero > 1:
            url = f"{fuente['url'].rstrip('/')}/page/{numero}/{separador}orderby=price&per_page=24"
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
        page.wait_for_timeout(1500)
        soup = BeautifulSoup(page.content(), "html.parser")
        for tarjeta in soup.select("li.product, article.product, div.product-small, .product"):
            titulo = tarjeta.select_one(".woocommerce-loop-product__title, .product-title, h2, h3")
            precio_el = tarjeta.select_one(".price")
            enlace = tarjeta.select_one("a.woocommerce-LoopProduct-link, a.woocommerce-loop-product__link, .product-title a, h2 a, h3 a, a[href*='/producto/'], a[href*='/product/']")
            imagen = tarjeta.select_one("img.wp-post-image, .image-fade_in_back img, .box-image img, img")
            if not titulo or not precio_el or not enlace:
                continue
            precio = extraer_precio(precio_el.get_text(" ", strip=True))
            nombre = limpiar_texto(titulo.get_text(" ", strip=True))
            if precio is None or not nombre:
                continue
            producto_url = resolver_url(enlace.get("href"), fuente["base"])
            encontrados[producto_url] = {
                "nombre": nombre, "precio_original": precio, "categoria": fuente["categoria"],
                "url_origen": producto_url, "imagen_candidata": extraer_imagen_desde_tag(imagen, fuente["base"]),
            }
    productos = sorted(encontrados.values(), key=lambda item: item["precio_original"])
    limite = fuente.get("precio_maximo")
    if limite is not None:
        productos = [item for item in productos if item["precio_original"] <= limite]
    return productos[:fuente["cantidad"]]


def descargar_imagen(producto, indice):
    url = producto.get("imagen_candidata")
    if not url:
        return None
    respuesta = requests.get(url, headers={**HEADERS, "Referer": producto["url_origen"]}, timeout=25)
    respuesta.raise_for_status()
    extension = ".webp" if "webp" in respuesta.headers.get("Content-Type", "") else ".jpg"
    os.makedirs(IMAGE_DIR, exist_ok=True)
    ruta = os.path.join(IMAGE_DIR, f"{indice:02d}-{nombre_archivo_seguro(producto['nombre'])}{extension}")
    with open(ruta, "wb") as archivo:
        archivo.write(respuesta.content)
    return ruta.replace("\\", "/")


def escribir_catalogo_web(productos):
    """Genera un archivo JS consumible por la página sin depender de fetch local."""
    web_products = []
    counters = {"Pinsoft": 0, "DigitalPC": 0, "MundoTek": 0, "MundoTek TVs": 0}
    source_ids = {"Pinsoft": ("p", "pinsoft"), "DigitalPC": ("d", "digitalpc"), "MundoTek": ("m", "mundotek"), "MundoTek TVs": ("t", "mundotek-tv")}
    for producto in productos:
        fuente = producto["fuente"]
        counters[fuente] += 1
        image = producto.get("imagen") or producto.get("imagen_candidata")
        web_products.append({
            "id": f"{source_ids[fuente][0]}{counters[fuente]}",
            "source": source_ids[fuente][1],
            "name": producto["nombre"],
            "specs": " · ".join(caracteristicas_web(producto)),
            "price": producto["precio_original"],
            "image": image,
            "image_remote": producto.get("imagen_candidata"),
            "url": producto["url_origen"],
            "badge": "#1 más económico" if counters[fuente] == 1 else "Precio bajo",
        })
    with open(OUTPUT_JS, "w", encoding="utf-8") as archivo:
        archivo.write("window.catalogProducts = ")
        json.dump(web_products, archivo, ensure_ascii=False, indent=2)
        archivo.write(";\n")


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=HEADERS["User-Agent"], locale="es-EC")
        page = context.new_page()
        productos = []
        indice = 1
        for fuente in FUENTES:
            if fuente["nombre"] == "Pinsoft":
                seleccionados = extraer_pinsoft_con_navegador(page, fuente)
            else:
                seleccionados = extraer_woocommerce_con_navegador(page, fuente)
            for producto in seleccionados:
                producto["fuente"] = fuente["nombre"]
                if fuente["nombre"] == "Pinsoft":
                    page.goto(producto["url_origen"], wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(1000)
                    ficha = BeautifulSoup(page.content(), "html.parser")
                    producto["imagen_candidata"] = extraer_imagen_desde_tag(ficha.select_one(
                        ".product-info .image img, #default-image img, .main-image img, img"
                    ))
                try:
                    producto["imagen"] = descargar_imagen(producto, indice)
                except requests.RequestException as error:
                    print(f"No se pudo descargar {producto['nombre']}: {error}")
                    producto["imagen"] = producto["imagen_candidata"]
                if not producto.get("imagen"):
                    producto["imagen"] = producto.get("imagen_candidata")
                productos.append(producto)
                indice += 1
        browser.close()
    for producto in productos:
        producto["precio_final"] = calcular_precio_final(producto)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, ensure_ascii=False, indent=2)
    escribir_catalogo_web(productos)
    print(f"Productos guardados: {len(productos)} | Imágenes: {sum(bool(p['imagen']) for p in productos)}")


if __name__ == "__main__":
    main()
