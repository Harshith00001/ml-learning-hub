#!/usr/bin/env python3
"""Phase 9 Content Validation Script"""

import json


def validate_phase9():
    """Validate Phase 9 content."""
    print("=" * 60)
    print("PHASE 9: Deep Learning Overview - Validation")
    print("=" * 60)

    # Validate quiz
    try:
        with open('challenges/mcq/phase9_questions.json', 'r', encoding='utf-8') as f:
            quiz = json.load(f)
        assert isinstance(quiz, dict), "Quiz JSON must be a dict mapping a section to a list of questions"
        quiz_items = []
        for value in quiz.values():
            assert isinstance(value, list), "Quiz section value must be a list"
            quiz_items.extend(value)
        quiz_count = len(quiz_items)
        quiz_xp = sum(q['xp'] for q in quiz_items)
        print(f"Phase 9 Quiz: {quiz_count} items, {quiz_xp} XP")
        for q in quiz_items:
            assert 'id' in q, "Missing id"
            assert 'section' in q, "Missing section"
            assert 'question' in q, "Missing question"
            assert 'options' in q, "Missing options"
            assert 'correct' in q, "Missing correct"
            assert 'explanation' in q, "Missing explanation"
            assert 'xp' in q, "Missing xp"
        print(f"  All {quiz_count} questions have correct structure")
    except Exception as e:
        print(f"Quiz validation failed: {e}")
        return False

    # Validate challenges
    try:
        with open('challenges/code/phase9_challenges.json', 'r', encoding='utf-8') as f:
            challenges = json.load(f)
        assert isinstance(challenges, dict), "Challenges JSON must be a dict mapping a section to a list of challenges"
        challenge_items = []
        for value in challenges.values():
            assert isinstance(value, list), "Challenge section value must be a list"
            challenge_items.extend(value)
        challenge_count = len(challenge_items)
        challenge_xp = sum(c['xp'] for c in challenge_items)
        print(f"Phase 9 Challenges: {challenge_count} items, {challenge_xp} XP")
        for c in challenge_items:
            assert 'id' in c, "Missing id"
            assert 'title' in c, "Missing title"
            assert 'description' in c, "Missing description"
            assert 'starter_code' in c, "Missing starter_code"
            assert 'solution' in c, "Missing solution"
            assert 'hints' in c, "Missing hints"
            assert 'xp' in c, "Missing xp"
        print(f"  All {challenge_count} challenges have correct structure")
    except Exception as e:
        print(f"Challenge validation failed: {e}")
        return False

    lessons_xp = 200 * 3
    total_items = 3 + quiz_count + challenge_count
    total_xp = lessons_xp + quiz_xp + challenge_xp

    print("\n" + "=" * 60)
    print("PHASE 9 TOTALS")
    print("=" * 60)
    print(f"Phase 9 Lessons: 3 items, {lessons_xp} XP")
    print(f"Phase 9 Quiz: {quiz_count} items, {quiz_xp} XP")
    print(f"Phase 9 Challenges: {challenge_count} items, {challenge_xp} XP")
    print(f"\nPHASE 9 COMPLETE: {total_items} items = {total_items}, {total_xp} XP total")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = validate_phase9()
    exit(0 if success else 1)
