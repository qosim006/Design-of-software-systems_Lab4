"""
Task 2 — The notifier that silently did nothing

Answers:
2.1 The base send() method returns None and raises no error. The misspelled
    sned() is a different method, so the inherited send() is still called.
2.2 Making send() abstract prevents creation of a child that has not
    implemented the required method.
2.3 send() is abstract; notify() is concrete shared logic.
2.4 SmsNotifier uses its own max_length, while notify() is implemented once.
"""

from abc import ABC, abstractmethod


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient: str, text: str) -> None:
        raise NotImplementedError

    def notify(self, recipient: str, text: str) -> None:
        self.send(recipient, text[: self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096

    def send(self, recipient: str, text: str) -> None:
        print(f"telegram -> {recipient}: {text}")


class SmsNotifier(Notifier):
    max_length = 160

    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, recipient: str, text: str) -> None:
        self.sent_messages.append((recipient, text))


class RecordingNotifier(Notifier):
    def __init__(self, max_length: int) -> None:
        self.max_length = max_length
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, recipient: str, text: str) -> None:
        self.sent_messages.append((recipient, text))


def test_base_notifier_cannot_be_created():
    import pytest
    with pytest.raises(TypeError):
        Notifier()


def test_sms_text_is_cut_to_160_characters():
    notifier = SmsNotifier()
    notifier.notify("+998901234567", "x" * 200)
    assert len(notifier.sent_messages[0][1]) == 160


def test_each_channel_uses_its_own_limit():
    short_channel = RecordingNotifier(5)
    long_channel = RecordingNotifier(12)

    short_channel.notify("user1", "abcdefghijkl")
    long_channel.notify("user2", "abcdefghijkl")

    assert short_channel.sent_messages[0][1] == "abcde"
    assert long_channel.sent_messages[0][1] == "abcdefghijkl"


def test_telegram_implementation_is_concrete():
    assert isinstance(TelegramNotifier(), Notifier)
