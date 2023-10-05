from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import json
import tkinter as tk
from tkinter import filedialog, Text, scrolledtext


def create_xml(data):
    nsmap = {
        "b": "http://schemas.openxmlformats.org/officeDocument/2006/bibliography",
        "ns1": "http://schemas.openxmlformats.org/officeDocument/2006/bibliography/bib1",
    }

    sources = Element("b:Sources", attrib={
        "xmlns:b": "http://schemas.openxmlformats.org/officeDocument/2006/bibliography",
        "xmlns:ns1": "http://schemas.openxmlformats.org/officeDocument/2006/bibliography/bib1"
    })

    for entry in data:
        source = SubElement(sources, 'b:Source')
        SubElement(source, 'b:Tag').text = entry['name'].split(',')[0].replace(" ", "") + entry['date']
        SubElement(source, 'b:SourceType').text = "Book"
        author = SubElement(source, 'b:Author')
        for auth in entry['author'].split('&'):
            ind_author = SubElement(author, 'b:Author')
            names = auth.strip().split()
            SubElement(ind_author, 'b:Last').text = names[1].replace(".", "")
            SubElement(ind_author, 'b:First').text = names[0]
        SubElement(source, 'b:Year').text = entry['date']
        SubElement(source, 'b:Title').text = entry['reference'].split(".")[0]
        SubElement(source, 'b:Publisher').text = entry['reference'].split('.')[1].strip()

    return parseString(tostring(sources)).toprettyxml(indent="  ")


def convert_json_to_xml():
    json_data = json_text.get("1.0", tk.END)
    data = json.loads(json_data)
    xml_content = create_xml(data)
    xml_text.delete("1.0", tk.END)
    xml_text.insert(tk.END, xml_content)


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as f:
            data = json.load(f)
            json_content = json.dumps(data, indent=4)
            json_text.delete("1.0", tk.END)
            json_text.insert(tk.END, json_content)


def save_xml_file():
    xml_data = xml_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(xml_data)

root = tk.Tk()
root.title("JSON to XML Converter")
root.geometry('800x600')

frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

json_frame = tk.Frame(frame, bg="lightgray", bd=2, relief=tk.GROOVE)
json_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

xml_frame = tk.Frame(frame, bg="lightgray", bd=2, relief=tk.GROOVE)
xml_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

json_label = tk.Label(json_frame, text="JSON Input", bg="lightgray")
json_label.pack(pady=10)

json_text = scrolledtext.ScrolledText(json_frame, wrap=tk.WORD, width=40, height=20)
json_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

xml_label = tk.Label(xml_frame, text="XML Output", bg="lightgray")
xml_label.pack(pady=10)

xml_text = scrolledtext.ScrolledText(xml_frame, wrap=tk.WORD, width=40, height=20)
xml_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=20)

open_btn = tk.Button(btn_frame, text="Open JSON File", command=open_file)
open_btn.pack(side=tk.LEFT, padx=10)

convert_btn = tk.Button(btn_frame, text="Convert JSON to XML", command=convert_json_to_xml)
convert_btn.pack(side=tk.LEFT, padx=10)

save_btn = tk.Button(btn_frame, text="Save XML File", command=save_xml_file)
save_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()