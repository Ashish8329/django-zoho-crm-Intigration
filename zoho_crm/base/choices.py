from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_choices(cls):
        return tuple(x.value for x in cls)

    @classmethod
    def has_value(cls, value):
        return any(value == item.value[0] for item in cls)

    @classmethod
    def get_help_text(cls):
        """
        Generate dynamic help_text for model field choices.
        """
        return "Choices include:\n" + "\n".join(
            f"- '{item.value[0]}': {item.value[1]}" for item in cls
        )


class Status(ChoiceEnum):
    PENDING = ("pending", "Pending")
    COMPLETED = ("completed", "Completed")
    REJECTED = ("rejected", "Rejected")


class EmailStatus(ChoiceEnum):
    PENDING = ("pending", "Pending")
    PROCESSING = ("processing", "Processing")
    SENT = ("sent", "Sent")
    FAILED = ("failed", "Failed")

class EmailSeenStatus(ChoiceEnum):
    SEEN = ("seen", "Seen")
    NOT_SEEN = ("not_seen", "Not Seen")