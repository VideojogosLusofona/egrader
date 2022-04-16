from yaml import SafeLoader, YAMLObject


class Results(YAMLObject):
    yaml_tag = "!Results"
    yaml_loader = SafeLoader

    def __init__(self, students):
        self.students = students

    def __repr__(self):
        return "%s(students=%r, hp=%r, ac=%r, attacks=%r)" % (
            self.__class__.__name__,
            self.students,
        )
