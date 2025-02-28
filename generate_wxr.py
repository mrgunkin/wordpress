from xml.etree import ElementTree as ET
from datetime import datetime
import re

# Создаём корневой элемент RSS
rss = ET.Element("rss", version="2.0")
rss.set("xmlns:excerpt", "http://wordpress.org/export/1.2/excerpt/")
rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
rss.set("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
rss.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
rss.set("xmlns:wp", "http://wordpress.org/export/1.2/")

channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "wp:wxr_version").text = "1.2"
ET.SubElement(channel, "title").text = "Import Data"
ET.SubElement(channel, "link").text = "http://example.com"  # Замените на свой сайт, если нужно
ET.SubElement(channel, "description").text = "Imported content"

# Читаем текст из файла
with open('input.txt', 'r', encoding='utf-8') as file:
    lines = file.read().split('---\n')

for post_id, post in enumerate(lines, start=1):  # Уникальный ID для каждого поста
    if post.strip():
        # Разделяем строки
        lines = post.strip().split('\n')
        title_text = lines[0]
        content_text = lines[1]
        
        # Ищем SEO-данные
        seo_title = re.search(r'SEO Title: (.*)', post)
        meta_desc = re.search(r'Meta Description: (.*)', post)
        keywords = re.search(r'Keywords: (.*)', post)
        
        # Создаём элемент поста
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title_text
        ET.SubElement(item, "link").text = f"http://example.com/?p={post_id}"
        ET.SubElement(item, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        ET.SubElement(item, "dc:creator").text = "admin"  # Укажите нужного автора
        ET.SubElement(item, "guid", isPermaLink="false").text = f"http://example.com/?p={post_id}"
        ET.SubElement(item, "description").text = ""
        ET.SubElement(item, "content:encoded").text = f"<![CDATA[{content_text}]]>"
        ET.SubElement(item, "excerpt:encoded").text = "<![CDATA[]]>"
        ET.SubElement(item, "wp:post_id").text = str(post_id)
        ET.SubElement(item, "wp:post_date").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:post_date_gmt").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(item, "wp:comment_status").text = "open"
        ET.SubElement(item, "wp:ping_status").text = "open"
        ET.SubElement(item, "wp:post_name").text = title_text.lower().replace(" ", "-")
        ET.SubElement(item, "wp:status").text = "publish"
        ET.SubElement(item, "wp:post_parent").text = "0"
        ET.SubElement(item, "wp:menu_order").text = "0"
        ET.SubElement(item, "wp:post_type").text = "post"
        ET.SubElement(item, "wp:post_password").text = ""
        ET.SubElement(item, "wp:is_sticky").text = "0"

        # Добавляем мета-поля для All in One SEO
        if seo_title:
            meta = ET.SubElement(item, "wp:postmeta")
            ET.SubElement(meta, "wp:meta_key").text = "_aioseo_title"
            ET.SubElement(meta, "wp:meta_value").text = f"<![CDATA[{seo_title.group(1)}]]>"
        
        if meta_desc:
            meta = ET.SubElement(item, "wp:postmeta")
            ET.SubElement(meta, "wp:meta_key").text = "_aioseo_description"
            ET.SubElement(meta, "wp:meta_value").text = f"<![CDATA[{meta_desc.group(1)}]]>"
        
        if keywords:
            meta = ET.SubElement(item, "wp:postmeta")
            ET.SubElement(meta, "wp:meta_key").text = "_aioseo_keywords"
            ET.SubElement(meta, "wp:meta_value").text = f"<![CDATA[{keywords.group(1)}]]>"

# Сохраняем в файл
tree = ET.ElementTree(rss)
tree.write("wordpress_import.xml", encoding="utf-8", xml_declaration=True)

print("WXR файл для импорта создан: wordpress_import.xml")
