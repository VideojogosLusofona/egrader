from yaml import SafeLoader, YAMLObject


class Repository(YAMLObject):
    yaml_tag = "!Repository"
    yaml_loader = SafeLoader

    def __init__(self, name, checks):
        self.name = name
        self.checks = checks



