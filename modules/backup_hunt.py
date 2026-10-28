"""Backup File Hunter — .bak/.old/.sql/.zip leaks"""
from core.config import BACKUP_EXTENSIONS, BACKUP_BASENAMES, R, R2, B, B2, W, Y, G, D, N
from core.engine import http_get, save_report, print_vuln

def run(target):
    print(f"\n{B2}  Hunting backup files on {W}{target}{N}")
    vulns = 0
    findings = []
    tested = 0

    # Generate combinations
    combos = []
    for base in BACKUP_BASENAMES:
        for ext in BACKUP_EXTENSIONS:
            combos.append(f"/{base}{ext}")
            # Also without extension replacement
            if "." in base:
                name = base.rsplit(".", 1)[0]
                combos.append(f"/{name}{ext}")

    # Add common backup paths
    extras = [
        "/backup.zip", "/backup.tar.gz", "/backup.sql", "/backup.sql.gz",
        "/db_backup.sql", "/database.sql", "/dump.sql", "/data.sql",
        "/site.zip", "/www.zip", "/public_html.zip", "/htdocs.zip",
        "/wp-content.zip", "/wp-backup.zip",
        "/backup/db.sql", "/backup/database.sql",
        "/sql/dump.sql", "/sql/backup.sql",
        "/.backup", "/.sql", "/.db",
        "/old/index.php.old", "/old/config.php.bak",
    ]
    combos.extend(extras)

    # Deduplicate
    combos = list(set(combos))
    print(f"\n{D}  Testing {len(combos)} backup file paths...{N}")

    for path in combos:
        url = target + path
        code, hdrs, body = http_get(url, timeout=6)
        tested += 1
        if code == 0 or code == 404:
            continue

        # Check if it's a real file (not a generic 200 page)
        content_type = hdrs.get("content-type", "")
        content_length = hdrs.get("content-length", str(len(body)))

        is_real = False
        reason = ""

        # SQL files
        if path.endswith((".sql", ".sql.gz", ".sql.bz2", ".dump")):
            if code == 200 and ("CREATE TABLE" in body or "INSERT INTO" in body or
                                "DROP TABLE" in body or "-- MySQL" in body or
                                "-- phpMyAdmin" in body):
                is_real = True
                reason = "SQL dump content detected"

        # PHP backup files
        elif path.endswith((".bak", ".old", ".orig", ".save", ".copy")):
            if code == 200 and ("<?php" in body or "define(" in body or
                                "password" in body.lower() or "mysql" in body.lower()):
                is_real = True
                reason = "PHP source in backup file"

        # Archive files
        elif path.endswith((".zip", ".tar", ".tar.gz", ".tgz", ".rar", ".7z", ".gz")):
            if code == 200 and len(body) > 100:
                # Check magic bytes
                if body[:2] == "PK" or body[:2] == "\x1f\x8b" or "application/" in content_type:
                    is_real = True
                    reason = f"Archive file ({content_length} bytes)"

        # Log files
        elif path.endswith((".log",)):
            if code == 200 and len(body) > 100 and ("error" in body.lower() or
                                                      "[" in body and "]" in body):
                is_real = True
                reason = "Log file content"

        # Config/DB files
        elif path.endswith((".db", ".sqlite", ".sqlite3", ".csv", ".json", ".xml")):
            if code == 200 and len(body) > 50:
                is_real = True
                reason = f"Data file ({content_length} bytes)"

        # Editor swap files
        elif path.endswith((".swp", ".swo", ".~")):
            if code == 200 and len(body) > 20:
                is_real = True
                reason = "Editor swap file"

        if is_real:
            sev = "CRITICAL" if "sql" in path or "password" in reason.lower() else "HIGH"
            print_vuln(sev, f"Backup file found: {path}", reason, url)
            vulns += 1
            findings.append({"type": "backup_file", "url": url,
                             "reason": reason, "severity": sev})

        if tested % 100 == 0:
            print(f"   {D}... tested {tested}/{len(combos)}{N}")

    print(f"\n{G}  [✓] Backup hunt complete — {vulns} findings ({tested} tested){N}")
    if findings:
        save_report("backup_hunt", {"target": target, "findings": findings})
    return vulns
