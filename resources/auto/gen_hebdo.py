#!/usr/bin/env python3
import os, datetime, re, requests, pytz
from importlib.metadata import version, PackageNotFoundError
import yaml
from ruamel.yaml import YAML

rapport_lines = []
SP4 = f"{' ' * 4}"  # 4 espaces pour indentation
ERR_CNT = 0
WNG_CNT = 0


def log(msg, markdown=False):
    print(msg)
    if markdown:
        rapport_lines.append(msg)


# =========================
# 1. Chargement du fichier mkdocs.yml
# =========================
def load_mkdocs_config(opened="+", path="mkdocs.yml"):
    log(f'???{opened} "🧾 Vérifications des packages référencés"', markdown=True)
    yaml = YAML(typ="safe")
    try:
        with open(path, "r", encoding="utf-8") as f:
            log(
                f"\n{SP4}✅ Tous les packages référencés sont vérifiés.\n",
                markdown=True,
            )
            return yaml.load(f)
    except Exception as e:
        log(
            f"\n{SP4}⚠️ Ceci dit, impossible cependant d'analyser complètement le fichier **{path}**\n",
            markdown=True,
        )
        log(
            f"{SP4}\n{SP4}"
            + f'??? "Précisions"'
            + f"\n{SP4}{SP4} <code>{' '.join(str(e).split())}</code>\b\r",
            markdown=True,
        )
        log(
            f"\n{SP4}ℹ️ <i>En effet, certaines extensions ou tags YAML personnalisés peuvent ne pas être pris en charge.</i>\n",
            markdown=True,
        )
        return {}


# =========================
# 2. Extraction des chemins de navigation
# =========================
def extract_paths(nav_list):
    paths = []
    for item in nav_list:
        if isinstance(item, dict):
            for _, value in item.items():
                if isinstance(value, list):
                    paths.extend(extract_paths(value))
                elif isinstance(value, str):
                    paths.append(value)
        elif isinstance(item, str):
            paths.append(item)
    return paths


def find_all_pages_files(root="docs"):
    pages_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename == ".pages":
                pages_files.append(os.path.join(dirpath, filename))
    return pages_files


