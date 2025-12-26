from datetime import datetime
from .candidate import Candidate

class ReviewedCandidate(Candidate):
    liked: int
    reviewed_at: datetime