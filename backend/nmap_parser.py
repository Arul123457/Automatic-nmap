import xml.etree.ElementTree as ET

def extract_targets(nmap_xml_path):
    """
    Extracts IP and open ports from an Nmap XML file.
    Returns a list of dictionaries: { ip: ..., port: ... }
    """
    try:
        tree = ET.parse(nmap_xml_path)
        root = tree.getroot()

        targets = []

        for host in root.findall("host"):
            address = host.find("address")
            ip = address.get("addr") if address is not None else None
            if not ip:
                continue

            for port in host.findall(".//port"):
                state = port.find("state")
                if state is None or state.get("state") != "open":
                    continue

                port_id = port.get("portid")
                if port_id:
                    targets.append({
                        "ip": ip,
                        "port": port_id
                    })

        return targets

    except Exception as e:
        print(f"[ERROR] Failed to parse Nmap XML: {e}")
        return []