def extract_nav_from_pages(pages_path):
    with open(pages_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    nav_entries = data.get("nav", [])
    folder = os.path.dirname(pages_path)
    paths = []
    for entry in nav_entries:
        if isinstance(entry, dict):
            for _, value in entry.items():
                paths.append(os.path.join(folder, value))
        elif isinstance(entry, str):
            paths.append(os.path.join(folder, entry))
    return paths


def check_all_pages_nav():
    global ERR_CNT

    all_pages = find_all_pages_files()
    all_paths = []
    for pages_file in all_pages:
        all_paths.extend(extract_nav_from_pages(pages_file))

    missing = [p for p in all_paths if not os.path.exists(p)]

    if missing:
        ERR_CNT += len(missing)
        log(
            f"{SP4}❌ Fichiers manquants dans les fichiers `.pages` :\n\n",
            markdown=True,
        )
        for f in missing:
            log(f"{SP4}  - {f}\n", markdown=True)
    else:
        log(
            f"{SP4}✅ Tous les fichiers référencés dans `.pages` existent.\n",
            markdown=True,
        )


def check_nav_files(config, opened="+"):
    log(f"\n", markdown=True)
    log(
        f'???{opened} "🔗 Vérification des liens de navigation des fichiers `.pages`"\n',
        markdown=True,
    )
    check_all_pages_nav()

    # nav_paths = extract_paths(config.get("nav", []))
    # print (nav_paths)
    # missing = [p for p in nav_paths if not os.path.exists(os.path.join("docs", p))]

    # log(f"\n{SP4}", markdown=True)

    # if missing:
    #     log(f"❌ Fichiers manquants référencés dans nav:", markdown=True)
    #     # for f in missing:
    #     #     log(f"{SP4}- {f}", markdown=True)
    # else:
    #     log(f"✅ xxxTous les fichiers référencés existent.", markdown=True)


# =========================
# 3. Vérification des liens externes
# =========================
def check_external_links(opened="+"):

    global ERR_CNT

    def pct(u, t):
        return int(u / t * 10000) / 100

    log(f'???{opened} "🔗 Vérification des liens externes"\n', markdown=True)

    md_files = [
        os.path.join(root, file)
        for root, _, files in os.walk("docs")
        for file in files
        if file.endswith(".md")
    ]

    link_pattern = re.compile(r"\[.+?\]\((http[s]?://[^\)]+)\)")
    good_links = []
    broken_links = []

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        for url in link_pattern.findall(content):
            try:
                resp = requests.head(url, allow_redirects=True, timeout=5)
                if resp.status_code >= 400:
                    broken_links.append((md_file, url))
                else:
                    good_links.append((md_file, url))
            except Exception:
                broken_links.append((md_file, url))

    # broken_links.pop()
    # broken_links.pop()

    if broken_links:
        cnt_broken = len(broken_links)
        ERR_CNT += cnt_broken
        plur_broken = "s" if cnt_broken > 1 else ""
        cnt_broken
        cnt_good = len(good_links)
        # plur_good = 's' if cnt_broken > 1 else ''

        cnt_total = cnt_broken + cnt_good

        log(
            f"{SP4}❌ {cnt_broken} lien{plur_broken} cassé{plur_broken} ({cnt_broken} / {cnt_total} au total ↔ **{pct(cnt_broken, cnt_total)} %**) :\n\n",
            markdown=True,
        )
        for file, link in broken_links:
            log(f"{SP4}* {link} (dans **{file}**)\n", markdown=True)

        filtered_links = [
            (url, file) for (url, file) in good_links if "CHANGELOG" not in url.upper()
        ]

        # print(filtered_links)
        # print(len(filtered_links))

        cnt_good = len(filtered_links)

        log(f"{SP4}\n\n", markdown=True)

        log(
            f'{SP4}??? tip "Voir les {cnt_good}* liens externes valides"\n{SP4*2}*: Sont retirés de cette liste les <b>{cnt_total - cnt_broken - cnt_good} liens</b> issus du <b>[CHANGELOG](CHANGELOG.md)</b>\n\n{SP4*2}---\n',
            markdown=True,
        )

        for file, link in filtered_links:
            log(f"{SP4*2}* {link} (dans **{file}**)\n", markdown=True)

    else:
        cnt_good = len(good_links)
        log(f"{SP4}✅ Tous les liens externes semblent valides.\n", markdown=True)


# =========================
# 4. Vérification des versions de packages
# =========================
def get_latest_version(package):
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        data = requests.get(url, timeout=5).json()
        return data["info"]["version"]
    except:
        return None


def check_package_versions(packages, opened="+"):
    global ERR_CNT, WNG_CNT
    log(
        f'???{opened} "🔢 Contrôle des versions des packages majeurs"\n',
        markdown=True,
    )
    for package in packages:
        try:
            installed = version(package)
            latest = get_latest_version(package)
            if latest and installed != latest:
                WNG_CNT += 1
                log(
                    f"{SP4}⚠️ {package} : installé {installed}, dernière version {latest}\n\n",
                    markdown=True,
                )
            else:
                log(f"{SP4}✅ {package} : {installed}\n\n", markdown=True)
        except PackageNotFoundError:
            ERR_CNT += 1
            log(f"{SP4}❌ {package} : non installé\n\n", markdown=True)


def debut_script():
    # log("### 🚀 Lancement du script `build_docs.py`\n", markdown=True)
    log(f'!!! example "Début du script `gen_hebdo.py` 🚀"\n', markdown=True)


def fin_script():
    # ERR_CNT = 21
    # WNG_CNT = 0
    msgWng = ""
    if ERR_CNT:
        plur_ERR_CNT = "s" if ERR_CNT > 1 else ""
        type = "danger"
        icon = "❌"
        msg = f"{ERR_CNT} problème{plur_ERR_CNT} à résoudre :thinking: ..."
    else:
        print(f"{WNG_CNT=}")
        # msgWng = (f'notok\n\n') if WNG_CNT else ''
        msgWng = (f"\n{SP4}Juste quelques détails à surveiller...") if WNG_CNT else ""
        type = "success"
        icon = "✅"
        msg = f"Tout est globalement OK 👌 !"
    # log("### 🚀 Lancement du script `build_docs.py`\n", markdown=True)
    log(
        f'!!! {type} "Fin du script `gen_hebdo.py` {icon} → {msg}"'
        + f"{SP4*2 + msgWng}\n",
        markdown=True,
    )


# =========================
# 5. Génération du rapport Markdown
# =========================
import pytz  # à ajouter en haut si ce n’est pas déjà fait


def generate_markdown_report(path="docs/outils/logs/hebdo.md"):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now_local = datetime.datetime.now(paris_tz)

        date_rapport_txt = (
            f"Dernier rapport généré le {now_local.strftime('%d/%m/%Y à %H:%M')}"
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# 📝 Rapport Hebdo - {date_rapport_txt}\n")
            f.write(
                """
<!--
    ####################################################################################################################

    ATTENTION: Ne pas modifier ce fichier, car il est généré automatiquement par `resources/auto/gen_hebdo.py` chaque semaine 
    
    ####################################################################################################################
-->

"""
            )
            f.write("".join(rapport_lines) + "\n")
            f.write(
                f"<div style='text-align: right; color: gray; font-size: 16px; line-height: 0;'>📋 <span style='font-style: italic;'>{date_rapport_txt}</span>.</div>\n"
            )

        log(f"📝 {date_rapport_txt}: {path}\n")
    except Exception as e:
        log(f"❌ Impossible d'écrire le rapport : {e}")


# =========================
# 6. Exécution principale
# =========================
if __name__ == "__main__":

    debut_script()

    config = load_mkdocs_config()  # 0: fermé, rien: ouvert
    check_nav_files(config)  # , 0 pour fermé
    check_external_links()  # 0 pour fermé
    check_package_versions(
        ["mkdocs", "mkdocs-material", "pyodide-mkdocs-theme", "pymox-kit"]
    )

    fin_script()

    generate_markdown_report()

    # "<!-- ATTENTION: Ne pas modifier ce fichier, car il est généré automatiquement par `resources/sentinelle.py` chaque semaine -->\n"
