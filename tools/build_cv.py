# -*- coding: utf-8 -*-
"""Erzeugt den Lebenslauf als zweispaltiges PDF (Seitenleiste + Hauptspalte).

Layout nach Vorlage: blaues Kopfband mit Namen, graue Seitenleiste mit Foto,
Kontakt, Kompetenzen, Sprachen und Staerken; rechts Profil, Erfahrung,
Ausbildung, Projekte und Zertifikate.

Bewusst ausgelassen: Anschrift, Geburtsdatum, Matrikelnummer, Telefonnummer.
Aufruf:  python tools/build_cv.py
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, KeepTogether, CondPageBreak, NextPageTemplate)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Lebenslauf_Moritz_Staat.pdf")
PHOTO = os.path.join(ROOT, "images", "portrait-cv.jpg")

PW, PH = A4

# ── Farben ────────────────────────────────────────────────────────────────
BLUE = colors.HexColor("#2f5f7c")   # Kopfband und Ueberschriften
BLUE_L = colors.HexColor("#7ba3bd")  # duenne Trennlinie
SIDE = colors.HexColor("#e8e9ea")   # Seitenleiste
INK = colors.HexColor("#333333")
MUTED = colors.HexColor("#5f5f5f")
RULE = colors.HexColor("#d0d2d4")

# ── Geometrie ─────────────────────────────────────────────────────────────
SIDE_W = 200          # Breite der Seitenleiste
BAND_H = 96           # Hoehe des Kopfbands, Seite 1
BAND_H2 = 46          # Hoehe des Kopfbands, Folgeseiten
PAD = 20              # Innenabstand der Seitenleiste
MAIN_X = SIDE_W + 30
MAIN_W = PW - MAIN_X - 34
BOTTOM = 34

PHOTO_X = PAD
PHOTO_W = SIDE_W - 2 * PAD
PHOTO_H = PHOTO_W * 5 / 4
PHOTO_TOP = PH - 24                      # ragt in das Kopfband hinein
SIDE_START = PHOTO_TOP - PHOTO_H - 30    # hier beginnt der Text der Seitenleiste

# ── Absatzstile ───────────────────────────────────────────────────────────
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=8.3, leading=11.8,
                      textColor=INK)
LEDE = ParagraphStyle("lede", parent=BODY, fontSize=8.5, leading=12.8, textColor=MUTED)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=12.5,
                    textColor=BLUE, spaceAfter=5)
ROLE = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=8.9, leading=11.8,
                      textColor=INK)
ORG = ParagraphStyle("org", fontName="Helvetica-Bold", fontSize=8.9, leading=11.8,
                     textColor=MUTED, spaceAfter=2)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=10, bulletIndent=1,
                        spaceAfter=2.0)
NOTE = ParagraphStyle("note", parent=BODY, fontSize=7.7, leading=10.6, textColor=MUTED)

# Stile der Seitenleiste
S_H2 = ParagraphStyle("sh2", fontName="Helvetica-Bold", fontSize=10.5, leading=12,
                      textColor=BLUE)
S_KEY = ParagraphStyle("skey", fontName="Helvetica-Bold", fontSize=8.2, leading=11,
                       textColor=INK)
S_VAL = ParagraphStyle("sval", fontName="Helvetica", fontSize=7.9, leading=10.8,
                       textColor=MUTED)


# ══════════════════════════════════════════════════════════════════════════
#  Inhalt der Seitenleiste
# ══════════════════════════════════════════════════════════════════════════
KONTAKT = [
    "moritz@moritz-staat.de",
    "www.moritz-staat.de",
    "github.com/Moritz-Staat",
    "linkedin.com/in/moritz-staat-848192215",
    "Dortmund, Nordrhein-Westfalen",
]

KOMPETENZEN = [
    ("Business Intelligence", "KPI-Frameworks, Datenmodellierung, Metric Layer, Reporting-Logik"),
    ("KI- und LLM-Integration", "Interne KI-Plattformen, lokale Modelle, Governance"),
    ("Prozessautomatisierung", "n8n-Workflows, Systemintegration, Dokumentenmanagement"),
    ("CRM &amp; Procurement", "HubSpot, SAP Ariba, Stammdaten- und Prozessdesign"),
    ("Entwicklung", "TypeScript, Python, SQL, R, Docker, Git"),
]

SPRACHEN = [
    ("Deutsch", "Muttersprache"),
    ("Englisch", "zwei englischsprachige Mastermodule"),
]

STAERKEN = [
    ("Eigenverantwortung",
     "Projektf&uuml;hrung und Messeverantwortung schon als Werkstudent"),
    ("Umsetzung statt Konzept",
     "Baut selbst, was er konzipiert &ndash; vom Datenmodell bis zur Infrastruktur"),
    ("Methodische Sorgfalt",
     "Misst nach, statt zu sch&auml;tzen"),
]


# ══════════════════════════════════════════════════════════════════════════
#  Seitenhintergrund
# ══════════════════════════════════════════════════════════════════════════
def draw_name(c, band_h, size):
    """Name gesperrt setzen. setCharSpace gibt es nur am Textobjekt, nicht am Canvas,
    deshalb wird die Breite von Hand berechnet und rechtsbuendig positioniert."""
    text = "MORITZ STAAT"
    gap = size * 0.075
    width = c.stringWidth(text, "Helvetica-Bold", size) + gap * (len(text) - 1)
    to = c.beginText(PW - 34 - width, PH - band_h / 2 - size * 0.34)
    to.setFont("Helvetica-Bold", size)
    to.setCharSpace(gap)
    to.setFillColor(colors.white)
    to.textOut(text)
    to.setCharSpace(0)   # Tc wirkt im Content-Stream fort - sonst ist die ganze Seite gesperrt
    c.drawText(to)


def draw_side_text(c):
    """Seitenleiste von Hand setzen: fester Inhalt, exakte Kontrolle ueber die Position."""
    y = SIDE_START
    x = PAD
    w = SIDE_W - 2 * PAD

    def heading(title, y):
        p = Paragraph(title, S_H2)
        _, h = p.wrapOn(c, w, 40)
        p.drawOn(c, x, y - h)
        y -= h + 5
        c.setStrokeColor(BLUE_L)
        c.setLineWidth(0.8)
        c.line(x, y, x + w, y)
        return y - 11

    def para(text, style, y, gap=3.5):
        p = Paragraph(text, style)
        _, h = p.wrapOn(c, w, 200)
        p.drawOn(c, x, y - h)
        return y - h - gap

    y = heading("KONTAKT", y)
    for line in KONTAKT:
        c.setFillColor(BLUE)
        c.circle(x + 2.2, y - 3.4, 1.7, fill=1, stroke=0)
        p = Paragraph(line, S_VAL)
        _, h = p.wrapOn(c, w - 10, 60)
        p.drawOn(c, x + 10, y - h)
        y -= h + 4.5

    y = heading("KOMPETENZEN", y - 12)
    for key, val in KOMPETENZEN:
        y = para(key, S_KEY, y, gap=1)
        y = para(val, S_VAL, y, gap=7)

    y = heading("SPRACHEN", y - 5)
    for key, val in SPRACHEN:
        y = para(f"<b>{key}</b> &ndash; {val}", S_VAL, y, gap=5)

    y = heading("STÄRKEN", y - 5)
    for key, val in STAERKEN:
        y = para(key, S_KEY, y, gap=1)
        y = para(val, S_VAL, y, gap=7)


def page_first(c, doc):
    c.saveState()
    c.setFillColor(SIDE)
    c.rect(0, 0, SIDE_W, PH - BAND_H, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.rect(0, PH - BAND_H, PW, BAND_H, stroke=0, fill=1)
    c.setStrokeColor(BLUE_L)
    c.setLineWidth(1.2)
    c.line(SIDE_W + 30, PH - BAND_H - 7, PW - 34, PH - BAND_H - 7)
    draw_name(c, BAND_H, 25)
    if os.path.exists(PHOTO):
        c.drawImage(ImageReader(PHOTO), PHOTO_X, PHOTO_TOP - PHOTO_H,
                    width=PHOTO_W, height=PHOTO_H, mask=None)
    draw_side_text(c)
    footer(c)
    c.restoreState()


def page_later(c, doc):
    c.saveState()
    c.setFillColor(SIDE)
    c.rect(0, 0, SIDE_W, PH - BAND_H2, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.rect(0, PH - BAND_H2, PW, BAND_H2, stroke=0, fill=1)
    draw_name(c, BAND_H2, 14)
    footer(c)
    c.restoreState()


def footer(c):
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawRightString(PW - 34, 18, f"Seite {c.getPageNumber()}")


# ══════════════════════════════════════════════════════════════════════════
#  Hauptspalte
# ══════════════════════════════════════════════════════════════════════════
def section(title, first=None):
    head = [Spacer(1, 7), CondPageBreak(46), Paragraph(title, H2)]
    return head if first is None else head + list(first)


def entry(role, org, period, bullets, note=None):
    """Kopf und erster Stichpunkt bleiben zusammen, der Rest darf umbrechen."""
    head = [Paragraph(role, ROLE),
            Paragraph(f"{org} &nbsp;&middot;&nbsp; {period}", ORG)]
    rest = []
    for i, b in enumerate(bullets):
        (head if i == 0 else rest).append(Paragraph(b, BULLET, bulletText="•"))
    if note:
        rest += [Spacer(1, 1), Paragraph(note, NOTE)]
    rest.append(Spacer(1, 6))
    return [KeepTogether(head)] + rest


def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MAIN_X, rightMargin=34, topMargin=BAND_H + 26, bottomMargin=BOTTOM,
        title="Lebenslauf – Moritz Staat", author="Moritz Staat",
        subject="Lebenslauf", creator="moritz-staat.de")

    f1 = Frame(MAIN_X, BOTTOM, MAIN_W, PH - BAND_H - 26 - BOTTOM, id="first",
               leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f2 = Frame(MAIN_X, BOTTOM, MAIN_W, PH - BAND_H2 - 24 - BOTTOM, id="later",
               leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[f1], onPage=page_first),
        PageTemplate(id="later", frames=[f2], onPage=page_later),
    ])

    # Ab Seite 2 gilt das schmale Kopfband ohne Foto.
    S = [NextPageTemplate("later")]

    # ── Profil ────────────────────────────────────────────────────────────
    S += section("MEIN PROFIL")
    S.append(Paragraph(
        "Wirtschaftswissenschaftler, der Digitalisierung nicht nur konzipiert, sondern selbst "
        "baut. Drei Jahre Praxis in einem mittelst&auml;ndischen Industrieunternehmen &ndash; vom "
        "CRM- und BI-Aufbau bis zur internen KI-Plattform &ndash; dazu Gr&uuml;ndungserfahrung mit "
        "einer eigenen KI-App und ein produktives Automatisierungssystem im Immobilienbereich. "
        "Schwerpunkte: Business Intelligence, KI-Integration und Prozessautomatisierung.", LEDE))

    # ── Erfahrung ─────────────────────────────────────────────────────────
    S += section("ERFAHRUNG", entry(
        "Werkstudent IT, Vertrieb &amp; Marketing",
        "W&amp;S Technik GmbH, Castrop-Rauxel", "M&auml;rz 2023 &ndash; heute",
        [
            "<b>Business Intelligence:</b> Aufbau der ersten BI-Metriken und eines KPI-Frameworks &ndash; "
            "Datenmodellierung, konsistente Kennzahlendefinitionen (Single Source of Truth) und "
            "Reporting-Logik f&uuml;r Priorisierung, Kapazit&auml;ten, Qualit&auml;t und Durchlaufzeiten.",
            "<b>WUSGPT &ndash; interne KI-Plattform:</b> Konzeption und Einf&uuml;hrung einer LLM-Plattform "
            "f&uuml;rs B&uuml;ro (Open WebUI + ChatGPT API) inklusive Governance: Rollen- und "
            "Use-Case-Definition, Prompt-Standards, Umgang mit sensiblen Daten.",
            "<b>CRM-Aufbau:</b> Pipeline- und Stage-Struktur, Datenmodell und Felderlogik, "
            "Stammdatenqualit&auml;t sowie Vertriebs- und Follow-up-Prozesse.",
            "<b>SAP Ariba:</b> Procurement-Integration, Prozessabbildung, Stammdaten- und "
            "Artikelstrukturen.",
            "<b>Standmeister InnoTrans 2024 und 2026, Berlin:</b> Verantwortung f&uuml;r den "
            "Messeauftritt auf der weltgr&ouml;&szlig;ten Verkehrstechnikmesse; selbst entwickelter "
            "Quiz-Preisautomat als Besuchermagnet.",
            "Digitales Schulungsmanagement mit eigenem Auswertungstool sowie "
            "Home-Assistant-Automatisierung im Office.",
        ]))

    S += entry(
        "Co-Founder", "SparMahl", "Juni 2023 &ndash; Dezember 2025",
        [
            "KI-gest&uuml;tzte Mobile App, die Supermarktangebote gegen Rezeptdaten abglich und daraus "
            "personalisierte Einkaufs- und Essensvorschl&auml;ge ableitete &ndash; bis zum Release im App Store.",
            "Verantwortlich f&uuml;r Positionierung, Go-to-Market und Nutzerforschung; aus den "
            "Interviews entstanden die MVP-Iterationen.",
            "Mitarbeit an der LLM-gest&uuml;tzten Produktklassifikation: Vektorraum &uuml;ber rund 25.000 "
            "Produkte, k-Nearest-Neighbor-Retrieval, Kategorieentscheidung durch das Sprachmodell.",
            "EXIST-F&ouml;rderantrag mit ausgearbeitet, Recruiting und Einstellung von "
            "Praktikant:innen (UI/UX), &Ouml;ffentlichkeitsarbeit inklusive Medienbeitrag im KURT Magazin.",
        ],
        note="Gef&ouml;rdert durch das Gr&uuml;ndungsstipendium.NRW, begleitet vom Centrum f&uuml;r "
             "Entrepreneurship &amp; Transfer der TU Dortmund. Das Vorhaben wird nicht weitergef&uuml;hrt.")

    S += entry(
        "KI-Automatisierung Immobilienverwaltung",
        "eigenverantwortlich, mehrere Wohngeb&auml;ude in Dortmund", "2025 &ndash; heute",
        [
            "Vollst&auml;ndig selbst gehostetes System: Mieterkommunikation &uuml;ber FreeScout-Helpdesk "
            "mit wohnungsbezogenen Custom Fields, Analyse und Antwortvorschl&auml;ge &uuml;ber lokal "
            "betriebene Sprachmodelle.",
            "Automatische Ticket-Kategorisierung und Priorisierung von Schadensmeldungen; "
            "Dokumentenmanagement mit Paperless-ngx, n8n-Webhook archiviert geschlossene Tickets.",
            "<b>Ergebnis:</b> rund 80&nbsp;% der Mieteranfragen werden automatisch klassifiziert und "
            "beantwortet; die Nebenkostenabrechnung sank von drei Tagen auf vier Stunden.",
        ])

    S += entry("Praktikant", "K&ouml;nigswege GmbH", "April 2022 &ndash; August 2022",
               ["Kaufm&auml;nnische Unterst&uuml;tzung mit Schwerpunkt Microsoft Office."])

    # ── Ausbildung ────────────────────────────────────────────────────────
    S += section("AUSBILDUNG", entry(
        "M.Sc. Wirtschaftswissenschaft &ndash; Digitalisierungsmanagement",
        "FernUniversit&auml;t in Hagen", "2024 &ndash; laufend",
        [
            "Technische Module: Entwurf und Implementierung von Informationssystemen "
            "(C-Programmierung, Algorithmen und Datenstrukturen, objektorientierter Systementwurf), "
            "Business Intelligence mit Auswertung in R, Vertiefung der Wirtschaftsmathematik und Statistik.",
            "Wirtschaftliche Module: Informationsmanagement, Digitale Transformation, Digital "
            "Entrepreneurship, Socio-Technical Information Systems Design, K&auml;uferverhalten.",
            "Pflichtseminar &bdquo;Angewandtes digitales Entrepreneurship in der Gesundheitswirtschaft&ldquo; "
            "bei Prof. Dr. Till Winkler: Gesch&auml;ftsidee <i>mycycle</i> prototypisch umgesetzt, im Juni 2026 "
            "beim <i>Digital Health on Campus</i> in Hamburg vorgestellt und im Juli m&uuml;ndlich verteidigt.",
            "Masterarbeit im Wintersemester 2026/27.",
        ]))

    S += entry(
        "B.Sc. Wirtschaftswissenschaften", "Technische Universit&auml;t Dortmund",
        "Oktober 2019 &ndash; M&auml;rz 2024",
        [
            "Schwerpunkt Technologiemanagement und Marketing; parallel Gr&uuml;ndung von SparMahl.",
            "Bachelorarbeit am Lehrstuhl f&uuml;r Wirtschaftsinformatik: &bdquo;Self-Service-Technologie im "
            "Retail-Shopping&ldquo; &ndash; Erweiterung des Technology Acceptance Model um wahrgenommene "
            "Kontrolle, Performance- und Datenrisiko sowie Trusting Beliefs.",
            "Feldbefragung am Point of Sale, Sch&auml;tzung des Strukturgleichungsmodells mit PLS-SEM "
            "inklusive Messmodell- und Strukturmodellevaluation, Diskriminanzvalidit&auml;t, "
            "Bootstrapping und Effektst&auml;rken.",
        ])

    S += entry("Abitur", "Georg-B&uuml;chner-Gymnasium, Frankfurt am Main",
               "2011 &ndash; 2019",
               ["Note 1,9; Schwerpunkte Mathematik sowie Politik und Wirtschaft."])

    # ── Projekte ──────────────────────────────────────────────────────────
    S += section("AUSGEWÄHLTE PROJEKTE", entry(
        "Lokale LLM-Inferenz und eigenes Benchmark-System",
        "privat, Repository <i>ki-benchmarks</i>", "2026",
        [
            "Quantisierte 27B-Dense- und 35B-A3B-MoE-Modelle unter llama.cpp auf 16&nbsp;GB VRAM &ndash; "
            "schichtweiser CPU-Offload, selektive Auslagerung der Expertengewichte und "
            "Multi-Token-Prediction als spekulative Dekodierung, die den Durchsatz bei 28k Kontext verdoppelt.",
            "Eigenes Telemetriesystem in Python: 1-Hz-Sampling &uuml;ber NVML, psutil und "
            "Windows-Leistungsindikatoren, Hardwaremetriken und Benchmarkergebnisse in einem "
            "gemeinsamen SQLite-Schema, Auswertung &uuml;ber ein FastAPI-Dashboard; 45 automatisierte Tests.",
        ]))

    S += entry(
        "Quiz-Preisautomat f&uuml;r den Messeeinsatz",
        "W&amp;S Technik GmbH, Repository <i>Snackautomat</i>", "2024, &uuml;berarbeitet 2026",
        [
            "Touch-Kiosk in TypeScript, per Vite zu rein statischem HTML/CSS/JS gebaut &ndash; ohne "
            "Server, Datenbank oder Internetverbindung, da Messe-WLAN keine Betriebsgrundlage ist.",
            "Drei Schwierigkeitsgrade auf gemeinsamer Quiz-Engine, Quizlaufzeit in eigenem iFrame "
            "mit origin-gepr&uuml;fter postMessage-Kommunikation; Preisausgabe &uuml;ber Relais eines "
            "Microcontrollers, ausfalltolerant ausgelegt.",
        ])

    # ── Zertifikate ───────────────────────────────────────────────────────
    S += section("ZERTIFIKATE & FÖRDERUNG")
    S.append(Paragraph(
        "<b>2026</b> &nbsp; Mendix Rapid Developer Certification &ndash; Low-Code-Entwicklung "
        "(Nachweis-ID 109843)", BODY))
    S.append(Spacer(1, 3))
    S.append(Paragraph(
        "<b>2023</b> &nbsp; Gr&uuml;ndungsstipendium.NRW &ndash; Landesf&ouml;rderung f&uuml;r das "
        "Gr&uuml;ndungsvorhaben SparMahl", BODY))

    doc.build(S)
    print("geschrieben:", OUT)


if __name__ == "__main__":
    build()
