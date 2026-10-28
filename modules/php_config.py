"""PHP Config Leak Scanner — phpinfo, .env, debug, exposed configs"""
from core.config import PHP_INFO_PATHS, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, get_php_version, get_server_info, save_report, print_vuln

def run(target):
    print(f"\n{B2}  Scanning PHP config leaks on {W}{target}{N}")
    vulns = 0
    findings = []
    php_ver = None
    server_info = {}

    # Quick homepage check for PHP version
    code, hdrs, body = http_get(target)
    if code > 0:
        php_ver = get_php_version(hdrs, body)
        server_info = get_server_info(hdrs)
        if php_ver:
            print_vuln("INFO", f"PHP Version Detected: {php_ver}",
                       f"Server: {server_info.get('server','?')}")
            vulns += 1
            findings.append({"type": "php_version", "version": php_ver})
        if server_info.get("x-powered-by"):
            print_vuln("LOW", "X-Powered-By header exposed",
                       server_info["x-powered-by"])
            vulns += 1
            findings.append({"type": "x-powered-by", "value": server_info["x-powered-by"]})

    # Scan paths
    print(f"\n{D}  Checking {len(PHP_INFO_PATHS)} paths...{N}")
    for path in PHP_INFO_PATHS:
        url = target + path
        code, hdrs, body = http_get(url, timeout=8)
        if code == 0:
            continue

        # phpinfo() detection
        if "phpinfo()" in body or "PHP Version" in body and "phpinfo" in body.lower():
            print_vuln("CRITICAL", "phpinfo() exposed!", f"Full PHP configuration leaked", url)
            vulns += 1
            findings.append({"type": "phpinfo", "url": url, "severity": "CRITICAL"})
            v = get_php_version(hdrs, body)
            if v and not php_ver:
                php_ver = v
                print(f"   {D}└─ PHP Version: {v}{N}")
            continue

        # .env file detection
        if ".env" in path and code == 200:
            if any(k in body.lower() for k in ["db_host", "db_password", "app_key",
                                                 "database", "secret", "mysql",
                                                 "password", "api_key"]):
                print_vuln("CRITICAL", "Environment file exposed!", "Credentials/secrets leaked", url)
                vulns += 1
                findings.append({"type": "env_leak", "url": url, "severity": "CRITICAL"})
                continue

        # Git/SVN exposure
        if ".git" in path and code == 200 and len(body) > 10:
            print_vuln("HIGH", "Git repository exposed!", "Source code accessible", url)
            vulns += 1
            findings.append({"type": "git_exposed", "url": url})
            continue
        if ".svn" in path and code == 200 and len(body) > 10:
            print_vuln("HIGH", "SVN repository exposed!", url)
            vulns += 1
            findings.append({"type": "svn_exposed", "url": url})
            continue

        # Config files with DB creds
        if any(x in path for x in ["config", "database", "connect", "db.php", "wp-config"]):
            if code == 200 and any(k in body.lower() for k in ["mysql", "password",
                                                                 "db_host", "dbname",
                                                                 "define(", "<?php"]):
                print_vuln("HIGH", "Database config exposed!", "DB credentials may be visible", url)
                vulns += 1
                findings.append({"type": "db_config", "url": url})
                continue

        # Log files
        if any(x in path for x in ["error_log", "error.log", "debug.log", "access.log"]):
            if code == 200 and len(body) > 50:
                print_vuln("MEDIUM", "Log file accessible", f"{len(body)} bytes", url)
                vulns += 1
                findings.append({"type": "log_leak", "url": url})
                continue

        # Server status/info
        if path in ("/server-info", "/server-status", "/status"):
            if code == 200 and ("Apache" in body or "Server Version" in body or "Active connections" in body):
                print_vuln("HIGH", "Server status page exposed!", url)
                vulns += 1
                findings.append({"type": "server_status", "url": url})
                continue

        # Composer/package files
        if path in ("/composer.json", "/composer.lock", "/package.json"):
            if code == 200 and ("{" in body and "}" in body):
                print_vuln("MEDIUM", f"Dependency file exposed: {path}", "Version info leaked", url)
                vulns += 1
                findings.append({"type": "dep_file", "url": url})
                continue

        # .htpasswd
        if ".htpasswd" in path and code == 200 and ":" in body:
            print_vuln("CRITICAL", ".htpasswd exposed!", "Password hashes leaked", url)
            vulns += 1
            findings.append({"type": "htpasswd", "url": url})
            continue

    # Check security headers
    code, hdrs, body = http_get(target)
    missing = []
    for h in ["x-frame-options", "x-content-type-options", "x-xss-protection",
              "strict-transport-security", "content-security-policy",
              "x-powered-by"]:
        if h == "x-powered-by":
            if h in hdrs:
                missing.append(h + " (should be removed)")
        else:
            if h not in hdrs:
                missing.append(h)
    if missing:
        print_vuln("LOW", f"Missing security headers: {len(missing)}", ", ".join(missing[:5]))
        vulns += 1
        findings.append({"type": "missing_headers", "headers": missing})

    print(f"\n{G}  [✓] Config scan complete — {vulns} findings{N}")
    if findings:
        save_report("php_config", {"target": target, "findings": findings})
    return vulns
