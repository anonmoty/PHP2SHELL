"""LFI / RFI Scanner — PHP include vulnerabilities"""
from core.config import LFI_PAYLOADS, LFI_PARAMS, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, save_report, print_vuln

def run(target):
    print(f"\n{B2}  Scanning LFI/RFI vulnerabilities on {W}{target}{N}")
    vulns = 0
    findings = []

    lfi_markers = ["root:x:0:0:", "root:*:0:0:", "daemon:", "nobody:",
                   "www-data:", "bin:x:", "sys:x:",
                   "Linux version", "processor\t:", "MemTotal:"]

    tested = 0
    for param in LFI_PARAMS:
        for payload in LFI_PAYLOADS[:8]:  # Top 8 payloads per param
            url = f"{target}/index.php?{param}={payload}"
            code, hdrs, body = http_get(url, timeout=8)
            tested += 1
            if code == 0:
                continue

            if any(m in body for m in lfi_markers):
                print_vuln("CRITICAL", f"LFI via ?{param}=",
                           f"Payload: {payload[:50]}", url)
                vulns += 1
                findings.append({"type": "lfi", "param": param,
                                 "payload": payload, "url": url,
                                 "severity": "CRITICAL"})
                break  # Found LFI on this param, move to next

            # Check for base64 encoded PHP source
            if "PD9waH" in body or "<?php" in body:
                if param in ("file", "page", "include", "path"):
                    print_vuln("HIGH", f"Source code disclosure via ?{param}=",
                               "PHP source visible", url)
                    vulns += 1
                    findings.append({"type": "source_disclosure", "param": param, "url": url})
                    break

        if tested % 50 == 0:
            print(f"   {D}... tested {tested} combinations{N}")

    # Test common LFI endpoints
    lfi_paths = [
        "/view.php", "/page.php", "/include.php", "/load.php",
        "/read.php", "/show.php", "/download.php", "/get.php",
        "/template.php", "/layout.php", "/content.php",
    ]
    for path in lfi_paths:
        for payload in LFI_PAYLOADS[:4]:
            url = f"{target}{path}?file={payload}"
            code, hdrs, body = http_get(url, timeout=8)
            if code == 0: continue
            if any(m in body for m in lfi_markers):
                print_vuln("CRITICAL", f"LFI on {path}?file=", url)
                vulns += 1
                findings.append({"type": "lfi_endpoint", "url": url})
                break

    print(f"\n{G}  [✓] LFI/RFI scan complete — {vulns} findings ({tested} tests){N}")
    if findings:
        save_report("lfi_rfi", {"target": target, "findings": findings})
    return vulns
