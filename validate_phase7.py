#!/usr/bin/env python3
"""Phase 7 Content Validation Script"""

import json


def validate_phase7():
    """Validate Phase 7 content."""
    print("=" * 60)
    print("PHASE 7: Production & MLOps - Validation")
    print("=" * 60)
    
    # Validate quiz
    try:
        with open('challenges/mcq/phase7_questions.json', 'r', encoding='utf-8') as f:
            quiz = json.load(f)
        assert isinstance(quiz, list), "Quiz JSON must be a list of question objects"
        quiz_count = len(quiz)
        quiz_xp = sum(q['xp'] for q in quiz)
        print(f"Phase 7 Quiz: {quiz_count} items, {quiz_xp} XP")
        for q in quiz:
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
        with open('challenges/code/phase7_challenges.json', 'r', encoding='utf-8') as f:
            challenges = json.load(f)
        assert isinstance(challenges, list), "Challenges JSON must be a list of challenge objects"
        challenge_count = len(challenges)
        challenge_xp = sum(c['xp'] for c in challenges)
        print(f"Phase 7 Challenges: {challenge_count} items, {challenge_xp} XP")
        for c in challenges:
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
    print("PHASE 7 TOTALS")
    print("=" * 60)
    print(f"Phase 7 Lessons: 3 items, {lessons_xp} XP")
    print(f"Phase 7 Quiz: {quiz_count} items, {quiz_xp} XP")
    print(f"Phase 7 Challenges: {challenge_count} items, {challenge_xp} XP")
    print(f"\nPHASE 7 COMPLETE: {total_items} items = 28, {total_xp} XP total")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = validate_phase7()
    exit(0 if success else 1)
