import json
import requests
import re  # Import modul re untuk ekspresi reguler

def extract_ip_and_format(line):
    """Ekstrak IP dan port dari berbagai format proxy dan kembalikan bersama format aslinya."""
    pattern = r'(?:http|socks4|socks5)://(?:\w*:?[\w]*@)?([\d\.]+:\d+)'
    match = re.search(pattern, line)
    if match:
        return match.group(1), line.strip()  # Kembalikan IP:port dan format asli
    return None, None

def read_proxy_file(filename):
    """Membaca file proxy dan menyimpannya dalam dictionary."""
    proxy_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            ip_port, original_format = extract_ip_and_format(line)
            if ip_port:
                proxy_dict[ip_port] = original_format  # Simpan dengan kunci IP:port
    return proxy_dict

def main():
    cookie_file = "cookie.json"
    proxy_file = "proxy.txt"
    output_file = "ipgood.txt"

    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "id,en-US;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": cookie_string
    }
    
    response = requests.get("https://api.getgrass.io/users/dash", headers=headers)
    data = response.json()
    
    devices = data.get('data', {}).get('devices', [])
    proxy_data = read_proxy_file(proxy_file)

    with open(output_file, 'w') as outfile:
        for device in devices:
            if device.get("is_proxy") is None:
                ip = device.get("device_ip")
                ip_found = False
                for ip_port in proxy_data.keys():
                    if ip in ip_port:
                        outfile.write(proxy_data[ip_port] + "\n")
                        print(f"Format proxy untuk IP {ip} disimpan.")
                        ip_found = True
                        break
                if not ip_found:
                    # Jika IP tidak ditemukan dalam proxy.txt, simpan saja IP-nya
                    outfile.write(ip + "\n")
                    print(f"IP {ip} disimpan karena tidak ditemukan dalam proxy.txt.")

if __name__ == "__main__":
    main()
