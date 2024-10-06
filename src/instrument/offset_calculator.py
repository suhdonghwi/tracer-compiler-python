class OffsetCalculator:
    def __init__(self, code: str):
        self.lines = code.splitlines(keepends=True)
        self.cumulative_line_lengths = self._calculate_cumulative_line_lengths()

    def _calculate_cumulative_line_lengths(self) -> list[int]:
        cumulative_line_lengths = [0]
        for line in self.lines:
            cumulative_line_lengths.append(cumulative_line_lengths[-1] + len(line))
        return cumulative_line_lengths

    def get_offsets(
        self, lineno: int, col_offset: int, end_lineno: int, end_col_offset: int
    ) -> tuple[int, int]:
        begin_offset = self.cumulative_line_lengths[lineno - 1] + col_offset
        end_offset = self.cumulative_line_lengths[end_lineno - 1] + end_col_offset
        return begin_offset, end_offset
