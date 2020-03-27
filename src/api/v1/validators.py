from rest_framework.validators import UniqueTogetherValidator


class UniqueTogetherFieldValidator(UniqueTogetherValidator):
    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, "instance", None)
        self.context = getattr(serializer, "context")

    def __call__(self, attrs):
        attrs["organization"] = self.context["request"].user.organization
        super().__call__(attrs)
