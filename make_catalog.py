# -*- coding: utf-8 -*-
"""Generate a professional product catalog PDF for Mohit Rubber Industries."""
import os, io, requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_catalog_imgs")
os.makedirs(CACHE, exist_ok=True)

RED = colors.HexColor("#C0392B")
CHARCOAL = colors.HexColor("#1a1a1a")
STEEL = colors.HexColor("#6b6b6b")
WARM = colors.HexColor("#f4f1ec")

PAGE_W, PAGE_H = A4

# ---- Company info ----
COMPANY = "MOHIT RUBBER INDUSTRIES"
TAGLINE = "Your Complete Rubber Solution"
ADDRESS = "Khasra M58, Gali No. 3, Near Bari Ka Bagh, Malerna Road,\nBallabgarh, Faridabad, Haryana 121004"
PHONE = "+91 98995 72755"
WHATSAPP = "+91 83686 94846"
EMAIL = "mohitrubberindustries@gmail.com"
WEB = "www.indiamart.com/mohit-rubber-industries"

# ---- Products grouped by category ----
PRODUCTS = {
  "EPDM Rubber Profiles": [
    ("EPDM Sponge Profile", "20mm · Black", "https://5.imimg.com/data5/SELLER/Default/2025/10/550883821/YO/AS/QQ/4077162/20mm-epdm-sponge-rubber-profile-500x500.png"),
    ("EPDM Rubber Profile", "20mm · Solid", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449708/OU/DM/OY/4077162/20mm-epdm-rubber-profile-500x500.jpeg"),
    ("EPDM Sponge Profile", "Custom Section", "https://5.imimg.com/data5/SELLER/Default/2025/10/550884319/LU/FS/DO/4077162/20mm-epdm-sponge-rubber-profile-500x500.png"),
    ("EPDM Sponge Profile", "D-Section", "https://5.imimg.com/data5/SELLER/Default/2025/10/550884807/GP/CI/FB/4077162/20mm-epdm-sponge-rubber-profile-500x500.png"),
    ("EPDM Sponge Profile", "5mm · P-Section", "https://5.imimg.com/data5/SELLER/Default/2025/10/550882603/MN/HN/TZ/4077162/5mm-epdm-sponge-rubber-profile-500x500.png"),
    ("EPDM Rubber Profile", "4mm · Solid", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449054/AY/SY/BY/4077162/4mm-epdm-rubber-profile-500x500.jpg"),
    ("K-Shape Window Profile", "EPDM · Casement Seal", "https://5.imimg.com/data5/SELLER/Default/2025/10/550450721/DV/WB/IX/4077162/k-shape-epdm-window-profile-500x500.jpg"),
  ],
  "Silicone & Silicon Profiles": [
    ("Silicone C-Profile", "4mm · C-Section", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449792/DF/TW/VX/4077162/4mm-silicone-c-rubber-profile-500x500.jpeg"),
    ("Silicone Profile", "Custom Extrusion", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449821/DA/ES/DP/4077162/4mm-silicone-c-rubber-profile-500x500.jpeg"),
    ("Silicon Rubber Profile", "8mm · T-Section", "https://5.imimg.com/data5/SELLER/Default/2025/10/550117061/WR/CN/KL/4077162/8mm-silicon-rubber-profile-500x500.jpg"),
    ("Silicon Profile", "8mm · High Temp", "https://5.imimg.com/data5/SELLER/Default/2025/10/550117281/KC/XI/FL/4077162/8mm-silicon-rubber-profile-500x500.jpeg"),
    ("Silicon Sponge Profile", "3mm · Flexible", "https://5.imimg.com/data5/SELLER/Default/2025/10/550885532/HS/IW/DB/4077162/3mm-silicon-sponge-rubber-profile-500x500.png"),
    ("Silicon Rubber Profile", "3mm", "https://5.imimg.com/data5/SELLER/Default/2025/10/550116775/UK/FR/FJ/4077162/3mm-silicon-rubber-profile-500x500.png"),
  ],
  "Sponge Strips & Seals": [
    ("EPDM Sponge Strips", "Self-Adhesive", "https://5.imimg.com/data5/SELLER/Default/2025/10/550119103/HK/OI/CJ/4077162/epdm-sponge-rubber-strips-500x500.jpeg"),
    ("EPDM Sponge Strips", "Door / Window Seal", "https://5.imimg.com/data5/SELLER/Default/2023/5/310857237/WE/ZH/AB/4077162/epdm-sponge-rubber-strips-500x500.jpg"),
    ("Sponge Rubber Strips", "3mm · Black", "https://5.imimg.com/data5/SELLER/Default/2023/5/310858545/CU/HC/BS/4077162/3mm-sponge-rubber-strips-500x500.jpg"),
    ("Natural Sponge Strip", "3mm · Brown", "https://5.imimg.com/data5/SELLER/Default/2025/10/550880328/AH/EE/GO/4077162/3mm-natural-sponge-rubber-strip-500x500.png"),
    ("Natural Sponge Strip", "Custom Width", "https://5.imimg.com/data5/SELLER/Default/2025/10/550447135/JJ/HJ/YT/4077162/3mm-natural-sponge-rubber-strip-500x500.jpg"),
    ("EPDM Sponge Strip", "20mm Wide", "https://5.imimg.com/data5/SELLER/Default/2025/10/550118701/HK/AL/PY/4077162/20mm-epdm-sponge-rubber-strip-500x500.jpeg"),
    ("EPDM Sponge Strip", "Weather Seal Grade", "https://5.imimg.com/data5/SELLER/Default/2025/10/550118940/GI/XR/EZ/4077162/20mm-epdm-sponge-rubber-strip-500x500.jpeg"),
    ("Rubber Sealing Strip", "4mm · EPDM", "https://5.imimg.com/data5/SELLER/Default/2023/5/310846354/LE/DT/CV/4077162/4mm-rubber-sealing-strip-500x500.jpg"),
    ("Natural Rubber Seal", "15mm · EPDM", "https://5.imimg.com/data5/SELLER/Default/2025/10/550450388/YB/ET/YB/4077162/15mm-epdm-natural-rubber-sealing-strip-500x500.jpg"),
    ("EPDM Sealing Strip", "Glazing / Panel Seal", "https://5.imimg.com/data5/SELLER/Default/2023/5/310853933/BC/UE/RH/4077162/epdm-rubber-sealing-strip-500x500.jpg"),
    ("EPDM Sealing Strip", "Industrial Grade", "https://5.imimg.com/data5/SELLER/Default/2023/5/310854517/KN/MR/SP/4077162/epdm-rubber-sealing-strip-500x500.jpg"),
  ],
  "Tubes, Cords & Fenders": [
    ("EPDM Rubber Tube", "4mm · White", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449864/TU/UR/LY/4077162/4mm-white-epdm-rubber-tube-500x500.jpeg"),
    ("EPDM Rubber Tube", "3mm · Black", "https://5.imimg.com/data5/SELLER/Default/2025/10/550887527/JB/SS/ZN/4077162/3mm-black-epdm-rubber-tube-500x500.png"),
    ("EPDM Rubber Tube", "10mm · Black", "https://5.imimg.com/data5/SELLER/Default/2025/10/550449367/FZ/ID/YO/4077162/10mm-black-epdm-rubber-tube-500x500.jpg"),
    ("EPDM Sponge Tube", "8mm · Hollow", "https://5.imimg.com/data5/SELLER/Default/2025/10/550759999/BT/XY/PY/4077162/8mm-black-epdm-sponge-rubber-tube-500x500.png"),
    ("EPDM Sponge Tube", "Custom Bore", "https://5.imimg.com/data5/SELLER/Default/2025/10/550113335/LB/HU/ZT/4077162/epdm-sponge-rubber-tube-500x500.jpeg"),
    ("Sponge Rubber Cords", "Round Section", "https://5.imimg.com/data5/SELLER/Default/2023/5/310847750/OG/GI/PO/4077162/sponge-rubber-cords-500x500.jpg"),
    ("Sponge Rubber Cords", "EPDM · Various Dia", "https://5.imimg.com/data5/SELLER/Default/2023/5/310847835/FD/JL/SM/4077162/sponge-rubber-cords-500x500.jpg"),
    ("EPDM Rubber Cord", "Grey · Round", "https://5.imimg.com/data5/SELLER/Default/2023/5/310851264/QL/RG/TO/4077162/grey-epdm-rubber-cord-500x500.jpg"),
    ("Synthetic Sponge Cord", "18mm · Red", "https://5.imimg.com/data5/SELLER/Default/2025/10/550758605/OG/ZF/UN/4077162/18mm-red-synthetic-sponge-rubber-cord-500x500.png"),
    ("Synthetic Sponge Cord", "Colored · Custom Dia", "https://5.imimg.com/data5/SELLER/Default/2025/10/550757834/XS/RI/CZ/4077162/18mm-red-synthetic-sponge-rubber-cord-500x500.png"),
    ("Rubber Ship Fender", "150mm · Parking", "https://5.imimg.com/data5/SELLER/Default/2025/10/550713249/NW/FM/DD/4077162/150mm-black-rubber-parking-ship-fender-500x500.png"),
    ("Rubber Dock Fender", "Marine Grade", "https://5.imimg.com/data5/SELLER/Default/2025/10/550712518/NG/BK/EX/4077162/150mm-black-rubber-parking-ship-fender-500x500.png"),
    ("EPDM Dock Fender", "100mm · Heavy Duty", "https://5.imimg.com/data5/SELLER/Default/2025/10/550451395/OB/HH/EP/4077162/100mm-black-epdm-rubber-dock-fender-500x500.jpg"),
  ],
}


def fetch(url):
    """Download and cache an image; return local path or None."""
    fname = os.path.join(CACHE, str(abs(hash(url))) + ".img")
    if os.path.exists(fname) and os.path.getsize(fname) > 0:
        return fname
    try:
        r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and len(r.content) > 100:
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            img.save(fname, "JPEG", quality=85)
            return fname
    except Exception as e:
        print("  ! failed", url[:60], e)
    return None


def draw_footer(c, pageno):
    c.setFillColor(STEEL)
    c.setFont("Helvetica", 7)
    c.drawString(18*mm, 10*mm, COMPANY + "  ·  " + EMAIL)
    c.drawRightString(PAGE_W - 18*mm, 10*mm, "Page %d" % pageno)
    c.setStrokeColor(colors.HexColor("#dddddd"))
    c.setLineWidth(0.5)
    c.line(18*mm, 13*mm, PAGE_W - 18*mm, 13*mm)


def cover(c):
    # charcoal background
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # top red bar
    c.setFillColor(RED)
    c.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    # logo (white)
    logo = os.path.join(HERE, "logo.png")
    if os.path.exists(logo):
        try:
            im = Image.open(logo).convert("RGBA")
            # make white version on transparent
            bg = Image.new("RGBA", im.size, (255,255,255,0))
            px = im.load()
            for y in range(im.size[1]):
                for x in range(im.size[0]):
                    r,g,b,a = px[x,y]
                    if a > 30:
                        bg.putpixel((x,y),(255,255,255,a))
            buf = io.BytesIO(); bg.save(buf,"PNG"); buf.seek(0)
            c.drawImage(ImageReader(buf), PAGE_W/2 - 30*mm, PAGE_H - 80*mm,
                        width=60*mm, height=60*mm, mask='auto', preserveAspectRatio=True)
        except Exception as e:
            print("logo err", e)
    # company name
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(PAGE_W/2, PAGE_H - 110*mm, "MOHIT")
    c.setFillColor(RED)
    c.drawCentredString(PAGE_W/2, PAGE_H - 124*mm, "RUBBER")
    c.setFillColor(colors.white)
    c.drawCentredString(PAGE_W/2, PAGE_H - 138*mm, "INDUSTRIES")
    # tagline
    c.setFont("Helvetica", 13)
    c.setFillColor(colors.HexColor("#cccccc"))
    c.drawCentredString(PAGE_W/2, PAGE_H - 152*mm, TAGLINE)
    # divider
    c.setStrokeColor(RED); c.setLineWidth(1.5)
    c.line(PAGE_W/2 - 25*mm, PAGE_H - 160*mm, PAGE_W/2 + 25*mm, PAGE_H - 160*mm)
    # subtitle
    c.setFont("Helvetica", 11); c.setFillColor(colors.HexColor("#aaaaaa"))
    c.drawCentredString(PAGE_W/2, PAGE_H - 172*mm, "PRODUCT CATALOG")
    c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_W/2, PAGE_H - 180*mm, "Natural  ·  EPDM  ·  Nitrile  ·  Neoprene  ·  Silicone  ·  Sponge")
    # bottom contact block
    c.setFillColor(RED)
    c.rect(0, 0, PAGE_W, 34*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(PAGE_W/2, 24*mm, "Est. 2005  ·  ISO 9001:2015 Certified  ·  Faridabad, Haryana")
    c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_W/2, 16*mm, "Phone: %s   ·   WhatsApp: %s" % (PHONE, WHATSAPP))
    c.drawCentredString(PAGE_W/2, 9*mm, "%s   ·   %s" % (EMAIL, WEB))
    c.showPage()


def about(c):
    c.setFillColor(WARM); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    c.setFillColor(RED); c.rect(0, PAGE_H-8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    y = PAGE_H - 30*mm
    c.setFillColor(RED); c.setFont("Helvetica-Bold", 11)
    c.drawString(18*mm, y, "ABOUT US")
    y -= 12*mm
    c.setFillColor(CHARCOAL); c.setFont("Helvetica-Bold", 24)
    c.drawString(18*mm, y, "Built on Precision.")
    y -= 11*mm
    c.drawString(18*mm, y, "Trusted for Quality.")
    y -= 14*mm
    para = [
      "Established in 2005 at Ballabgarh, Faridabad, Mohit Rubber Industries",
      "manufactures a comprehensive range of EPDM rubber profiles, gaskets,",
      "seals, and custom-extruded components. We serve the UPVC window,",
      "aluminium door, and industrial sectors with products that meet",
      "IS 11149 specifications.",
      "",
      "Our facility houses Kneaders, Extruders, Mixing Mills, Curing Ovens,",
      "and Boilers — all operated by an experienced team committed to",
      "on-time delivery at competitive prices.",
    ]
    c.setFillColor(STEEL); c.setFont("Helvetica", 11)
    for line in para:
        c.drawString(18*mm, y, line); y -= 6.5*mm

    # stat boxes
    y -= 6*mm
    stats = [("20+","Years of Experience"),("4","Extruder Lines"),
             ("200+","Profile Designs"),("ISO","9001:2015 Certified")]
    bx = 18*mm; bw = (PAGE_W-36*mm-3*4*mm)/4
    for big, small in stats:
        c.setFillColor(CHARCOAL); c.rect(bx, y-22*mm, bw, 22*mm, fill=1, stroke=0)
        c.setFillColor(RED); c.setFont("Helvetica-Bold", 20)
        c.drawString(bx+4*mm, y-11*mm, big)
        c.setFillColor(colors.white); c.setFont("Helvetica", 7.5)
        c.drawString(bx+4*mm, y-18*mm, small)
        bx += bw + 4*mm

    # materials list
    y -= 34*mm
    c.setFillColor(RED); c.setFont("Helvetica-Bold", 13)
    c.drawString(18*mm, y, "Materials We Work With")
    y -= 9*mm
    mats = ["EPDM Rubber","Natural Rubber","Nitrile (NBR)","Neoprene","Silicone",
            "EPDM Sponge","Natural Sponge","Silicone Sponge"]
    c.setFillColor(CHARCOAL); c.setFont("Helvetica", 11)
    col = 18*mm
    for i, m in enumerate(mats):
        c.setFillColor(RED); c.circle(col+1.5*mm, y+1*mm, 1.2*mm, fill=1, stroke=0)
        c.setFillColor(CHARCOAL)
        c.drawString(col+5*mm, y, m)
        if i % 2 == 0:
            col2 = PAGE_W/2
            col, save = col2, col
        else:
            col = 18*mm; y -= 7*mm
    draw_footer(c, 2)
    c.showPage()


def product_pages(c, start_page):
    pageno = start_page
    cols, rows = 3, 4
    margin = 16*mm
    gx, gy = 6*mm, 6*mm
    cell_w = (PAGE_W - 2*margin - (cols-1)*gx)/cols
    cell_h = (PAGE_H - 55*mm - (rows-1)*gy)/rows

    for cat, items in PRODUCTS.items():
        idx = 0
        while idx < len(items):
            # header
            c.setFillColor(WARM); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
            c.setFillColor(RED); c.rect(0, PAGE_H-8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
            c.setFillColor(CHARCOAL); c.setFont("Helvetica-Bold", 18)
            c.drawString(margin, PAGE_H-24*mm, cat)
            c.setStrokeColor(RED); c.setLineWidth(2)
            c.line(margin, PAGE_H-27*mm, margin+45*mm, PAGE_H-27*mm)

            top = PAGE_H - 35*mm
            for r in range(rows):
                for cc in range(cols):
                    if idx >= len(items): break
                    name, sub, url = items[idx]; idx += 1
                    x = margin + cc*(cell_w+gx)
                    y = top - r*(cell_h+gy) - cell_h
                    # card bg
                    c.setFillColor(colors.white)
                    c.rect(x, y, cell_w, cell_h, fill=1, stroke=0)
                    c.setStrokeColor(colors.HexColor("#e3ddd4")); c.setLineWidth(0.5)
                    c.rect(x, y, cell_w, cell_h, fill=0, stroke=1)
                    # image
                    p = fetch(url)
                    img_h = cell_h - 14*mm
                    if p:
                        try:
                            c.drawImage(p, x+1*mm, y+13*mm, width=cell_w-2*mm,
                                        height=img_h-1*mm, preserveAspectRatio=True,
                                        anchor='c', mask='auto')
                        except Exception as e:
                            print("draw err", e)
                    # label band
                    c.setFillColor(CHARCOAL)
                    c.rect(x, y, cell_w, 12*mm, fill=1, stroke=0)
                    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 8.5)
                    c.drawString(x+2.5*mm, y+7*mm, name[:28])
                    c.setFillColor(colors.HexColor("#e6b0aa")); c.setFont("Helvetica", 7)
                    c.drawString(x+2.5*mm, y+2.5*mm, sub[:30])
                if idx >= len(items): break
            draw_footer(c, pageno); pageno += 1
            c.showPage()
    return pageno


def certifications(c, pageno):
    c.setFillColor(WARM); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    c.setFillColor(RED); c.rect(0, PAGE_H-8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    c.setFillColor(CHARCOAL); c.setFont("Helvetica-Bold", 20)
    c.drawString(18*mm, PAGE_H-26*mm, "Credentials & Certifications")
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(18*mm, PAGE_H-30*mm, 70*mm, PAGE_H-30*mm)

    certs = [("cert_iso.png","ISO 9001:2015","Quality Management System"),
             ("cert_msme.png","MSME / Udyam Registered","UDYAM-HR-03-0065031")]
    y = PAGE_H - 45*mm
    cw = (PAGE_W - 36*mm - 8*mm)/2
    x = 18*mm
    for fn, title, sub in certs:
        path = os.path.join(HERE, fn)
        c.setFillColor(colors.white); c.rect(x, y-95*mm, cw, 95*mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#e3ddd4")); c.rect(x, y-95*mm, cw, 95*mm, fill=0, stroke=1)
        if os.path.exists(path):
            try:
                c.drawImage(path, x+3*mm, y-80*mm, width=cw-6*mm, height=70*mm,
                            preserveAspectRatio=True, anchor='c', mask='auto')
            except Exception as e:
                print("cert err", e)
        c.setFillColor(CHARCOAL); c.setFont("Helvetica-Bold", 11)
        c.drawString(x+3*mm, y-88*mm, title)
        c.setFillColor(STEEL); c.setFont("Helvetica", 8)
        c.drawString(x+3*mm, y-93*mm, sub)
        x += cw + 8*mm

    # GST text
    y2 = y - 105*mm
    c.setFillColor(RED); c.setFont("Helvetica-Bold", 12)
    c.drawString(18*mm, y2, "GST Registration")
    c.setFillColor(STEEL); c.setFont("Helvetica", 10)
    c.drawString(18*mm, y2-7*mm, "GST No.: 06APIPK6971R1ZZ  ·  Regular Taxpayer  ·  Trade name: Mohit Rubber Industries")
    draw_footer(c, pageno)
    c.showPage()
    return pageno+1


def back_cover(c):
    c.setFillColor(CHARCOAL); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    c.setFillColor(RED); c.rect(0, PAGE_H-8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(PAGE_W/2, PAGE_H-70*mm, "Get in Touch")
    c.setStrokeColor(RED); c.setLineWidth(1.5)
    c.line(PAGE_W/2-25*mm, PAGE_H-76*mm, PAGE_W/2+25*mm, PAGE_H-76*mm)
    info = [("Address", ADDRESS.replace("\n"," ")),("Phone", PHONE),
            ("WhatsApp", WHATSAPP),("Email", EMAIL),("Online", WEB)]
    y = PAGE_H - 95*mm
    for label, val in info:
        c.setFillColor(RED); c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(PAGE_W/2, y, label.upper())
        c.setFillColor(colors.white); c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W/2, y-6*mm, val)
        y -= 18*mm
    c.setFillColor(colors.HexColor("#888888")); c.setFont("Helvetica", 9)
    c.drawCentredString(PAGE_W/2, 20*mm, "© 2025 Mohit Rubber Industries  ·  ISO 9001:2015 Certified")
    c.showPage()


def main():
    out = os.path.join(HERE, "catalog.pdf")
    print("Downloading product images (this may take a minute)...")
    total = sum(len(v) for v in PRODUCTS.values())
    done = 0
    for items in PRODUCTS.values():
        for _,_,url in items:
            fetch(url); done += 1
            print("  %d/%d" % (done, total))
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Mohit Rubber Industries — Product Catalog")
    c.setAuthor(COMPANY)
    cover(c)
    about(c)
    pageno = product_pages(c, 3)
    pageno = certifications(c, pageno)
    back_cover(c)
    c.save()
    print("DONE ->", out, "(%d bytes)" % os.path.getsize(out))


if __name__ == "__main__":
    main()
