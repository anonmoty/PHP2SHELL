import urllib.request, urllib.parse, urllib.error, ssl, json, os, time, re
import socket, datetime
from core.config import R, R2, B, B2, W, Y, G, D, N

# SSL bypass context
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def http_get(url, timeout=12, headers=None):
    """GET request → (status, headers_dict, body_str)"""
    hdrs = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=CTX)
        body = resp.read().decode(errors="replace")
        rh = {k.lower(): v for k, v in resp.getheaders()}
        return resp.getcode(), rh, body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode(errors="replace")
            rh = {k.lower(): v for k, v in e.headers.items()}
        except:
            body = ""; rh = {}
        return e.code, rh, body
    except Exception:
        return 0, {}, ""

def http_post(url, data, timeout=12, content_type="application/x-www-form-urlencoded"):
    """POST request → (status, headers_dict, body_str)"""
    hdrs = {"User-Agent": "Mozilla/5.0", "Content-Type": content_type}
    if isinstance(data, str):
        data = data.encode()
    req = urllib.request.Request(url, data=data, headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=CTX)
        body = resp.read().decode(errors="replace")
        rh = {k.lower(): v for k, v in resp.getheaders()}
        return resp.getcode(), rh, body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode(errors="replace")
            rh = {k.lower(): v for k, v in e.headers.items()}
        except:
            body = ""; rh = {}
        return e.code, rh, body
    except Exception:
        return 0, {}, ""

def http_upload(url, field_name, filename, content, timeout=15):
    """Multipart file upload → (status, body_str)"""
    boundary = "----Php2Shell" + str(int(time.time()))
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f"Content-Type: application/x-php\r\n\r\n"
        f"{content}\r\n"
        f"--{boundary}--\r\n"
    ).encode()
    hdrs = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(url, data=body, headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=CTX)
        return resp.getcode(), resp.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        try: return e.code, e.read().decode(errors="replace")
        except: return e.code, ""
    except Exception:
        return 0, ""

def get_php_version(headers, body):
    """Extract PHP version from headers/body"""
    # X-Powered-By header
    xpb = headers.get("x-powered-by", "")
    m = re.search(r"PHP/(\d+\.\d+(?:\.\d+)?)", xpb)
    if m: return m.group(1)
    # Server header
    srv = headers.get("server", "")
    m = re.search(r"PHP/(\d+\.\d+(?:\.\d+)?)", srv)
    if m: return m.group(1)
    # phpinfo() output
    m = re.search(r"PHP Version\s*</td><td[^>]*>(\d+\.\d+(?:\.\d+)?)", body)
    if m: return m.group(1)
    m = re.search(r"PHP Version (\d+\.\d+(?:\.\d+)?)", body)
    if m: return m.group(1)
    return None

def get_server_info(headers):
    """Extract server technology"""
    info = {}
    info["server"] = headers.get("server", "unknown")
    info["x-powered-by"] = headers.get("x-powered-by", "")
    info["x-aspnet"] = headers.get("x-aspnet-version", "")
    info["x-generator"] = headers.get("x-generator", "")
    return info

def save_report(name, data):
    """Save scan results to loot/"""
    loot = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "loot")
    os.makedirs(loot, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{name}_{ts}.json"
    path = os.path.join(loot, fname)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n{G}  [✓] Report saved: loot/{fname}{N}")
    return path

def print_vuln(severity, title, detail, url=""):
    """Print a vulnerability finding"""
    colors = {"CRITICAL": R, "HIGH": R2, "MEDIUM": O, "LOW": Y, "INFO": B2}
    c = colors.get(severity, W)
    print(f"  {c}[{severity}]{W} {title}{N}")
    if detail:
        print(f"   {D}└─ {detail}{N}")
    if url:
        print(f"   {D}   URL: {url}{N}")

def resolve_host(url):
    """Get IP from URL"""
    try:
        host = urllib.parse.urlparse(url).hostname
        return socket.gethostbyname(host)
    except:
        return "unknown"
