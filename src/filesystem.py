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
        "": {
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
    }
    return fs


class Filesystem:
    _filesystem = _init_filesystem()

    @staticmethod
    def filesystem() -> dict[str, dict[str, dict[str, str], str, str]]:
        return Filesystem._filesystem


class Interface:
    @staticmethod
    def fix_path(path: str) -> str:
        if len(path) == 0:
            path = "/"
        if path[0] != "/":
            path = "/" + path
        if path[-1] == "/":
            path = path[:-1]
        if len(path) == 0:
            path = "/"
        return path

    @staticmethod
    def split_path(path: str) -> list[str]:
        components = path.split("/")[1:]
        if components[0] != "":
            components = [""] + components
        return components

    @staticmethod
    def cat(path: str) -> str:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
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
        else:
            return cwd[filename]

    @staticmethod
    def ls(path: str) -> str:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
        fs = Filesystem.filesystem()
        cwd = fs
        for directory in components[:-1]:
            if isinstance(cwd, str):
                return f"ls: {path}: Not a directory"
            elif directory not in cwd:
                return f"ls: {path}: No such file or directory"
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd:
            return f"ls: {path}: No such file or directory"
        elif isinstance(cwd[filename], str):
            return filename
        else:
            return " ".join(cwd[filename].keys())

    @staticmethod
    def tree(path: str) -> str:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
        fs = Filesystem.filesystem()
        cwd = fs
        for directory in components[:-1]:
            if isinstance(cwd, str) or directory not in cwd:
                return f"{path} [error opening dir]"
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd or isinstance(cwd[filename], str):
            return f"{path} [error opening dir]"

        def text_tree(dir, level) -> str:
            things = []
            spacer = " " * level
            for key, value in dir.items():
                things.append(spacer + key)
                if isinstance(value, dict):
                    things.append(f"{spacer}\n".join(text_tree(value, level + 1)))
            return things

        return "\n".join(text_tree(cwd[filename], 1))
