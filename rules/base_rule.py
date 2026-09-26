class BaseRule:

    name = "Base Rule"

    def evaluate(self, context):
        raise NotImplementedError