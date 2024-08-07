from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import re

app = Flask(__name__)

def natural_sort_key(s):
    """ Sort keys for natural sorting of filenames """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# SORT CHAPTERS
chapter_files = sorted(os.listdir("martial_god"), key=natural_sort_key)

def format_title(chapter_file):
    title = chapter_file.replace("p-m-u-", "P.M.U ")
    title = title.replace("-", " ").replace(".html", "").replace("_", "").title()
    return title

@app.route("/")
def index():
    return render_template('index.html', chapters=chapter_files)

@app.route("/martial_god/<chapter>")
def read_chapter(chapter):
    if chapter in chapter_files:
        current_index = chapter_files.index(chapter)
        next_chapter = chapter_files[current_index + 1] if current_index < len(chapter_files) - 1 else None
        prev_chapter = chapter_files[current_index - 1] if current_index > 0 else None
        formatted_title = format_title(chapter)
        
        # READ CONTENT!!!
        with open(os.path.join('martial_god', chapter), 'r', encoding='utf-8') as file:
            chapter_content = file.read()
        
        # REMOVE UGLY TITLE!!
        if "<h1>" in chapter_content and "</h1>" in chapter_content:
            chapter_content = chapter_content.split("</h1>", 1)[-1].strip()
        
        # REMOVE BIOGRAPHIA
        if "wp-biographia-container-around" in chapter_content:
            chapter_content = chapter_content.split('<div class="wp-biographia-container-around"', 1)[0].strip()
        
        # REMOVE AD SECTION!
        if '<hr class="wp-block-separator has-css-opacity"/>' in chapter_content:
            chapter_content = chapter_content.split('<hr class="wp-block-separator has-css-opacity"/>', 1)[0].strip()

        # REMOVE ADS!!!
        chapter_content = re.sub(r'<div class="code-block.*?</div>', '', chapter_content, flags=re.DOTALL)
        
        return render_template('reader.html', chapter_content=chapter_content, next_chapter=next_chapter, prev_chapter=prev_chapter, formatted_title=formatted_title)
    return redirect(url_for('index'))

@app.route("/martial_god/<filename>")
def chapters(filename):
    return send_from_directory('martial_god', filename)

if __name__ == "__main__":
    app.run(debug=True)
