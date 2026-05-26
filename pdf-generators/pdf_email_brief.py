"""
Crystaland Numerology System
6-Page Free Report Generator
Returns raw PDF bytes via generate_free_report(data).
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from io import BytesIO

# Brand Colors
DARK_BG    = HexColor('#08080f')
GOLD       = HexColor('#c9a96e')
CREAM      = HexColor('#f5f0e8')
SOFT_WHITE = HexColor('#e8e0d0')
MID_GRAY   = HexColor('#7a7068')

W, H = letter  # 612 x 792 pts

# Number Meanings
LIFE_PATH = {
    1:  {"title": "The Pioneer",        "essence": "You came here to lead. Your soul carries the blueprint of the self-starter — someone meant to forge new paths, act on instinct, and stand in the full power of original thought. Life Path 1 is the number of initiation. Where others wait for permission, you are meant to move first.", "gift": "Courage, independence, and an unshakeable drive to create something from nothing.", "shadow": "The shadow of 1 is ego rigidity — the fear that needing others means weakness. Your growth lives in learning that collaboration does not dilute your power; it amplifies it.", "affirmation": "I lead with integrity. My originality is my gift to the world."},
    2:  {"title": "The Peacemaker",     "essence": "You are here to build bridges. Your soul came in tuned to the frequency of harmony, partnership, and deep emotional intelligence. Life Path 2 is the number of the diplomat — you sense what others need before they say it, and your presence has a quiet power that brings rooms into alignment.", "gift": "Empathy, intuition, and the rare ability to make every person feel genuinely seen.", "shadow": "The shadow of 2 is self-erasure — giving so completely that you lose the thread back to yourself. Your evolution lives in learning that your needs are not a burden; they are sacred.", "affirmation": "I am worthy of the love I so freely give to others."},
    3:  {"title": "The Creator",        "essence": "You are here to express. Life Path 3 is the vibration of the artist, the storyteller, the one whose words and presence light up a room. You carry joy as a spiritual practice — and when you allow yourself to fully inhabit your creative voice, you give others permission to do the same.", "gift": "Radiant creativity, natural charisma, and a gift for turning emotion into art, words, or beauty.", "shadow": "The shadow of 3 is scattered energy and self-doubt masked as perfectionism. Your work does not need to be perfect — it needs to be real.", "affirmation": "My voice matters. My creative expression is a healing force."},
    4:  {"title": "The Architect",      "essence": "You are here to build. Life Path 4 carries the frequency of structure, discipline, and mastery. You understand instinctively that lasting things are built slowly, with intention and precision. You are the one who turns visions into reality — the foundation beneath every dream.", "gift": "Reliability, strategic thinking, and an extraordinary capacity for focused, disciplined effort.", "shadow": "The shadow of 4 is rigidity — mistaking the plan for the destination. Growth comes when you let life surprise you within the structure you have built.", "affirmation": "I build with purpose. My steadiness is my superpower."},
    5:  {"title": "The Adventurer",     "essence": "You are here to experience. Life Path 5 is the vibration of freedom, curiosity, and the relentless pursuit of aliveness. You learn through living — through travel, risk, connection, and the willingness to begin again. The world is your classroom.", "gift": "Adaptability, magnetism, and a gift for inspiring others to break free from limitation.", "shadow": "The shadow of 5 is restlessness that keeps you moving before you have absorbed what each experience had to teach. Freedom is not found by running — it is found within.", "affirmation": "I embrace change as my greatest teacher. I am free."},
    6:  {"title": "The Nurturer",       "essence": "You are here to love. Life Path 6 carries the vibration of responsibility, beauty, and deep care for others. You hold the world together in ways that often go unseen. Your sense of duty is sacred — and when expressed from wholeness rather than obligation, it becomes one of the most powerful forces on earth.", "gift": "Unconditional love, an eye for beauty, and the ability to create sanctuary wherever you go.", "shadow": "The shadow of 6 is martyrdom — giving from depletion and then resenting those you serve. You cannot pour from an empty vessel. Caring for yourself is the foundation.", "affirmation": "I love deeply and I receive love fully. I am worthy of my own devotion."},
    7:  {"title": "The Mystic",         "essence": "You are here to seek truth. Life Path 7 is the vibration of the philosopher, the researcher, the one who cannot rest until they understand the deeper pattern beneath the surface of things. Your inner world is vast, and your greatest gift to others is the depth of your knowing.", "gift": "Profound intellect, spiritual sensitivity, and an almost uncanny ability to perceive what is hidden.", "shadow": "The shadow of 7 is isolation — retreating so deeply into the mind that the heart goes cold. Your wisdom only becomes medicine when you share it.", "affirmation": "I trust my inner knowing. I share my depth with those who are ready."},
    8:  {"title": "The Powerhouse",     "essence": "You are here to master the material world. Life Path 8 carries the vibration of abundance, authority, and the understanding that power wielded with integrity is a form of spiritual mastery. You are meant to build empires — of influence, of wealth, of impact.", "gift": "Natural leadership, business acumen, and a magnetic authority that draws resources and people toward your vision.", "shadow": "The shadow of 8 is control — the fear that if you let go, everything will fall apart. True power is not grip; it is trust.", "affirmation": "I am a vessel for abundance. I lead with integrity and receive with grace."},
    9:  {"title": "The Sage",           "essence": "You are here to serve the whole. Life Path 9 is the vibration of the humanitarian — the one who has lived many cycles and now carries the distilled wisdom of all of them. You feel others pain as your own, and your deepest fulfillment comes from contributing to something larger than yourself.", "gift": "Compassion, wisdom, and the rare capacity to love without condition or attachment.", "shadow": "The shadow of 9 is difficulty releasing — people, eras, identities that have run their course. Your evolution comes through learning that endings are the gateway to what is next.", "affirmation": "I release what no longer serves. I trust the wisdom of every ending."},
    11: {"title": "The Illuminator",    "essence": "You carry a master vibration. Life Path 11 is the number of the spiritual messenger — highly intuitive, deeply sensitive, here to inspire and illuminate. You often feel the weight of not quite fitting in the ordinary world. That is because you are not ordinary. You are a bridge between the seen and unseen.", "gift": "Extraordinary intuition, visionary insight, and the ability to transmit spiritual truth through art, words, or presence.", "shadow": "The shadow of 11 is nervous energy and self-doubt — the gap between what you sense you are meant to do and the courage to actually do it. The world needs what you carry.", "affirmation": "I trust my visions. I was born to shine a light others have never seen."},
    22: {"title": "The Master Builder", "essence": "You carry one of the most powerful vibrations in numerology. Life Path 22 is the Master Builder — capable of turning the most ambitious spiritual vision into tangible, lasting form in the physical world. Your potential is immense and your responsibility is equally great.", "gift": "Strategic brilliance, unwavering endurance, and the rare ability to build systems that serve thousands.", "shadow": "The shadow of 22 is feeling the weight of your own potential — the paralysis of knowing you are capable of so much. Start. The vision will refine itself in motion.", "affirmation": "I build for legacy. My vision serves the world."},
    33: {"title": "The Master Teacher", "essence": "You carry the rarest master vibration in numerology. Life Path 33 is the Master Teacher — a being whose very presence is an invitation for others to rise. You did not come here for a small life. You came here to love at scale, to teach through example, and to hold space for collective transformation.", "gift": "Boundless compassion, healing presence, and the ability to see the highest potential in every person.", "shadow": "The shadow of 33 is self-sacrifice — giving so completely that you neglect your own sacred vessel. You cannot teach wholeness from a place of depletion.", "affirmation": "I embody the love I teach. My wholeness is my offering."},
}

EXPRESSION = {
    1: "You are here to create — to originate, to lead, and to stand behind your ideas with conviction. Your destiny is one of self-determination.",
    2: "Your destiny is to bridge, to harmonize, and to create environments where others feel safe to be fully themselves. You are a natural diplomat.",
    3: "Your destiny is to express — to bring joy, beauty, and creative vision into the world. You are meant to communicate in ways that move people.",
    4: "Your destiny is to build — to create the systems, structures, and foundations that give others a solid ground to stand on.",
    5: "Your destiny is to catalyze change — to move through the world with freedom, adaptability, and an infectious enthusiasm for what is possible.",
    6: "Your destiny is to love and to serve — to create beauty, nurture community, and hold the heart of every space you inhabit.",
    7: "Your destiny is to seek and to teach — to go deep into the mystery of life and return with wisdom that lights the way for others.",
    8: "Your destiny is to master power — to build influence, create abundance, and demonstrate that integrity and success are not opposites.",
    9: "Your destiny is to uplift the whole — to pour your wisdom, compassion, and creative force into service of something larger than yourself.",
    11: "Your destiny is to inspire — to carry spiritual light into ordinary spaces and awaken what is highest in those around you.",
    22: "Your destiny is to build at scale — to take visionary ideas and give them form, structure, and permanence in the physical world.",
    33: "Your destiny is to heal through love — to embody compassion so fully that your very presence becomes a catalyst for transformation.",
}

SOUL_URGE = {
    1: "At your core, your soul craves autonomy. You are driven by a deep need to be original, to self-direct, and to know that your life is truly your own.",
    2: "At your core, your soul craves connection. Deep down, you long for a love that is safe, seen, and reciprocal — a place where you can finally exhale.",
    3: "At your core, your soul craves expression. More than almost anything, you need to create — to take what lives inside you and give it form in the world.",
    4: "At your core, your soul craves stability. You are most alive when you have a solid foundation beneath you — a clear plan, meaningful work, and order.",
    5: "At your core, your soul craves freedom. You came here to experience — to taste, explore, and move through life with the full use of your senses.",
    6: "At your core, your soul craves harmony. You long for a world where people are cared for, where beauty is honored, and where love is the organizing principle.",
    7: "At your core, your soul craves understanding. You need to know the why beneath the why — the hidden pattern, the deeper truth, the thing others overlook.",
    8: "At your core, your soul craves achievement. You are driven by a need to build something that matters — to leave a mark, to earn mastery, to lead.",
    9: "At your core, your soul craves meaning. You are not satisfied with surface — you need your life to contribute to something larger than your individual story.",
    11: "At your core, your soul craves transcendence. You long to touch the infinite — to live in alignment with something so true it vibrates beyond words.",
    22: "At your core, your soul craves legacy. You are driven by a need to build something that will outlast you — something the world will still feel after you are gone.",
    33: "At your core, your soul craves love as a spiritual practice. You long to be of service at the deepest level — to love without condition and teach without ego.",
}

PERSONAL_YEAR = {
    1: {"theme": "New Beginnings",          "message": "This is your year to plant seeds. The slate is fresh, the energy is electric, and everything you initiate now carries a long arc of momentum. Do not wait for perfect conditions. Begin."},
    2: {"theme": "Patience and Partnership","message": "This year invites you to slow down and tend to relationships. What you planted last year is taking root beneath the surface — trust the process. Collaborate, listen, and receive."},
    3: {"theme": "Expression and Expansion","message": "This is your year to be seen. Creativity, social energy, and joy are your allies. Say yes to what lights you up. Your voice is a gift the world needs right now."},
    4: {"theme": "Work and Foundation",     "message": "This year is about building something solid. The universe is asking you to commit — to your craft, your health, your systems. The effort you put in now pays dividends for years."},
    5: {"theme": "Change and Freedom",      "message": "This year brings movement, unexpected turns, and the invitation to release what has grown too small. Stay adaptable. The disruptions are redirections."},
    6: {"theme": "Love and Responsibility", "message": "This year centers home, family, and service. You may be called to show up for others in deeper ways. Let love guide your decisions, and remember to include yourself in your own care."},
    7: {"theme": "Reflection and Depth",    "message": "This is a year of inner development. Step back from the noise. The answers you seek are found in stillness, study, and the willingness to question what you think you know."},
    8: {"theme": "Power and Abundance",     "message": "This is a year of manifestation. Your efforts are meeting their rewards. Step into leadership, make bold moves, and trust your capacity to handle more than you think."},
    9: {"theme": "Completion and Release",  "message": "This year brings endings that make room for everything next. Release what has run its course — with gratitude, not grief. You are clearing the field for your next great cycle."},
}


def _reduce(n):
    if n in (11, 22, 33):
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if n in (11, 22, 33):
            return n
    return n if n >= 1 else 1


def _bg(c):
    c.setFillColor(DARK_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def _gold_line(c, y, x1=None, x2=None):
    if x1 is None: x1 = 0.65 * inch
    if x2 is None: x2 = W - 0.65 * inch
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(x1, y, x2, y)


def _body_text(c, text, x, y, width, font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = simpleSplit(text, font, size, width)
    for line in lines:
        if y < 0.65 * inch:
            break
        c.drawString(x, y, line)
        y -= leading
    return y


def _badge(c, number, cx, cy, r=28):
    c.setFillColor(GOLD)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(DARK_BG)
    label = str(number)
    c.setFont("Times-Bold", 24)
    tw = c.stringWidth(label, "Times-Bold", 24)
    c.drawString(cx - tw / 2, cy - 8, label)


def _header(c, title, sub=None):
    _bg(c)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08 * inch, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Times-Bold", 10)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, H - 0.42 * inch, "CRYSTALAND  |  YOUR NUMEROLOGY BLUEPRINT")
    _gold_line(c, H - 0.55 * inch)
    c.setFont("Times-Bold", 24)
    c.setFillColor(CREAM)
    c.drawString(0.65 * inch, H - 0.95 * inch, title)
    if sub:
        c.setFont("Helvetica", 10)
        c.setFillColor(GOLD)
        c.drawString(0.65 * inch, H - 1.18 * inch, sub.upper())


# Page builders

def _cover(c, data):
    _bg(c)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.12 * inch, W, 0.12 * inch, fill=1, stroke=0)
    c.setFont("Times-Bold", 12)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 0.55 * inch, "C R Y S T A L A N D")
    _gold_line(c, H - 0.70 * inch, x1=1.5 * inch, x2=W - 1.5 * inch)
    c.setFont("Times-Bold", 36)
    c.setFillColor(CREAM)
    c.drawCentredString(W / 2, H - 1.45 * inch, "Your Numerology")
    c.setFont("Times-BoldItalic", 36)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 1.9 * inch, "Blueprint")
    name = (data.get("name") or "Beloved").title()
    c.setFont("Helvetica", 10)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, H - 2.5 * inch, "Prepared for")
    c.setFont("Times-Bold", 20)
    c.setFillColor(CREAM)
    c.drawCentredString(W / 2, H - 2.8 * inch, name)
    _gold_line(c, H - 3.05 * inch, x1=1.8 * inch, x2=W - 1.8 * inch)
    labels = [("Life Path", data.get("lp", 1)), ("Expression", data.get("exp", 1)),
              ("Soul Urge", data.get("su", 1)), ("Personal Year", data.get("py", 1))]
    xs = [1.1, 2.7, 4.3, 5.9]
    by = H - 4.1 * inch
    for i, (lbl, num) in enumerate(labels):
        bx = (xs[i] + 0.5) * inch
        _badge(c, num, bx, by, r=22)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MID_GRAY)
        c.drawCentredString(bx, by - 34, lbl.upper())
    _gold_line(c, H - 4.85 * inch, x1=1.5 * inch, x2=W - 1.5 * inch)
    msg = (
        "Every number in your chart is a doorway — a frequency that shapes the way you love, lead, "
        "create, and move through the world. The pages that follow are your personal guide to those "
        "frequencies. Read slowly. Let what resonates land."
    )
    _body_text(c, msg, 1.0 * inch, H - 5.25 * inch, W - 2.0 * inch,
               font="Times-Roman", size=11.5, color=SOFT_WHITE, leading=18)
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.18 * inch, "crystaland.online  |  Your path. Your numbers. Your identity.")


def _life_path_page(c, data):
    n = _reduce(data.get("lp", 1))
    info = LIFE_PATH.get(n, LIFE_PATH[1])
    _header(c, f"Life Path  {n}", f"The {info['title']}")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.22 * inch
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, "YOUR ESSENCE")
    y -= 0.2 * inch
    y = _body_text(c, info["essence"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11.5, color=CREAM, leading=17)
    y -= 0.25 * inch
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, "YOUR GIFT")
    y -= 0.2 * inch
    y = _body_text(c, info["gift"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    y -= 0.25 * inch
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, "YOUR SHADOW")
    y -= 0.2 * inch
    y = _body_text(c, info["shadow"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    y -= 0.3 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    c.setFont("Times-BoldItalic", 12)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, y, f'"{info["affirmation"]}"')
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _expression_page(c, data):
    n = _reduce(data.get("exp", 1))
    _header(c, f"Expression  {n}", "Your Destiny Number")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Your Expression Number — also called your Destiny Number — is calculated from the letters "
        "of your full birth name. It reveals the energetic frequency you are here to embody: "
        "the role your soul agreed to play in this lifetime."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    _badge(c, n, W / 2, y - 0.1 * inch, r=30)
    y -= 1.0 * inch
    meaning = EXPRESSION.get(n, EXPRESSION[1])
    y = _body_text(c, meaning, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    note = (
        "Your Life Path is who you are at your core; your Expression is who you are here to become. "
        "When these two numbers are in harmony, life flows with purpose. When they create tension, "
        "that friction is the invitation to grow."
    )
    _body_text(c, note, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _soul_urge_page(c, data):
    n = _reduce(data.get("su", 1))
    _header(c, f"Soul Urge  {n}", "The Desire Beneath All Desires")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Your Soul Urge — calculated from the vowels of your birth name — is the quiet voice "
        "beneath every decision you make. It is what you are drawn toward before your mind "
        "talks you out of it. It is your truest want."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    _badge(c, n, W / 2, y - 0.1 * inch, r=30)
    y -= 1.0 * inch
    meaning = SOUL_URGE.get(n, SOUL_URGE[1])
    y = _body_text(c, meaning, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    note = (
        "Many people spend their whole lives pursuing what they think they want — only to discover "
        "the real longing was always something quieter. Your Soul Urge is an invitation to stop "
        "negotiating with that deeper voice and start honoring it."
    )
    _body_text(c, note, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _personal_year_page(c, data):
    n = data.get("py", 1)
    n = _reduce(n) % 9 or 9
    info = PERSONAL_YEAR.get(n, PERSONAL_YEAR[1])
    _header(c, f"Personal Year  {n}", info["theme"])
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Your Personal Year number reveals the overarching theme of your current annual cycle. "
        "Numerology operates in 9-year waves — each year carries a distinct energy, lesson, and "
        "invitation. Knowing yours is like having a compass."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    _badge(c, n, W / 2, y - 0.1 * inch, r=30)
    y -= 1.0 * inch
    y = _body_text(c, info["message"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    note = (
        "The Personal Year does not override your free will — it reveals the current tide. "
        "You can swim with it or against it, but knowing which direction the current is moving "
        "changes everything."
    )
    _body_text(c, note, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _cta_page(c, data):
    _bg(c)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08 * inch, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Times-Bold", 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 0.44 * inch, "C R Y S T A L A N D")
    _gold_line(c, H - 0.58 * inch, x1=1.5 * inch, x2=W - 1.5 * inch)
    c.setFont("Times-Bold", 28)
    c.setFillColor(CREAM)
    c.drawCentredString(W / 2, H - 1.1 * inch, "There Is More")
    c.setFont("Times-BoldItalic", 28)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 1.55 * inch, "Waiting for You")
    y = H - 2.1 * inch
    _gold_line(c, y, x1=1.5 * inch, x2=W - 1.5 * inch)
    y -= 0.3 * inch
    teaser = (
        "What you have just read is your foundation — the core frequencies that shape who you are. "
        "But numerology goes so much deeper. Your full chart includes your Pinnacle cycles, your "
        "Challenge numbers, your hidden Karmic Lessons, and a month-by-month forecast for your "
        "current Personal Year. It is the difference between knowing your sun sign and reading "
        "your entire birth chart."
    )
    y = _body_text(c, teaser, 0.8 * inch, y, W - 1.6 * inch,
                   font="Times-Roman", size=11.5, color=SOFT_WHITE, leading=18)
    y -= 0.5 * inch
    box_y = y - 0.9 * inch
    boxes = [
        (0.6 * inch, "Complete Blueprint", "$47", "33-page deep dive into your full chart"),
        (3.3 * inch, "The Full Transmission", "$97", "77-page numerology + Human Design report"),
    ]
    for bx, label, price, desc in boxes:
        c.setStrokeColor(GOLD)
        c.setFillColor(HexColor('#12111a'))
        c.setLineWidth(0.8)
        c.roundRect(bx, box_y, 2.4 * inch, 1.05 * inch, 6, fill=1, stroke=1)
        c.setFont("Times-Bold", 12)
        c.setFillColor(CREAM)
        c.drawCentredString(bx + 1.2 * inch, box_y + 0.72 * inch, label)
        c.setFont("Times-Bold", 20)
        c.setFillColor(GOLD)
        c.drawCentredString(bx + 1.2 * inch, box_y + 0.42 * inch, price)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(MID_GRAY)
        c.drawCentredString(bx + 1.2 * inch, box_y + 0.16 * inch, desc)
    y = box_y - 0.45 * inch
    _gold_line(c, y, x1=1.5 * inch, x2=W - 1.5 * inch)
    y -= 0.28 * inch
    c.setFont("Times-BoldItalic", 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, y, "Visit crystaland.online to go deeper")
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.18 * inch, "crystaland.online  |  Your path. Your numbers. Your identity.")


def generate_free_report(data: dict) -> bytes:
    """
    Generate the 6-page free numerology PDF.
    data = { name, email, lp, exp, su, per, py }
    Returns raw PDF bytes.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle("Your Numerology Blueprint - Crystaland")
    c.setAuthor("Crystaland")
    for fn in [_cover, _life_path_page, _expression_page, _soul_urge_page, _personal_year_page, _cta_page]:
        fn(c, data)
        c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


if __name__ == "__main__":
    test = {"name": "Rita Kirkendoll", "email": "rita@crystaland.online",
            "lp": 7, "exp": 3, "su": 9, "per": 3, "py": 5}
    b = generate_free_report(test)
    open("test_free_report.pdf", "wb").write(b)
    print(f"Generated test_free_report.pdf ({len(b):,} bytes)")
