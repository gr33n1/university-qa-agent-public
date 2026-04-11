class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeSQLLLM:
    def __init__(
        self,
        response_text: str = "SELECT COUNT(*) AS student_count FROM students;"
    ):
        self.response_text = response_text

    def invoke(self, _: str):
        return FakeResponse(self.response_text)


class FakeAnswerLLM:
    def __init__(
        self,
        response_text: str = "There are 6 students."
    ):
        self.response_text = response_text

    def invoke(self, _: str):
        return FakeResponse(self.response_text)