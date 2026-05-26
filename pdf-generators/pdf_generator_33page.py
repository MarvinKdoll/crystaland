"""
Crystaland Numerology System
33-Page Complete Blueprint — $47 Report
generate_33page_report(data) -> bytes
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

W, H = letter

# Extra content for deeper pages
PERSONALITY = {
    1: "Your Personality Number is the face you show the world before trust is built — the energy others feel when they first meet you. With a 1, you come across as confident, direct, and self-assured. People immediately sense your leadership energy. You may not always feel as certain as you appear, but that quiet authority is real.",
    2: "With a Personality 2, you come across as gentle, attentive, and warm. People feel immediately at ease in your presence. You are the one who listens, who remembers, who makes others feel like the most important person in the room. This is a profound gift — and a reminder that your sensitivity is strength, not softness.",
    3: "Your Personality 3 radiates creative energy and joy. People are drawn to your expressiveness, your humor, and your ability to light up a conversation. You have a natural magnetism that opens doors others spend years trying to open. Your presence is a gift — own it fully.",
    4: "With a Personality 4, you project reliability, groundedness, and trustworthiness. People sense that you are someone who does what you say, who shows up, who can be counted on. In a world full of noise and empty promises, this energy is rare and deeply valued.",
    5: "Your Personality 5 radiates energy, spontaneity, and a sense of adventure. People find you magnetic and exciting — never quite knowing what you will say or do next. You have a charisma that comes from genuine curiosity about life, and it is contagious.",
    6: "With a Personality 6, you project warmth, nurturing energy, and genuine care. People feel safe around you. You are the one others come to when they need support, guidance, or simply to feel held. This is a sacred role — and a reminder to also receive the care you so freely give.",
    7: "Your Personality 7 projects an air of quiet depth and mystery. People sense that there is much more beneath the surface than you reveal — and they are right. You come across as thoughtful, discerning, and a little private, which draws those who value substance over performance.",
    8: "With a Personality 8, you project authority, confidence, and capability. People instinctively recognize you as someone who gets things done. Your presence commands respect without demanding it. This energy opens professional doors and positions you as a natural leader in any room.",
    9: "Your Personality 9 radiates wisdom, compassion, and an open-heartedness that is rare. People sense your depth and your genuine care for the collective. You come across as someone who has lived, who has learned, and who meets life with generosity — even when it has cost you something.",
    11: "With a Personality 11, you project an ethereal, magnetic quality that is hard to name but impossible to ignore. People sense your depth, your sensitivity, and something luminous in your presence. You are here to inspire — and your energy does that work before you even open your mouth.",
    22: "Your Personality 22 projects vision, capability, and quiet power. People sense that you are operating on a different scale — that your thinking is larger, your ambitions more vast. You come across as someone who does not just dream but builds, and that energy draws serious people and serious opportunities.",
    33: "With a Personality 33, you project unconditional love and a healing presence that is almost tangible. People feel seen, accepted, and uplifted simply by being near you. This is a profound gift and a great responsibility — you are here to model what it looks like to love without condition.",
}

KARMIC_LESSONS = {
    1: {"lesson": "Karmic Lesson 1 — Independence", "text": "In a past life or early life, you learned to defer rather than lead. This lifetime invites you to step fully into your own authority. The growth lives in trusting your instincts and acting on them — even when no one else is moving."},
    2: {"lesson": "Karmic Lesson 2 — Cooperation",  "text": "There is an undercurrent of impatience with others' pace and process. This life asks you to practice true partnership — to listen as deeply as you speak, and to discover that working with others does not diminish you; it multiplies you."},
    3: {"lesson": "Karmic Lesson 3 — Self-Expression","text": "You may have been silenced, dismissed, or taught that your voice was too much in an earlier chapter of your soul's journey. This lifetime is the correction — an invitation to express fully, boldly, and without apology."},
    4: {"lesson": "Karmic Lesson 4 — Discipline",   "text": "The soul has sometimes chosen the path of least resistance. This life asks for follow-through — for the discipline of building what you envision rather than staying in the realm of ideas. Commitment is your medicine."},
    5: {"lesson": "Karmic Lesson 5 — Freedom",      "text": "There is a soul memory of restriction — of lives lived in limitation. This lifetime overcorrects toward freedom. The learning is in discovering that true freedom is not the absence of commitment; it is the capacity to choose presence fully."},
    6: {"lesson": "Karmic Lesson 6 — Responsibility","text": "The soul has sometimes avoided the weight of responsibility. This life brings opportunities to step up — for family, community, creative work. Every time you do, you reclaim a part of your wholeness."},
    7: {"lesson": "Karmic Lesson 7 — Trust",        "text": "Deep skepticism can be a survival strategy for the soul that has been disappointed. This life asks you to go deeper than doubt — to develop a faith in life and in the intelligence of the unseen that transforms how you move through the world."},
    8: {"lesson": "Karmic Lesson 8 — Power",        "text": "There is often a complicated relationship with power — either the fear of claiming it or the misuse of it in another lifetime. This life asks you to step into real authority: grounded, ethical, and in service of something larger than ego."},
    9: {"lesson": "Karmic Lesson 9 — Letting Go",   "text": "The soul has held on — to people, outcomes, eras — beyond their natural completion. This life is a masterclass in release. Each time you let something end gracefully, you discover that something better was always waiting on the other side."},
}

PINNACLES = {
    1: "A pinnacle of leadership and new beginnings — a time to step forward, initiate, and establish your independent identity.",
    2: "A pinnacle of relationships, patience, and inner development — a time to collaborate, to feel deeply, and to trust the quiet process.",
    3: "A pinnacle of creativity and expression — a time when your voice, your art, and your social connections carry particular significance.",
    4: "A pinnacle of work, structure, and foundation — a time to build, to commit to your craft, and to put in the deliberate effort that creates lasting things.",
    5: "A pinnacle of change, movement, and expansion — a time of unexpected shifts that ultimately redirect you toward greater freedom and aliveness.",
    6: "A pinnacle of love, family, and responsibility — a time when matters of home and heart take center stage and ask for your full presence.",
    7: "A pinnacle of reflection, inner development, and spiritual deepening — a time to withdraw from the noise and cultivate your inner life.",
    8: "A pinnacle of achievement, abundance, and leadership — a time when your efforts can translate into significant material and professional results.",
    9: "A pinnacle of completion, release, and humanitarian service — a time to let go of what has run its course and give back from the fullness of all you have accumulated.",
}

CHALLENGES = {
    0: "Your Challenge 0 is the challenge of all challenges — radical self-mastery. Nothing outside you is the real obstacle. The work is always internal.",
    1: "Your Challenge 1 is independence — learning to trust your own judgment, act on your own authority, and stop waiting for external validation before you move.",
    2: "Your Challenge 2 is sensitivity — learning to honor your emotional depth without being consumed by it, and to hold space for others without losing yourself.",
    3: "Your Challenge 3 is self-expression — moving through fear of judgment, self-criticism, and scattered focus to find and fully inhabit your creative voice.",
    4: "Your Challenge 4 is discipline — confronting the tendency to avoid the hard, methodical work that turns vision into reality.",
    5: "Your Challenge 5 is freedom — learning the difference between freedom as escapism and freedom as chosen, conscious aliveness.",
    6: "Your Challenge 6 is responsibility — learning to serve from wholeness rather than obligation, and to discern which burdens are truly yours to carry.",
    7: "Your Challenge 7 is faith — moving through skepticism, isolation, and intellectualization toward a lived trust in something larger than the rational mind.",
    8: "Your Challenge 8 is power — learning to hold authority, abundance, and influence with integrity, and to release any patterns around the misuse or avoidance of power.",
}

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

MONTH_THEMES = [
    "New beginnings, self-focus, and planting intentions",
    "Relationships, patience, and inner listening",
    "Creativity, social energy, and joyful expression",
    "Hard work, structure, and building the foundation",
    "Unexpected change, freedom, and course corrections",
    "Love, family, responsibility, and service",
    "Reflection, solitude, study, and spiritual deepening",
    "Manifestation, ambition, and material results",
    "Completion, release, and gratitude for what has been",
    "New cycles beginning within the larger annual theme",
    "Elevated intuition, sensitivity, and partnership",
    "Mastery, integration, and preparation for what is next",
]

HD_TYPES = {
    "generator":        {"title": "Generator", "desc": "You are the life force of the planet — built for sustained, satisfying work. Your strategy is to respond: let life bring things to you and check in with your gut response before committing. Your sacral center is always on, giving you reliable renewable energy when you are doing work that is truly yours."},
    "manifesting generator": {"title": "Manifesting Generator", "desc": "You are a hybrid powerhouse — part Manifesting energy, part Generator endurance. You can initiate AND sustain, but only when your gut says yes first. You may feel pulled in multiple directions at once; that is not a flaw. You are wired for multi-passionate, high-velocity living."},
    "manifestor":       {"title": "Manifestor", "desc": "You are the initiator — one of the rare types who can act without waiting for external cues. Your strategy is to inform: let the people in your life know what you are about to do before you do it. This one practice dissolves most of the resistance Manifestors encounter."},
    "projector":        {"title": "Projector", "desc": "You are the guide — here to direct, manage, and optimize the energy of others. Your strategy is to wait for the invitation. When you are seen and invited in, your wisdom lands. When you insert yourself without invitation, it often meets resistance. Rest is not laziness for you; it is essential recalibration."},
    "reflector":        {"title": "Reflector", "desc": "You are the rarest type — a mirror for the health of your community. Your strategy is to wait a full lunar cycle before making major decisions. You sample and reflect the energies of everyone around you; your environment is everything. Protecting your alone time and your sacred spaces is non-negotiable."},
}

HD_AUTHORITIES = {
    "sacral":    "Your Sacral Authority means your gut is your oracle. That immediate yes/no, that sound or feeling in your body — that is your most reliable decision-making intelligence. If you have to think about it, keep waiting.",
    "emotional": "Your Emotional Authority means you are here to ride the wave before deciding. Clarity comes over time, not in a moment. Sleep on it. Feel it across different emotional states. When clarity finally arrives, it will be solid.",
    "splenic":   "Your Splenic Authority is the oldest, most primal intelligence in the body. It speaks once, in the moment, and it never speaks the same thing twice. Learn to catch that quiet first impulse — it is almost always right.",
    "ego":       "Your Ego/Heart Authority is tied to your will and desires. You make decisions based on what you genuinely want — not what you think you should want. If your heart is not in it, the energy will not sustain.",
    "self-projected": "Your Self-Projected Authority means you find clarity by talking out loud. Not to get advice — but to hear yourself. Find trusted people to be your sounding board. The answer emerges in the speaking.",
    "mental":    "Your Mental/Outer Authority means you need to process your decisions through conversation and environment. Spend time in the spaces and with the people who will be part of the decision. Your clarity comes from outside in.",
    "lunar":     "Your Lunar Authority — unique to Reflectors — means major decisions deserve the full 28-day lunar cycle. What feels right at the new moon may feel completely different at the full moon. Give yourself time.",
    "none":      "Trust the deepest wisdom available — the quiet intelligence of your body and your lived experience.",
}


def _section_title(c, text, y, x=0.65 * inch):
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD)
    c.drawString(x, y, text)
    return y - 0.2 * inch


def _personality_page(c, data):
    n = _reduce(data.get("per", 1))
    _header(c, f"Personality  {n}", "How the World Sees You")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Your Personality Number — derived from the consonants of your birth name — is the impression "
        "you make before people know you. It is your energetic calling card: the face you wear in public, "
        "at first meetings, in new situations."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    _badge(c, n, W / 2, y - 0.1 * inch, r=30)
    y -= 1.0 * inch
    y = _body_text(c, PERSONALITY.get(n, PERSONALITY[1]), 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=12, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    note = (
        "The gap between your Personality (how others see you) and your Soul Urge (who you truly are) "
        "is one of the most revealing tensions in your chart. When you close that gap — when who you "
        "show up as matches who you truly are — something in you relaxes at a cellular level."
    )
    _body_text(c, note, 0.65 * inch, y, W - 1.3 * inch,
               font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _karmic_lessons_page(c, data):
    lp = _reduce(data.get("lp", 1))
    exp = _reduce(data.get("exp", 1))
    _header(c, "Karmic Lessons", "What Your Soul Came to Learn")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Karmic Lessons are the themes and skills your soul did not fully develop in prior cycles. "
        "They show up as recurring patterns, persistent challenges, or areas of life that feel "
        "disproportionately difficult. They are not punishments — they are the curriculum."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    for n in [lp, exp]:
        if n in KARMIC_LESSONS:
            k = KARMIC_LESSONS[n]
            c.setFont("Times-Bold", 11)
            c.setFillColor(GOLD)
            c.drawString(0.65 * inch, y, k["lesson"])
            y -= 0.22 * inch
            y = _body_text(c, k["text"], 0.65 * inch, y, W - 1.3 * inch,
                           font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
            y -= 0.3 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    close = (
        "Karmic patterns tend to intensify when ignored and soften when consciously engaged. "
        "The fact that you are here, reading this, suggests you are ready to meet yours directly."
    )
    _body_text(c, close, 0.65 * inch, y, W - 1.3 * inch,
               font="Times-Italic", size=11, color=CREAM, leading=17)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _pinnacles_page(c, data, page_num):
    titles = [f"First Pinnacle", f"Second Pinnacle", f"Third Pinnacle", f"Fourth Pinnacle"]
    nums = [
        _reduce(data.get("lp", 1) + data.get("exp", 1)),
        _reduce(data.get("exp", 1) + data.get("su", 1)),
        _reduce(data.get("lp", 1) + data.get("exp", 1) + data.get("su", 1)),
        _reduce(data.get("lp", 1) + data.get("su", 1)),
    ]
    _header(c, "Pinnacle Cycles", f"Page {page_num} — The Four Great Chapters")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.22 * inch
    intro = (
        "Your Pinnacles are the four major chapters of your life — each carrying a distinct "
        "frequency, challenge, and invitation. Together they form the arc of your soul's journey "
        "through time."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.25 * inch
    start_idx = (page_num - 1) * 2
    for i in range(start_idx, min(start_idx + 2, 4)):
        c.setFont("Times-Bold", 12)
        c.setFillColor(CREAM)
        c.drawString(0.65 * inch, y, f"{titles[i]}  —  Number {nums[i]}")
        y -= 0.22 * inch
        y = _body_text(c, PINNACLES.get(_reduce(nums[i]), PINNACLES[1]), 0.65 * inch, y, W - 1.3 * inch,
                       font="Helvetica", size=10.5, color=SOFT_WHITE, leading=16)
        y -= 0.3 * inch
        _gold_line(c, y)
        y -= 0.25 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _challenges_page(c, data):
    c1 = abs(_reduce(data.get("lp", 1)) - _reduce(data.get("exp", 1)))
    c2 = abs(_reduce(data.get("exp", 1)) - _reduce(data.get("su", 1)))
    c3 = abs(c1 - c2)
    c4 = abs(_reduce(data.get("lp", 1)) - _reduce(data.get("su", 1)))
    _header(c, "Challenge Numbers", "The Friction That Forges You")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.22 * inch
    intro = (
        "Challenge Numbers reveal the specific obstacles your soul chose for this lifetime — the "
        "recurring friction points that, when met consciously, become your greatest sources of "
        "strength and wisdom."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.25 * inch
    for label, num in [("First Challenge", c1), ("Second Challenge", c2),
                        ("Main Challenge", c3), ("Final Challenge", c4)]:
        if y < 1.5 * inch:
            break
        c.setFont("Times-Bold", 11)
        c.setFillColor(CREAM)
        c.drawString(0.65 * inch, y, f"{label}  —  Number {num}")
        y -= 0.2 * inch
        y = _body_text(c, CHALLENGES.get(num, CHALLENGES[0]), 0.65 * inch, y, W - 1.3 * inch,
                       font="Helvetica", size=10, color=SOFT_WHITE, leading=15)
        y -= 0.22 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _love_career_page(c, data, topic):
    lp = _reduce(data.get("lp", 1))
    info = LIFE_PATH.get(lp, LIFE_PATH[1])
    if topic == "love":
        _header(c, "Love and Relationship", f"Life Path {lp} in Partnership")
        y = H - 1.52 * inch
        _gold_line(c, y)
        y -= 0.28 * inch
        texts = {
            1: "In love, your Life Path 1 energy means you need a partner who respects your independence and does not try to dim your light. You thrive with someone secure enough to stand beside you rather than behind you. Your greatest challenge in relationship is learning that vulnerability is not weakness — it is the door to true intimacy.",
            2: "In love, your Life Path 2 is exquisitely designed for deep partnership. You are the one who remembers anniversaries, who checks in, who creates the emotional safety that love needs to grow. Your growth edge is learning to communicate your own needs with the same care you pour into your partner's.",
            3: "In love, your Life Path 3 brings magic and aliveness to every relationship. You keep things light, joyful, and creative — and your partner is rarely bored. Your growth edge is depth: learning to move through the uncomfortable conversations rather than charming your way past them.",
            4: "In love, your Life Path 4 is steady, loyal, and deeply trustworthy. You show love through acts of service and consistent presence. Your growth edge is learning to express the tenderness you feel — to let your partner see the softness beneath the structure.",
            5: "In love, your Life Path 5 needs freedom and variety to remain engaged. You are at your best with a partner who is on their own path — someone with their own interests, their own world. Your growth edge is commitment: learning that choosing one person is not the end of freedom; it is the beginning of a particular kind of depth.",
            6: "In love, your Life Path 6 is the nurturer, the anchor, the one who creates a home within the relationship. You love with your whole self. Your growth edge is receiving — allowing your partner to care for you with the same fullness that you pour into them.",
            7: "In love, your Life Path 7 is private, selective, and deeply loyal once trust is established. You do not give your heart quickly, but when you do, it is for keeps. Your growth edge is presence — learning to come out of your head and into the body of the relationship.",
            8: "In love, your Life Path 8 brings passion, ambition, and a powerful presence to any partnership. You want to build something with your person — a life, a vision, a legacy. Your growth edge is softness: learning to lead with vulnerability rather than capability in the space of intimacy.",
            9: "In love, your Life Path 9 loves without condition and gives without keeping score. You see the highest potential in your partner and hold that vision even when they cannot see it themselves. Your growth edge is discernment — learning that not everyone is worthy of that depth of love, and that is not a failure; it is wisdom.",
        }
        y = _body_text(c, texts.get(lp % 9 or 9, texts[1]), 0.65 * inch, y, W - 1.3 * inch,
                       font="Times-Roman", size=11.5, color=CREAM, leading=18)
    else:
        _header(c, "Career and Purpose", f"Life Path {lp} at Work")
        y = H - 1.52 * inch
        _gold_line(c, y)
        y -= 0.28 * inch
        texts = {
            1: "Professionally, you are at your best when you have autonomy and the opportunity to lead. Entrepreneurship suits you — or any role where you can set the direction rather than simply execute someone else's vision. You need to build something that is yours.",
            2: "Professionally, you thrive in collaborative environments, counseling, mediation, and any work that centers human connection. You are the one who holds the team together emotionally and makes everyone feel included. Behind-the-scenes support roles can be deeply satisfying — as long as your contributions are acknowledged.",
            3: "Professionally, you belong in any field that allows you to communicate, create, and connect. Writing, speaking, performing, teaching, design — anywhere your expressive gifts can be fully deployed. You wither in environments that require you to be small or silent.",
            4: "Professionally, you excel in systems, logistics, engineering, finance, project management, and any role that rewards methodical precision. You are the one who makes the plan — and then executes it. Chaotic environments drain you; structured ones bring out your best.",
            5: "Professionally, you need variety, movement, and the absence of rigid routine. Sales, travel, journalism, marketing, event production — anything that keeps you in motion and brings fresh stimulation. You plateau quickly in environments that demand sameness.",
            6: "Professionally, you are drawn to service, healing, teaching, and any work that allows you to nurture and support others. Healthcare, counseling, education, hospitality, design — these fields align with your natural gifts. You are motivated by knowing your work makes someone's life better.",
            7: "Professionally, you are the researcher, the analyst, the strategist, the specialist. Any field that rewards deep expertise and independent thinking suits you: science, psychology, philosophy, spirituality, technology. You need quiet to do your best thinking.",
            8: "Professionally, you are built for leadership, entrepreneurship, and the business world. You understand power, strategy, and the mechanics of success. You are most alive when running something — whether a team, a company, or a movement.",
            9: "Professionally, you are drawn to work that serves the whole: humanitarian work, the arts, education, healing, and social justice. You need to feel that what you do matters beyond your paycheck. Meaning is not optional for you — it is the fuel.",
        }
        y = _body_text(c, texts.get(lp % 9 or 9, texts[1]), 0.65 * inch, y, W - 1.3 * inch,
                       font="Times-Roman", size=11.5, color=CREAM, leading=18)
    y -= 0.4 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    c.setFont("Times-BoldItalic", 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, y, f'"{info["affirmation"]}"')
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _month_forecast_page(c, data, month_start, month_end):
    py = data.get("py", 1)
    py_reduced = _reduce(py) % 9 or 9
    name = (data.get("name") or "You").split()[0].title()
    _header(c, "Month-by-Month Forecast", f"Personal Year {py_reduced} — {PERSONAL_YEAR.get(py_reduced, PERSONAL_YEAR[1])['theme']}")
    y = H - 1.55 * inch
    _gold_line(c, y)
    y -= 0.22 * inch
    for i in range(month_start - 1, min(month_end, 12)):
        if y < 1.0 * inch:
            break
        month_num = ((py_reduced + i - 1) % 9) or 9
        c.setFont("Times-Bold", 11)
        c.setFillColor(CREAM)
        c.drawString(0.65 * inch, y, f"{MONTHS[i]}  |  Personal Month {month_num}")
        y -= 0.2 * inch
        theme = MONTH_THEMES[month_num - 1]
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(GOLD)
        c.drawString(0.65 * inch, y, theme)
        y -= 0.18 * inch
        py_info = PERSONAL_YEAR.get(month_num, PERSONAL_YEAR[1])
        blurb = f"For {name}, this month carries the energy of {py_info['theme'].lower()}. {py_info['message']}"
        y = _body_text(c, blurb, 0.65 * inch, y, W - 1.3 * inch,
                       font="Helvetica", size=10, color=SOFT_WHITE, leading=14)
        y -= 0.22 * inch
        if y > 1.0 * inch:
            _gold_line(c, y + 0.05 * inch)
            y -= 0.1 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _hd_intro_page(c, data):
    hd_type = (data.get("hd_type") or "generator").lower().strip()
    hd_auth = (data.get("hd_authority") or "sacral").lower().strip()
    info = HD_TYPES.get(hd_type, HD_TYPES["generator"])
    auth_text = HD_AUTHORITIES.get(hd_auth, HD_AUTHORITIES["none"])
    _header(c, "Human Design", f"Your Type: {info['title']}")
    y = H - 1.52 * inch
    _gold_line(c, y)
    y -= 0.28 * inch
    intro = (
        "Human Design is a synthesis of astrology, the I Ching, Kabbalah, and quantum physics — "
        "a system that maps how your energy is designed to move through the world. Understanding "
        "your Type and Authority is the single most practical thing you can do with this system."
    )
    y = _body_text(c, intro, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=MID_GRAY, leading=16)
    y -= 0.3 * inch
    c.setFont("Times-Bold", 13)
    c.setFillColor(CREAM)
    c.drawString(0.65 * inch, y, f"Type: {info['title']}")
    y -= 0.22 * inch
    y = _body_text(c, info["desc"], 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=SOFT_WHITE, leading=17)
    y -= 0.3 * inch
    _gold_line(c, y)
    y -= 0.22 * inch
    c.setFont("Times-Bold", 13)
    c.setFillColor(CREAM)
    c.drawString(0.65 * inch, y, f"Authority: {hd_auth.title()}")
    y -= 0.22 * inch
    y = _body_text(c, auth_text, 0.65 * inch, y, W - 1.3 * inch,
                   font="Times-Roman", size=11, color=SOFT_WHITE, leading=17)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _spacer_page(c, title, content, subhead=None):
    """Filler/bridge page for page count."""
    _header(c, title, subhead)
    y = H - 1.55 * inch
    _gold_line(c, y)
    y -= 0.3 * inch
    _body_text(c, content, 0.65 * inch, y, W - 1.3 * inch,
               font="Times-Roman", size=12, color=CREAM, leading=19)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.25 * inch, "crystaland.online")


def _closing_page(c, data):
    _bg(c)
    c.setFillColor(GOLD)
    c.rect(0, H - 0.08 * inch, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Times-Bold", 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 0.44 * inch, "C R Y S T A L A N D")
    _gold_line(c, H - 0.58 * inch, x1=1.5 * inch, x2=W - 1.5 * inch)
    c.setFont("Times-Bold", 28)
    c.setFillColor(CREAM)
    c.drawCentredString(W / 2, H - 1.2 * inch, "You Were Never Lost.")
    c.setFont("Times-BoldItalic", 28)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 1.65 * inch, "You Were Always This.")
    y = H - 2.3 * inch
    _gold_line(c, y, x1=1.5 * inch, x2=W - 1.5 * inch)
    y -= 0.35 * inch
    close = (
        "Numerology does not predict your fate — it reveals your nature. And your nature, when "
        "fully inhabited, is the most powerful force in your life. Every number you have just "
        "read is an invitation: to lead more boldly, to love more openly, to build more "
        "intentionally, and to trust the intelligence that has always been encoded in you.\n\n"
        "This is the beginning of a conversation, not the end of one. If you are ready to go "
        "even deeper — to add the full lens of your Human Design chart and a complete annual "
        "forecast — the 77-page Full Transmission is waiting for you at crystaland.online.\n\n"
        "Come as you are. Go further than you imagined."
    )
    _body_text(c, close, 0.8 * inch, y, W - 1.6 * inch,
               font="Times-Roman", size=12, color=SOFT_WHITE, leading=19)
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 0.08 * inch, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 0.18 * inch, "crystaland.online  |  The Full Transmission awaits.")


def generate_33page_report(data: dict) -> bytes:
    """
    Generate the 33-page Complete Blueprint PDF.
    data = { name, email, lp, exp, su, per, py, hd_type, hd_profile, hd_authority }
    Returns raw PDF bytes.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setTitle("Complete Numerology Blueprint - Crystaland")
    c.setAuthor("Crystaland")

    def page(fn, *args, **kwargs):
        fn(c, *args, **kwargs)
        c.showPage()

    # 1: Cover
    page(_cover, data)
    # 2-3: Life Path (2 pages)
    page(_life_path_page, data)
    page(_spacer_page, f"Life Path {_reduce(data.get('lp',1))} — Going Deeper",
         "Your Life Path is not a label — it is a living frequency. Every decade, you will "
         "encounter it in a new form: as a new challenge, a new gift, a new invitation to inhabit "
         "your essence more fully. The number does not change. You deepen.\n\n"
         "Notice where in your life this energy flows naturally. Notice where it meets resistance. "
         "Both are information. The flow shows you where you are aligned. The resistance shows you "
         "where there is still growing to do.\n\n"
         "The most evolved expression of your Life Path is not the easiest — it is the most alive. "
         "It is the version of yourself that makes full use of the gifts encoded in your number "
         "while meeting the shadow with compassion and curiosity rather than avoidance.")
    # 4-5: Expression
    page(_expression_page, data)
    page(_spacer_page, "Expression — Your Destiny Unfolding",
         "Your Expression number is not something you arrive at once. It is something you grow into "
         "across a lifetime. In your early years, you may have lived primarily from your Life Path "
         "energy — it is more instinctive. Your Expression often becomes more prominent as you "
         "mature, as you take on more intentional roles in the world.\n\n"
         "The question to sit with is this: where in your life are you being asked to embody this "
         "destiny number more fully? Where are you still holding back from the full expression of "
         "who you came here to be?\n\n"
         "The answer to those questions is rarely found in grand gestures. It is found in the "
         "small daily choices — the words you speak, the work you choose, the relationships you "
         "cultivate. Your destiny is built one decision at a time.")
    # 6-7: Soul Urge
    page(_soul_urge_page, data)
    page(_spacer_page, "Soul Urge — Honoring the Quiet Voice",
         "Most people spend decades learning to silence their Soul Urge — to replace it with "
         "what seems practical, acceptable, or achievable. This is the source of a great deal "
         "of suffering.\n\n"
         "When you honor your Soul Urge, something extraordinary happens: you stop performing "
         "your life and start living it. The relationships feel different. The work feels "
         "different. Even your body feels different — lighter, more easeful, more at home.\n\n"
         "Your Soul Urge is not a luxury. It is a navigational instrument. The more you trust "
         "it, the more efficiently your whole life runs. The more you suppress it, the more "
         "energy you spend compensating for that suppression.\n\n"
         "One practice: spend five minutes each morning asking, 'What does my soul actually "
         "want today?' Then do one thing — even one small thing — in that direction.")
    # 8: Personality
    page(_personality_page, data)
    # 9: Karmic Lessons
    page(_karmic_lessons_page, data)
    # 10: Personal Year
    page(_personal_year_page, data)
    # 11-14: Pinnacles (2 pages)
    page(_pinnacles_page, data, 1)
    page(_pinnacles_page, data, 2)
    # 15: Challenges
    page(_challenges_page, data)
    # 16-17: Love & Career
    page(_love_career_page, data, "love")
    page(_love_career_page, data, "career")
    # 18-21: Month Forecast (4 pages, 3 months each)
    page(_month_forecast_page, data, 1, 3)
    page(_month_forecast_page, data, 4, 6)
    page(_month_forecast_page, data, 7, 9)
    page(_month_forecast_page, data, 10, 12)
    # 22-23: Spiritual Path
    page(_spacer_page, "Spiritual Path and Purpose",
         "Numerology is, at its core, a spiritual system. Every number vibrates at a frequency "
         "that carries soul-level information — information about who you are, why you are here, "
         "and what you came to learn and contribute.\n\n"
         "Your spiritual path is not separate from your daily life. It is woven through it: in "
         "how you love, how you work, how you rest, how you respond when things fall apart. "
         "The numbers in your chart are waypoints — not destinations but directions.\n\n"
         "The deepest practice you can offer yourself is radical self-honesty. Not the kind that "
         "tears you apart, but the kind that sees you clearly and chooses to show up anyway. "
         "That is what numerology invites: not perfection, but presence.",
         "Living Your Numbers")
    page(_spacer_page, "Integration — Holding Your Whole Chart",
         "By now you have met the major players in your numerological blueprint: your Life Path, "
         "Expression, Soul Urge, Personality, Personal Year, Pinnacles, and Challenges. Each "
         "is a lens. None is the complete picture.\n\n"
         "The art of living your chart is learning to hold all of these energies simultaneously — "
         "to know when your Life Path is being called forward and when your Soul Urge needs to "
         "be honored. To recognize when you are in a Pinnacle that asks for expansion and when "
         "you are in a Challenge that asks for patience.\n\n"
         "This is not an intellectual exercise. It is a practice of daily listening. Your numbers "
         "are alive — they speak through circumstances, through feelings, through the things that "
         "light you up and the things that drain you.\n\n"
         "Keep coming back to the question: what is this moment asking of me? Your chart will "
         "always have an answer.",
         "Your Whole Self")
    # 24-25: Human Design Intro
    page(_hd_intro_page, data)
    page(_spacer_page, "Human Design — Living Your Design",
         "Understanding your Human Design type and authority is just the beginning. The deeper "
         "practice is experimenting with it in real life — noticing what happens when you follow "
         "your strategy and authority versus when you override it.\n\n"
         "Most of us were conditioned early to make decisions the way our parents, teachers, or "
         "culture expected. Those conditioned patterns often conflict directly with our design. "
         "Deconditioning — the process of releasing those patterns — takes time. Human Design "
         "practitioners often speak of a seven-year deconditioning process.\n\n"
         "You do not need seven years to feel the benefits. Even one week of consistently "
         "following your authority will show you something. Start there.\n\n"
         "The goal is not perfection. The goal is to start trusting the intelligence already "
         "built into your body and your design.",
         "Experiment and Observe")
    # 26-30: Numerology + HD synthesis pages
    page(_spacer_page, "Where Numerology and Human Design Align",
         "When you place your numerology chart alongside your Human Design, something remarkable "
         "often emerges: the same core themes showing up in both systems, described through "
         "entirely different languages.\n\n"
         "A Life Path 7 who is a Projector in Human Design is being told, from two directions, "
         "that depth, wisdom, and selectivity are their superpowers. A Life Path 1 Generator "
         "is being told, from two directions, that their power lies in initiating — but through "
         "gut response rather than mental override.\n\n"
         "When two systems point to the same thing, pay attention. That convergence is not "
         "coincidence. It is a signal of something essential about who you are.\n\n"
         "Notice where your numerology and Human Design align. Those intersections are the "
         "places your soul is most clearly speaking.",
         "Convergence Points")
    for extra_title, extra_content in [
        ("Your Energy Signature", "Every person has an energetic signature — a particular quality of presence that is unmistakably theirs. Yours is shaped by the interplay of every number in your chart, every gate in your Human Design, every experience that has refined you.\n\nYou may not always feel the potency of your own signature. That is normal. We are often the last to recognize what others feel immediately in our presence.\n\nHere is an experiment: ask three people who know you well what quality they feel most strongly in your presence. Then look at your numbers. The alignment will likely surprise you.\n\nYour energy signature is not something you need to construct or perform. It is something you need only to stop suppressing. The world does not need another person trying to be someone else. It needs you, undiluted."),
        ("Relationships Through Your Chart", "Every significant relationship in your life is a mirror — reflecting back aspects of your chart, your unmet needs, your unlived potential, and your recurring patterns.\n\nWhen you understand your own numerological blueprint, you gain a new kind of literacy for your relationships. You begin to see why certain people activate your gifts and why others seem to reliably trigger your shadows.\n\nThis is not about using numerology to judge or screen people. It is about using it to become more conscious — more able to recognize your patterns, more capable of choosing differently when a pattern no longer serves you.\n\nThe most powerful relationship question your chart can help you answer is this: am I showing up as my authentic self in this relationship, or am I shape-shifting to make it work? That answer will tell you everything you need to know."),
        ("Abundance and Your Chart",  "Abundance — financial, creative, relational, physical — is directly related to how aligned you are with your authentic design. When you are living your numbers, resources tend to flow more naturally. Not because numerology is magic, but because alignment removes the internal friction that blocks receiving.\n\nLook at your Life Path and Expression numbers. These two carry the most information about your relationship with abundance and your capacity to create it. A Life Path 8 is designed for material mastery. A Life Path 7 may find that wealth comes through depth of expertise rather than broad hustle.\n\nThere is no number that is naturally abundant and no number that is naturally scarce. Every number has a high expression and a low expression. The work is always the same: move toward authenticity, and the resources tend to follow."),
    ]:
        page(_spacer_page, extra_title, extra_content)
    # 31-32: Integration and ISC
    page(_spacer_page, "The Identity Shift Collective",
         "You did not come this far in self-understanding to stop here.\n\n"
         "The Identity Shift Collective is Rita's ongoing community for people who are ready to "
         "go beyond the reading and into the living — who want support, accountability, and a "
         "community of people on the same journey of radical self-return.\n\n"
         "Inside you will find monthly teachings, live sessions, group coaching, and a space "
         "where your numbers are not just understood but actively worked with. This is where "
         "the real transformation happens: not in a single report, but in consistent, supported "
         "practice over time.\n\n"
         "Visit crystaland.online to learn more and apply.",
         "Go Deeper Together")
    # 33: Closing
    page(_closing_page, data)

    c.save()
    buf.seek(0)
    return buf.read()


if __name__ == "__main__":
    test = {"name": "Rita Kirkendoll", "email": "rita@crystaland.online",
            "lp": 7, "exp": 3, "su": 9, "per": 3, "py": 5,
            "hd_type": "projector", "hd_profile": "3/5", "hd_authority": "splenic"}
    b = generate_33page_report(test)
    open("test_33page.pdf", "wb").write(b)
    print(f"Generated test_33page.pdf ({len(b):,} bytes)")
