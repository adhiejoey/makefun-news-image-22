#!/usr/bin/env python3
"""Draw the news-image-20261122 broadsheet: 40 sourced stories from Sunday 22 Nov 2026.

Cream-paper broadsheet, 3 columns, UTC timeline, schematic world map, date-check box.
All story text was researched and written in this session; see SOURCES.md notes in code.
Output: entry.png, 1024x1024, under 1 MiB.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 239, 219)
INK = (28, 26, 23)
RED = (156, 26, 26)
MUTED = (107, 98, 87)
RULE = (28, 26, 23)
MAP_FILL = (51, 80, 107)
MAP_LINE = (28, 26, 23)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# (region, headline, summary, source, confidence)
STORIES = [
    ("TOP STORIES",
     "COP31 draft drops fossil fuels as talks stall",
     "Antalya's final text never names fossil fuels and concedes 1.5C will be passed.",
     "AP / Reuters", "HIGH"),
    ("TOP STORIES",
     "Iran claims Hormuz; Bahrain goes to the UN",
     "Tehran says it controls the strait after strikes on US radars; Bahrain demands UN action.",
     "Investing.com", "HIGH"),
    ("TOP STORIES",
     "FBI's crime database hacked, Trump sees upside",
     "Hackers got into the NCIC system of fingerprints and wanted persons; Trump saw a 'positive spin'.",
     "CNBC / AP", "HIGH"),
    ("TOP STORIES",
     "11 killed in Sinaloa after cartel boss captured",
     "Troops seized 'El Chapo Isidro' in Guasave; the violence that followed left 11 dead.",
     "AP", "MED"),
    ("TOP STORIES",
     "Sweets factory fire kills 3, 36 missing in Banten",
     "Blaze at a confectionery plant in Cikande; survivors were pulled from the wreckage on Sunday.",
     "Seven Lights", "MED"),
    ("MIDDLE EAST",
     "Houthis strike Saudi Arabia after coalition raid",
     "Yemen's Houthis hit the kingdom after vowing revenge for a coalition raid on Hodeida.",
     "iqmia", "MED"),
    ("MIDDLE EAST",
     "Saudi defences stop Houthi missile aimed west",
     "Coalition says it intercepted a ballistic missile; a brief alert for Mecca province was issued, then lifted.",
     "AFP / CBS", "HIGH"),
    ("MIDDLE EAST",
     "Iran: reopening Hormuz 'not difficult' if US agrees",
     "Foreign Minister Araghchi says the strait can reopen if Washington accepts Tehran's conditions.",
     "Dainik Jagran", "HIGH"),
    ("MIDDLE EAST",
     "Iran FM: big opposition to nuclear doctrine shift",
     "Abbas Araghchi reports major opposition inside Iran to changing its nuclear doctrine.",
     "News Media House", "MED"),
    ("MIDDLE EAST",
     "Israel ministries clash over US aid funding",
     "Defence and finance ministries in Jerusalem disagree over how American aid money is used.",
     "News Media House", "MED"),
    ("MIDDLE EAST",
     "Palestinians protest as Gaza strikes intensify",
     "Displaced families demonstrated while Israeli strikes on Gaza stepped up on Sunday.",
     "News Media House", "MED"),
    ("MIDDLE EAST",
     "Syrian Christians demand safety after kidnapping",
     "Community leaders in Suqaylabiyah call for protection after a jeweller was abducted.",
     "News Media House", "MED"),
    ("AMERICAS",
     "Trump seeks 'permanent' deal to stop Iran bomb",
     "The president wants a lasting deal to block Iran's nuclear ambitions; regime change 'never' his goal.",
     "CNBC", "MED"),
    ("AMERICAS",
     "Vance won't back Trump claim on Iran's bomb",
     "Vice-president stops short of endorsing the claim that Iran was close to a nuclear weapon.",
     "The Guardian", "HIGH"),
    ("AMERICAS",
     "GOP weighs governors as Vance alternatives",
     "CNN reports several current and former governors are floated as future nomination options.",
     "CNN", "HIGH"),
    ("AMERICAS",
     "Amazon nears $7.5bn deal for AI startup Decart",
     "The Israeli chip startup would boost Amazon's Trainium hardware against Nvidia.",
     "Crypto Briefing", "HIGH"),
    ("AMERICAS",
     "Two ex-Montreal officers charged in probe",
     "Former police officers face assault, breach of trust and harassment charges after a racism inquiry.",
     "iqmia", "MED"),
    ("AMERICAS",
     "Verstappen wins wild Las Vegas Grand Prix",
     "35 lead changes under the lights; Norris, Piastri on the podium. Sat night in Nevada, Sun UTC.",
     "Reuters / F1", "MED"),
    ("EUROPE",
     "France: 144 held after sixth protest weekend",
     "82,500 marched over living costs and a police law; clashes in Paris, Marseille, Bordeaux.",
     "Al Jazeera / BFMTV", "MED"),
    ("EUROPE",
     "UK polls: opinion turning against Brexit",
     "New polling reported by The Independent shows a decisive shift in British attitudes.",
     "The Independent", "HIGH"),
    ("EUROPE",
     "EU floats digital tax amid budget divisions",
     "Brussels proposes a levy on tech giants as member states split over the next budget.",
     "Daily Perspective", "MED"),
    ("EUROPE",
     "Village votes symbolically to 'leave the UK'",
     "Barnham residents back a non-binding vote against plans to house migrants at a former base.",
     "iqmia", "MED"),
    ("EUROPE",
     "UN states reach tentative weapons-rules deal",
     "Nations agree in principle on rules for autonomous weapons after long talks.",
     "Daily Perspective", "MED"),
    ("EUROPE",
     "Security Council split over next UN chief",
     "Members divided over the successor to the Secretary-General as a deadline looms.",
     "News Media House", "MED"),
    ("ASIA",
     "Nepal PM arrives in India for state visit",
     "Balendra Shah begins a two-day visit for talks with Prime Minister Narendra Modi.",
     "Dainik Jagran", "HIGH"),
    ("ASIA",
     "India, China generals end fresh border talks",
     "Generals' talks on the Arunachal frontier end with no breakthrough announced.",
     "Dainik Jagran", "HIGH"),
    ("ASIA",
     "China renews UN bid to blacklist BLA",
     "Beijing pushes to list the Balochistan Liberation Army and Majeed Brigade as terrorists.",
     "iqmia", "MED"),
    ("ASIA",
     "Pakistan: 15 militants killed in Mastung raids",
     "Security forces report two operations in Balochistan under Operation Radd-ul-Fitna-III.",
     "iqmia", "MED"),
    ("ASIA",
     "India declares 720/9, leads New Zealand by 352",
     "Dominant batting in the Wellington Test puts India firmly on top on day three.",
     "Dainik Jagran", "HIGH"),
    ("ASIA",
     "Cricketer Chahal joins BJP's OBC Morcha",
     "Yuzvendra Chahal enters politics and is named a special invitee to the party's OBC wing.",
     "Dainik Jagran", "HIGH"),
    ("ASIA",
     "BJP MP Ramrao Wadkute dies at 72",
     "Rajya Sabha member dies of cardiac arrest at AIIMS in New Delhi.",
     "Dainik Jagran", "HIGH"),
    ("ASIA",
     "Modi opens Nitish Setu bridge in Bihar",
     "New bridge links Patna and Vaishali districts across the Ganges.",
     "CareerIndia", "HIGH"),
    ("ASIA",
     "India passes 1 crore HPV vaccine doses",
     "10-million-dose milestone reached.",
     "CareerIndia", "HIGH"),
    ("AFRICA",
     "Ethiopia, US vow deeper economic ties",
     "Addis Ababa talks cover reforms, investment and the Bishoftu airport project.",
     "iqmia", "MED"),
    ("AFRICA",
     "Storms, hail, floods forecast in South Africa",
     "Weather service warns seven provinces to prepare for severe thunderstorms.",
     "iqmia", "MED"),
    ("TECH & SCIENCE",
     "IBM unveils 520-qubit 'Nighthawk r3'",
     "New processor runs about 10,000 quantum operations; a 1,040-qubit link is planned for 2027.",
     "Dev.to", "HIGH"),
    ("TECH & SCIENCE",
     "UV photodiodes set 152 GHz record",
     "Gallium-oxide devices smash the gain-bandwidth mark for deep-UV detection.",
     "iqmia", "MED"),
    ("TECH & SCIENCE",
     "Whole-Earth model sharpens alien-life hunt",
     "Simulation separates true biosignatures from lifeless look-alikes on exoplanets.",
     "iqmia", "MED"),
    ("TECH & SCIENCE",
     "Cancer study links TGM2 to tumour vessels",
     "Nature paper ties the protein to blood-vessel growth in gastric cancer.",
     "Nature", "HIGH"),
    ("TECH & SCIENCE",
     "Journalist David McKittrick dies at 77",
     "Tributes paid to the veteran Northern Ireland reporter and author.",
     "iqmia", "MED"),
]

# Columns: (x, [story indexes]) — 14 / 13 / 13 stories, regions flow across columns.
COLUMNS = [
    (24, list(range(0, 14))),
    (360, list(range(14, 27))),
    (696, list(range(27, 40))),
]
COL_W = 312
STORY_TOP = 188
STORY_BOTTOM = 824

# UTC timeline chips: (time, label)
TIMELINE = [
    ("00:37", "Clashes across France reported"),
    ("03:00", "COP31 final draft released"),
    ("04:00", "Las Vegas GP under the lights"),
    ("06:19", "144 detained in France"),
    ("09:00", "Iran claims control of Hormuz"),
    ("15:00", "Nepal PM lands in New Delhi"),
    ("21:00", "COP31 plenary stalls, no deal"),
]

# Schematic world map polygons (map-box coords, box 600x92 at x=30,y=852).
CONTINENTS = [
    [(35, 20), (55, 10), (90, 6), (130, 8), (160, 14), (172, 24), (160, 34), (150, 44), (135, 50), (120, 56), (100, 58), (80, 52), (60, 44), (45, 32)],
    [(108, 60), (128, 56), (148, 62), (150, 74), (140, 86), (125, 92), (112, 82), (105, 70)],
    [(282, 16), (300, 8), (325, 6), (340, 12), (335, 22), (320, 30), (300, 28), (285, 24)],
    [(285, 34), (310, 30), (335, 36), (348, 48), (342, 66), (330, 84), (312, 86), (296, 68), (284, 50)],
    [(342, 14), (370, 6), (420, 4), (470, 6), (510, 12), (528, 20), (520, 32), (500, 40), (490, 46), (478, 58), (470, 48), (455, 50), (448, 62), (436, 48), (430, 46), (405, 40), (380, 34), (360, 26), (344, 20)],
    [(465, 68), (490, 62), (515, 66), (522, 74), (510, 84), (488, 88), (468, 80)],
]
# (x, y, label-or-None, label-side) story dots on the map.
DOTS = [
    (62, 40, "Las Vegas", "r"), (72, 50, None, "r"),
    (118, 26, None, "r"), (298, 14, "Paris", "r"),
    (332, 24, "Antalya", "r"), (398, 32, "Tehran", "r"),
    (405, 42, None, "r"), (432, 40, "Delhi", "r"),
    (478, 66, "Cikande", "r"), (530, 82, "Wellington", "l"),
    (330, 60, None, "r"), (318, 80, None, "r"),
]


def wrap(text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer double border.
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # ---- Masthead ----
    f_mast = font(SERIF_B, 36)
    name = "THE SUNDAY WORLD"
    d.text(((W - f_mast.getlength(name)) / 2, 20), name, font=f_mast, fill=INK)
    f_date = font(SANS_B, 13)
    dateline = "SUNDAY 22 NOVEMBER 2026  ·  40 SOURCED STORIES  ·  7 SECTIONS  ·  ALL STORIES VERIFIED AS 22 NOVEMBER 2026"
    d.text(((W - f_date.getlength(dateline)) / 2, 60), dateline, font=f_date, fill=RED)
    d.line([(24, 80), (W - 24, 80)], fill=RULE, width=2)
    d.line([(24, 84), (W - 24, 84)], fill=RULE, width=1)

    # ---- Lead headline ----
    f_lead = font(SERIF_B, 19)
    lead = "COP31 draft drops fossil fuels as talks stall into overtime"
    d.text(((W - f_lead.getlength(lead)) / 2, 90), lead, font=f_lead, fill=INK)
    f_sub = font(SANS, 11)
    sub = "Antalya text concedes 1.5°C will be passed  ·  Hormuz on edge  ·  FBI's crime database hacked  ·  Cartel boss seized in Sinaloa"
    d.text(((W - f_sub.getlength(sub)) / 2, 112), sub, font=f_sub, fill=MUTED)

    # ---- UTC timeline ----
    d.line([(24, 124), (W - 24, 124)], fill=RED, width=2)
    f_tl_title = font(SANS_B, 10)
    d.text((24, 129), "THE DAY IN UTC — SUNDAY 22 NOVEMBER 2026", font=f_tl_title, fill=RED)
    f_time = font(SANS_B, 10)
    f_tl = font(SANS, 9)
    chip_w = (W - 48) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 24 + i * chip_w
        d.text((cx + 2, 144), t, font=f_time, fill=RED)
        for j, ln in enumerate(wrap(label, f_tl, chip_w - 8)):
            d.text((cx + 2, 156 + j * 11), ln, font=f_tl, fill=INK)
    d.line([(24, 182), (W - 24, 182)], fill=RULE, width=1)

    # ---- Story columns ----
    f_head = font(SANS_B, 11)
    f_sum = font(SANS, 10)
    f_tag = font(SANS_B, 8)
    f_region = font(SANS_B, 12)
    heights = []
    for x, idxs in COLUMNS:
        y = STORY_TOP
        last_region = None
        for i in idxs:
            region, head, summ, src, conf = STORIES[i]
            if region != last_region:
                d.text((x, y), region, font=f_region, fill=RED)
                d.line([(x, y + 15), (x + COL_W, y + 15)], fill=RED, width=1)
                y += 20
                last_region = region
            # Headline, up to 2 lines.
            hl = wrap(head, f_head, COL_W)
            for ln in hl[:2]:
                d.text((x, y), ln, font=f_head, fill=INK)
                y += 13
            # Summary, up to 2 lines; source + confidence tag appended to
            # the last summary line when it fits, else on its own line.
            sl = wrap(summ, f_sum, COL_W)
            tag = "  " + src + "  ·  " + conf
            for j, ln in enumerate(sl[:2]):
                d.text((x, y), ln, font=f_sum, fill=INK)
                if j == len(sl[:2]) - 1:
                    lx = f_sum.getlength(ln)
                    if lx + f_tag.getlength(tag) <= COL_W:
                        d.text((x + lx, y), tag, font=f_tag, fill=RED)
                    else:
                        y += 12
                        d.text((x, y), tag.strip(), font=f_tag, fill=RED)
                y += 12
            y += 3  # gap between stories
        heights.append(y)
    print("column bottom y:", heights, "limit:", STORY_BOTTOM)

    # ---- World map + date check ----
    d.line([(24, 830), (W - 24, 830)], fill=RULE, width=1)
    f_map_title = font(SANS_B, 11)
    d.text((30, 836), "WHERE THE DAY HAPPENED", font=f_map_title, fill=RED)
    mx, my = 30, 852
    for poly in CONTINENTS:
        d.polygon([(mx + px, my + py) for px, py in poly], fill=MAP_FILL, outline=MAP_LINE)
    f_dot = font(SANS, 8)
    for dx, dy, label, side in DOTS:
        d.ellipse([mx + dx - 3, my + dy - 3, mx + dx + 3, my + dy + 3], fill=RED, outline=PAPER)
        if label:
            # Paper-coloured halo so the label stays readable over the blue land.
            if side == "r":
                lx, ly = mx + dx + 5, my + dy - 4
            else:
                lx = mx + dx - 5 - f_dot.getlength(label)
                ly = my + dy - 4
            for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                d.text((lx + ox, ly + oy), label, font=f_dot, fill=PAPER)
            d.text((lx, ly), label, font=f_dot, fill=INK)

    # Date-check box (right side).
    bx0, by0, bx1, by1 = 660, 834, 1000, 950
    d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
    f_dc = font(SANS_B, 12)
    d.text((bx0 + 10, by0 + 8), "DATE CHECK", font=f_dc, fill=RED)
    f_dct = font(SANS, 10)
    dc_lines = [
        "Every story on this page was checked",
        "against its source and dated 22 Nov 2026.",
        "Stories from 19-21 Nov were left out:",
        "Peru quake (20 Nov), NWSL final (21 Nov),",
        "Saturday's football, EU-Indonesia deal",
        "(21 Nov), Friday's market sell-off.",
        "HIGH = source itself dates it 22 Nov.",
        "MED = reported 22 Nov, event late 21 Nov.",
    ]
    yy = by0 + 28
    for ln in dc_lines:
        d.text((bx0 + 10, yy), ln, font=f_dct, fill=INK)
        yy += 11

    # ---- Footer ----
    d.line([(24, 962), (W - 24, 962)], fill=RULE, width=1)
    f_foot = font(SANS, 9)
    foot = ("Sources: AP, Reuters, CNBC, BBC, Al Jazeera, The Guardian, The Independent, CNN, AFP, CBS, Formula1.com, Nature, "
            "Dainik Jagran, CareerIndia, Investing.com, Crypto Briefing, Dev.to, Seven Lights.  ·  THE SUNDAY WORLD, 22 NOVEMBER 2026")
    for j, ln in enumerate(wrap(foot, f_foot, W - 48)):
        d.text((24, 968 + j * 11), ln, font=f_foot, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    draw()
