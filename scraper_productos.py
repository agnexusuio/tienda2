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
import shutil
import sys
import unicodedata
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
    {"nombre": "Pinsoft", "base": "https://www.pinsoft.ec", "categoria": "Computadoras", "url": CATALOG_URL},
    {"nombre": "Planeta Digital", "base": "https://planetadigitalec.com", "categoria": "Computadoras", "url": "https://planetadigitalec.com/collections/all"},
    {"nombre": "MundoTek", "base": "https://mundotek.com.ec", "categoria": "Celulares", "url": "https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/"},
    {"nombre": "Alta Gama Store", "base": "https://altagamastore.ec", "categoria": "Celulares", "url": "https://altagamastore.ec/categoria-producto/telefonos/"},
    {"nombre": "MundoTek TVs", "base": "https://mundotek.com.ec", "categoria": "Televisores", "url": "https://mundotek.com.ec/product-category/mejores-televisores-calidad-precio/"},
]
PRECIO_MAXIMO_CATALOGO = 700
TERMINOS_EXCLUIDOS_PLANETA = re.compile(r"\b(?:leer|danada|danado)\b", re.IGNORECASE)
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


def vaciar_carpeta_imagenes():
    """Elimina las imágenes del catálogo anterior antes de una actualización."""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    for nombre in os.listdir(IMAGE_DIR):
        ruta = os.path.join(IMAGE_DIR, nombre)
        if os.path.isdir(ruta):
            shutil.rmtree(ruta)
        else:
            os.remove(ruta)


def extraer_precio(texto):
    valores = []
    for coincidencia in re.findall(r"\$\s*(\d[\d.,]*)", texto or ""):
        if "," in coincidencia and "." in coincidencia:
            separador_decimal = "," if coincidencia.rfind(",") > coincidencia.rfind(".") else "."
            separador_miles = "." if separador_decimal == "," else ","
            normalizado = coincidencia.replace(separador_miles, "").replace(separador_decimal, ".")
        elif "," in coincidencia:
            entero, separador, decimal = coincidencia.rpartition(",")
            normalizado = f"{entero.replace(',', '')}.{decimal}" if separador and len(decimal) in (1, 2) else coincidencia.replace(",", "")
        else:
            normalizado = coincidencia
        try:
            valores.append(float(normalizado))
        except ValueError:
            continue
    return min(valores, default=None)


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


def formatear_titulo_producto(nombre):
    """Normaliza mayúsculas y espacios sin alterar marcas ni especificaciones."""
    nombre = re.sub(r"\s+", " ", limpiar_texto(nombre))
    nombre = re.sub(r"\s+([,.)])", r"\1", nombre)
    nombre = re.sub(r",(\S)", r", \1", nombre)
    nombre = nombre.title()
    reemplazos = {
        r"\bAmd\b": "AMD",
        r"\bAsus\b": "ASUS",
        r"\bDell\b": "Dell",
        r"\bEnv\b": "ENV",
        r"\bHp\b": "HP",
        r"\bLg\b": "LG",
        r"\bNvme\b": "NVMe",
        r"\bMsi\b": "MSI",
        r"\bNvidia\b": "NVIDIA",
        r"\bOled\b": "OLED",
        r"\bOppo\b": "OPPO",
        r"\bRca\b": "RCA",
        r"\bRtx\b": "RTX",
        r"\bSsd\b": "SSD",
        r"\bRam\b": "RAM",
        r"\bQled\b": "QLED",
        r"\bUhd\b": "UHD",
        r"\bVivobook\b": "VivoBook",
        r"\bIdeapad\b": "IdeaPad",
        r"\b(\d+(?:[.,]\d+)?)\s*Pulg(?:adas?)?\b": lambda match: f"{match.group(1)} pulgadas",
        r"\b(\d+)(Hs|Hx|Va|Th|U|W)\b": lambda match: f"{match.group(1)}{match.group(2).upper()}",
        r"\bTcl\b": "TCL",
        r"\b(\d+)\s*(Gb|Tb)\b": lambda match: f"{match.group(1)} {match.group(2).upper()}",
        r"\bI([3579])\b": lambda match: f"i{match.group(1)}",
    }
    for patron, reemplazo in reemplazos.items():
        nombre = re.sub(patron, reemplazo, nombre, flags=re.IGNORECASE)
    return nombre


