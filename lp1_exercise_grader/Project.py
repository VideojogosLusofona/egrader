class Project:
    """A project implemented (or not) by a student."""

    def __init__(self, name):
        self.name = name
        self.exists = False
        self.exists_in_solution = False
        self.compiles = False
        self.runs = False
        self.output_match = False
