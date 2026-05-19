from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".github",
    "assets",
    "scripts",
    "__pycache__"
}

TOP_DESCRIPTIONS = {
    "Book-Chapters": "Published book chapters and edited volume contributions.",
    "Conference-Publications": "Conference papers and proceedings.",
    "ExamArchive": "Exam archive materials.",
    "Journal-Publications": "Journal articles and related publications.",
    "Presentations": "Academic and technical presentations.",
    "Projects": "Research projects and project materials.",
    "Technical-Reports": "Technical reports and documentation.",
    "Theses": "Theses and dissertation-related materials."
}


def pretty_name(name: str) -> str:
    return name.replace("-", " ").replace("_", " ")


def has_skipped_part(path: Path) -> bool:
    if path == ROOT:
        return False

    parts = path.relative_to(ROOT).parts

    for part in parts:
        if part in SKIP_DIRS or part.startswith("."):
            return True

    return False


def rel_root_prefix(directory: Path) -> str:
    depth = len(directory.relative_to(ROOT).parts)
    return "../" * depth


def rel_css_path(directory: Path) -> str:
    return rel_root_prefix(directory) + "assets/css/style.css"


def is_visible_dir(path: Path) -> bool:
    return path.is_dir() and not has_skipped_part(path)


def is_visible_file(path: Path) -> bool:
    return (
        path.is_file()
        and path.name != "index.html"
        and not path.name.startswith(".")
    )


def breadcrumb(directory: Path) -> str:
    if directory == ROOT:
        return "Home"

    parts = directory.relative_to(ROOT).parts
    html = [f'<a href="{rel_root_prefix(directory)}index.html">Home</a>']

    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            html.append(escape(pretty_name(part)))
        else:
            target_parts = parts[:i + 1]
            up = rel_root_prefix(directory)
            target = "/".join(quote(p) for p in target_parts)
            html.append(
                f'<a href="{up}{target}/index.html">{escape(pretty_name(part))}</a>'
            )

    return " / ".join(html)


def render_nav(directory: Path) -> str:
    root_prefix = rel_root_prefix(directory)

    return f'''
  <nav>
    <a href="{root_prefix}index.html">Home</a>
    <a href="{root_prefix}Book-Chapters/index.html">Book Chapters</a>
    <a href="{root_prefix}Conference-Publications/index.html">Conference Publications</a>
    <a href="{root_prefix}ExamArchive/index.html">Exam Archive</a>
    <a href="{root_prefix}Journal-Publications/index.html">Journal Publications</a>
    <a href="{root_prefix}Presentations/index.html">Presentations</a>
    <a href="{root_prefix}Projects/index.html">Projects</a>
    <a href="{root_prefix}Technical-Reports/index.html">Technical Reports</a>
    <a href="{root_prefix}Theses/index.html">Theses</a>
  </nav>
'''


def render_header(title: str, subtitle: str) -> str:
    return f'''
  <header>
    <h1>{escape(title)}</h1>
    <p>{escape(subtitle)}</p>
  </header>
'''


def render_home_page():
    title = "Olcay Taner Yıldız"
    subtitle = "Academic publications, projects, presentations, reports, theses, and related materials."

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
{render_header(title, subtitle)}
{render_nav(ROOT)}

  <main>
    <div class="home-layout">
      <aside class="profile-sidebar">
        <div class="photo-card">
          <img src="assets/img/profile.jpg" alt="Olcay Taner Yıldız">
          <div class="photo-caption">Olcay Taner YILDIZ</div>
        </div>

        <div class="contact-card">
          <p>☎ 02165649081</p>
          <p>✉ <a href="mailto:olcay.yildiz@ozyegin.edu.tr">olcay.yildiz@ozyegin.edu.tr</a></p>
        </div>
      </aside>

      <section class="profile-content">
        <div class="profile-heading">
          <h2>Olcay Taner YILDIZ</h2>
          <p>Professor (AI), <strong>Natural Language Processing</strong></p>
        </div>

        <div class="info-section">
          <div class="education-block">
            <h3>Ph.D.</h3>
            <p>Computer Engineering, Boğaziçi University, 2005</p>
          </div>

          <div class="education-block">
            <h3>M.Sc.</h3>
            <p>Computer Engineering, Boğaziçi University, 2000</p>
          </div>

          <div class="education-block">
            <h3>B.Sc.</h3>
            <p>Computer Engineering, Boğaziçi University, 1997</p>
          </div>
        </div>

        <div class="info-section">
          <h3>Biography</h3>
          <p>
            Olcay Taner Yıldız received his Ph.D. degree from the Department of
            Computer Engineering at Boğaziçi University and completed his postdoctoral
            research at the University of Minnesota in 2005. Between 2005 and 2020,
            he worked in the Department of Computer Engineering at Işık University.
            Since 2020, he has been serving as a professor at Özyeğin University.
            His research interests include natural language processing, machine
            learning, and bioinformatics.
          </p>
        </div>

        <div class="info-section">
          <h3>Research Interests</h3>
          <p>Natural language processing, machine learning, bioinformatics</p>
        </div>
      </section>
    </div>
  </main>

  <footer>
    © Olcay Taner Yıldız
  </footer>
</body>
</html>
'''

    (ROOT / "index.html").write_text(html, encoding="utf-8")


def render_folder_page(directory: Path):
    title = pretty_name(directory.name)
    subtitle = f"Contents of {pretty_name(directory.name)}."

    dirs = sorted(
        [p for p in directory.iterdir() if is_visible_dir(p)],
        key=lambda p: p.name.lower()
    )

    files = sorted(
        [p for p in directory.iterdir() if is_visible_file(p)],
        key=lambda p: p.name.lower()
    )

    folder_cards = ""
    if dirs:
        folder_cards += '<h2 class="section-title">Folders</h2>\n<div class="grid">\n'
        for d in dirs:
            desc = TOP_DESCRIPTIONS.get(d.name, "Open this folder to view its contents.")
            folder_cards += f'''
            <a class="card" href="{quote(d.name)}/index.html">
              <h3>{escape(pretty_name(d.name))}</h3>
              <p>{escape(desc)}</p>
            </a>
            '''
        folder_cards += "</div>\n"

    file_list = ""
    if files:
        file_list += '<h2 class="section-title">Files</h2>\n<div class="file-list">\n'
        for f in files:
            ext = f.suffix.upper().replace(".", "") or "FILE"
            file_list += f'''
            <a class="file-row" href="{quote(f.name)}" target="_blank">
              <span>{escape(f.name)}</span>
              <span class="badge">{escape(ext)}</span>
            </a>
            '''
        file_list += "</div>\n"

    if not dirs and not files:
        file_list = "<p>No files found in this folder.</p>"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{rel_css_path(directory)}">
</head>
<body>
{render_header(title, subtitle)}
{render_nav(directory)}

  <main>
    <div class="breadcrumb">{breadcrumb(directory)}</div>

    {folder_cards}

    {file_list}
  </main>

  <footer>
    © Olcay Taner Yıldız
  </footer>
</body>
</html>
'''

    (directory / "index.html").write_text(html, encoding="utf-8")


def generate_all():
    render_home_page()

    all_dirs = []

    for p in ROOT.rglob("*"):
        if is_visible_dir(p):
            all_dirs.append(p)

    for directory in all_dirs:
        render_folder_page(directory)


if __name__ == "__main__":
    generate_all()
    print("Site pages generated successfully.")