def nombre_celular_con_marca(nombre, url="", imagen="", fuente=""):
    """Normaliza el prefijo de marca de celulares usando título y URL de producto."""
    nombre = limpiar_texto(nombre).strip()
    slug = re.sub(r"[-_]+", " ", url.rsplit("/producto/", 1)[-1].lower())
    imagen_slug = re.sub(r"[-_]+", " ", imagen.lower().rsplit("/", 1)[-1])
    texto = f"{nombre} {slug} {imagen_slug}".casefold()
    reglas = (
        (r"^(?:samsung\s+)?galaxy\b", "Samsung Galaxy"),
        (r"^samsung\b", "Samsung"),
        (r"^(?:motorola|moto)\b", "Motorola"),
        (r"^(?:xiaomi\s+)?redmi\b", "Xiaomi Redmi"),
        (r"^(?:xiaomi\s+)?poco\b", "Xiaomi Poco"),
        (r"^xiaomi\b", "Xiaomi"),
        (r"^(?:apple\s+)?iphone\b", "Apple iPhone"),
        (r"^(?:google\s+)?pixel\b", "Google Pixel"),
        (r"^(?:one[\s-]*plus\s+)?nord\b", "OnePlus Nord"),
        (r"^one[\s-]*plus\b", "OnePlus"),
        (r"^(?:blackview\s+)?bv\d+", "Blackview"),
    )
    for patron, marca in reglas:
        coincidencia_nombre = re.match(patron, nombre, re.IGNORECASE)
        if coincidencia_nombre:
            if marca == "Blackview" and nombre.lower().startswith("bv"):
                return f"Blackview {nombre}"
            resto = nombre[coincidencia_nombre.end():].strip()
            if marca == "Samsung Galaxy" and nombre.lower().startswith("samsung"):
                resto = re.sub(r"^galaxy\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "Xiaomi Redmi" and nombre.lower().startswith("xiaomi"):
                resto = re.sub(r"^redmi\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "Xiaomi Poco" and nombre.lower().startswith("xiaomi"):
                resto = re.sub(r"^poco\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "Apple iPhone" and nombre.lower().startswith("apple"):
                resto = re.sub(r"^iphone\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "Google Pixel" and nombre.lower().startswith("google"):
                resto = re.sub(r"^pixel\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "OnePlus Nord" and re.match(r"^one[\s-]*plus", nombre, re.IGNORECASE):
                resto = re.sub(r"^one[\s-]*plus\s+nord\b", "", resto, flags=re.IGNORECASE).strip()
            elif marca == "Blackview" and nombre.lower().startswith("blackview"):
                resto = re.sub(r"^bv\d+\s*", "", resto, flags=re.IGNORECASE).strip()
            return f"{marca} {resto}".strip()
        if re.search(patron, texto, re.IGNORECASE):
            if marca == "Samsung Galaxy" and re.search(r"\bsamsung\b", nombre, re.IGNORECASE):
                continue
            return f"{marca} {nombre}".strip()
    if re.match(r"^a6(?:c|x)?(?:\s|$)|^a6\s+pro\b", nombre, re.IGNORECASE) and (
        fuente == "Alta Gama Store" or re.search(r"\boppo\b", texto, re.IGNORECASE)
    ):
        return f"OPPO {nombre}"
    for marca in ("HONOR", "OPPO", "TECNO", "INFINIX", "REALME", "HUAWEI", "ZTE", "TCL", "OUKITEL", "LOGIC", "NOKIA"):
        if re.match(rf"^{marca}\b", nombre, re.IGNORECASE) or re.search(rf"\b{marca}\b", texto, re.IGNORECASE):
            resto = re.sub(rf"^{marca}\b\s*", "", nombre, flags=re.IGNORECASE)
            return f"{marca.title()} {resto}".strip()
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
        and not es_texto_promocional(parte)
    ]


def es_texto_promocional(texto):
    texto_normalizado = unicodedata.normalize("NFKD", limpiar_texto(texto))
    texto_normalizado = texto_normalizado.encode("ascii", "ignore").decode("ascii").casefold()
    return bool(re.search(
        r"\b(?:somos tienda fisica|enviamos rapido y seguro|tenemos mas laptop|"
        r"nuestro local esta ubicado|somos importadores directos|entregamos a domicilio|"
        r"envios a todo el ecuador|formas de pago|aceptamos todas las tarjetas|"
        r"favor consultar precio|garantia de \d+ ano)\b",
        texto_normalizado,
    ))


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


def caracteristicas_producto(soup, nombre_original, url, texto_adicional=""):
    """Visita la ficha y selecciona hasta seis especificaciones técnicas relevantes."""
    candidatos = []
    vistos = set()
    titulo = nombre_marca_modelo(nombre_original, url).lower()
    titulo_clave = re.sub(r"[^a-z0-9]+", "", titulo)
    texto_fuente = f"{nombre_original} | {texto_adicional}" if texto_adicional else nombre_original
    for valor in extraer_caracteristicas(soup) + caracteristicas_desde_texto(texto_fuente):
        valor = normalizar_caracteristica(valor)
        if es_texto_promocional(valor):
            continue
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
    return precio_catalogo(producto["precio_original"], producto.get("fuente"))


def precio_catalogo(precio_original, fuente):
    incremento = 40 if fuente == "MundoTek" else 70
    total = round(precio_original + incremento, 2)
    return math.ceil(total / 10) * 10


def caracteristicas_web(producto):
    caracteristicas = producto.get("caracteristicas", [])
    if caracteristicas:
        return caracteristicas
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
    pagina_anterior = set()
    for numero in range(1, 101):
        url = fuente["url"] if numero == 1 else f"{fuente['url'].rstrip('/')}/{numero}/"
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
        page.wait_for_timeout(1500)
        pagina = extraer_pinsoft(page.content())
        urls_pagina = {producto["url_origen"] for producto in pagina}
        if not urls_pagina or urls_pagina == pagina_anterior:
            break
        pagina_anterior = urls_pagina
        for producto in pagina:
            encontrados[producto["url_origen"]] = producto
    productos = [
        producto for producto in encontrados.values()
        if precio_catalogo(producto["precio_original"], fuente["nombre"]) <= PRECIO_MAXIMO_CATALOGO
    ]
    productos.sort(key=lambda item: item["precio_original"])
    return productos


def extraer_woocommerce(fuente):
    """Extrae todas las páginas de productos WooCommerce de una categoría."""
    encontrados = {}
    paginas_sin_novedades = 0
    session = requests.Session()
    session.headers.update(HEADERS)
    for numero in range(1, 101):
        page_url = fuente["url"] if numero == 1 else f"{fuente['url'].rstrip('/')}/page/{numero}/"
        respuesta = session.get(page_url, params={"orderby": "price", "per_page": 24}, timeout=40)
        if respuesta.status_code == 404 and numero > 1:
            break
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, "html.parser")
        encontrados_antes = len(encontrados)
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
            if not producto_url:
                continue
            encontrados[producto_url] = {
                "nombre": nombre, "precio_original": precio, "categoria": fuente["categoria"],
                "url_origen": producto_url, "imagen_candidata": extraer_imagen_desde_tag(imagen, fuente["base"]),
            }
        if len(encontrados) == encontrados_antes:
            paginas_sin_novedades += 1
        else:
            paginas_sin_novedades = 0
        if not soup.select("li.product, article.product, div.product-small, .product"):
            break
        if paginas_sin_novedades >= 2:
            break
    productos = [
        producto for producto in encontrados.values()
        if precio_catalogo(producto["precio_original"], fuente["nombre"]) <= PRECIO_MAXIMO_CATALOGO
    ]
    productos.sort(key=lambda item: item["precio_original"])
    return productos


def extraer_planeta_digital(fuente):
    """Obtiene laptops de catálogo y las 60 más baratas con RTX/NVIDIA."""
    endpoint = f"{fuente['url'].rstrip('/')}/products.json"
    productos = {}
    laptops_gamers = {}
    session = requests.Session()
    session.headers.update(HEADERS)
    for numero in range(1, 101):
        respuesta = session.get(endpoint, params={"limit": 250, "page": numero}, timeout=40)
        respuesta.raise_for_status()
        try:
            lote = respuesta.json().get("products", [])
        except (ValueError, AttributeError) as error:
            raise requests.RequestException(
                f"Planeta Digital devolvió un catálogo inválido en la página {numero}"
            ) from error
        if not lote:
            break
        for item in lote:
            tipo = limpiar_texto(item.get("product_type", "")).casefold()
            if tipo not in ("laptop", "laptops", "computadoras"):
                continue
            nombre = limpiar_texto(item.get("title"))
            es_laptop_gamer = bool(re.search(r"\b(?:RTX|NVIDIA)\b", nombre, re.IGNORECASE))
            nombre_busqueda = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
            if TERMINOS_EXCLUIDOS_PLANETA.search(nombre_busqueda):
                continue
            variantes = item.get("variants", [])
            variantes_disponibles = [variante for variante in variantes if variante.get("available", True)]
            precios = []
            for variante in (variantes_disponibles if es_laptop_gamer else variantes):
                try:
                    precios.append(float(variante.get("price")))
                except (TypeError, ValueError):
                    continue
            if not precios:
                continue
            precio = min(precios)
            url = f"{fuente['base'].rstrip('/')}/products/{item.get('handle', '')}"
            imagenes = item.get("images", [])
            imagen = imagenes[0].get("src") if imagenes else None
            descripcion = BeautifulSoup(item.get("body_html") or "", "html.parser")
            texto_descripcion = descripcion.get_text(" | ", strip=True)
            caracteristicas = caracteristicas_producto(
                descripcion, item.get("title", ""), url, texto_descripcion
            )
            producto = {
                "nombre": nombre,
                "precio_original": precio,
                "categoria": fuente["categoria"],
                "url_origen": url,
                "imagen_candidata": imagen,
                "caracteristicas": caracteristicas,
            }
            if es_laptop_gamer and variantes_disponibles:
                producto["categoria"] = "Laptop Gaming"
                producto["catalog_source"] = "planeta-gamer"
                laptops_gamers[url] = producto
            elif precio_catalogo(precio, fuente["nombre"]) <= PRECIO_MAXIMO_CATALOGO:
                productos[url] = producto
    laptops_gamers_seleccionadas = sorted(
        laptops_gamers.values(), key=lambda item: item["precio_original"]
    )[:60]
    return sorted(
        [*productos.values(), *laptops_gamers_seleccionadas],
        key=lambda item: item["precio_original"],
    )


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
    counters = {
        "Pinsoft": 0, "Planeta Digital": 0, "planeta-gamer": 0, "MundoTek": 0,
        "Alta Gama Store": 0, "MundoTek TVs": 0,
    }
    source_ids = {
        "Pinsoft": ("p", "pinsoft"),
        "Planeta Digital": ("pd", "planeta-digital"),
        "planeta-gamer": ("pg", "planeta-gamer"),
        "MundoTek": ("m", "mundotek"),
        "Alta Gama Store": ("ag", "alta-gama"),
        "MundoTek TVs": ("t", "mundotek-tv"),
    }
    for producto in productos:
        fuente = producto.get("catalog_source", producto["fuente"])
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
    vaciar_carpeta_imagenes()
    print(f"Carpeta '{IMAGE_DIR}' vaciada.")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=HEADERS["User-Agent"], locale="es-EC")
        page = context.new_page()
        productos = []
        indice = 1
        for fuente in FUENTES:
            if fuente["nombre"] == "Pinsoft":
                seleccionados = extraer_pinsoft_con_navegador(page, fuente)
            elif fuente["nombre"] == "Planeta Digital":
                seleccionados = extraer_planeta_digital(fuente)
            else:
                seleccionados = extraer_woocommerce(fuente)
            print(f"{fuente['nombre']}: {len(seleccionados)} productos encontrados")
            for producto in seleccionados:
                producto["fuente"] = fuente["nombre"]
                nombre_original = producto["nombre"]
                if producto.get("catalog_source") == "planeta-gamer":
                    producto["nombre"] = formatear_titulo_producto(producto["nombre"])
                else:
                    producto["nombre"] = nombre_marca_modelo(producto["nombre"], producto["url_origen"])
                if producto["categoria"] == "Celulares":
                    producto["nombre"] = nombre_celular_con_marca(
                        producto["nombre"],
                        producto["url_origen"],
                        producto.get("imagen_candidata", ""),
                        fuente["nombre"],
                    )
                if fuente["nombre"] == "Pinsoft":
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
                if not producto.get("nombre") or producto.get("precio_original") is None or not producto.get("url_origen"):
                    print(f"Producto omitido por datos incompletos: {nombre_original}")
                    continue
                productos.append(producto)
                indice += 1
        browser.close()
    for producto in productos:
        producto["precio_final"] = calcular_precio_final(producto)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, ensure_ascii=False, indent=2)
    escribir_catalogo_web(productos)
    fuentes = ", ".join(
        f"{fuente['nombre']}={sum(p['fuente'] == fuente['nombre'] for p in productos)}"
        for fuente in FUENTES
    )
    print(f"Productos guardados: {len(productos)} | Imágenes: {sum(bool(p['imagen']) for p in productos)} | {fuentes}")


if __name__ == "__main__":
    main()
