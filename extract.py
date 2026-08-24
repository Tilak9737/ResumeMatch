import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('ResumeMatch_7-Day_Data_Science_Product_Sprint_Plan.docx', 'r') as docx:
    xml_content = docx.read('word/document.xml')
    tree = ET.XML(xml_content)
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text = '\n'.join([t.text for t in tree.findall('.//w:t', namespace) if t.text])
with open('sprint_plan_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(text)
