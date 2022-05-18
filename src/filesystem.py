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


class Interface:
    @staticmethod
    def cat(path: str) -> str:
        return ""

    @staticmethod
    def ls(path: str) -> str:
        return ""

    @staticmethod
    def tree(path: str) -> str:
        return ""
