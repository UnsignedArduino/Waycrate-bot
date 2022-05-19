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


async def _init_filesystem() -> dict[str, dict[str, dict[str, str], str, str]]:
    repos = {}
    for repo in REPOSITORIES:
        repos[repo] = _copy_repo_struct()
        repos[repo]["github"]["url"] = f"{REPO_URL_PREFIX}{repo}"
    people = "\n".join((f"{person} ({username}) at "
                        f"{PEOPLE_URL_PREFIX}{username}"
                        for person, username in PEOPLE.items()))
    return {
        "": {
            "Waycrate": {
                "repos": repos,
                "stats": {
                    "repocount": f"{len(repos)} repositories",
                    "people": people
                },
                "githuborg": "https://github.com/waycrate",
                "website": "https://waycrate.github.io/"
            }
        }
    }


class Filesystem:
    _filesystem = None

    @staticmethod
    async def filesystem() -> dict[str, dict[str, dict[str, str], str, str]]:
        if Filesystem._filesystem is None:
            Filesystem._filesystem = await _init_filesystem()
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
    async def cat(path: str) -> dict[str, str, bool]:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
        fs = await Filesystem.filesystem()
        cwd = fs
        cmd = f"cat {path}"
        for directory in components[:-1]:
            if isinstance(cwd, str):
                return {"command": cmd,
                        "output": f"cat: can't open '{path}': Not a directory",
                        "success": False}
            elif directory not in cwd:
                return {"command": cmd,
                        "output": f"cat: can't open '{path}': "
                                  f"No such file or directory",
                        "success": False}
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd:
            return {"command": cmd,
                    "output": f"cat: can't open '{path}': "
                              f"No such file or directory",
                    "success": False}
        elif isinstance(cwd[filename], dict):
            return {"command": cmd,
                    "output": f"cat: read error: Is a directory",
                    "success": False}
        else:
            return {"command": cmd,
                    "output": cwd[filename],
                    "success": True}

    @staticmethod
    async def ls(path: str) -> dict[str, str, bool]:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
        fs = await Filesystem.filesystem()
        cwd = fs
        cmd = f"ls {path}"
        for directory in components[:-1]:
            if isinstance(cwd, str):
                return {"command": cmd,
                        "output": f"ls: {path}: Not a directory",
                        "success": False}
            elif directory not in cwd:
                return {"command": cmd,
                        "output": f"ls: {path}: No such file or directory",
                        "success": False}
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd:
            return {"command": cmd,
                    "output": f"ls: {path}: No such file or directory",
                    "success": False}
        elif isinstance(cwd[filename], str):
            return {"command": cmd,
                    "output": filename,
                    "success": True}
        else:
            return {"command": cmd,
                    "output": " ".join(cwd[filename].keys()),
                    "success": True}

    @staticmethod
    async def tree(path: str) -> dict[str, str, bool]:
        path = Interface.fix_path(path)
        components = Interface.split_path(path)
        fs = await Filesystem.filesystem()
        cwd = fs
        cmd = f"tree {path}"
        for directory in components[:-1]:
            if isinstance(cwd, str) or directory not in cwd:
                return {"command": cmd,
                        "output": f"{path} [error opening dir]",
                        "success": False}
            cwd = cwd[directory]
        filename = components[-1]
        if filename not in cwd or isinstance(cwd[filename], str):
            return {"command": cmd,
                    "output": f"{path} [error opening dir]",
                    "success": False}

        def text_tree(dir, level=1) -> str:
            things = []
            spacer = (" |  " * (level - 1)) + " |- "
            for key, value in dir.items():
                things.append(spacer + key)
                if isinstance(value, dict):
                    things.append(text_tree(value, level+1))
            return "\n".join(things)

        return {"command": cmd,
                "output": f"{path}\n{text_tree(cwd[filename])}",
                "success": True}
