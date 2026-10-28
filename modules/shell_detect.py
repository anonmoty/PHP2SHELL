"""Webshell Detector — scan for existing PHP shells"""
from core.config import WEBSHELL_PATHS, WEBSHELL_SIGNATURES, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, save_report, print_vuln

def run(target):
    print(f"\n{B2}  Scanning for existing webshells on {W}{target}{N}")
    vulns = 0
    findings = []

    print(f"\n{D}  Checking {len(WEBSHELL_PATHS)} common shell paths...{N}")
    for path in WEBSHELL_PATHS:
        url = target + path
        code, hdrs, body = http_get(url, timeout=8)
        if code == 0 or code == 404:
            continue
        if code != 200:
            continue

        # Check for shell signatures in response
        matched_sigs = []
        for sig in WEBSHELL_SIGNATURES:
            if sig in body:
                matched_sigs.append(sig)

        # Shell indicators
        shell_indicators = [
            "c99" in body.lower(), "r57" in body.lower(),
            "b374k" in body.lower(), "wso " in body.lower(),
            "webshell" in body.lower(), "backdoor" in body.lower(),
            "file manager" in body.lower() and "upload" in body.lower(),
            "server info" in body.lower() and "execute" in body.lower(),
            "cmd" in body.lower() and "exec" in body.lower(),
            len(matched_sigs) >= 3,
        ]

        if any(shell_indicators):
            print_vuln("CRITICAL", f"Possible webshell detected: {path}",
                       f"Signatures: {', '.join(matched_sigs[:5])}", url)
            vulns += 1
            findings.append({"type": "webshell", "url": url,
                             "signatures": matched_sigs, "severity": "CRITICAL"})
        elif len(matched_sigs) >= 2 and len(body) < 5000:
            print_vuln("HIGH", f"Suspicious PHP file: {path}",
                       f"Signatures: {', '.join(matched_sigs[:3])}", url)
            vulns += 1
            findings.append({"type": "suspicious_php", "url": url,
                             "signatures": matched_sigs})

    # Test for command execution on suspicious files
    print(f"\n{D}  Testing command execution on suspicious files...{N}")
    for f in findings[:5]:
        url = f["url"]
        for param in ["?cmd=id", "?c=id", "?exec=id", "?shell=id"]:
            test_url = url + param
            code, hdrs, body = http_get(test_url, timeout=8)
            if code == 200 and ("uid=" in body or "root:" in body):
                print_vuln("CRITICAL", f"Active webshell confirmed!",
                           f"Command execution via {param}", test_url)
                f["confirmed"] = True
                f["severity"] = "CRITICAL"
                vulns += 1
                break

    print(f"\n{G}  [✓] Webshell scan complete — {vulns} findings{N}")
    if findings:
        save_report("webshell_detect", {"target": target, "findings": findings})
    return vulns
