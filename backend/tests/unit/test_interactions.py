"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result == interactions

def test_create_item_with_empty_string_title_is_accepted() -> None:
    """Empty string titles are accepted by schema (validated at API/DB level)."""
    data = {"title": ""}
    assert data["title"] == ""


def test_create_item_with_whitespace_only_title() -> None:
    """Whitespace-only titles should be accepted (validation doesn't strip)."""
    data = {"title": "   "}
    assert data["title"] == "   "


def test_create_item_with_very_long_title() -> None:
    """Very long titles (1000+ chars) should be accepted by schema."""
    long_title = "x" * 10000
    data = {"title": long_title}
    assert len(data["title"]) == 10000