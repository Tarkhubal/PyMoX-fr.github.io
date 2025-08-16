import re
from semantic_release.commit_parser import ParsedCommit, CommitParser


class CustomCommitParser(CommitParser):
    # Ajoute ici tes types personnalisés
    allowed_types = {"maj", "up", "fix", "feat", "docs", "refactor", "test", "chore"}

    # Expression régulière adaptée à Conventional Commits
    commit_re = re.compile(
        r"^(?P<type>[a-zA-Z]+)"
        r"(?:\((?P<scope>[^\)]+)\))?"
        r"(?P<breaking>!)?: (?P<description>.+)"
    )

    def parse_message(self, message: str):
        match = self.commit_re.match(message.strip())
        if not match:
            return None

        type_ = match.group("type")
        if type_ not in self.allowed_types:
            return None

        return ParsedCommit(
            type=type_,
            scope=match.group("scope"),
            description=match.group("description"),
            breaking=bool(match.group("breaking")),
            footer="",
        )
