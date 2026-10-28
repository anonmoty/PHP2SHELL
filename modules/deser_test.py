"""PHP Deserialization Vulnerability Tester"""
from core.config import DESER_PARAMS, DESER_PAYLOADS, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, http_post, save_report, print_vuln

DESER_ENDPOINTS = [
    "/index.php", "/api/data", "/api/session", "/login.php",
    "/process.php", "/handler.php", "/api/v1/data",
    "/cache.php", "/session.php", "/state.php",
    "/admin/process.php", "/api/config",
]

def run(target):
    print(f"\n{B2}  Testing PHP deserialization on {W}{target}{N}")
    vulns = 0
    findings = []

    # Test GET parameters with serialized payloads
    print(f"\n{D}  Testing GET deserialization injection...{N}")
    for ep in DESER_ENDPOINTS:
        for param in DESER_PARAMS:
            for payload in DESER_PAYLOADS[:2]:
                import urllib.parse
                encoded = urllib.parse.quote(payload)
                url = f"{target}{ep}?{param}={encoded}"
                code, hdrs, body = http_get(url, timeout=8)
                if code == 0:
                    continue

                # Error-based detection
                deser_errors = [
                    "unserialize()", "Error at offset",
                    "Incomplete allowed classes",
                    "__wakeup()", "__destruct()",
                    "Fatal error", "Class not found",
                    "Object of class",
                ]
                for err in deser_errors:
                    if err in body:
                        print_vuln("HIGH", f"Deserialization error via ?{param}=",
                                   f"Error: {err}", url)
                        vulns += 1
                        findings.append({"type": "deser_error", "param": param,
                                         "url": url, "error": err})
                        break

    # Test POST deserialization
    print(f"\n{D}  Testing POST deserialization injection...{N}")
    for ep in DESER_ENDPOINTS[:5]:
        for param in DESER_PARAMS[:5]:
            for payload in DESER_PAYLOADS[:2]:
                url = target + ep
                post_data = f"{param}={urllib.parse.quote(payload)}"
                code, hdrs, body = http_post(url, post_data, timeout=8)
                if code == 0:
                    continue

                if "unserialize()" in body or "Error at offset" in body:
                    print_vuln("HIGH", f"POST deserialization error via {param}",
                               url)
                    vulns += 1
                    findings.append({"type": "deser_post", "param": param, "url": url})
                    break

    # Test cookie-based deserialization
    print(f"\n{D}  Testing cookie deserialization...{N}")
    import urllib.parse
    for payload in DESER_PAYLOADS[:2]:
        cookie_val = urllib.parse.quote(payload)
        code, hdrs, body = http_get(target, headers={"Cookie": f"session={cookie_val}"})
        if code > 0 and ("unserialize()" in body or "Error at offset" in body):
            print_vuln("CRITICAL", "Cookie deserialization vulnerability!",
                       "Session cookie passed to unserialize()")
            vulns += 1
            findings.append({"type": "deser_cookie", "severity": "CRITICAL"})
            break

    print(f"\n{G}  [✓] Deserialization scan complete — {vulns} findings{N}")
    if findings:
        save_report("deserialization", {"target": target, "findings": findings})
    return vulns
