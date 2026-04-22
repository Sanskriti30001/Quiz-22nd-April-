import pytest
from engagement_engine import EngagementEngine


def test_initial_state_default():
    engine = EngagementEngine("user1")
    assert engine.user_handle == "user1"
    assert engine.score == 0.0
    assert engine.verified is False


def test_initial_state_verified():
    engine = EngagementEngine("user2", verified=True)
    assert engine.verified is True


def test_process_like():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("like", 3)
    assert result is True
    assert engine.score == 3


def test_process_comment():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("comment", 2)
    assert result is True
    assert engine.score == 10


def test_process_share():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("share", 2)
    assert result is True
    assert engine.score == 20


def test_process_invalid_type():
    engine = EngagementEngine("user1")
    result = engine.process_interaction("follow", 1)
    assert result is False
    assert engine.score == 0.0


def test_process_negative_count_raises():
    engine = EngagementEngine("user1")
    with pytest.raises(ValueError, match="Negative count"):
        engine.process_interaction("like", -1)


def test_verified_bonus_applied():
    engine = EngagementEngine("user1", verified=True)
    result = engine.process_interaction("share", 2)
    assert result is True
    assert engine.score == 30.0


def test_get_tier_newbie():
    engine = EngagementEngine("user1")
    assert engine.get_tier() == "Newbie"


def test_get_tier_influencer_at_100():
    engine = EngagementEngine("user1")
    engine.score = 100
    assert engine.get_tier() == "Influencer"


def test_get_tier_influencer_at_1000():
    engine = EngagementEngine("user1")
    engine.score = 1000
    assert engine.get_tier() == "Influencer"


def test_get_tier_icon():
    engine = EngagementEngine("user1")
    engine.score = 1000.1
    assert engine.get_tier() == "Icon"


def test_apply_penalty_reduces_score_without_unverifying():
    engine = EngagementEngine("user1", verified=True)
    engine.score = 100
    engine.apply_penalty(1)
    assert engine.score == 80
    assert engine.verified is True


def test_apply_penalty_unverifies_when_report_count_above_10():
    engine = EngagementEngine("user1", verified=True)
    engine.score = 100
    engine.apply_penalty(11)
    assert engine.verified is False
    assert engine.score == 0
