"""Descarga productos e imágenes siguiendo el formato del scraper entregado.

Uso:
    pip install requests beautifulsoup4
    python scraper_productos.py

Pinsoft puede responder 403 a peticiones automatizadas; en ese caso se
conservan los datos locales de demostración y se informa del bloqueo.
"""

import hashlib
from html import unescape
import json
import os
import re
import math
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="backslashreplace")


def limpiar_texto(texto):
    texto = unescape(str(texto or ""))
    if "://" not in texto:
        texto = BeautifulSoup(texto, "html.parser").get_text(" ", strip=True)
    texto = texto.replace("\ufffd", "")
    return re.sub(r"\s+", " ", texto).strip()


def extraer_precio(texto):
    valores = re.findall(r"\$\s*(\d+(?:\.\d{1,2})?)", (texto or "").replace(",", ""))
    return min((float(valor) for valor in valores), default=None)


def resolver_url(url, base=BASE_URL):
    return urljoin(base, url) if url else None


def marca_modelo_desde_url(url):
    if not url:
        return ""
    slug = limpiar_texto(url.rsplit("/producto/", 1)[-1]).lower()
    if "/p-" in slug:
        slug = slug.rsplit("/", 1)[0]
    slug = re.sub(r"[-_]+", " ", slug)
    marcas = (
        "samsung", "motorola", "xiaomi", "redmi", "oppo", "honor", "tecno",
        "infinix", "realme", "huawei", "tcl", "hisense", "philips", "riviera",
        "indurama", "innova", "lg", "rca", "lenovo", "asus", "hp", "dell", "env",
    )
    for marca in marcas:
        coincidencia = re.search(rf"\b{re.escape(marca)}\b", slug)
        if coincidencia:
            resto = slug[coincidencia.end():].strip()
            modelo = re.split(
                r"(?:^|\s+)(?:amd|intel|ryzen|core|ram|gb|tb|ssd|nvme|pulgadas?|led|qled|uhd|fhd|4k|"
                r"android|google tv|smart tv|windows|freedos|sin sistema)\b",
                resto,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip(" -")
            if modelo.isdigit():
                siguiente = re.search(rf"\b{re.escape(modelo)}\s+pulgadas?\s+([a-z0-9-]+)", resto, re.IGNORECASE)
                if siguiente:
                    modelo = siguiente.group(1)
            if not modelo:
                modelo_match = re.search(r"\b\d{2,}[a-z][a-z0-9-]*\b", resto, re.IGNORECASE)
                if modelo_match:
                    modelo = modelo_match.group(0)
            modelo = " ".join(modelo.split()[:4])
            return f"{marca.upper() if marca == 'env' else marca.title()} {modelo}".strip()
    return ""


def nombre_marca_modelo(nombre, url=""):
    """Conserva únicamente la marca y el modelo, sin código ni ficha técnica."""
    nombre = limpiar_texto(nombre)
    nombre = re.sub(r"^cod\.?\s*[\w:-]+\s*", "", nombre, flags=re.IGNORECASE)
    nombre = re.sub(
        r"^(?:laptop|computadora|computador|televisor(?:\s+inteligente)?|smart\s+tv|tv)\s+",
        "",
        nombre,
        flags=re.IGNORECASE,
    )
    nombre = re.sub(r"^kit\s+(?:fotográfico|fotografico)(?:\s+del?)?\s+", "", nombre, flags=re.IGNORECASE)
    nombre = re.sub(r"^kit\s+", "", nombre, flags=re.IGNORECASE)
    nombre = re.split(r"\s+(?:/|\|)\s+", nombre, maxsplit=1)[0]
    nombre = re.split(
        r"\s+(?=(?:intel|amd|ryzen|core\s+i\d|celeron|pentium|apple\s+m\d|snapdragon|mediatek|ram\b|\d+\s*(?:gb|tb|ssd|nvme|pulgadas?|[\"″])))",
        nombre,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    nombre = re.sub(r"\s+\$[\d.,]+.*$", "", nombre, flags=re.IGNORECASE)
    nombre = re.sub(r"\s+(?:w11|windows\s+\d+|freedos|sin\s+sistema|android|google\s+tv|smart\s+tv).*$", "", nombre, flags=re.IGNORECASE)
    nombre = re.sub(r"\s{2,}", " ", nombre).strip(" -:")
    desde_url = marca_modelo_desde_url(url)
    if desde_url and (
        len(nombre.split()) < 2
        or nombre.lower() in {"led", "tcl", "rca", "hisense", "samsung", "motorola"}
        or re.search(r"\b(?:smart tv|google tv)\b", nombre, re.IGNORECASE)
        or re.search(r"\s+(?:led|\d{2,})$", nombre, re.IGNORECASE)
    ):
        nombre = desde_url
    return nombre


def extraer_imagen_desde_tag(img, base=BASE_URL):
    if not img:
        return None
    # Los atributos de alta resolución son más fiables que `src`, que suele
    # apuntar a una miniatura o a un placeholder de carga diferida.
    for atributo in ("data-large_image", "data-full-image", "data-zoom-image", "data-lazy-src", "data-src", "data-original"):
        if img.get(atributo):
            return resolver_url(img[atributo], base)
    srcset = img.get("data-srcset") or img.get("srcset")
    if srcset:
        candidatos = []
        for item in srcset.split(","):
            partes = item.strip().split()
            if partes:
                ancho = int(re.sub(r"\D", "", partes[1])) if len(partes) > 1 and re.sub(r"\D", "", partes[1]) else 0
                candidatos.append((ancho, partes[0]))
        if candidatos:
            return resolver_url(max(candidatos)[1], base)
    if img.get("src"):
        return resolver_url(img["src"], base)
    return None


def extraer_caracteristicas(soup):
    """Extrae atributos técnicos publicados en la ficha del producto."""
    if not soup:
        return []
    caracteristicas = []
    selectores = (
        ".woocommerce-product-attributes tr",
        ".woocommerce-product-attributes-item",
        ".product-attributes li",
        ".product-specifications li",
        ".specifications li",
        ".product-features li",
        ".features li",
    )
    for elemento in soup.select(", ".join(selectores)):
        partes = [limpiar_texto(nodo.get_text(" ", strip=True)) for nodo in elemento.select("th, td, dt, dd, .label, .value")]
        partes = [parte for parte in partes if parte]
        texto = ": ".join(partes[:2]) if len(partes) >= 2 else limpiar_texto(elemento.get_text(" ", strip=True))
        if texto and len(texto) >= 3 and texto not in caracteristicas:
            caracteristicas.append(texto)
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            datos = json.loads(script.string or script.get_text())
        except (TypeError, json.JSONDecodeError):
            continue
        bloques = datos if isinstance(datos, list) else [datos]
        for bloque in bloques:
            for atributo in bloque.get("additionalProperty", []) if isinstance(bloque, dict) else []:
                nombre = limpiar_texto(str(atributo.get("name", "")))
                valor = limpiar_texto(str(atributo.get("value", "")))
                texto = f"{nombre}: {valor}".strip(": ")
                if texto and texto not in caracteristicas:
                    caracteristicas.append(texto)
    return caracteristicas


def caracteristicas_desde_texto(texto):
    texto = limpiar_texto(texto).replace("·", "|").replace("•", "|")
    partes = [limpiar_texto(parte) for parte in re.split(r"\s*(?:\||;|/\s+)\s*", texto or "")]
    return [
        parte for parte in partes
        if 3 <= len(parte) <= 90
        and not re.match(r"^(cod\.?|laptop|kit|consulta disponibilidad|cotizaci[oó]n por whatsapp)\b", parte, re.I)
    ]


def normalizar_caracteristica(valor):
    valor = limpiar_texto(valor).strip(" .,:;|-")
    valor = re.sub(r"\s*:\s*", ": ", valor)
    valor = re.sub(r"\s+", " ", valor)
    return valor


def puntaje_caracteristica(valor):
    """Prioriza datos técnicos útiles frente a textos comerciales de la ficha."""
    texto = valor.lower()
    puntaje = 0
    prioridades = (
        (r"\b(procesador|cpu|intel|amd|ryzen|core i|celeron|snapdragon|mediatek)\b", 100),
        (r"\bmemoria ram\b|\bram\b", 90),
        (r"\b(ssd|nvme|hdd|almacenamiento|disco|capacidad)\b", 80),
        (r"\bpulgadas?\b|[\"″]|\b(pantalla|display|resoluci[oó]n|fhd|uhd|qled|oled|4k)\b", 70),
        (r"\b(windows|android|ios|google tv|tizen|vidaa|freedos)\b", 60),
        (r"\b(5g|4g|wi-?fi|bluetooth|hdmi|usb)\b", 50),
        (r"\b(c[aá]mara|bater[ií]a|mah|mp)\b", 40),
        (r"\b(color|teclado|idioma)\b", 8),
    )
    for patron, valor_puntaje in prioridades:
        if re.search(patron, texto, re.IGNORECASE):
            puntaje += valor_puntaje
    if len(valor) > 100:
        puntaje -= 15
    if re.search(r"(consulta|cotizaci[oó]n|disponibilidad|compra|env[ií]o|garant[ií]a comercial)", texto):
        puntaje -= 100
    return puntaje


def caracteristicas_producto(soup, nombre_original, url):
    """Visita la ficha y selecciona hasta seis especificaciones técnicas relevantes."""
    candidatos = []
    vistos = set()
    titulo = nombre_marca_modelo(nombre_original, url).lower()
    titulo_clave = re.sub(r"[^a-z0-9]+", "", titulo)
    for valor in extraer_caracteristicas(soup) + caracteristicas_desde_texto(nombre_original):
        valor = normalizar_caracteristica(valor)
        clave = re.sub(r"[^a-z0-9]+", "", valor.lower())
        if (
            valor
            and clave not in vistos
            and len(valor) >= 3
            and len(valor) <= 120
            and re.sub(r"[^a-z0-9]+", "", valor.lower()) != titulo_clave
            and not (
                titulo
                and valor.lower().startswith(titulo)
                and re.search(r"\b(?:ram|gb|tb|ssd|nvme|pulgadas?|4g|5g)\b", valor, re.IGNORECASE)
            )
            and not re.match(
                r"^(consulta disponibilidad|cotizaci[oó]n por whatsapp|precio final|"
                r"equipo tecnol[oó]gico|rendimiento confiable|smartphone|smart tv|"
                r"imagen de alta definici[oó]n|marca:|modelo:|categor[ií]a:|tipo de producto:)",
                valor,
                re.I,
            )
        ):
            candidatos.append(valor)
            vistos.add(clave)
    if len(candidatos) < 6:
        tecnicos = re.findall(
            r"(?:Intel|AMD|Ryzen|Core\s+i\d|Celeron|Pentium|Snapdragon|MediaTek)[^/,|]{0,45}"
            r"|(?:\d+\s*(?:GB|TB)\s*(?:RAM|SSD|NVMe|HDD|de almacenamiento)?)"
            r"|(?:\d+(?:[.,]\d+)?\s*(?:pulgadas?|[\"″])(?:\s*(?:FHD|Full HD|HD|4K|UHD|QLED))?)"
            r"|(?:Windows\s+\d+|FreeDOS|Android|Google TV|Smart TV|5G|4K UHD)",
            limpiar_texto(f"{nombre_original} {url}"),
            flags=re.I,
        )
        for valor in tecnicos:
            valor = normalizar_caracteristica(valor)
            clave = re.sub(r"[^a-z0-9]+", "", valor.lower())
            if valor and clave not in vistos:
                candidatos.append(valor)
                vistos.add(clave)
    ordenados = sorted(
        enumerate(candidatos),
        key=lambda item: (-puntaje_caracteristica(item[1]), item[0]),
    )
    resultado = [valor for _, valor in ordenados[:6]]
    if not resultado and re.search(r"\bkit\s+fotogr[aá]fico\b", nombre_original, re.IGNORECASE):
        resultado.append("Kit fotográfico")
    return resultado


def extraer_imagen_producto(soup, base=BASE_URL):
    """Obtiene la imagen principal de la ficha, no la miniatura de catálogo."""
    meta = soup.select_one('meta[property="og:image"], meta[name="twitter:image"]')
    if meta and meta.get("content"):
        return resolver_url(meta["content"], base)
    for selector in (
        ".woocommerce-product-gallery__image img",
        ".product-gallery img",
        ".product-info .image img",
        "#default-image img",
        ".main-image img",
    ):
        imagen = soup.select_one(selector)
        url = extraer_imagen_desde_tag(imagen, base)
        if url:
            return url
    return None


def nombre_archivo_seguro(texto):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", texto.lower()).strip("-")[:60]


def calcular_precio_final(producto):
    incremento = 50 if producto.get("fuente") == "MundoTek" else 90 if producto.get("fuente") in {"Pinsoft", "DigitalPC"} else 80
    return math.ceil((producto["precio_original"] + incremento) / 10) * 10


def caracteristicas_web(producto):
    caracteristicas = producto.get("caracteristicas", [])
    if caracteristicas:
        return caracteristicas[:6]
    categoria = producto["categoria"]
    if categoria == "Celulares":
        return ["Smartphone", "Consulta disponibilidad", "Cotización por WhatsApp"]
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
        if (
            url == CATALOG_URL
            or not re.search(r"/p-\d+\.html(?:$|[?#])", url.lower())
            or any(part in url.lower() for part in ("/cart", "/login", "/contact"))
        ):
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
            imagen = tarjeta.select_one(
                "img.wp-post-image, .box-image-primary img, .box-image img:not(.back-image), "
                ".product-image img:not(.hover-image), img"
            )
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
    content_type = respuesta.headers.get("Content-Type", "").lower()
    if not content_type.startswith("image/"):
        raise requests.RequestException(f"la respuesta no es una imagen ({content_type or 'tipo desconocido'})")
    extension = ".webp" if "webp" in content_type else ".png" if "png" in content_type else ".jpg"
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
                nombre_original = producto["nombre"]
                producto["nombre"] = nombre_marca_modelo(producto["nombre"], producto["url_origen"])
                try:
                    page.goto(producto["url_origen"], wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(700)
                    ficha = BeautifulSoup(page.content(), "html.parser")
                    imagen_ficha = extraer_imagen_producto(ficha, fuente["base"])
                    if imagen_ficha:
                        producto["imagen_candidata"] = imagen_ficha
                    producto["caracteristicas"] = caracteristicas_producto(
                        ficha, nombre_original, producto["url_origen"]
                    )
                except PlaywrightTimeoutError as error:
                    print(f"No se pudo abrir la ficha de {producto['nombre']}: {error}")
                if not producto.get("caracteristicas"):
                    producto["caracteristicas"] = caracteristicas_desde_texto(nombre_original)
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
