const pinsoftImages = [
  "https://www.pinsoft.ec/getimage/510x510/products/1(155).png?r=y",
  "https://www.pinsoft.ec/getimage/510x510/products/1(156).png?r=y",
  "https://www.pinsoft.ec/getimage/510x510/products/thumbs_500_0bb2991cbc8280bc205e(1).png?r=y"
];
const fallbackProducts = [
  {id:"p1",source:"pinsoft",name:"ENV Book Pro Max",specs:"Intel Celeron N4020 · 8 GB · 256 GB SSD · 14.1” FHD IPS · Windows 11",price:319,image:pinsoftImages[0],url:"https://www.pinsoft.ec/cod-1768-laptop-env-book-pro-max-intel-celeron-n4020-8gb-256gb-ssd-14-1-full-hd-ips-windows-11-preinstalado-wi-fi-5-ac-teclado-espanol-alfanumerico-gris-oscuro/p-9535.html",badge:"#1 más económica"},
  {id:"p2",source:"pinsoft",name:"ENV Book Elite",specs:"AMD Ryzen 5 3500U · 8 GB · 256 GB NVMe · 15.6” FHD · Windows 11",price:374,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-1780-laptop-env-book-elite-amd-ryzen-5-3500u-2-1ghzhasta-3-7ghz-8gb-256gb-nvme-ssd-15-6-full-hd-windows-11-teclado-espanol-alfanumerico-gris-oscuro/p-9623.html",badge:"#2 más económica"},
  {id:"p3",source:"pinsoft",name:"HP 14-dq3500la",specs:"Intel Celeron N4500 · 8 GB · 256 GB NVMe · 14” HD · FreeDOS",price:379.5,image:pinsoftImages[2],url:"https://www.pinsoft.ec/cod-h-1779-hp-14-dq3500la-intel-celeron-n4500-8gb-256gb-pcie-nvme-ssd-14-0-hd-wi-fi-6-bt-5-4-freedos-teclado-espanol-plateado-natural/p-9621.html",badge:"#3 más económica"},
  {id:"p4",source:"pinsoft",name:"Lenovo IdeaPad Slim 3 15AMN8",specs:"AMD Ryzen 3 7320U · 8 GB · 512 GB NVMe · 15.6” FHD · Sin sistema",price:462,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-1791-lenovo-ideapad-slim-3-15amn8-amd-ryzen-3-7320u-8gb-lpddr5-512gb-nvme-ssd-m-2-15-6-fhd-sin-sistema-os-wi-fi6-2x2-bt5-2-teclado-espanol-alfanumerico-artic-grey/p-9675.html",badge:"Precio bajo"},
  {id:"p5",source:"pinsoft",name:"ASUS VivoBook Go 15",specs:"AMD Ryzen 3 7320U · 8 GB · 512 GB NVMe · 15.6” FHD · Mouse incluido",price:473,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-1795-asus-vivobook-go-15-e1504f-amd-ryzen-37320u-8-gb-lpddr5-512gb-nvme-ssd-15-6-fhd-sin-sistema-os-wi-fi-6e-bt-5-3-lector-de-huellas-teclado-espanol-alfanumerico-mixed-black-incl-mouseasus/p-9701.html",badge:"Precio bajo"},
  {id:"p6",source:"pinsoft",name:"ENV Laptop Ryzen 5 15.6”, 16 GB",specs:"AMD Ryzen 5 3500U · 16 GB · 512 GB NVMe · FHD · Windows 11",price:484,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-e-1776-laptop-env-amd-ryzen-5-3500u-2-1ghzhasta-3-7ghz-16gb-512gb-nvme-ssd-15-6-full-hd-windows-11-teclado-espanol-alfanumerico-gris/p-9592.html",badge:"Precio bajo"},
  {id:"p7",source:"pinsoft",name:"ENV Laptop Ryzen 5 14.1”, 16 GB",specs:"AMD Ryzen 5 3500U · 16 GB · 512 GB NVMe · FHD · Windows 11",price:484,image:pinsoftImages[2],url:"https://www.pinsoft.ec/cod-1775-laptop-env-amd-ryzen-5-3500u-2-1ghzhasta-3-7ghz-16gb-512gb-nvme-ssd-14-1-full-hd-windows-11-teclado-espanol-gris/p-9593.html",badge:"Precio bajo"},
  {id:"p8",source:"pinsoft",name:"Lenovo IdeaPad Slim 3 15IAN8",specs:"Intel Core i3-N305 · 8 GB · 512 GB SSD · 15.6” FHD · Sin sistema",price:493.9,image:pinsoftImages[2],url:"https://www.pinsoft.ec/cod-1787-lenovo-ideapad-slim-3-15ian8-intel-core-i3-n305-8-nucleos-hasta-3-8-ghz-8gb-lpddr5-512gb-ssd-pcie-4-0-15-6-full-hd-sin-sistema-os-wi-fi-6-bt5-2-teclado-espanol-la-alfanumerico-arctic-grey/p-9649.html",badge:"Precio bajo"},
  {id:"p9",source:"pinsoft",name:"ASUS VivoBook 15 X1504V, 8 GB",specs:"Intel Core i3-1315U · 8 GB · 512 GB NVMe · 15.6” FHD · Kit",price:517,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-1766-kit-asus-vivobook-15-x1504v-intel-corei3-1315u-13va-gen-10mb-cache-hasta-4-4-ghz-8gb-512gb-nvme-ssd-15-6-fhd/p-9534.html",badge:"Precio bajo"},
  {id:"p10",source:"pinsoft",name:"ASUS VivoBook 15 X1504V, 16 GB",specs:"Intel Core i3-1315U · 16 GB · 512 GB NVMe · 15.6” FHD · Kit",price:566.5,image:pinsoftImages[1],url:"https://www.pinsoft.ec/cod-1774-kit-asus-vivobook-15-x1504v-intel-corei3-1315u-13va-gen-10mb-cache-hasta-4-4-ghz-16gb-512gb-nvme/p-9588.html",badge:"Precio bajo"},
  {id:"d1",source:"digitalpc",name:"Lenovo IdeaPad Slim 3",specs:"Intel Core i3-N305 · 8 GB RAM · 128 GB SSD · 15.6” · Windows 11",price:435,image:"https://digitalpcecuador.com/wp-content/uploads/2025/08/FOTOS-WEB-12.jpg",url:"https://digitalpcecuador.com/producto/lenovo-ideapad-slim-3-intel-core-i3-n305-8gb-ram-128gb-ssd-15-6-w11/",badge:"#1 más económica"},
  {id:"d2",source:"digitalpc",name:"ASUS VivoBook 14 X1404VA",specs:"Intel Core i3-1315U · 8 GB RAM · 128 GB SSD · 14” · Windows 11",price:455,image:"https://digitalpcecuador.com/wp-content/uploads/2025/07/descarga-7.png",url:"https://digitalpcecuador.com/producto/asus-vivobook-14-x1404va-intel-core-i3-1315u-8gb-ram-128gb-ssd-14-w11-2/",badge:"#2 más económica"},
  {id:"d3",source:"digitalpc",name:"HP 15-FD0130WM",specs:"Intel Core i3-N305 · 8 GB RAM · 256 GB SSD · 15.6” · Windows 11",price:499,image:"https://digitalpcecuador.com/wp-content/uploads/2026/09/HP1-3.png",url:"https://digitalpcecuador.com/producto/hp-15-fd0130wm-intel-core-i3-n305-8gb-ram-256gb-ssd-15-6-w11/",badge:"#3 más económica"},
  {id:"d4",source:"digitalpc",name:"HP 15-FD0133WM",specs:"Intel Core i3-N305 · 8 GB RAM · 256 GB SSD · 15.6” · Windows 11",price:499,image:"https://digitalpcecuador.com/wp-content/uploads/2026/09/HP1-3.png",url:"https://digitalpcecuador.com/producto/hp-15-fd0133wm-intel-core-i3-n305-8gb-ram-256gb-ssd-15-6-w11/",badge:"Precio bajo"},
  {id:"d5",source:"digitalpc",name:"ASUS VivoBook 14 X1404VAP",specs:"Intel Core 5-120U · 8 GB RAM · 256 GB SSD · 14” · Windows 11",price:575,image:"https://digitalpcecuador.com/wp-content/uploads/2025/07/descarga-7.png",url:"https://digitalpcecuador.com/producto/asus-vivobook-14-x1404vap-intel-core-5-120u-8gb-ram-256gb-ssd-14-w11/",badge:"Precio bajo"},
  {id:"d6",source:"digitalpc",name:"HP 15-fc0256la",specs:"AMD Ryzen 5-7520U · 16 GB RAM · 512 GB SSD · 15.6”",price:655,image:"https://digitalpcecuador.com/wp-content/uploads/2026/09/HP1-3.png",url:"https://digitalpcecuador.com/producto/hp-15-fc0256la-amd-ryzen-5-7520u-16gb-ram-512gb-ssd-15-6/",badge:"Precio bajo"},
  {id:"d7",source:"digitalpc",name:"Lenovo IdeaPad 1",specs:"Intel Core i5-1335U · 16 GB RAM · 256 GB SSD · 15.6” · Windows 11",price:675,image:"https://digitalpcecuador.com/wp-content/uploads/2025/08/FOTOS-WEB-12.jpg",url:"https://digitalpcecuador.com/producto/lenovo-ideapad-1-intel-core-i5-1335u-16gb-ram-256gb-ssd-15-6-w11/",badge:"Precio bajo"},
  {id:"d8",source:"digitalpc",name:"ASUS VivoBook Go 15",specs:"Ryzen 5-7520U · 16 GB RAM · 512 GB SSD · 15.6” FHD",price:675,image:"https://digitalpcecuador.com/wp-content/uploads/2025/07/descarga-7.png",url:"https://digitalpcecuador.com/producto/asus-vivobook-go-15-e1504fa-ryzen-5-4016gb512ssd156fhd/",badge:"Precio bajo"},
  {id:"d9",source:"digitalpc",name:"HP 250R G10",specs:"Intel Core 5-120U · 16 GB RAM · 512 GB SSD · 15.6”",price:675,image:"https://digitalpcecuador.com/wp-content/uploads/2026/09/HP1-3.png",url:"https://digitalpcecuador.com/producto/hp-250r-g10-intel-core-i5-120u-16gb-ram-512gb-ssd-15-6/",badge:"Precio bajo"},
  {id:"d10",source:"digitalpc",name:"HP OmniBook 3 16",specs:"AMD Ryzen 5 40 · 16 GB RAM · 256 GB SSD · 16” 2K IPS Touch · W11",price:695,image:"https://digitalpcecuador.com/wp-content/uploads/2026/09/HP1-3.png",url:"https://digitalpcecuador.com/producto/hp-omnibook-3-16-amd-ryzen-5-40-apu-16gb-ram-256g-ssd-16-2k-ips-touch-w11/",badge:"Precio bajo"},
  {id:"m1",source:"mundotek",name:"Infinix SMART 6 HD",specs:"2 GB RAM · 32 GB almacenamiento",price:69,image:"https://mundotek.com.ec/wp-content/uploads/2026/08/infinix-smart-6-hd-azul.webp",url:"https://mundotek.com.ec/producto/infinix-smart-6-hd-ram-2gb-32gb/",badge:"#1 más económico"},
  {id:"m2",source:"mundotek",name:"ZTE Blade A35e",specs:"4+2 GB RAM · 64 GB almacenamiento",price:89,image:"https://mundotek.com.ec/wp-content/uploads/2025/05/zte_blade_a35e.webp",url:"https://mundotek.com.ec/producto/zte-blade-a35e-ram-42gb-64gb/",badge:"#2 más económico"},
  {id:"m3",source:"mundotek",name:"Kit fotográfico Xiaomi 15 Ultra",specs:"Kit fotográfico para Xiaomi 15 Ultra",price:99,image:"https://mundotek.com.ec/wp-content/uploads/2025/04/kit15.webp",url:"https://mundotek.com.ec/producto/kit-fotografico-del-xiaomi-15-ultra/",badge:"#3 más económico"},
  {id:"m4",source:"mundotek",name:"Realme C21Y",specs:"4 GB RAM · 64 GB almacenamiento",price:99,image:"https://mundotek.com.ec/wp-content/uploads/2025/09/rmc21y-464gb-blu-9-1000x1000-1-300x300.jpg",url:"https://mundotek.com.ec/producto/realme-c21y-ram4gb-64gb/",badge:"Precio bajo"},
  {id:"m5",source:"mundotek",name:"Realme C11 (2021)",specs:"2 GB RAM · 32 GB almacenamiento",price:102,image:"https://mundotek.com.ec/wp-content/uploads/2021/07/Realme-C11-300x300.jpg",url:"https://mundotek.com.ec/producto/realme-c11/",badge:"Precio bajo"},
  {id:"m6",source:"mundotek",name:"ZTE Blade A56 Pro",specs:"4+8 GB RAM · 128 GB almacenamiento",price:125,image:"https://mundotek.com.ec/wp-content/uploads/2025/12/a56-pro-768x1024.webp",url:"https://mundotek.com.ec/producto/zte-blade-a56-pro-ram-48-128gb/",badge:"Precio bajo"},
  {id:"m7",source:"mundotek",name:"Infinix Hot 20i",specs:"4+3 GB RAM · 128 GB almacenamiento",price:129,image:"https://mundotek.com.ec/wp-content/uploads/2026/08/hot-20i-300x300.webp",url:"https://mundotek.com.ec/producto/infinix-hot-20i-ram-43-gb-128gb/",badge:"Precio bajo"},
  {id:"m8",source:"mundotek",name:"Samsung A07",specs:"4 GB RAM · 128 GB almacenamiento",price:135,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/a07-300x300.webp",url:"https://mundotek.com.ec/producto/samsung-a07-ram-4gb-128gb/",badge:"Precio bajo"},
  {id:"m9",source:"mundotek",name:"Tecno Spark Go 3",specs:"4+4 GB RAM · 128 GB almacenamiento",price:135,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/tecno-spark-go-3-300x300.webp",url:"https://mundotek.com.ec/producto/tecno-spark-go-3-ram44gb-64gb-128gb/",badge:"Precio bajo"},
  {id:"m10",source:"mundotek",name:"Honor Play 10",specs:"4+4 GB RAM · 128 GB almacenamiento",price:135,image:"https://mundotek.com.ec/wp-content/uploads/2026/07/honor-play-10-300x300.jpg",url:"https://mundotek.com.ec/producto/honor-play-10-ram44-gb-128gb/",badge:"Precio bajo"},
  {id:"m11",source:"mundotek",name:"Xiaomi Redmi A7 Pro",specs:"4 GB RAM · 128 GB almacenamiento",price:135,image:"https://mundotek.com.ec/wp-content/uploads/2026/08/xiaomi-redmi-a7-pro-300x300.webp",url:"https://mundotek.com.ec/producto/xiaomi-redmi-a7-pro-ram-4gb-128gb/",badge:"Precio bajo"},
  {id:"m12",source:"mundotek",name:"LOGIC G1L Gaming Phone",specs:"4+10 GB RAM · 128 GB · Game Pad + Buds",price:139,image:"https://mundotek.com.ec/wp-content/uploads/2025/08/logi-300x170.png",url:"https://mundotek.com.ec/producto/logic-g1l-gaming-phonegame-padbuds-ram-410gb-128gb/",badge:"Precio bajo"},
  {id:"m13",source:"mundotek",name:"Infinix Smart 20",specs:"4+4 GB RAM · 128/256 GB",price:139,image:"https://mundotek.com.ec/wp-content/uploads/2026/04/infinix-smart-20-300x300.jpg",url:"https://mundotek.com.ec/producto/infinix-smart-20-ram-4-4-gb-64gb/",badge:"Precio bajo"},
  {id:"m14",source:"mundotek",name:"Motorola G06",specs:"4+4 GB RAM · 256 GB almacenamiento",price:149,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/g06-289x300.jpeg",url:"https://mundotek.com.ec/producto/motorola-g06-ram-4gb4gb-256gb/",badge:"Precio bajo"},
  {id:"m15",source:"mundotek",name:"TCL L10+",specs:"Smartphone TCL L10+",price:150,image:"https://mundotek.com.ec/wp-content/uploads/2021/04/1062-300x300.jpg",url:"https://mundotek.com.ec/producto/l10/",badge:"Precio bajo"},
  {id:"m16",source:"mundotek",name:"Honor X5c Plus",specs:"4 GB RAM · 256 GB almacenamiento",price:155,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/x5plus.jpg",url:"https://mundotek.com.ec/producto/honor-x5c-plus-ram-4gb-256gb/",badge:"Precio bajo"},
  {id:"m17",source:"mundotek",name:"Tecno Spark 30C",specs:"4 GB RAM · 256 GB almacenamiento",price:159,image:"https://mundotek.com.ec/wp-content/uploads/2024/11/spark30c-300x300.webp",url:"https://mundotek.com.ec/producto/telefono-tecno-spark-30c-ram-4gb-256gb/",badge:"Precio bajo"},
  {id:"m18",source:"mundotek",name:"OPPO A5 4G",specs:"4 GB RAM · 256 GB almacenamiento",price:165,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/a5-4g-300x300.png",url:"https://mundotek.com.ec/producto/oppo-a5-4g-ram-4gb-256gb/",badge:"Precio bajo"},
  {id:"m19",source:"mundotek",name:"Motorola moto g15 4G",specs:"4+8 GB RAM · 256/512 GB",price:169,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/g15-300x300.png",url:"https://mundotek.com.ec/producto/motorola-moto-g15-ram-48gb-256gb/",badge:"Precio bajo"},
  {id:"m20",source:"mundotek",name:"Tecno Spark 9 Pro",specs:"Smartphone Tecno Spark 9 Pro",price:175,image:"https://mundotek.com.ec/wp-content/uploads/2022/11/Tecno-Spark-9-Pro-4-300x300.jpg",url:"https://mundotek.com.ec/producto/tecno-spark-9-pro/",badge:"Precio bajo"},
  {id:"m21",source:"mundotek",name:"Xiaomi Redmi 15C",specs:"8 GB RAM · 256 GB almacenamiento",price:179,image:"https://mundotek.com.ec/wp-content/uploads/2025/09/redmi15c.webp",url:"https://mundotek.com.ec/producto/xiaomi-redmi-15c-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m22",source:"mundotek",name:"Honor X6C",specs:"6/8 GB RAM · 256 GB almacenamiento",price:185,image:"https://mundotek.com.ec/wp-content/uploads/2025/06/x6c-300x300.webp",url:"https://mundotek.com.ec/producto/honor-x6c-ram-6gb-256gb/",badge:"Precio bajo"},
  {id:"m23",source:"mundotek",name:"Motorola G17",specs:"4 GB RAM · 256 GB almacenamiento",price:185,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/moto-g17.jpg",url:"https://mundotek.com.ec/producto/motorola-g17-ram-4gb-256gb/",badge:"Precio bajo"},
  {id:"m24",source:"mundotek",name:"Realme Narzo 30 5G",specs:"Smartphone Realme Narzo 30 · 5G",price:195,image:"https://mundotek.com.ec/wp-content/uploads/2021/11/719tm7l723L._SL1500_.jpg",url:"https://mundotek.com.ec/producto/realme-narzo-30-5g/",badge:"Precio bajo"},
  {id:"m25",source:"mundotek",name:"Oukitel G1",specs:"6+18 GB RAM · 256 GB almacenamiento · Color naranja",price:225,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/g1.jpg",url:"https://mundotek.com.ec/producto/celular-oukitel-g1-24-618-gb-ram-256-gb-color-negro/",badge:"Precio bajo"},
  {id:"m26",source:"mundotek",name:"Honor X7d",specs:"6+6 GB RAM · 256 GB almacenamiento",price:229,image:"https://mundotek.com.ec/wp-content/uploads/2025/10/honor-x7d-300x300.jpg",url:"https://mundotek.com.ec/producto/honor-x7d-ram-88gb-256gb/",badge:"Precio bajo"},
  {id:"m27",source:"mundotek",name:"Motorola G56 5G",specs:"8+8 GB RAM · 256 GB almacenamiento · 5G",price:229,image:"https://mundotek.com.ec/wp-content/uploads/2025/12/moto-56-300x300.png",url:"https://mundotek.com.ec/producto/motorola-g56-5g-8gb8gb-256gb/",badge:"Precio bajo"},
  {id:"m28",source:"mundotek",name:"ZTE Nubia Air 5G",specs:"8+12 GB RAM · 256 GB almacenamiento · 5G",price:235,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/celular-zte-nubia-air-5g-300x300.png",url:"https://mundotek.com.ec/producto/celular-zte-nubia-air-5g-ram-812-256gb/",badge:"Precio bajo"},
  {id:"m29",source:"mundotek",name:"Honor 90 Lite",specs:"8 GB RAM · 256 GB almacenamiento",price:239,image:"https://mundotek.com.ec/wp-content/uploads/2025/05/honor-90-lite--300x300.jpg",url:"https://mundotek.com.ec/producto/honor-90-lite-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m30",source:"mundotek",name:"Infinix Hot 60 Pro Plus",specs:"8+8 GB RAM · 256 GB almacenamiento",price:255,image:"https://mundotek.com.ec/wp-content/uploads/2025/07/hot60pro-244x300.png",url:"https://mundotek.com.ec/producto/infinix-hot-60-pro-plus-88gb-256gb/",badge:"Precio bajo"},
  {id:"m31",source:"mundotek",name:"Samsung Galaxy A17",specs:"8 GB RAM · 256 GB almacenamiento",price:259,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/sam-a17-4g-300x300.webp",url:"https://mundotek.com.ec/producto/samsung-galaxy-a17-4gb-128gb/",badge:"Precio bajo"},
  {id:"m32",source:"mundotek",name:"Xiaomi Mi 10 Lite 5G",specs:"6 GB RAM · 128 GB almacenamiento · 5G",price:269,image:"https://mundotek.com.ec/wp-content/uploads/2023/01/1-15.svg",url:"https://mundotek.com.ec/producto/xiaomi-mi-10-lite-128gb-6gb-ram-5g/",badge:"Precio bajo"},
  {id:"m33",source:"mundotek",name:"OPPO A5 5G",specs:"8 GB RAM · 256 GB almacenamiento · 5G",price:269,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/oppoa5-300x294.png",url:"https://mundotek.com.ec/producto/oppo-a5-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m34",source:"mundotek",name:"Oukitel WP53 4G",specs:"8+16 GB RAM · 128 GB · 6.52 pulgadas",price:276,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/112-oukitel-wp53-4g-8gb-128gb-300x300.jpg",url:"https://mundotek.com.ec/producto/oukitel-wp53-4g-8gb-128gb-6-52-negro/",badge:"Precio bajo"},
  {id:"m35",source:"mundotek",name:"Redmi Note 15 Pro 4G",specs:"8 GB RAM · 256 GB almacenamiento · 4G",price:299,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/xiaomi-redmi-note-15-pro-4g-300x300.webp",url:"https://mundotek.com.ec/producto/redmi-note-15-4g-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m36",source:"mundotek",name:"Tecno Camon 18 Premier",specs:"Smartphone Tecno Camon 18 Premier",price:315,image:"https://mundotek.com.ec/wp-content/uploads/2022/04/camon--300x300.jpg",url:"https://mundotek.com.ec/producto/tecno-camon-18-premier/",badge:"Precio bajo"},
  {id:"m37",source:"mundotek",name:"OPPO A5 Pro 5G",specs:"8 GB RAM · 256 GB · IP69 sumergible · 5G",price:319,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/oppo-a5pro-300x300.webp",url:"https://mundotek.com.ec/producto/oppo-a5-pro-5g-ram8gb-256gb-ip69-sumergible/",badge:"Precio bajo"},
  {id:"m38",source:"mundotek",name:"HONOR X8d",specs:"8 GB RAM · 256/512 GB almacenamiento",price:319,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/honor-x8d-300x300.webp",url:"https://mundotek.com.ec/producto/honor-x8d-ram-8gb-256gb-512gb/",badge:"Precio bajo"},
  {id:"m39",source:"mundotek",name:"Tecno Camón 50 Pro",specs:"8+8 GB RAM · 256 GB · Audífonos incluidos",price:339,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/camon-con-audifonos-300x300.png",url:"https://mundotek.com.ec/producto/tecno-camon-50-pro-ram-88-gb-256gb/",badge:"Precio bajo"},
  {id:"m40",source:"mundotek",name:"Samsung Galaxy A36 5G",specs:"8 GB RAM · 256 GB almacenamiento · 5G",price:349,image:"https://mundotek.com.ec/wp-content/uploads/2025/04/a36-black-mtk-300x300.jpg",url:"https://mundotek.com.ec/producto/samsung-galaxy-a36-5g-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m41",source:"mundotek",name:"OPPO Reno13F 5G",specs:"12 GB RAM · 512 GB · IP69 · 5G",price:499,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/reno-13f.jpg",url:"https://mundotek.com.ec/producto/reno13-f-5g-ram-12gb-512gb/",badge:"Precio bajo"},
  {id:"m42",source:"mundotek",name:"Oukitel WP62 5G",specs:"24+24 GB RAM · 512 GB · 5G",price:509,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/wp60.jpg",url:"https://mundotek.com.ec/producto/oukitel-wp62-5g-ram-24gb-512gb/",badge:"Precio bajo"},
  {id:"m43",source:"mundotek",name:"OPPO Reno14F",specs:"12 GB RAM · 512 GB · Audífonos incluidos",price:535,image:"https://mundotek.com.ec/wp-content/uploads/2026/01/reno.webp",url:"https://mundotek.com.ec/producto/oppo-reno14f-ram-12gb-512gb-audifonos/",badge:"Precio bajo"},
  {id:"m44",source:"mundotek",name:"Samsung Galaxy A57",specs:"8/12 GB RAM · 256 GB",price:549,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/a57-300x300.png",url:"https://mundotek.com.ec/producto/samsung-galaxy-a57-ram-8gb-256gb/",badge:"Precio bajo"},
  {id:"m45",source:"mundotek",name:"Xiaomi Poco X8 Pro",specs:"12 GB RAM · 512 GB",price:569,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/x8-pro-300x300.jpg",url:"https://mundotek.com.ec/producto/xiaomi-poco-x8-pro-ram-12gb-512gb/",badge:"Precio bajo"},
  {id:"m46",source:"mundotek",name:"iPhone 11 Pro Max Open Box",specs:"256 GB · Open Box",price:579,image:"https://mundotek.com.ec/wp-content/uploads/2022/09/11-pro-max-p-300x300.jpg",url:"https://mundotek.com.ec/producto/iphone-11-pro-max-open-box/",badge:"Precio bajo"},
  {id:"m47",source:"mundotek",name:"Samsung Galaxy S25 FE 5G",specs:"8 GB RAM · 256 GB · 5G",price:579,image:"https://mundotek.com.ec/wp-content/uploads/2025/12/samsung_galaxy_s25_fe-300x300.png",url:"https://mundotek.com.ec/producto/samsung-galaxy-s25-fe-ram-8gb-256gb-5g/",badge:"Precio bajo"},
  {id:"m48",source:"mundotek",name:"Infinix GT 50 Pro",specs:"12+12 GB RAM · 256 GB · Gaming",price:599,image:"https://mundotek.com.ec/wp-content/uploads/2026/07/infinix-gt-50-pro-launched-in-ph-c-300x188.jpg",url:"https://mundotek.com.ec/producto/infinix-gt-50-pro-hydroflow-y-gatillos-laterales-ram-1212-gb-256gb/",badge:"Precio bajo"},
  {id:"t1",source:"mundotek-tv",name:"TV Box Xiaomi Mi Box S 3ra Gen",specs:"TV Box · 4K",price:89,image:"https://mundotek.com.ec/wp-content/uploads/2021/06/tvbox2.webp",url:"https://mundotek.com.ec/producto/tv-box-xiaomi-mi-box-s/",badge:"#1 más económica"},
  {id:"t2",source:"mundotek-tv",name:"Smart TV House TV HT-32",specs:"32 pulgadas · HD LED · Android 14",price:135,image:"https://mundotek.com.ec/wp-content/uploads/2025/07/hausetv.jpg",url:"https://mundotek.com.ec/producto/smart-tv-house-tv-ht-32-32-fhd-led-android-14-definicion-full-hd/",badge:"#2 más económica"},
  {id:"t3",source:"mundotek-tv",name:"Smart TV Philips PH-32GFS-FISDB",specs:"32 pulgadas · HD LED · Google TV",price:155,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/tv-philips32.jpg",url:"https://mundotek.com.ec/producto/smart-tv-philips-ph-32gfs-fisdb-32-hd-led-android-14-google-tv-mando-de-voz-sin-bordes/",badge:"#3 más económica"},
  {id:"t4",source:"mundotek-tv",name:"Smart TV Riviera GLT32TPXM",specs:"32 pulgadas · HD · HDR · Google TV",price:159,image:"https://mundotek.com.ec/wp-content/uploads/2024/10/ri-rled-glt32tpxm-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-riviera-ri-rled-glt32tpxm-32-hd-1366x768-led-hdr-android-google-tv-mando-de-voz/",badge:"Precio bajo"},
  {id:"t5",source:"mundotek-tv",name:"Smart TV Innova IN-LED-32HD",specs:"32 pulgadas · HD LED · Google TV",price:159,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/in-led32hd-gtv-mp-300x300.jpg",url:"https://mundotek.com.ec/producto/13477/",badge:"Precio bajo"},
  {id:"t6",source:"mundotek-tv",name:"Televisor RCA 32 HDRC",specs:"32 pulgadas · HDR",price:159,image:"https://mundotek.com.ec/wp-content/uploads/2026/08/tvrca-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-rca-32-hdrc/",badge:"Precio bajo"},
  {id:"t7",source:"mundotek-tv",name:"TV Hisense 32Q4Q QLED",specs:"32 pulgadas · QLED · Vidaa",price:169,image:"https://mundotek.com.ec/wp-content/uploads/2026/06/hisense-serie-a4-smart-tv-a4q-300x225.png",url:"https://mundotek.com.ec/producto/tv-hisense-32q4q-qled-sistema-operativo-vida/",badge:"Precio bajo"},
  {id:"t8",source:"mundotek-tv",name:"TV Motorola 32TMKFHD",specs:"32 pulgadas · Google TV",price:170,image:"https://mundotek.com.ec/wp-content/uploads/2024/03/32tmkgfhd-300x300.jpg",url:"https://mundotek.com.ec/producto/tv-motorola-32tmkgfhd-android-11-32pulgadas/",badge:"Precio bajo"},
  {id:"t9",source:"mundotek-tv",name:"TV QLED Riviera GLT32TPQ10",specs:"32 pulgadas · QLED · Google TV",price:175,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/ri-rled-glt32tpq10-300x300.jpeg",url:"https://mundotek.com.ec/producto/televisor-google-qled-riviera-32-glt32tpq10/",badge:"Precio bajo"},
  {id:"t10",source:"mundotek-tv",name:"TV LED HD Indurama 32TIKGF5HD",specs:"32 pulgadas · LED · Google TV",price:185,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/32tikgf5hd-300x300.jpeg",url:"https://mundotek.com.ec/producto/televisor-google-led-hd-indurama-32-32tikgf5hd/",badge:"Precio bajo"},
  {id:"t11",source:"mundotek-tv",name:"HouseTV 40 pulgadas",specs:"40 pulgadas · Android 14",price:185,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/tv40-300x300.png",url:"https://mundotek.com.ec/producto/housetv-televisor-housetv-40-android-14/",badge:"Precio bajo"},
  {id:"t12",source:"mundotek-tv",name:"Smart TV TCL 32S5K",specs:"32 pulgadas · FHD · QLED · Google TV",price:195,image:"https://mundotek.com.ec/wp-content/uploads/2025/09/s5k32-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-tcl-32s5k-32-fhd-qled-android-14-google-tv/",badge:"Precio bajo"},
  {id:"t13",source:"mundotek-tv",name:"LG Smart TV 32LR650BPSA",specs:"32 pulgadas · Smart TV · ThinQ AI",price:199,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/32lr650bpsa-300x199.avif",url:"https://mundotek.com.ec/producto/pantalla-lg-smart-tv-32-smart-tv-con-thinq-ai-32lr650bpsa/",badge:"Precio bajo"},
  {id:"t14",source:"mundotek-tv",name:"Smart TV House TV HT-43",specs:"43 pulgadas · FHD LED · Android 14",price:209,image:"https://mundotek.com.ec/wp-content/uploads/2025/07/hausetv-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-house-tv-ht-43-43-fhd-led-android-14-definicion-full-hd/",badge:"Precio bajo"},
  {id:"t15",source:"mundotek-tv",name:"TV RCA 40FHDRC",specs:"40 pulgadas · FHD · Google TV · Bluetooth",price:215,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/40fhdrc-full-hd-300x300.jpg",url:"https://mundotek.com.ec/producto/tv-rca-40fhdrc-40-fhd-led-android-11-google-tv-dolby-audio-bluetooth/",badge:"Precio bajo"},
  {id:"t16",source:"mundotek-tv",name:"Smart TV Innova 40GFHD",specs:"40 pulgadas · FHD · Android 11 · Google TV",price:219,image:"https://mundotek.com.ec/wp-content/uploads/2025/07/40gfhd-mp-google-tv-300x300.jpg",url:"https://mundotek.com.ec/producto/mart-tv-innova-in-tvled-40gfhd-mp-40-fhd-led-android-11-google/",badge:"Precio bajo"},
  {id:"t17",source:"mundotek-tv",name:"TV Motorola 43MKNFHD",specs:"43 pulgadas · LED · Google TV",price:240,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/43mknfhd-300x300.jpg",url:"https://mundotek.com.ec/producto/televisor-led-43-google-tv-motorola-43mknfhd/",badge:"Precio bajo"},
  {id:"t18",source:"mundotek-tv",name:"Smart TV Philips 43GFS",specs:"43 pulgadas · FHD LED · Android 14",price:245,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/philips-43-gfs-fisdb-1-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-philips-ph-43gfs-fisdb-43-fhd-led-android-14-mando-2/",badge:"Precio bajo"},
  {id:"t19",source:"mundotek-tv",name:"TV TCL 43S5400",specs:"43 pulgadas · Google TV",price:249,image:"https://mundotek.com.ec/wp-content/uploads/2023/08/s5400-front--300x300.jpg",url:"https://mundotek.com.ec/producto/tv-32-pulgadas-tcl-43s5400/",badge:"Precio bajo"},
  {id:"t20",source:"mundotek-tv",name:"Smart TV Innova 43FHD",specs:"43 pulgadas · FHD · Android 14 · Google TV",price:249,image:"https://mundotek.com.ec/wp-content/uploads/2025/12/tvled-43gfhd-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-innova-in-led-43fhd-gtv-mp-43-fhd-led-android-14-google-tv/",badge:"Precio bajo"},
  {id:"t21",source:"mundotek-tv",name:"TV Hyundai HYLED4326G",specs:"43 pulgadas · FHD · Google TV",price:275,image:"https://mundotek.com.ec/wp-content/uploads/2025/06/hyled4326g.jpg",url:"https://mundotek.com.ec/producto/tv-hyundai-fhd-43-pulgadas-hyled4326g-google-tv/",badge:"Precio bajo"},
  {id:"t22",source:"mundotek-tv",name:"TV TCL 43S5K QLED",specs:"43 pulgadas · QLED · Android 14 · Google TV",price:275,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/43s5k.jpg",url:"https://mundotek.com.ec/producto/tv-tcl-43s5k-43-fhd-qled-android-14-google-tv/",badge:"Precio bajo"},
  {id:"t23",source:"mundotek-tv",name:"Smart TV Riviera GLT43TPQ10",specs:"43 pulgadas · QLED",price:289,image:"https://mundotek.com.ec/wp-content/uploads/2024/10/riviera-43.webp",url:"https://mundotek.com.ec/producto/smart-tv-riviera-ri-rled-glt43tpxm-43-fhd-1920x1080-led-hdr-android-google-tv-mando-de-voz/",badge:"Precio bajo"},
  {id:"t24",source:"mundotek-tv",name:"TV TCL 43 P635 4K HDR",specs:"43 pulgadas · 4K HDR · Google TV",price:299,image:"https://mundotek.com.ec/wp-content/uploads/2022/11/Captura-de-pantalla_20221130_173941.png",url:"https://mundotek.com.ec/producto/tv-tcl-43%e2%80%b3-4k-hdr-google-tv-p635/",badge:"Precio bajo"},
  {id:"t25",source:"mundotek-tv",name:"Smart TV Indurama 43TIKJ5UHD",specs:"43 pulgadas · 4K · Smart TV",price:309,image:"https://mundotek.com.ec/wp-content/uploads/2024/02/tikhudhd.webp",url:"https://mundotek.com.ec/producto/smart-tv-indurama-tv-43tikjuhd-43pulgadas/",badge:"Precio bajo"},
  {id:"t26",source:"mundotek-tv",name:"TV LG 43UA75 UHD AI",specs:"43 pulgadas · 4K · Smart TV 2025",price:325,image:"https://mundotek.com.ec/wp-content/uploads/2025/10/43ua75.webp",url:"https://mundotek.com.ec/producto/televisor-lg-43pulgadas-uhd-ai-43ua75-4k-smart-tv-2025/",badge:"Precio bajo"},
  {id:"t27",source:"mundotek-tv",name:"TV Innova 50UHD GTV",specs:"50 pulgadas · Google TV",price:345,image:"https://mundotek.com.ec/wp-content/uploads/2024/10/50uhd.png",url:"https://mundotek.com.ec/producto/tv-innova-in-led-50uhd-gtv-50-google-tv/",badge:"Precio bajo"},
  {id:"t28",source:"mundotek-tv",name:"Smart TV TCL 50S5K QLED",specs:"50 pulgadas · QLED · Google TV",price:349,image:"https://mundotek.com.ec/wp-content/uploads/2025/09/s5k-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-tcl-50s5k-50-fhd-qled-android-14-google-tv-panel-hva-qled/",badge:"Precio bajo"},
  {id:"t29",source:"mundotek-tv",name:"TCL P755 4K UHD",specs:"50 pulgadas · 4K UHD · Google TV",price:369,image:"https://mundotek.com.ec/wp-content/uploads/2024/03/tcl-p755-300x225.png",url:"https://mundotek.com.ec/producto/tcl-p755-4k-uhd-google-tv-50pulgadas/",badge:"Precio bajo"},
  {id:"t30",source:"mundotek-tv",name:"TV Riviera QLED GLT50TPQ10",specs:"50 pulgadas · QLED 4K · Google TV",price:369,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/rled-glt50tpq10-300x300.png",url:"https://mundotek.com.ec/producto/tv-riviera-qled-4k-glt50tpq10-50%e2%80%b3-google-tv/",badge:"Precio bajo"},
  {id:"t31",source:"mundotek-tv",name:"Smart TV Samsung Crystal UHD DU7000",specs:"50 pulgadas · 4K · Tizen",price:369,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/du7000-mtk-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-inteligente-crystal-uhd-du7000-4k-de-50-con-sistema-operativo-tizen-oferta-de-verano/",badge:"Precio bajo"},
  {id:"t32",source:"mundotek-tv",name:"TV Indurama 50TIKGF2GUHD",specs:"50 pulgadas · 4K · Google TV",price:379,image:"https://mundotek.com.ec/wp-content/uploads/2023/10/d_nq_np_783527-mec53271187298_012023-o-300x199.webp",url:"https://mundotek.com.ec/producto/tv-indurama-qled-50-pulgadas-50tikgf2guhd-google-tv/",badge:"Precio bajo"},
  {id:"t33",source:"mundotek-tv",name:"Smart TV Innova 55UHD GTV",specs:"55 pulgadas · 4K · Google TV",price:379,image:"https://mundotek.com.ec/wp-content/uploads/2024/12/in-led55mtk-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-innova-in-led-55uhd-gtv-mp-55-4k-uhd-led/",badge:"Precio bajo"},
  {id:"t34",source:"mundotek-tv",name:"Smart TV RCA LED55RCA684GT",specs:"55 pulgadas · 4K · Android Google TV",price:399,image:"https://mundotek.com.ec/wp-content/uploads/2024/07/rca684gt-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-rca-led55rca684gt-55-4k-uhd-led-android-google-tv/",badge:"Precio bajo"},
  {id:"t35",source:"mundotek-tv",name:"Smart TV Riviera RLED-GLT55PX9",specs:"55 pulgadas · 4K · Google TV",price:399,image:"https://mundotek.com.ec/wp-content/uploads/2025/05/google-tv-glt55px9-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-riviera-rled-glt55tpx9-55-4k-uhd-led-android-google-tv-color-negro/",badge:"Precio bajo"},
  {id:"t36",source:"mundotek-tv",name:"TV LG 50UA7500 UHD AI",specs:"50 pulgadas · 4K · Smart TV",price:409,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/50ua7500-300x199.jpeg",url:"https://mundotek.com.ec/producto/televisor-lg-uhd-ai-50ua7500-4k-smart-tv/",badge:"Precio bajo"},
  {id:"t37",source:"mundotek-tv",name:"LG UHD 50UR7300",specs:"50 pulgadas · 4K · ThinQ AI",price:419,image:"https://mundotek.com.ec/wp-content/uploads/2023/07/image-1-300x300.jpg",url:"https://mundotek.com.ec/producto/lg-uhd-50-ur7300-4k-smart-tv-con-thinq-ai-4k-procesador-inteligente/",badge:"Precio bajo"},
  {id:"t38",source:"mundotek-tv",name:"TV Hisense 55A6H",specs:"55 pulgadas · LED 4K · Vidaa",price:419,image:"https://mundotek.com.ec/wp-content/uploads/2024/05/tv-hisense-55-55a6h-300x300.jpg",url:"https://mundotek.com.ec/producto/televisor-tv-hisense-55%e2%80%b3-led-4k-smart-vidaa/",badge:"Precio bajo"},
  {id:"t39",source:"mundotek-tv",name:"TV Hisense 55Q6QV QLED",specs:"55 pulgadas · 4K · QLED · Vidaa",price:419,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/55q6qv-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-hisense-55q6qv-55-4k-uhd-qled-vidaa/",badge:"Precio bajo"},
  {id:"t40",source:"mundotek-tv",name:"TCL P6K 4K UHD",specs:"55 pulgadas · 4K UHD",price:429,image:"https://mundotek.com.ec/wp-content/uploads/2025/04/tv-tcl-55-55p6k-300x300.jpg",url:"https://mundotek.com.ec/producto/televisor-55pulgadas-tcl-p6k-4k-uhd/",badge:"Precio bajo"},
  {id:"t41",source:"mundotek-tv",name:"TV Riviera QLED GLT55TPQ10",specs:"55 pulgadas · QLED 4K · Google TV",price:429,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/rled-glt55tpq10-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-riviera-qled-55-rled-glt55tpq10/",badge:"Precio bajo"},
  {id:"t42",source:"mundotek-tv",name:"TV Motorola 55MGFUHD",specs:"55 pulgadas · 4K · Google TV",price:439,image:"https://mundotek.com.ec/wp-content/uploads/2024/10/mtk-tmkuhd-300x300.png",url:"https://mundotek.com.ec/producto/televisor-motorola-55tmkuhd-google-tv-55/",badge:"Precio bajo"},
  {id:"t43",source:"mundotek-tv",name:"TV Philips QLED Q55GFU",specs:"55 pulgadas · QLED 4K · Google TV",price:439,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/55gfu-300x300.png",url:"https://mundotek.com.ec/producto/televisor-philips-qled-55%e2%80%b3-pulgadas-uhd-4k-google-tv-q55gfu/",badge:"Precio bajo"},
  {id:"t44",source:"mundotek-tv",name:"Smart TV Samsung Crystal UHD DU7000",specs:"50 pulgadas · 4K · Tizen",price:459,image:"https://mundotek.com.ec/wp-content/uploads/2025/01/du7000-mtk-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-inteligente-crystal-uhd-du7000-4k-de-50-con-sistema-operativo-tizen-2024-copia/",badge:"Precio bajo"},
  {id:"t45",source:"mundotek-tv",name:"TV TCL T6C QLED",specs:"55 pulgadas · QLED · 4K",price:489,image:"https://mundotek.com.ec/wp-content/uploads/2025/05/qled-tcl-t6c-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-qled-tcl-t6c-55-pulgadas/",badge:"Precio bajo"},
  {id:"t46",source:"mundotek-tv",name:"Samsung 50Q7FAA Vision AI",specs:"50 pulgadas · 4K · Vision AI",price:489,image:"https://mundotek.com.ec/wp-content/uploads/2026/04/q7faa-50.avif",url:"https://mundotek.com.ec/producto/samsung-50-pulgadas-50q7faa-series-4k-vision-ai-smart-tv/",badge:"Precio bajo"},
  {id:"t47",source:"mundotek-tv",name:"TV Samsung 55U8000",specs:"55 pulgadas · Crystal UHD 4K · Tizen",price:499,image:"https://mundotek.com.ec/wp-content/uploads/2025/09/ue65u8000-300x300.png",url:"https://mundotek.com.ec/producto/tv-55-crystal-uhd-4k-u8000-tizen-os-smart-tv-2025/",badge:"Precio bajo"},
  {id:"t48",source:"mundotek-tv",name:"TV Innova 65GUHD Google TV",specs:"65 pulgadas · 4K · Google TV",price:519,image:"https://mundotek.com.ec/wp-content/uploads/2026/04/tv65.avif",url:"https://mundotek.com.ec/producto/televisor-innova-in-tvled-65guhd-mp-google-tv-65/",badge:"Precio bajo"},
  {id:"t49",source:"mundotek-tv",name:"TV Philips 65GFS-FISDB",specs:"65 pulgadas · LED · Google TV",price:525,image:"https://mundotek.com.ec/wp-content/uploads/2025/11/philips-65-300x300.jpg",url:"https://mundotek.com.ec/producto/televisor-philips-led-65gfs-fisdb-google-tv-65/",badge:"Precio bajo"},
  {id:"t50",source:"mundotek-tv",name:"LG 55UA7300 UHD AI",specs:"55 pulgadas · 4K · Smart TV",price:530,image:"https://mundotek.com.ec/wp-content/uploads/2025/10/55ua7300-300x300.webp",url:"https://mundotek.com.ec/producto/55-lg-uhd-ai-4k-smart-tv-55ua7300-2025/",badge:"Precio bajo"},
  {id:"t51",source:"mundotek-tv",name:"Samsung 55M70HAGXPE Mini LED",specs:"55 pulgadas · Mini LED · UHD",price:539,image:"https://mundotek.com.ec/wp-content/uploads/2026/04/m70hag-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-samsung-55-mini-led-uhd-un55m70hagxpe/",badge:"Precio bajo"},
  {id:"t52",source:"mundotek-tv",name:"TV LG 60UA8500PSA",specs:"60 pulgadas · LED 4K UHD",price:549,image:"https://mundotek.com.ec/wp-content/uploads/2026/03/60ua8500-300x300.jpeg",url:"https://mundotek.com.ec/producto/televisor-lg-60-led-4k-uhd-60ua8500psa/",badge:"Precio bajo"},
  {id:"t53",source:"mundotek-tv",name:"LG NanoCell NANO80TSA",specs:"55 pulgadas · NanoCell · 4K · ThinQ AI",price:555,image:"https://mundotek.com.ec/wp-content/uploads/2024/05/nano80-300x300.jpg",url:"https://mundotek.com.ec/producto/pantalla-lg-nanocell-55-nano77-4k-smart-tv-con-thinq-ai/",badge:"Precio bajo"},
  {id:"t54",source:"mundotek-tv",name:"Smart TV Riviera GLT65PX9",specs:"65 pulgadas · 4K · Google TV",price:569,image:"https://mundotek.com.ec/wp-content/uploads/2025/05/google-tv-glt65px9-300x300.jpg",url:"https://mundotek.com.ec/producto/smart-tv-riviera-glt65px9-65-4k-uhd-led-android-google-tv-sin-borde-mando-de-voz-2025/",badge:"Precio bajo"},
  {id:"t55",source:"mundotek-tv",name:"TV Motorola 65MNUHD",specs:"65 pulgadas · LED 4K UHD",price:569,image:"https://mundotek.com.ec/wp-content/uploads/2026/05/65mnuhd-300x300.webp",url:"https://mundotek.com.ec/producto/televisor-motorola-65-led-4k-uhd-65mnuhd/",badge:"Precio bajo"},
  {id:"t56",source:"mundotek-tv",name:"TV Hisense 65Q6QV QLED",specs:"65 pulgadas · 4K · QLED · Vidaa",price:579,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/65q6qv-300x300.jpg",url:"https://mundotek.com.ec/producto/televisores-hisense-65q6qv-65-4k-uhd-qled-vidaa-color/",badge:"Precio bajo"},
  {id:"t57",source:"mundotek-tv",name:"TV Indurama 65TIKGF2GUHD",specs:"65 pulgadas · UHD · Google TV",price:580,image:"https://mundotek.com.ec/wp-content/uploads/2024/02/tikhudhd.webp",url:"https://mundotek.com.ec/producto/televisor-65-indurama-uhd-google-tv-tikgf2guhd/",badge:"Precio bajo"},
  {id:"t58",source:"mundotek-tv",name:"TV Samsung 55Q7FAA QLED",specs:"55 pulgadas · QLED 4K · Vision AI",price:589,image:"https://mundotek.com.ec/wp-content/uploads/2026/04/q7faa-50.avif",url:"https://mundotek.com.ec/producto/55-qled-q7f-4k-samsung-vision-ai-smart-tv-2025/",badge:"Precio bajo"},
  {id:"t59",source:"mundotek-tv",name:"TCL P6K 4K UHD",specs:"65 pulgadas · 4K UHD",price:599,image:"https://mundotek.com.ec/wp-content/uploads/2025/04/tv-tcl-55-55p6k-300x300.jpg",url:"https://mundotek.com.ec/producto/televisor-65pulgadas-tcl-p6k-4k-uhd/",badge:"Precio bajo"},
  {id:"t60",source:"mundotek-tv",name:"TV Hisense 55U6ESG MiniLED",specs:"55 pulgadas · MiniLED 4K · Google TV",price:599,image:"https://mundotek.com.ec/wp-content/uploads/2026/02/55u6esg-300x300.jpg",url:"https://mundotek.com.ec/producto/tv-hisense-hi-qled-miniled-55-4k-55u6esg-google-tv-2026/",badge:"Precio bajo"},
];
const rawProducts = window.catalogProducts || fallbackProducts;
const roundUpTen = value => Math.ceil(value / 10) * 10;
const finalPrice = product => {
  const increment = product.source === "mundotek" ? 50 : ["pinsoft", "digitalpc"].includes(product.source) ? 90 : 80;
  return roundUpTen(product.price + increment);
};
const products = rawProducts.map(product => ({...product, price: finalPrice(product)}));

const emptyState = document.getElementById("emptyState");
const grid = document.getElementById("productGrid");
const resultCount = document.getElementById("resultCount");
const suggestions = document.getElementById("searchSuggestions");
let selectedCategory = "all";
const money = value => `$${value.toLocaleString("en-US", {minimumFractionDigits: Number.isInteger(value) ? 0 : 2, maximumFractionDigits: 2})}`;
const cardPrice = product => Math.round(product.price * 1.1 * 100) / 100;
const genericSpecs = /^(consulta disponibilidad|cotizaci[oó]n por whatsapp|precio final|equipo tecnol[oó]gico|rendimiento confiable|smartphone|smart tv|imagen de alta definici[oó]n|computadora|celular|televisor)$/i;
const genericSpecLabels = /^(marca|modelo|categor[ií]a|tipo de producto|disponibilidad)\s*:/i;
const normalizeSpec = value => String(value).replace(/\s+/g, " ").replace(/\s*:\s*/g, ": ").trim().replace(/^[|;,. -]+|[|;,. -]+$/g, "");
const specificSpecs = product => String(product.specs || "")
  .split(/\s*(?:·|\||;|\n|(?<!\d),)\s*/)
  .map(normalizeSpec)
  .filter((spec, index, all) => spec && !genericSpecs.test(spec) && !genericSpecLabels.test(spec) && all.findIndex(item => item.toLowerCase().replace(/\W/g, "") === spec.toLowerCase().replace(/\W/g, "")) === index)
  .slice(0, 6);
const categorySources = category => category === "computers" ? ["pinsoft", "digitalpc"] : category === "phones" ? ["mundotek"] : category === "tvs" ? ["mundotek-tv"] : ["pinsoft", "digitalpc", "mundotek", "mundotek-tv"];
const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character]));
function productArt(product) {
  const remoteImage = product.image_remote || product.image;
  const localImage = product.image || remoteImage;
  const image = localImage || remoteImage;
  return `<a class="product-image-link" href="${product.url}" target="_blank" rel="noopener"><img class="product-photo" src="${image}" alt="${product.name}" loading="lazy" onerror="if(this.dataset.fallback){this.classList.add('image-error');this.closest('.product-image').querySelector('.image-fallback').hidden=false}else{this.dataset.fallback='1';this.src='${remoteImage}' }"></a><span class="image-fallback" hidden>${product.name}</span>`;
}
function brandModel(name) {
  const cleanName = name.replace(/^cod\.?\s*[\w:-]+\s*/i, "")
    .replace(/^(laptop|computadora|computador|televisor(?:\s+inteligente)?|smart\s+tv|tv)\s+/i, "")
    .replace(/^kit\s+(?:fotográfico|fotografico)(?:\s+del?)?\s+/i, "")
    .replace(/^kit\s+/i, "")
    .split(/\s+(?:\/|\|)\s+/, 1)[0]
    .split(/\s+(?=(?:intel|amd|ryzen|core\s+i\d|celeron|pentium|apple\s+m\d|snapdragon|mediatek|ram\b|\d+\s*(?:gb|tb|ssd|nvme|pulgadas?|["″])))/i, 1)[0]
    .replace(/\s+\$[\d.,]+.*$/i, "")
    .replace(/\s{2,}/g, " ").trim();
  return cleanName.replace(/\s+(?:w11|windows\s+\d+|freedos|sin\s+sistema|android|google\s+tv|smart\s+tv).*$/i, "").trim();
}
function renderProducts() {
  const query = document.getElementById("searchInput").value.toLowerCase().trim();
  const sort = document.getElementById("sortSelect").value;
  const priceRange = document.getElementById("priceFilter").value;
  const [minPrice, maxPrice] = priceRange === "all" ? [0, Infinity] : priceRange === "601-plus" ? [601, Infinity] : priceRange.split("-").map(Number);
  const sources = categorySources(selectedCategory);
  const visible = products.filter(p => sources.includes(p.source) && p.price >= minPrice && p.price <= maxPrice && `${p.name} ${p.specs}`.toLowerCase().includes(query)).sort((a,b) => sort === "popular" ? a.id.localeCompare(b.id) : a.price - b.price);
  grid.innerHTML = visible.map(productCard).join("");
  if (resultCount) resultCount.textContent = `${visible.length} resultados`;
  emptyState.style.display = visible.length ? "none" : "block";
}
function renderSearchSuggestions() {
  const query = document.getElementById("searchInput").value.toLowerCase().trim();
  if (!query) {
    suggestions.innerHTML = "";
    suggestions.classList.remove("is-visible");
    return;
  }
  const matches = products.filter(product => categorySources(selectedCategory).includes(product.source) && `${product.name} ${product.specs}`.toLowerCase().includes(query)).slice(0, 8);
  suggestions.innerHTML = matches.length ? matches.map(product => `<button type="button" class="search-suggestion" data-product-id="${escapeHtml(product.id)}"><span>${escapeHtml(brandModel(product.name))}</span><strong>${money(product.price)}</strong></button>`).join("") : `<div class="search-no-results">No encontramos ese producto</div>`;
  suggestions.classList.add("is-visible");
}
function productCard(p) {
  const specs = specificSpecs(p);
  const specsMarkup = specs.map(spec => `<li>${spec}</li>`).join("");
  return `<article class="product-card ${p.id.endsWith("1") ? "featured" : ""}"><div class="product-image">${productArt(p)}</div><h3>${brandModel(p.name)}</h3><ul class="specs" aria-label="Características principales">${specsMarkup}</ul><div class="price-options"><div class="price-option card-price"><strong>Tarjeta de crédito</strong><b>${money(cardPrice(p))}</b></div><div class="price-option direct-price"><strong>Efectivo/Transferencia</strong><b>${money(p.price)}</b></div></div><a class="quote-btn quote-full" href="${whatsappUrl(p)}" target="_blank" rel="noopener">Cotizar este producto</a></article>`;
}
function whatsappUrl(product) { return `https://wa.me/593992217314?text=${encodeURIComponent(`Hola AGNEXUSUIO, deseo cotizar el producto: ${product.name}. Precio final: ${money(product.price)}.`)}`; }
document.getElementById("searchSubmit").addEventListener("click", () => document.getElementById("catalogo").scrollIntoView({behavior:"smooth", block:"start"}));
document.getElementById("searchInput").addEventListener("input", () => { renderProducts(); renderSearchSuggestions(); });
suggestions.addEventListener("click", event => {
  const option = event.target.closest("[data-product-id]");
  if (!option) return;
  const product = products.find(item => item.id === option.dataset.productId);
  if (!product) return;
  document.getElementById("searchInput").value = brandModel(product.name);
  suggestions.classList.remove("is-visible");
  renderProducts();
  document.getElementById("catalogo").scrollIntoView({behavior:"smooth", block:"start"});
});
document.getElementById("priceFilter").addEventListener("change", renderProducts);
document.getElementById("sortSelect").addEventListener("change", renderProducts);
document.getElementById("headerCategory").addEventListener("change", event => {
  selectedCategory = event.target.value;
  document.querySelectorAll("[name=sideCategory]").forEach(input => input.checked = input.value === selectedCategory);
  renderProducts();
  renderSearchSuggestions();
});
document.querySelectorAll("[name=sideCategory]").forEach(input => input.addEventListener("change", event => {
  selectedCategory = event.target.value;
  document.getElementById("headerCategory").value = selectedCategory;
  document.querySelectorAll(".category-tab").forEach(tab => tab.classList.toggle("active", tab.dataset.category === selectedCategory));
  renderProducts();
}));
document.getElementById("mobileFilter").addEventListener("click", () => document.getElementById("filters").classList.toggle("is-open"));
document.addEventListener("click", event => {
  if (!event.target.closest(".search-wrap")) suggestions.classList.remove("is-visible");
});
document.querySelectorAll(".category-tab").forEach(tab => tab.addEventListener("click", () => {
  selectedCategory = tab.dataset.category;
  document.querySelectorAll(".category-tab").forEach(item => item.classList.toggle("active", item === tab));
  document.getElementById("catalogTitle").textContent = selectedCategory === "computers" ? "Computadoras para cada objetivo" : selectedCategory === "phones" ? "Celulares para todos los días" : selectedCategory === "tvs" ? "Televisores para disfrutar más" : "Tecnología lista para ti";
  renderProducts();
}));
renderProducts();
