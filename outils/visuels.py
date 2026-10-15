"""Génère les SVG de profile/ selon l'identité visuelle (design/docs/assets/etymo.css).

Chaque panneau existe en atelier (clair) et en nocturne (-nuit) : le README les sert par <picture>.
Lancer : python3 outils/visuels.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "profile"

# Jetons d'etymo.css. Les couleurs de ressource ne changent pas entre les thèmes.
FIXED_INK, NIGHT, CREAM_FIXED, PAPER_FIXED = "#0f1f19", "#0c1814", "#fffbf3", "#f3eee3"
PREFIX, SUFFIX, LANG, ACTION, ACTION_DEEP = "#cdf25a", "#4fd1c5", "#8f7bf0", "#ff6b4a", "#c23d1f"
THEMES = {
    "": dict(paper="#f3eee3", cream="#fffbf3", ink="#0f1f19", ink2="#44564d", ink3="#5c6b62",
             line="rgba(15, 31, 25, 0.14)", strong="rgba(15, 31, 25, 0.9)", shadow="#0f1f19",
             accent=ACTION_DEEP),
    # Nocturne : neutres inversés ; le texte d'accent reprend le Corail, comme le hero.
    "-nuit": dict(paper="#0f1f19", cream="#182c24", ink="#f3eee3", ink2="#b8c6bd", ink3="#809088",
                  line="rgba(243, 238, 227, 0.14)", strong="rgba(243, 238, 227, 0.8)",
                  shadow="rgba(243, 238, 227, 0.28)", accent=ACTION),
}
SERIF = "'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif"
SANS = "'Avenir Next', 'Segoe UI', Futura, 'Helvetica Neue', sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Mono', Menlo, monospace"
EASE_OUT, EASE_SPRING = "cubic-bezier(0.16, 1, 0.3, 1)", "cubic-bezier(0.34, 1.56, 0.64, 1)"
CSS = (f".serif{{font-family:{SERIF}}}.sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
       "@media (prefers-reduced-motion: reduce){*{animation:none !important}}")


def svg(w, h, body, label, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}"><style>{CSS}{css}</style>{body}</svg>\n')


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


def seal(x, y, size):
    """Le sceau ÉL (design/docs/assets/logo.svg)."""
    return (f'<g transform="translate({x},{y}) scale({size / 64})"><g transform="rotate(-6 32 32)">'
            f'<rect x="12" y="12" width="44" height="44" rx="12" fill="{FIXED_INK}"/>'
            f'<rect x="7" y="7" width="44" height="44" rx="12" fill="{ACTION}" stroke="{FIXED_INK}" stroke-width="2.5"/>'
            f'<text class="serif" x="29" y="40" text-anchor="middle" fill="{FIXED_INK}" font-size="25" '
            f'font-weight="700" letter-spacing="-0.5">ÉL</text></g></g>')


def brick(x, y, w, h, color, meta, label, t, size=34, radius=10, shadow=4, cls="", dot=False):
    """Brique : contour Encre 1,5 px, rayon 10, ombre dure 4 px, texte en Encre fixe."""
    return (f'<g class="{cls}"><rect x="{x + shadow}" y="{y + shadow}" width="{w}" height="{h}" rx="{radius}" fill="{t["shadow"]}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" stroke="{FIXED_INK}" stroke-width="1.5"/>'
            + (f'<circle cx="{x + 24}" cy="{y + 21}" r="6" fill="{ACTION}" stroke="{FIXED_INK}" stroke-width="1.5"/>' if dot else "")
            + (f'<text class="mono" x="{x + (38 if dot else 18)}" y="{y + 25}" font-size="11" letter-spacing="0.66" fill="{FIXED_INK}">{meta}</text>' if meta else "")
            + f'<text class="serif" x="{x + (18 if meta else 16)}" y="{y + h - 18}" font-size="{size}" font-weight="700" fill="{FIXED_INK}">{label}</text></g>')


def panel(h, num, plain, em, t, after=""):
    """Panneau Papier avec le numéro de section et le titre (.sec-num, h2)."""
    return (f'<rect x="0.75" y="0.75" width="998.5" height="{h - 1.5}" rx="14" fill="{t["paper"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
            f'<rect x="36" y="45" width="28" height="1.5" fill="{t["accent"]}"/>'
            f'<text class="mono" x="74" y="50" font-size="12" font-weight="700" letter-spacing="1.7" fill="{t["accent"]}">{num}</text>'
            f'<text class="serif" x="34" y="104" font-size="46" font-weight="600" letter-spacing="-1.6" fill="{t["ink"]}">{plain}'
            f'<tspan fill="{t["accent"]}" font-style="italic">{em}</tspan>{after}</text>')


def card(x, y, w, h, t):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["cream"]}" stroke="{t["strong"]}" stroke-width="1.5"/>'


# ---------- Bannière : le hero du dossier, toujours sur Nuit ----------
def banner():
    chain = ""
    for i, (form, sens) in enumerate([("τῆλε", "au loin"), ("σκοπεῖν", "regarder")]):
        y = 196 + i * 50
        on = (f'<rect x="20" y="{y}" width="312" height="42" rx="10" fill="{PAPER_FIXED}" stroke="{FIXED_INK}" stroke-width="1"/>'
              if i == 0 else "")
        chain += (on + f'<circle cx="38" cy="{y + 21}" r="5" fill="{LANG}" stroke="{FIXED_INK}"/>'
                  f'<text class="mono" x="54" y="{y + 25}" font-size="10" letter-spacing="0.8" fill="#44564d">GREC ANCIEN</text>'
                  f'<text class="serif" x="146" y="{y + 27}" font-size="18" fill="{FIXED_INK}">{form} <tspan font-style="italic" fill="#44564d">« {sens} »</tspan></text>')
    hero_card = (
        f'<g transform="translate(770,70) rotate(-3 176 180)">'
        f'<rect x="12" y="12" width="352" height="360" rx="20" fill="{ACTION}"/>'  # identite: vitrine Corail de l'accueil
        f'<rect width="352" height="360" rx="20" fill="{CREAM_FIXED}" stroke="{FIXED_INK}" stroke-width="1.5"/>'
        f'<text class="mono" x="24" y="40" font-size="10" letter-spacing="1" fill="{FIXED_INK}">FASCICULE 01</text>'
        f'<g class="badge"><rect x="222" y="22" width="106" height="26" rx="13" fill="{ACTION}" stroke="{FIXED_INK}"/>'
        f'<text class="mono" x="275" y="39" text-anchor="middle" font-size="10" letter-spacing="1" fill="{FIXED_INK}">DÉCOUVERTE</text></g>'
        f'<text class="serif" x="22" y="112" font-size="50" font-weight="600" letter-spacing="-2" fill="{FIXED_INK}">télescope</text>'
        f'<text class="sans" x="24" y="146" font-size="14" fill="{FIXED_INK}">Instrument d’optique qui fait voir</text>'
        f'<text class="sans" x="24" y="166" font-size="14" fill="{FIXED_INK}">les objets éloignés.</text>'
        + chain
        + brick(24, 300, 104, 40, PREFIX, "", "télé-", THEMES[""], size=19, radius=6, shadow=3)
        + f'<text class="serif" x="146" y="328" font-size="24" fill="{FIXED_INK}">+</text>'
        + brick(170, 300, 120, 40, SUFFIX, "", "-scope", THEMES[""], size=19, radius=6, shadow=3)
        + '</g>')
    body = (
        f'<defs><radialGradient id="glow" cx="72%" cy="40%" r="55%"><stop offset="0" stop-color="{ACTION}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{ACTION}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="grid" width="56" height="56" patternUnits="userSpaceOnUse"><path d="M56 0H0V56" fill="none" stroke="{PAPER_FIXED}" stroke-opacity="0.055"/></pattern>'
        f'<clipPath id="clip"><rect width="1200" height="480" rx="14"/></clipPath></defs>'
        f'<g clip-path="url(#clip)"><rect width="1200" height="480" fill="{NIGHT}"/>'
        f'<rect width="1200" height="480" fill="url(#grid)"/><rect width="1200" height="480" fill="url(#glow)"/></g>'
        + seal(56, 46, 40)
        + f'<text class="serif" x="106" y="74" font-size="20" font-weight="700" letter-spacing="-0.2" fill="{PAPER_FIXED}">ÉtymoLogique</text>'
        f'<rect x="64.5" y="112.5" width="372" height="31" rx="15.5" fill="none" stroke="{PAPER_FIXED}" stroke-opacity="0.2"/>'
        f'<circle class="ping" cx="83" cy="128" r="4" fill="{ACTION}"/>'
        f'<text class="mono" x="97" y="132" font-size="11" letter-spacing="0.9" fill="#b8c6bd">JEU DE LOGIQUE · DÉCOUVERTE · COLLECTION</text>'
        f'<text class="serif" x="58" y="258" font-size="118" font-weight="600" letter-spacing="-6.5" fill="{PAPER_FIXED}">Étymo</text>'
        f'<text class="serif" x="108" y="356" font-size="118" font-weight="600" font-style="italic" letter-spacing="-6.5" fill="{ACTION}">Logique</text>'
        f'<text class="serif" x="64" y="410" font-size="22" fill="#b8c6bd">Comprendre comment les mots voyagent,</text>'
        f'<text class="serif" x="64" y="440" font-size="22" fill="#b8c6bd">se transforment et se composent.</text>'
        + hero_card)
    css = (f".badge{{animation:breathe 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}"
           "@keyframes breathe{50%{transform:scale(1.07)}}"
           f".ping{{animation:ping 2s {EASE_OUT} infinite;transform-box:fill-box;transform-origin:center}}"
           "@keyframes ping{0%{opacity:1}80%,100%{opacity:0.25}}")
    write("banner.svg", svg(1200, 480, body, "ÉtymoLogique : comprendre comment les mots voyagent, se transforment et se composent", css))


# ---------- Boutons (.btn-primary, .btn-secondary) ----------
ICONS = {
    "jouer": '<path d="M5 3v16l13-8z"/>',
    "cafe": '<path d="M2 7h14v6a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5z"/><path d="M16 9h2a3 3 0 0 1 0 6h-2" fill="none" stroke="currentColor" stroke-width="2"/>',
    "dossier": '<path d="M2 4h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2zM22 4h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/>',
}


def button(name, label, icon, primary):
    w = int(len(label) * 8.8 + 80)
    for suffix, t in THEMES.items():
        fg = FIXED_INK if primary else t["ink"]
        face = (f'<rect x="7" y="0.75" width="{w}" height="48" rx="12" fill="{ACTION}" stroke="{FIXED_INK}" stroke-width="1.5"/>'
                if primary else
                f'<rect x="0.75" y="0.75" width="{w}" height="48" rx="12" fill="none" stroke="{t["strong"]}" stroke-width="1.5"/>')
        shadow = (f'<rect x="11" y="4.75" width="{w}" height="48" rx="12" fill="{t["shadow"]}"/>' if primary else "")
        x0 = 7 if primary else 0.75
        body = (shadow + face
                + f'<g transform="translate({x0 + 22},14)" fill="{fg}" color="{fg}">{ICONS[icon]}</g>'
                + f'<text class="sans" x="{x0 + 54}" y="30" font-size="13" font-weight="800" letter-spacing="0.8" fill="{fg}">{label.upper()}</text>')
        write(f"btn-{name}{suffix}.svg", svg(w + 12, 54, body, label))


# ---------- 01 Le jeu : fusion animée ----------
def jeu():
    for suffix, t in THEMES.items():
        # Briques à la taille de leur contenu (.brick : rayon 10, ombre dure 4) ; le mot est une brique Crème (.brick[data-kind="mot"]).
        y, h = 178, 84
        body = (panel(400, "01 · LA TABLE DE FUSION", "Le jeu en ", "trente secondes", t)
                + brick(146, y, 189, h, PREFIX, "PRÉFIXE · GREC ANCIEN", "télé-", t, cls="b1")
                + f'<text class="serif" x="365" y="{y + 56}" text-anchor="middle" font-size="40" fill="{t["ink"]}">+</text>'
                + brick(395, y, 189, h, SUFFIX, "SUFFIXE · GREC ANCIEN", "-scope", t, cls="b2")
                + f'<text class="serif" x="614" y="{y + 56}" text-anchor="middle" font-size="40" fill="{t["ink"]}">=</text>'
                + brick(644, y, 210, h, CREAM_FIXED, "DÉCOUVERTE · FRANÇAIS", "télescope", t, cls="res", dot=True)
                + f'<line x1="36" x2="964" y1="318" y2="318" stroke="{t["line"]}" stroke-width="1.5"/>'
                + f'<text class="sans" x="36" y="358" font-size="16" fill="{t["ink2"]}">Se tromper ne coûte rien : seule une découverte consomme un exemplaire de chaque brique.</text>')
        css = (f".b1,.b2{{animation:2.6s {EASE_SPRING} infinite alternate}}.b1{{animation-name:in1}}.b2{{animation-name:in2}}"
               "@keyframes in1{0%,30%{transform:translateX(-14px)}100%{transform:none}}"
               "@keyframes in2{0%,30%{transform:translateX(14px)}100%{transform:none}}"
               f".res{{animation:pop 2.6s {EASE_SPRING} infinite alternate;transform-box:fill-box;transform-origin:center}}"
               "@keyframes pop{0%,60%{opacity:0;transform:scale(0.85) rotate(-3deg)}100%{opacity:1;transform:none}}")
        write(f"jeu{suffix}.svg", svg(1000, 400, body, "Table de fusion : télé- plus -scope donne télescope", css))


# ---------- 02 Piliers ----------
PILLAR_ICONS = [
    '<circle cx="12" cy="12" r="8"/><path d="M18 18l8 8"/>',
    '<path d="M10 2h8M12 2v8L4 26h20L16 10V2"/>',
    '<path d="M4 4h10v10H4zM14 14h10v10H14z"/>',
    '<path d="M4 4h8v8H4zM16 4h8v8h-8zM4 16h8v8H4zM16 16h8v8h-8z"/>',
    '<path d="M3 6h22v13H13l-6 5v-5H3z"/>',
    '<path d="M3 24l7-9 6 4 9-14"/>',
]
PILLARS = [
    ("Déduction", "Une découverte s’anticipe", "à partir d’indices cohérents."),
    ("Expérimentation", "Une tentative est rapide.", "Se tromper ne coûte rien."),
    ("Rareté des briques", "Chaque exemplaire compte ;", "seuls les plis en redonnent."),
    ("Collection", "Chaque découverte complète", "un codex lisible."),
    ("Transmission", "Le résultat explique la", "filiation sans casser le rythme."),
    ("Progression maîtrisée", "Aucune brique impossible,", "aucune attente sans fin."),
]


def piliers():
    for suffix, t in THEMES.items():
        body = panel(530, "02 · LA BOUSSOLE", "Pourquoi on ", "y revient", t)
        for i, (title, l1, l2) in enumerate(PILLARS):
            x, y = 36 + (i % 3) * 316, 146 + (i // 3) * 182
            body += (card(x, y, 296, 164, t)
                     + f'<text class="mono" x="{x + 22}" y="{y + 34}" font-size="11" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">PILIER 0{i + 1}</text>'
                     + f'<g transform="translate({x + 248},{y + 18})" fill="none" stroke="{t["ink"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{PILLAR_ICONS[i]}</g>'
                     + f'<text class="serif" x="{x + 22}" y="{y + 84}" font-size="25" font-weight="600" letter-spacing="-0.5" fill="{t["ink"]}">{title}</text>'
                     + f'<text class="sans" x="{x + 22}" y="{y + 116}" font-size="15" fill="{t["ink2"]}">{l1}</text>'
                     + f'<text class="sans" x="{x + 22}" y="{y + 138}" font-size="15" fill="{t["ink2"]}">{l2}</text>')
        write(f"piliers{suffix}.svg", svg(1000, 530, body, "Six piliers : déduction, expérimentation, rareté des briques, collection, transmission, progression maîtrisée"))


# ---------- 03 Engagements : pastilles ----------
PROMISES = ["Gratuit", "Sans publicité", "Aucun avantage payant", "Compte facultatif", "Aucun traceur tiers", "Code libre · AGPL 3.0"]


def respect():
    for suffix, t in THEMES.items():
        body = panel(282, "03 · ENGAGEMENTS", "Un jeu qui ", "respecte", t, after=" ses joueurs")
        for i, label in enumerate(PROMISES):
            x, y = 36 + (i % 3) * 316, 146 + (i // 3) * 62
            body += (f'<rect x="{x}" y="{y}" width="296" height="46" rx="23" fill="none" stroke="{t["strong"]}" stroke-width="1.5"/>'
                     f'<rect x="{x + 20}" y="{y + 19}" width="8" height="8" fill="{t["ink"]}" transform="rotate(45 {x + 24} {y + 23})"/>'
                     f'<text class="mono" x="{x + 42}" y="{y + 28}" font-size="12" letter-spacing="0.7" fill="{t["ink"]}">{label.upper()}</text>')
        write(f"respect{suffix}.svg", svg(1000, 282, body, "Gratuit, sans publicité, aucun avantage payant, compte facultatif, aucun traceur tiers, code libre"))


# ---------- 04 Sous le capot ----------
STACK = [("PWA", "React · TypeScript · Vite, installable"),
         ("API", "Rust · axum · sqlx, autoritaire sur toute mutation"),
         ("Données", "PostgreSQL, catalogue statique servi par CDN"),
         ("Infra", "Terraform · Scaleway · GitHub Actions"),
         ("Décisions", "Plus de soixante-dix ADR publiés")]


def capot():
    for suffix, t in THEMES.items():
        body = panel(430, "04 · ARCHITECTURE", "Sous le ", "capot", t)
        for i, (k, v) in enumerate(STACK):
            y = 140 + i * 56
            body += (f'<line x1="36" x2="964" y1="{y}" y2="{y}" stroke="{t["line"]}" stroke-width="1.5"/>'
                     f'<text class="mono" x="36" y="{y + 35}" font-size="12" letter-spacing="1.4" fill="{t["ink3"]}">{k.upper()}</text>'
                     f'<text class="sans" x="200" y="{y + 36}" font-size="18" fill="{t["ink"]}">{v}</text>')
        body += f'<line x1="36" x2="964" y1="{140 + 5 * 56}" y2="{140 + 5 * 56}" stroke="{t["line"]}" stroke-width="1.5"/>'
        write(f"capot{suffix}.svg", svg(1000, 430, body, "PWA React, API Rust, PostgreSQL, Terraform sur Scaleway, plus de soixante-dix ADR"))


# ---------- 05 Soutien Ko-fi : carte à bandeau Corail ----------
def soutien():
    for suffix, t in THEMES.items():
        cup = (f'<g transform="translate(64,170) scale(1.3)" fill="{FIXED_INK}">{ICONS["cafe"].replace("currentColor", FIXED_INK)}'
               + "".join(f'<path class="s{i}" d="M{5 + i * 4} 4q-1.5 -2 0 -4" fill="none" stroke="{FIXED_INK}" stroke-width="1.6" stroke-linecap="round"/>' for i in range(3))
               + '</g>')
        body = (panel(436, "05 · SOUTENIR", "Un café pour les ", "prochains fascicules", t)
                + f'<clipPath id="c"><rect x="36" y="140" width="928" height="260" rx="14"/></clipPath>'
                + card(36, 140, 928, 260, t)
                + f'<rect x="36" y="140" width="928" height="64" fill="{ACTION}" clip-path="url(#c)"/>'
                + f'<line x1="36" x2="964" y1="204" y2="204" stroke="{t["strong"]}" stroke-width="1.5"/>'
                + f'<rect x="36" y="140" width="928" height="260" rx="14" fill="none" stroke="{t["strong"]}" stroke-width="1.5"/>'
                + cup
                + f'<text class="mono" x="112" y="178" font-size="12" font-weight="700" letter-spacing="1.5" fill="{FIXED_INK}">KO-FI · LUNIK_TIWABBIT</text>'
                + f'<text class="sans" x="64" y="250" font-size="18" fill="{t["ink"]}">ÉtymoLogique est fait par une seule personne, sur son temps libre.</text>'
                + f'<text class="sans" x="64" y="280" font-size="18" fill="{t["ink2"]}">Un don finance l’hébergement. Il ne change rien à votre partie.</text>'
                + f'<rect x="68" y="320" width="300" height="48" rx="12" fill="{t["shadow"]}"/>'
                + f'<rect x="64" y="316" width="300" height="48" rx="12" fill="{ACTION}" stroke="{FIXED_INK}" stroke-width="1.5"/>'
                + f'<g transform="translate(86,329)" fill="{FIXED_INK}" color="{FIXED_INK}">{ICONS["cafe"]}</g>'
                + f'<text class="sans" x="118" y="345" font-size="13" font-weight="800" letter-spacing="0.8" fill="{FIXED_INK}">OFFRIR UN CAFÉ SUR KO-FI</text>')
        css = "".join(f".s{i}{{animation:steam 2.4s ease-in-out {i * 0.5}s infinite}}" for i in range(3)) + "@keyframes steam{0%,100%{opacity:0}50%{opacity:1}}"
        write(f"soutien{suffix}.svg", svg(1000, 436, body, "Soutenir ÉtymoLogique sur Ko-fi", css))


# ---------- Bandeaux défilants (.marquee), identiques dans les deux thèmes ----------
def bandeaux():
    def track(fill, star, y, cls):
        unit = (f'ÉtymoLogique · remonter le fil <tspan fill="{star}">✦</tspan> Chaque mot est une '
                f'<tspan font-style="italic">piste</tspan>. <tspan fill="{star}">✦</tspan> ')
        return f'<text class="serif {cls}" x="0" y="{y}" font-size="30" fill="{fill}">{unit * 4}</text>'
    body = (f'<g transform="rotate(-1.4 500 60)"><rect x="-40" y="28" width="1080" height="60" fill="{FIXED_INK}"/>{track(PAPER_FIXED, ACTION, 69, "t1")}</g>'
            f'<g transform="rotate(1 500 120)"><rect x="-40" y="94" width="1080" height="60" fill="{ACTION}" stroke="{FIXED_INK}" stroke-width="1.5"/>{track(FIXED_INK, FIXED_INK, 135, "t2")}</g>')
    css = ".t1{animation:marq 40s linear infinite}.t2{animation:marq 52s linear infinite reverse}@keyframes marq{to{transform:translateX(-50%)}}"
    write("bandeaux.svg", svg(1000, 180, body, "ÉtymoLogique · remonter le fil · Chaque mot est une piste", css))


if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        old.unlink()
    banner()
    button("jouer", "Jouer", "jouer", True)
    button("kofi", "Offrir un café", "cafe", False)
    button("dossier", "Dossier de conception", "dossier", False)
    jeu(); piliers(); respect(); capot(); soutien(); bandeaux()
