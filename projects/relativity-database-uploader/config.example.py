rows = [
    "production_begin_bates",
    "control_number",
    "custodian",
    "subject_email_and_loose_files",
    "email_from",
    "email_to",
    "email_cc",
    "email_bcc",
    "author",
    "title",
    "text_link",
    "all_custodians_deduplication",
    "record_id",
]

ingest = dict(
    apiKey="", # GroundX API Key
    url="https://api.groundx.ai/api/v1/ingest/document",
)
