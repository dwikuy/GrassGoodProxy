import json
import requests

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    proxy_dict = {}
    for proxy in proxies:
        # Extract the IP for matching; maintain full proxy detail for storage
        if proxy.startswith(('http://', 'socks5://', 'socks4://')):
            proxy_parts = proxy.split('@')[-1] if '@' in proxy else proxy.split('//')[-1]
            ip = proxy_parts.split(':')[0]
            proxy_dict[ip] = proxy.strip()  # Store full proxy string
    return proxy_dict

def main():
    cookie_file = "cookie.json"
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
    proxies = load_proxies("proxy.txt")
    
    with open("ipjoss.txt", 'w') as outfile:
        for device in devices:
            if device.get("is_proxy") is None:
                ip = device.get("device_ip")
                if ip in proxies:
                    outfile.write(proxies[ip] + "\n")
                    print(f"Proxy {proxies[ip]} disimpan.")
                else:
                    outfile.write(ip + "\n")
                    print(f"IP {ip} disimpan.")

if __name__ == "__main__":
    main()
