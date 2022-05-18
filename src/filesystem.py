REPO_URL_PREFIX = "https://github.com/waycrate/"

REPOSITORIES = [
    "HerbWM",
    "rpm-rs",
    "rypper",
    "swhkd",
    "swhkd-vim",
    "swiv",
    "vim-swhkdrc",
    "wayboard",
    "waycast",
    "waylevel",
    "wayout",
    "wayshot"
]

PEOPLE_URL_PREFIX = "https://github.com/"

PEOPLE = {
    "Angelo Fallaria": "angelofallars",
    "Eden": "EdenQwQ",
    "Aakash Sen Sharma": "Shinyzenith",
    "Soc Virnyl S. Estela": "uncomfyhalomacro",
    "Ckyiu": "UnsignedArduino",
    "Väinö Mäkelä": "vainiovano"
}

# Commands:
# cat
# ls
# tree
# help

# "Filesystem":
# Waycrate
#   |- repos
#   |   |- HerbWM
#   |   |   |- githubrepo
#   |   |   |- srhtrepo  # only if they have one
#   |   |   |- github
#   |   |   |   |- description
#   |   |   |   |- stars
#   |   |   |   |- forks
#   |   |   |   |- watching
#   |   |   |   |- language
#   |   |   |   |- openissuescount
#   |   |   |   |- license
#   |   |   |   |- topics
#   |   |- rpm-rs, rypper, swhkd, swhkd-vim, swiv, vim-swhkdrc, wayboard,
#          waycast, waylevel, wayout, wayshot
#   |- stats
#   |   |- repocount
#   |   |- people
#   |- githuborg
#   |- website


def _copy_repo_struct() -> dict[str, dict[str, ...]]:
    return {
        "github": {
            "url": "",
            "description": "",
            "stars": "",
            "forks": "",
            "watching": "",
            "language": "",
            "openissuescount": "",
            "license": "",
            "topics": ""
        }
    }.copy()


def _init_filesystem() -> dict[str, dict[str, dict[str, str], str, str]]:
    repos = {}
    for repo in REPOSITORIES:
        repos[repo] = _copy_repo_struct()
        repos[repo]["github"]["url"] = f"{REPO_URL_PREFIX}{repo}"
    people = "\n".join((f"{person} ({username}) at "
                        f"{PEOPLE_URL_PREFIX}{username}"
                        for person, username in PEOPLE.items()))
    fs = {
        "Waycrate": {
            "repos": repos,
            "stats": {
                "repocount": f"{len(repos)} repositories",
                "people": people
            },
            "githuborg": "",
            "website": ""
        }
    }
    return fs


class Filesystem:
    _filesystem = _init_filesystem()

    @staticmethod
    def filesystem() -> dict[str, dict[str, dict[str, str], str, str]]:
        return Filesystem._filesystem


class Interface:
    @staticmethod
    def cat(path: str) -> str:
        if path[0] != "/":
            path = "/" + path
        if path[-1] == "/":
            path = path[:-1]
        components = path.split("/")[1:]
        fs = Filesystem.filesystem()
        cwd = fs
        for directory in components[:-1]:
            if isinstance(cwd, str):
                return f"cat: can't open '{path}': Not a directory"
            elif directory not in cwd:
                return f"cat: can't open '{path}': No such file or directory"
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd:
            return f"cat: can't open '{path}': No such file or directory"
        elif isinstance(cwd[filename], dict):
            return f"cat: read error: Is a directory"
        return cwd[filename]

    @staticmethod
    def ls(path: str) -> str:
        return ""

    @staticmethod
    def tree(path: str) -> str:
        return ""
