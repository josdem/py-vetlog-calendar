KEYWORDS = [
    "spay",
    "neuter",
    "medical",
    "surgery",
    "cirugia",
    "cirugía",
    "esterilización",
    "esterilizacion",
    "médica",
    "medica",
]


def is_medical_event(title: str) -> bool:
    """Determines if an event is a medical event based on its title."""
    title = title.lower()
    return any(keyword in title for keyword in KEYWORDS)
