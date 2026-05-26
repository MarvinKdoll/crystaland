"""
Crystaland Numerology System
77-Page Full Transmission — $97 Report
generate_77page_report(data) -> bytes
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from io import BytesIO
from pdf_email_brief import (
    DARK_BG, GOLD, CREAM, SOFT_WHITE, MID_GRAY,
    LIFE_PATH, EXPRESSION, SOUL_URGE, PERSONAL_YEAR,
    _reduce, _bg, _gold_line, _body_text, _badge, _header,
    _cover, _life_path_page, _expression_page, _soul_urge_page, _personal_year_page
)
from pdf_generator_33page import (
    PERSONALITY, KARMIC_LESSONS, PINNACLES, CHALLENGES,
    MONTHS, MONTH_THEMES, HD_TYPES, HD_AUTHORITIES,
    _personality_page, _karmic_lessons_page, _pinnacles_page, _challenges_page,
    _love_career_page, _month_forecast_page, _hd_intro_page, _spacer_page, _closing_page
)

W, H = letter

HD_PROFILES = {
    "1/3": {"name": "Investigator/Martyr", "desc": "You are here to build a solid foundation of knowledge — and to learn through trial, error, and direct experience. You are most confident when you have done your research. You are most alive when you let life teach you through doing."},
    "1/4": {"name": "Investigator/Opportunist", "desc": "You need deep foundational knowledge AND a network of trusted people to share it with. Your opportunities come through people you already know. Invest in both your research and your relationships."},
    "2/4": {"name": "Hermit/Opportunist", "desc": "You have natural gifts you may not even be aware of — talents that emerge when you are left alone to develop them. And your opportunities come through your network. The rhythm for you: periods of solitude to cultivate your gifts, followed by showing up for the people in your life."},
    "2/5": {"name": "Hermit/Heretic", "desc": "You are seen by others as someone who has answers — often before you feel ready to give them. You need significant alone time to recharge and develop your natural gifts. When you do show up, people project savior energy onto you. The key is discerning which projections to step into."},
    "3/5": {"name": "Martyr/Heretic", "desc": "You learn by trial and error — by doing things, finding what does not work, and adjusting. This is not failure; it is your methodology. And you are here to share what you have learned with others who need your hard-won wisdom. Your lived experience is your greatest asset."},
    "3/6": {"name": "Martyr/Role Model", "desc": "Your life unfolds in three distinct phases: experimenting and making mistakes in youth, a period of stepping back and observing, and finally fully embodying your role as a wise, experienced guide for others. Trust every phase."},
    "4/6": {"name": "Opportunist/Role Model", "desc": "Your life is built through relationships and your network is everything. You are also here to eventually become a role model — someone others look to as an example of what is possible. This role deepens over time; do not rush it."},
    "4/1": {"name": "Opportunist/Investigator", "desc": "You need a secure foundation — in knowledge, in relationships, in resources — to feel safe enough to show up fully. Invest in building that foundation and trust that your opportunities will flow through the people you have cultivated."},
    "5/1": {"name": "Heretic/Investigator", "desc": "You are here to provide practical solutions to the collective. People project their needs onto you and look to you for answers. Having a solid foundation of knowledge gives you real authority to step into that role."},
    "5/2": {"name": "Heretic/Hermit", "desc": "You carry universal wisdom that others project onto you, and you need significant alone time to access and develop it. The balance for you is between answering the call of the collective and protecting your sacred solitude."},
    "6/2": {"name": "Role Model/Hermit", "desc": "You are here to live a life worth modeling — not by trying, but by following your own design so authentically that others are naturally inspired. You also need significant alone time. Trust both your need for solitude and your eventual role as a guide."},
    "6/3": {"name": "Role Model/Martyr", "desc": "You learn through experience — often through things that do not work — and you are here to eventually become a role model who has earned their wisdom through living. Every apparent failure is preparation for the authority you will carry later."},
}

HD_CENTERS = {
    "head":     {"name": "Head Center", "defined": "You have consistent access to inspiration and mental pressure. Your mind is a reliable source of ideas — just remember that not every question your mind generates needs to be answered.", "undefined": "You are here to be inspired by and amplify the questions of others — not to answer them all yourself. You absorb mental pressure easily; time away from mentally heavy environments is essential."},
    "ajna":     {"name": "Ajna Center", "defined": "Your mind processes information in a consistent and reliable way. You have fixed ways of thinking and conceptualizing the world. This gives you certainty — and can also create rigidity. Practice staying open.", "undefined": "Your mind is flexible and takes on the certainty of others easily. This makes you a great thinker — you can consider multiple perspectives. The caution: avoid making commitments based on mental certainty alone."},
    "throat":   {"name": "Throat Center", "defined": "You have a consistent, reliable way of communicating and expressing yourself. Your voice carries authority. You are designed to speak and be heard.", "undefined": "Your communication style adapts to the environment and the people around you. You may feel pressure to speak before you are ready. Wait until you are invited — your words carry more impact when called forth."},
    "g":        {"name": "G Center (Identity)", "defined": "You have a consistent sense of who you are and where you are going. Your direction and identity are fixed. This gives you stability and magnetic presence.", "undefined": "Your sense of identity and direction is fluid and environment-dependent. You are deeply influenced by the spaces and people you surround yourself with. This is a gift: you can taste many identities. The key is choosing your environments wisely."},
    "heart":    {"name": "Heart/Ego Center", "defined": "You have consistent willpower and the ability to make and keep promises. You can follow through on commitments with sustained energy. Use this gift wisely — commit only to what you genuinely want.", "undefined": "Willpower is not consistent for you — and that is okay. You are not designed to muscle through things on sheer determination. Release the pressure to always follow through and instead trust your body's natural ebbs and flows."},
    "solar":    {"name": "Solar Plexus Center", "defined": "You have emotional authority. Your feelings move in waves — from hope to pain and back again. Wisdom lives at the still point of the wave. Never make major decisions in emotional highs or lows.", "undefined": "You absorb and amplify the emotions of those around you. You feel other people's feelings as if they are your own. This can be overwhelming without awareness. Know that not every feeling you feel belongs to you."},
    "sacral":   {"name": "Sacral Center", "defined": "You have a reliable, renewable life-force energy. You are designed to work — to find deeply satisfying work and do it with your whole self. Your body will tell you when something is right (expansion) or wrong (contraction).", "undefined": "You do not have consistent access to life-force energy. You take in and amplify the sacral energy of others — which can make you feel like you have more energy than you actually do. Rest before you are depleted."},
    "spleen":   {"name": "Spleen Center", "defined": "You have a consistent and powerful intuitive immune system — an instinctive knowing that operates in the moment. Trust your first instinct. It is almost always right.", "undefined": "Your intuition is inconsistent — you pick up on and amplify the health and fear frequencies of others. You may feel others' fear as your own. Ground yourself regularly and learn to distinguish between your intuition and absorbed anxiety."},
    "root":     {"name": "Root Center", "defined": "You have consistent adrenal pressure — a steady drive to move, complete, and get things done. This energy is a resource, not a burden. Channel it into meaningful work.", "undefined": "You absorb and amplify the adrenaline and pressure of others. You may feel rushed even when you do not need to be. Practice distinguishing between true urgency and absorbed pressure."},
}


def _hd_profile_page(c, data):
    profile = data.get("hd_profile", "3/5")
    info = HD_PROFILES.get(profile, HD_PROFILES.get("3/5"))
    _header(c, f"Human Design Profile  {profile}", info["name"])
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Your Profile is the costume your soul wears in this lifetime — the specific role you "
        "are here to play in the larger drama. It shapes how you learn, how you connect, and "
        "how your life's purpose unfolds over time."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.35 * inch
    c.setFont("Times-Bold", 14)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, f"Profile {profile}: {info['name']}")
    y -= 0.25 * inch
    y = _body_text(c, info["desc"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    note = (
        "Your profile does not change based on circumstances — it is fixed. But how fully you "
        "inhabit it depends on how aligned you are with your overall design. As you live more "
        "authentically, your profile expresses with increasing grace and ease."
    )
    _body_text(c, note, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _hd_center_page(c, center_key, defined=True):
    info = HD_CENTERS.get(center_key, HD_CENTERS["throat"])
    status = "Defined" if defined else "Undefined/Open"
    _header(c, info["name"], status)
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    text = info["defined"] if defined else info["undefined"]
    y = _body_text(c, text, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=19)
    y -= 0.45 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    reflection = (
        "Understanding whether each center is defined or open transforms how you relate to "
        "your energy, emotions, and decisions. Defined centers are consistent parts of who you "
        "are. Undefined centers are where you are most susceptible to conditioning — and also "
        "where you can develop the greatest wisdom."
    )
    _body_text(c, reflection, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _annual_theme_page(c, data):
    py = _reduce(data.get("py", 1)) % 9 or 9
    info = PERSONAL_YEAR.get(py, PERSONAL_YEAR[1])
    name = (data.get("name") or "You").split()[0].title()
    _header(c, f"Annual Theme — Personal Year {py}", info["theme"])
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    text = (
        f"For {name}, this entire year vibrates at the frequency of Personal Year {py} — "
        f"a year of {info['theme'].lower()}. {info['message']}\n\n"
        "This theme is the backdrop against which every month, every decision, and every "
        "significant event of this year unfolds. It does not determine what happens — "
        "it shapes the energy available to you and the lessons being highlighted.\n\n"
        "The most aligned year is not the one where everything goes according to plan. "
        "It is the year where you consciously work with the energy rather than against it. "
        "When you understand the theme, you stop fighting the current and start swimming "
        "with it.\n\n"
        f"Your invitation this year: lean into the energy of {info['theme'].lower()}. "
        "Notice where life is naturally pulling you in that direction. Say yes to those "
        "invitations. Release what pulls you backward into last year's lesson."
    )
    _body_text(c, text, 0.65 * inch, y, W - 1.3 * inch,
               font="Times-Roman", size=11.5, color=CREAM, leading=18)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _month_deep_page(c, data, month_idx):
    py = _reduce(data.get("py", 1)) % 9 or 9
    month_num = ((py + month_idx - 1) % 9) or 9
    name = (data.get("name") or "You").split()[0].title()
    month_name = MONTHS[month_idx - 1]
    py_info = PERSONAL_YEAR.get(month_num, PERSONAL_YEAR[1])
    _header(c, month_name, f"Personal Month {month_num} — {py_info['theme']}")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.25 * inch
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, "THE ENERGY")
    y -= 0.2 * inch
    energy_texts = {
        1: f"{month_name} carries the energy of initiation and new beginnings for {name}. This is a month to start — to reach out, to launch, to step forward. The energy supports bold action and first moves. Do not overthink. Begin.",
        2: f"{month_name} slows the pace for {name} and asks for patience and presence. Relationships are highlighted — both the ones that nourish and the ones that drain. Listen more than you speak this month. The insight you are seeking lives in the quiet.",
        3: f"{month_name} invites {name} into creative expansion and social connection. Express yourself — through writing, conversation, art, or simply showing up with your full personality. Joy is not a distraction this month; it is the point.",
        4: f"{month_name} is a work month for {name}. The energy asks for discipline, focus, and the willingness to put your head down and build. What you complete or commit to this month carries lasting weight. Do the work.",
        5: f"{month_name} brings movement and change for {name}. Plans may shift. Unexpected opportunities may appear. Stay flexible and trust that what is changing is changing for a reason. Freedom is available — but it requires letting go first.",
        6: f"{month_name} centers love, home, and responsibility for {name}. Family matters or creative commitments may require your full attention. Show up for the people who need you — and remember to include yourself in that circle of care.",
        7: f"{month_name} is a reflective month for {name}. Step back from the noise. Study, journal, meditate, or simply be still. The insight available this month does not come from doing — it comes from listening. Honor the introversion.",
        8: f"{month_name} amplifies ambition and manifestation for {name}. Professional opportunities, financial decisions, and leadership moments are highlighted. Trust your capacity. This is a month to ask for what you want and receive what you have earned.",
        9: f"{month_name} is a completion month for {name}. Something in your life has run its course — and this month is asking you to let it end with grace. Release the grip. What you release creates space for what is genuinely next.",
    }
    y = _body_text(c, energy_texts.get(month_num, energy_texts[1]), 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=SOFT_WHITE, leading=17)
    y -= 0.3 * inch
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(0.65 * inch, y, "MONTHLY FOCUS AREAS")
    y -= 0.2 * inch
    focus = {
        1: "Initiating new projects. Making the first move in relationships. Setting clear intentions.",
        2: "Deepening partnerships. Practicing patience. Listening to your intuition.",
        3: "Creative expression. Social connection. Speaking your truth with joy.",
        4: "Focused work. Building systems. Honoring commitments you have already made.",
        5: "Embracing change. Releasing what is outgrown. Staying curious and adaptable.",
        6: "Family and home. Service to others. Creating beauty in your immediate environment.",
        7: "Solitude and study. Spiritual practice. Going deeper rather than wider.",
        8: "Career moves. Financial decisions. Stepping into greater leadership.",
        9: "Completion and release. Gratitude practice. Preparing for what is genuinely next.",
    }
    y = _body_text(c, focus.get(month_num, focus[1]), 0.65 * inch, y, W - 1.3 * inch,
                   font="Helvetica", size=10.5, color=CREAM, leading=16)
    y -= 0.3 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    affirmations = {
        1: "I initiate with confidence. My beginnings are blessed.",
        2: "I listen deeply. I trust the quiet wisdom within.",
        3: "My expression is welcome. I share myself freely.",
        4: "I build with intention. My consistency creates my future.",
        5: "I flow with change. I release what no longer serves me.",
        6: "I love from wholeness. I give and receive with equal grace.",
        7: "I trust my inner knowing. In stillness, I find everything I need.",
        8: "I step into my power. I receive what I have earned with gratitude.",
        9: "I release with grace. Every ending is a sacred beginning.",
    }
    c.setFont("Times-BoldItalic", 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, y, f'"{affirmations.get(month_num, affirmations[1])}"')
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def generate_77page_report(data: dict) -> bytes:
    """
    Generate the 77-page Full Transmission PDF.
    data = { name, email, lp, exp, su, per, py, hd_type, hd_profile, hd_authority }
    Returns raw PDF bytes.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle("The Full Transmission - Crystaland")
    c.setAuthor("Crystaland")

    def page(fn, *args, **kwargs):
        fn(c, *args, **kwargs)
        c.showPage()

    hd_type = (data.get("hd_type") or "generator").lower()
    hd_profile = data.get("hd_profile", "3/5")

    # Determine defined/undefined centers based on type (simplified model)
    type_centers = {
        "generator":         {"sacral": True, "root": True, "solar": False, "spleen": False, "heart": False, "g": True, "throat": False, "ajna": False, "head": False},
        "manifesting generator": {"sacral": True, "root": True, "solar": False, "spleen": True, "heart": False, "g": True, "throat": True, "ajna": False, "head": False},
        "manifestor":        {"sacral": False, "root": False, "solar": False, "spleen": True, "heart": True, "g": True, "throat": True, "ajna": True, "head": False},
        "projector":         {"sacral": False, "root": False, "solar": False, "spleen": False, "heart": False, "g": True, "throat": False, "ajna": True, "head": True},
        "reflector":         {"sacral": False, "root": False, "solar": False, "spleen": False, "heart": False, "g": False, "throat": False, "ajna": False, "head": False},
    }
    centers = type_centers.get(hd_type, type_centers["generator"])

    # PAGE 1: Cover
    page(_cover, data)
    # PAGES 2-10: Core Numerology (9 pages)
    page(_life_path_page, data)
    page(_spacer_page, "Life Path — The Deeper Layer",
         "The most important thing to understand about your Life Path is that it is not a ceiling — "
         "it is a frequency. You do not arrive at your Life Path and stay there. You grow into it, "
         "expand it, and continually discover new dimensions of it as your life evolves.\n\n"
         "The highest expression of your Life Path is also the most challenging one — because it "
         "requires the full surrender of what is comfortable for what is true. Most people inhabit "
         "the shadow of their Life Path for years before they discover the gift.\n\n"
         "That is not failure. That is the journey.")
    page(_expression_page, data)
    page(_soul_urge_page, data)
    page(_personality_page, data)
    page(_personal_year_page, data)
    page(_karmic_lessons_page, data)
    page(_spacer_page, "Your Core Numbers — Synthesis",
         "You now hold all five core numbers of your numerology blueprint. Together they form a "
         "complete picture of who you are, who you are becoming, and what you came here to do.\n\n"
         "The most revealing practice at this point is to sit with the interplay between them. "
         "Where do they harmonize? Where do they create tension? The harmony shows you your gifts "
         "in their most natural expression. The tension shows you your growing edges.\n\n"
         "Neither is more important. The gift without the growing edge stays comfortable and small. "
         "The growing edge without the gift has no fuel. You need both.\n\n"
         "This is your chart. This is your curriculum. This is your invitation.")
    # PAGES 11-20: Pinnacles, Challenges, Love, Career (10 pages)
    page(_pinnacles_page, data, 1)
    page(_pinnacles_page, data, 2)
    page(_challenges_page, data)
    page(_love_career_page, data, "love")
    page(_love_career_page, data, "career")
    for title, content in [
        ("Relationships — Going Deeper",
         "The most profound relationship you will ever have is with yourself. Every other relationship "
         "is, in part, a reflection of that primary one.\n\n"
         "When you understand your Soul Urge — what you truly need at the core — you stop unconsciously "
         "expecting your relationships to fill voids that can only be filled from within. This does not "
         "make connection less important. It makes it more real.\n\n"
         "Your numbers reveal the recurring patterns in your relationships: what you are drawn to, "
         "what you struggle with, and what you are ultimately here to learn through the mirror of "
         "the other. Every significant relationship is a teacher. The question is always: what is "
         "this person showing me about myself?"),
        ("Career — Finding Your True Work",
         "Your numerology chart does not tell you what job to take. It tells you something more "
         "fundamental: what kind of work feeds your soul versus what kind depletes it.\n\n"
         "When your work aligns with your Life Path and Expression, it does not feel like sacrifice — "
         "it feels like expression. When it conflicts with your core numbers, no amount of success "
         "will feel satisfying.\n\n"
         "The practical guidance: look for work that activates your Life Path gifts, requires your "
         "Expression number's strengths, and honors your Soul Urge's deepest needs. That intersection "
         "is where your true work lives. It may not pay the most immediately. It will cost you the "
         "least in the long run."),
        ("Abundance Codes",
         "Your relationship with abundance is encoded in your chart — particularly in your Life Path "
         "and the number 8's influence wherever it appears. But abundance is not exclusively a number "
         "8 domain. Every Life Path has its own abundance code.\n\n"
         "The key to unlocking yours is alignment. When you are living authentically — making "
         "decisions that honor your design, expressing your gifts, serving in ways that feel natural "
         "— resources tend to move toward you. Not always immediately, but consistently.\n\n"
         "The blocks to abundance are almost always internal: the belief that you are not worthy, "
         "the fear of being seen, the pattern of overgiving without receiving. Your chart shows you "
         "where those blocks are most likely to live. Your work is to meet them there."),
        ("Spirituality and Your Chart",
         "Every number carries a spiritual dimension. Life Path 7 is perhaps the most obvious — "
         "the mystic, the seeker — but every number has its sacred charge.\n\n"
         "Life Path 1 finds the sacred in the act of creation. Life Path 2 finds it in genuine "
         "connection. Life Path 3 finds it in beauty and expression. Life Path 4 finds it in "
         "mastery and craft. Life Path 5 finds it in aliveness and exploration. Life Path 6 "
         "finds it in service and love. Life Path 8 finds it in stewardship of power. "
         "Life Path 9 finds it in surrender and service to the whole.\n\n"
         "Your spiritual path is not separate from your human life. It is your human life, "
         "lived with full awareness of what it means to be here."),
        ("Integration Practice",
         "Knowledge without practice remains theory. The real value of this report comes not from "
         "reading it once and setting it aside — but from returning to it as a living document.\n\n"
         "A suggested practice: choose one number from your chart to work with each month. Spend "
         "30 days consciously embodying its highest expression. Notice what shifts.\n\n"
         "Another practice: at the beginning of each month, review the monthly forecast and set "
         "one intention that aligns with the personal month energy. At the end of the month, "
         "reflect on how the energy showed up.\n\n"
         "The numbers are not passive descriptions. They are active invitations. The more you "
         "engage with them, the more they guide you."),
    ]:
        page(_spacer_page, title, content)
    # PAGES 21-26: Human Design (6 pages)
    page(_hd_intro_page, data)
    page(_hd_profile_page, data)
    for center in ["sacral", "solar", "spleen", "heart", "g", "throat"]:
        page(_hd_center_page, center, centers.get(center, False))
    # PAGES 27-35: More HD Centers + Deep Dive (9 pages)
    for center in ["ajna", "head", "root"]:
        page(_hd_center_page, center, centers.get(center, False))
    for title, content in [
        ("Your Not-Self Theme",
         "Every Human Design type has a Not-Self theme — the emotional signal that tells you when "
         "you are living out of alignment with your design.\n\n"
         "For Generators and Manifesting Generators: the Not-Self theme is frustration. When you "
         "are not responding correctly — when you are initiating from the mind rather than the gut "
         "— you feel chronically frustrated. That frustration is not a character flaw. It is a "
         "navigation signal.\n\n"
         "For Manifestors: the Not-Self theme is anger. When you are not informing, when you are "
         "hiding your intentions or feeling controlled, anger arises. It is your body asking for "
         "the freedom that is your birthright.\n\n"
         "For Projectors: the Not-Self theme is bitterness. When you are not being invited, when "
         "you are giving guidance that was not asked for, bitterness builds. The invitation is "
         "the medicine.\n\n"
         "For Reflectors: the Not-Self theme is disappointment. When your environment does not "
         "reflect the health and harmony you are here to mirror, disappointment signals the need "
         "for a change of environment."),
        ("Your Signature Theme",
         "Just as there is a Not-Self theme that signals misalignment, there is a Signature theme "
         "that signals you are living correctly.\n\n"
         "For Generators and Manifesting Generators: Satisfaction. When you are doing the right "
         "work, the work that genuinely lights you up, you feel a deep satisfaction — a sense of "
         "rightness that is unmistakable.\n\n"
         "For Manifestors: Peace. When you are moving freely, informing those around you, and not "
         "being controlled or controlled by others, you experience an inner peace that is your "
         "natural state.\n\n"
         "For Projectors: Success. When you are recognized and invited, when your guidance is "
         "received and valued, success follows naturally. It does not have to be forced.\n\n"
         "For Reflectors: Delight. When you are in the right environment, surrounded by the right "
         "people, a sense of delight and wonder is your constant companion."),
        ("Human Design and Relationships",
         "Understanding both your own Human Design and the types and authorities of those you are "
         "in relationship with transforms how you relate.\n\n"
         "A Generator and a Projector in relationship: the Generator provides the energy, the "
         "Projector guides the direction. When the Projector waits for the invitation to advise "
         "and the Generator responds from the gut rather than the mind — magic happens.\n\n"
         "A Manifestor in relationship needs to inform their partner before acting. This one "
         "practice dissolves most of the resistance Manifestors encounter in close relationships.\n\n"
         "A Reflector in relationship needs a partner who understands their need for time and "
         "space — who does not pressure them for immediate decisions or constant output.\n\n"
         "The most important thing: everyone is right in their own design. There are no superior "
         "or inferior types. There is only alignment or misalignment with your own nature."),
        ("Conditioning and Deconditioning",
         "From the moment we are born, we begin absorbing the conditioning of our environment — "
         "the beliefs, expectations, and energetic patterns of our families, schools, cultures, "
         "and relationships. This conditioning shapes how we think we should make decisions, "
         "what we think we should want, and who we think we should be.\n\n"
         "In Human Design, deconditioning is the process of releasing those patterns and returning "
         "to your authentic design. It is not a fast process. Practitioners speak of a seven-year "
         "experiment — seven years of consistently following your strategy and authority, observing "
         "the results, and recalibrating.\n\n"
         "The beginning of deconditioning is simply awareness. Now that you know your design, you "
         "can start to notice when you are living it and when you are not. That awareness alone "
         "begins to shift things."),
        ("Numerology and Human Design Together",
         "The real power of this report comes from the convergence of two systems.\n\n"
         "Numerology reveals the soul's curriculum — the numbers it chose before incarnating as "
         "the specific lessons, gifts, and experiences it came to explore. Human Design reveals "
         "the vehicle — the specific energetic architecture the soul is working through in this "
         "particular body, in this particular lifetime.\n\n"
         "When you read both systems together, a more complete picture emerges. The recurring "
         "themes become unmistakable. The places where both systems point to the same thing are "
         "the places to pay the most attention.\n\n"
         "Look for the convergences in your own chart. They are the places where your design "
         "speaks most clearly, most insistently, most lovingly."),
        ("Living the Integration",
         "You now hold a comprehensive map of your soul's design — in numerology and in Human "
         "Design. The map is only as useful as the territory you actually walk through with it.\n\n"
         "The invitation now is to take what you have learned into the laboratory of your daily "
         "life. Notice where you are living in alignment with your design. Notice where you are "
         "not. Be curious rather than critical about both.\n\n"
         "The numbers and types and profiles are not judgments. They are invitations. Every day "
         "is a new opportunity to inhabit your design a little more fully, to trust your "
         "authority a little more deeply, to offer your gifts a little more freely.\n\n"
         "This is the work. And it is also the gift."),
    ]:
        page(_spacer_page, title, content)
    # PAGES 36-37: Annual Theme
    page(_annual_theme_page, data)
    page(_spacer_page, "Working With Your Personal Year",
         "Your Personal Year number is your annual compass. But it is most powerful when you "
         "understand not just the overall theme but how that theme shows up month by month — "
         "wave by wave within the larger cycle.\n\n"
         "The months within your Personal Year each carry a sub-frequency that modulates the "
         "annual theme. A month of rest within a year of action. A month of expansion within a "
         "year of consolidation. Learning to read these sub-frequencies helps you navigate with "
         "far more precision.\n\n"
         "The month-by-month forecast that follows gives you that precision. Use it as a planning "
         "tool, a reflection tool, and a permission slip — permission to flow with what each "
         "month is genuinely asking of you.")
    # PAGES 38-49: Deep monthly forecast (12 pages, one per month)
    for m in range(1, 13):
        page(_month_deep_page, data, m)
    # PAGES 50-65: Extended content (16 pages)
    extended_pages = [
        ("Numerological Cycles Overview",
         "Numerology operates in cycles within cycles: the 9-year Personal Year cycle, the "
         "larger Pinnacle cycles, and the even larger Life Cycles — each spanning approximately "
         "one third of your lifetime.\n\n"
         "Your First Life Cycle (birth to approximately age 27-34) is governed by your birth "
         "month and carries the themes of formation and early conditioning.\n\n"
         "Your Second Life Cycle (roughly the middle third of your life) is governed by your "
         "birth day and carries the themes of productivity, relationships, and your primary "
         "contribution to the world.\n\n"
         "Your Third Life Cycle (the final third) is governed by your birth year and carries "
         "the themes of completion, wisdom, and legacy.\n\n"
         "Understanding which cycle you are in right now helps contextualize the specific "
         "challenges and opportunities you are experiencing."),
        ("The Master Numbers",
         "Master numbers — 11, 22, and 33 — appear in numerology charts as signals of elevated "
         "frequency and correspondingly elevated challenge.\n\n"
         "If you carry a master number in any position in your chart, you have taken on a soul "
         "contract that includes both extraordinary potential and extraordinary sensitivity to "
         "misalignment.\n\n"
         "Master number 11 (the Illuminator): here to inspire, transmit, and bridge the mundane "
         "and the divine. Often highly intuitive, sometimes psychic, almost always deeply "
         "sensitive to energy and environment.\n\n"
         "Master number 22 (the Master Builder): here to translate the grandest visions into "
         "real-world systems and structures. Has access to Masterly ideas AND the practical "
         "capacity to execute them.\n\n"
         "Master number 33 (the Master Teacher): the rarest master vibration, here to heal "
         "through unconditional love and teach by example at the highest level."),
        ("Your Maturity Number",
         "The Maturity Number — calculated by adding your Life Path and Expression numbers — "
         "reveals the energy that begins to emerge strongly in your mid-thirties to forties "
         "and becomes more prominent as you age.\n\n"
         "Think of it as the frequency of your second act — the energy that increasingly "
         "defines you as you move away from the urgency of young adulthood and into the "
         "deeper, more intentional terrain of your mature self.\n\n"
         "If your Maturity Number resonates with something you already feel stirring in you, "
         "pay attention. Your soul is beginning to remember what it came here to embody in "
         "the second half of the journey."),
        ("Hidden Passion Numbers",
         "Within your name lies another layer of information: the Hidden Passion Number, "
         "determined by which number appears most frequently in your name's numerical translation.\n\n"
         "The Hidden Passion reveals a skill, quality, or area of life that you return to "
         "again and again — almost compulsively. It is neither purely good nor bad; it is simply "
         "a powerful undercurrent that shapes your experience.\n\n"
         "When channeled consciously, Hidden Passion numbers become tremendous assets — areas "
         "where your natural skill and enthusiasm create exceptional results. When unconscious, "
         "they can become obsessions or blind spots."),
        ("Numerology and Health",
         "Every number carries information about the energy systems of the body — the areas "
         "of physical and energetic vulnerability that each vibration tends to concentrate.\n\n"
         "Life Path 1: head, brain, eyes — the centers of individual perception and will.\n"
         "Life Path 2: nervous system, the gut, the immune system — the systems of sensitivity.\n"
         "Life Path 3: throat, skin, nervous system — the systems of expression.\n"
         "Life Path 4: bones, joints, the foundational structural systems.\n"
         "Life Path 5: adrenal system, the lungs, the senses — the systems of experience.\n"
         "Life Path 6: heart, the reproductive system — the systems of love and creation.\n"
         "Life Path 7: the brain, the pineal gland — the systems of perception and intuition.\n"
         "Life Path 8: the skeletal system, the blood — the systems of structure and power.\n"
         "Life Path 9: the lymphatic system, the liver — the systems of release and integration."),
        ("Numerology and Money",
         "Every Life Path has a distinct relationship with money — not because some numbers "
         "are destined for wealth and others are not, but because each number has a different "
         "energetic relationship with the material world.\n\n"
         "The key is always the same: alignment. When you are living authentically, when your "
         "work expresses your Life Path and your Expression number, money becomes a byproduct "
         "of that alignment rather than the goal you are perpetually chasing.\n\n"
         "Common money blocks by number: 1 often fears accepting help or investment. 2 often "
         "undervalues itself. 3 often makes impulsive financial decisions. 4 often hoards rather "
         "than invests. 5 often overspends on experiences. 6 often gives money away and then "
         "resents it. 7 often avoids thinking about money at all. 8 often experiences dramatic "
         "financial swings as a test of relationship with power. 9 often struggles to charge "
         "what their gifts are worth."),
        ("Destiny and Free Will",
         "The deepest question numerology raises is the oldest one in philosophy: are we "
         "determined, or do we choose?\n\n"
         "The answer numerology offers is nuanced. Your numbers are real. They shape the "
         "terrain of your life — the themes that recur, the gifts that come naturally, the "
         "challenges that keep appearing until they are met. In that sense, there is something "
         "like destiny encoded in your chart.\n\n"
         "But within that terrain, every choice is yours. The Life Path 5 can choose to use "
         "their freedom constructively or self-destructively. The Life Path 8 can use their "
         "power with integrity or not. The numbers reveal the landscape; you decide how to "
         "move through it.\n\n"
         "This is not fate. It is invitation. The question is always: what will you do with "
         "the frequency you arrived with?"),
        ("The Crystaland Framework",
         "Rita built Crystaland on a fundamental belief: that every person already carries "
         "everything they need for the life they are here to live. The numbers are not adding "
         "something new — they are revealing what was always there.\n\n"
         "The Crystaland framework has three pillars:\n\n"
         "Know Your Design — understand the specific energetic blueprint you arrived with, "
         "through numerology and Human Design.\n\n"
         "Live Your Design — begin making choices from that blueprint rather than from "
         "conditioning, fear, or comparison.\n\n"
         "Embody Your Design — over time, as you practice living from your authentic design, "
         "the gap between who you are and who you perform closes. That is the identity shift. "
         "That is the work."),
        ("The Identity Shift",
         "Most people spend enormous energy trying to become someone they are not — trying to "
         "fix the parts of themselves that feel wrong, to amplify the parts that seem "
         "acceptable, and to hide the parts that feel too much or not enough.\n\n"
         "The Identity Shift is a different paradigm entirely. It is not about becoming someone "
         "new. It is about returning to who you already are at the deepest level — beneath the "
         "conditioning, beneath the performance, beneath the survival strategies.\n\n"
         "When that shift happens — even partially, even in one area of your life — something "
         "fundamental changes. The effort it takes to simply be yourself decreases dramatically. "
         "The right people and opportunities find you with less friction. Life begins to feel "
         "less like a battle and more like an unfolding.\n\n"
         "That is what your numbers are pointing toward. That is the invitation."),
        ("Practical Integration — Daily Practices",
         "The gap between understanding your design and living it is practice. Here are "
         "practices that support the integration of your chart:\n\n"
         "Morning check-in: before you begin the day, spend two minutes asking your body — "
         "not your mind — what it needs and what it wants to move toward. Trust what comes.\n\n"
         "Monthly review: at the start of each month, revisit your personal month energy. "
         "Set one intention aligned with it. At month's end, reflect on how it showed up.\n\n"
         "Yearly rhythm: return to your Personal Year theme at each solstice and equinox. "
         "Where are you in the cycle? What is the year asking of you now?\n\n"
         "Design check: when facing a significant decision, run it through your Human Design "
         "authority. Does your body say yes? Does it feel right in the system designed to "
         "guide you? Trust that more than your mind."),
        ("Community and Connection",
         "One of the most powerful things you can do with the knowledge in this report is "
         "share it — not to convince others, but to invite conversation.\n\n"
         "When you begin to understand your own design, you naturally become more curious "
         "about the designs of those around you. Why does your partner make decisions the way "
         "they do? Why does your colleague seem to have an endless supply of energy while you "
         "need recovery time after intense periods?\n\n"
         "The Identity Shift Collective exists as a space for exactly this kind of community "
         "— a place where people who take their own design seriously can learn from, support, "
         "and witness each other's unfolding.\n\n"
         "Visit crystaland.online to learn more."),
        ("A Letter to You",
         "You have just moved through one of the most comprehensive maps of your soul's "
         "design that exists. That is not nothing. Most people will never look this closely "
         "at who they are and why they are here.\n\n"
         "The fact that you are here — reading this, curious about this — says something "
         "about your Life Path, your expression, your readiness.\n\n"
         "What matters now is not that you remember every detail of what you have read. What "
         "matters is that something in you has shifted — some small recognition, some quiet "
         "yes, some sense of being known at a deeper level than usual.\n\n"
         "Carry that with you. Let it guide your next choice. And the one after that. That "
         "is how the identity shift happens — not all at once, but one honest decision at a time.\n\n"
         "With love and intention,\nRita and the Crystaland team"),
    ]
    for title, content in extended_pages:
        page(_spacer_page, title, content)
    # PAGES 66-74: Compatibility, Life Cycle Analysis (9 pages)
    compat_pages = [
        ("Numerological Compatibility — Overview",
         "Compatibility in numerology is not about finding your perfect number match — it is "
         "about understanding how two designs interact. Every combination has gifts and every "
         "combination has growth edges.\n\n"
         "The most important compatibility factor is not whether two people's numbers harmonize "
         "perfectly — it is whether both people are committed to living authentically. Two people "
         "in genuine alignment with their own designs will find a way to honor each other's.\n\n"
         "That said, certain number combinations do create natural resonance, and others create "
         "natural tension. Neither is good or bad. Resonance brings ease; tension brings growth. "
         "Both are necessary ingredients in a meaningful relationship."),
        ("Life Cycle Analysis",
         "Your life unfolds in three major cycles, each governed by a different number derived "
         "from your birthdate. Understanding which cycle you are currently in provides enormous "
         "clarity about what this chapter of your life is asking of you.\n\n"
         "These cycles are not rigid boxes — they are energetic streams that carry particular "
         "lessons and opportunities. The transition between cycles (which occurs at your first "
         "and second pinnacle years) is often a period of significant outer and inner change.\n\n"
         "If you are currently in a cycle transition, you are likely feeling the old chapter "
         "completing and the new one beginning to assert itself. This is normal. It is, in fact, "
         "exactly as it should be."),
        ("Your Soul's Journey",
         "From the perspective of numerology, this lifetime is one chapter in a much longer "
         "story — the story of your soul's evolution across many cycles of experience and learning.\n\n"
         "The numbers you carry in this lifetime reflect what your soul has accumulated and what "
         "it still seeks to complete. The Karmic Lessons point to what was left unfinished. "
         "The gifts in your Life Path reflect what was mastered in prior cycles and is now "
         "available as natural talent.\n\n"
         "You are not starting from zero. You arrived with centuries of experience, encoded in "
         "your numbers. Every time you live your design authentically, you honor not just this "
         "lifetime but the whole arc of who you have been becoming."),
        ("Year Ahead Reflection",
         "As you move through your Personal Year, specific questions can help you stay "
         "aligned with the energy available to you:\n\n"
         "What am I being asked to initiate, develop, or complete this year?\n\n"
         "Where am I resisting the current year's energy — and what would it look like to "
         "stop resisting and start flowing?\n\n"
         "Who are the people who seem to be showing up with particular significance this "
         "year? What is the lesson they carry?\n\n"
         "What version of myself is this year asking me to grow into?\n\n"
         "Return to these questions quarterly. Let your answers evolve as the year evolves."),
        ("Manifestation and Your Chart",
         "Manifestation is not magic — it is alignment. When your desires, your actions, and "
         "your authentic design are pointing in the same direction, things tend to move.\n\n"
         "The numerology of manifestation: your Life Path number reveals what you are designed "
         "to create. Your Expression number reveals how you are meant to bring it into form. "
         "Your Personal Year number reveals when the energy is most supportive.\n\n"
         "A Personal Year 1 is optimal for beginning new projects. A Personal Year 8 is "
         "optimal for material manifestation. A Personal Year 9 is optimal for completion "
         "and release — not always ideal for launching, but powerful for finishing.\n\n"
         "Working with these cycles rather than against them is one of the most practical "
         "gifts numerology offers."),
        ("Receiving Your Gifts",
         "One of the most overlooked aspects of living your design is the practice of "
         "receiving — allowing the recognition, resources, and connections that are meant "
         "for you to actually land.\n\n"
         "Many people are skilled at giving — their gifts, their time, their energy — "
         "but struggle to receive with equal grace. The numerological lens reveals where "
         "this pattern is most likely to show up based on your specific chart.\n\n"
         "A practical receiving practice: for the next thirty days, when someone offers "
         "you a compliment, help, or resource, simply say 'thank you' — without deflecting, "
         "minimizing, or immediately reciprocating. Notice what that feels like. Notice what "
         "shifts in your energy and in what shows up."),
        ("Shadow Work and Integration",
         "Every number has a shadow — a lower expression that emerges when fear, conditioning, "
         "or depletion overrides authentic living. Working consciously with your shadow is "
         "not about fixing yourself. It is about witnessing yourself fully.\n\n"
         "The shadow aspects of your numbers are not weaknesses to be eliminated. They are "
         "information. They tell you where you are still operating from old programming, where "
         "the wound is still active, where the growth is still available.\n\n"
         "The practice is not to transcend the shadow but to bring it into relationship with "
         "the light of your authentic design. When the shadow is seen and held with compassion, "
         "it loses its power to run the show from below the surface."),
        ("The Next Level",
         "Everything in this report is a beginning.\n\n"
         "The 77 pages you have just moved through are a comprehensive foundation — but the "
         "living of it, the ongoing practice, the community and support that sustains it — "
         "that is available in the Identity Shift Collective.\n\n"
         "Inside the Collective, Rita works with members over time — not just delivering "
         "information but supporting the actual shift in identity that comes from consistently "
         "living your design.\n\n"
         "If you feel called to that level of support and community, visit crystaland.online "
         "to learn more. The door is open for those who are ready."),
        ("Closing Reflection",
         "You arrived in this body, in this lifetime, with a specific blueprint. Not because "
         "someone handed it to you, but because at some level — the level of the soul — you "
         "chose it.\n\n"
         "Every number in your chart is a choice your soul made. Every gift is something you "
         "earned in prior cycles. Every challenge is something your soul knew you were ready "
         "to meet.\n\n"
         "That is not a small thing. That is everything.\n\n"
         "You are not an accident. You are not a mistake. You are not someone who needs to "
         "be fixed or improved beyond recognition. You are a soul living its specific design "
         "in a specific moment in time — with access to more wisdom about that design than "
         "most people will ever have.\n\n"
         "Use it. Live it. Share it. That is the work. And it is also the gift."),
    ]
    for title, content in compat_pages:
        page(_spacer_page, title, content)
    # PAGES 75-77: Final pages
    page(_spacer_page, "The Identity Shift Collective",
         "The Identity Shift Collective is the ongoing community for people who have done "
         "the reading and are ready to do the work.\n\n"
         "Inside the Collective:\n\n"
         "Monthly live sessions with Rita exploring numerology, Human Design, and the "
         "practical application of both in your real life.\n\n"
         "A supportive community of people who take their own design seriously — and who "
         "will witness and celebrate yours.\n\n"
         "Ongoing teachings, resources, and practices that support the integration of "
         "your chart across every area of life.\n\n"
         "Group coaching and accountability for those ready to close the gap between "
         "who they are and who they are designed to be.\n\n"
         "Visit crystaland.online to apply.",
         "Go Deeper Together")
    page(_spacer_page, "Thank You",
         "Thank you for trusting this process — and for trusting yourself enough to look "
         "this closely at who you are.\n\n"
         "This report was created with care, with respect for the systems it draws from, "
         "and with genuine belief in the person who is reading it.\n\n"
         "Your design is real. Your gifts are real. The life you are here to live is not "
         "a fantasy — it is a frequency waiting to be inhabited fully.\n\n"
         "With love and deep respect for your path,\n\n"
         "Rita Kirkendoll\nCrystaland\ncrystalnd.online")
    page(_closing_page, data)

    c.save()
    buf.seek(0)
    return buf.read()


if __name__ == "__main__":
    test = {"name": "Rita Kirkendoll", "email": "rita@crystaland.online",
            "lp": 7, "exp": 3, "su": 9, "per": 3, "py": 5,
            "hd_type": "projector", "hd_profile": "3/5", "hd_authority": "splenic"}
    b = generate_77page_report(test)
    open("test_77page.pdf", "wb").write(b)
    print(f"Generated test_77page.pdf ({len(b):,} bytes)")
