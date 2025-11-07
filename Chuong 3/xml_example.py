import xml.etree.ElementTree as ET
tree = ET.parse('sinhvien.xml')
root = tree.getroot()

for sv in root.findall('sinhvien'):
    name = sv.find('ten').text
    print(name)

sv = root.find("sinhvien[@id='SV02']")

root = ET.Element('DS_SV')
ma_sv = ET.SubElement(root, 'ma_sv')
