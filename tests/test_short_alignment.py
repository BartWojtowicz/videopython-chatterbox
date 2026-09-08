import importlib.util
from pathlib import Path

import pytest
import torch

spec = importlib.util.spec_from_file_location("alignment", Path(__file__).parents[1] / "src/chatterbox/models/t3/inference/alignment_stream_analyzer.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

@pytest.mark.parametrize("width", [1, 2, 3, 4, 5, 6, 20])
def test_complete_alignment_keeps_token_repetition_eos(width):
    analyzer = module.AlignmentStreamAnalyzer.__new__(module.AlignmentStreamAnalyzer)
    analyzer.text_tokens_slice = (0, width)
    analyzer.eos_idx = 9
    analyzer.alignment = torch.zeros(1, width)
    analyzer.curr_frame_pos = 1
    analyzer.text_position = width - 1
    analyzer.started = True
    analyzer.started_at = 0
    analyzer.complete = True
    analyzer.completed_at = 0
    analyzer.generated_tokens = [1, 2]
    analyzer.last_aligned_attns = [torch.ones(1, width) / width]
    result = analyzer.step(torch.zeros(1, 10), torch.tensor(2))
    assert result[0, 9] == 2**15
    assert result[0, 0] == -(2**15)
    assert analyzer.generated_tokens == [1, 2, 2]
    assert analyzer.curr_frame_pos == 2
