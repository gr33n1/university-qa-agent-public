FORBIDDEN_SQL_TERMS = [
    "delete",
    "drop",
    "update",
    "insert",
    "alter",
    "truncate",
    "create",
    "replace",
    "attach",
    "detach",
    "pragma",
]

FORBIDDEN_INPUT_PREFIXES = FORBIDDEN_SQL_TERMS
FORBIDDEN_SQL_KEYWORDS = FORBIDDEN_SQL_TERMS

SUSPICIOUS_INPUT_PATTERNS = [
    "--",
    "/*",
    "*/",
    " union select ",
    " or 1=1",
    " xp_",
    "\\x00",
]

MAX_INPUT_LENGTH = 500
MAX_SQL_LENGTH = 5000