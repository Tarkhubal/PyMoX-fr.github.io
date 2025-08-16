from custom_parser import CustomCommitParser


def analyze_commit(message: str):
    parser = CustomCommitParser()
    parsed = parser.parse_message(message)

    if not parsed:
        return "❌ Commit non reconnu"

    return (
        f"✅ Reconnu\n"
        f"Type: {parsed.type}\n"
        f"Scope: {parsed.scope}\n"
        f"Description: {parsed.description}\n"
        f"Breaking change: {'Oui' if parsed.breaking else 'Non'}"
    )


# Exemple
message = "maj(api): ajout d'une nouvelle fonctionnalité"
print(analyze_commit(message))
