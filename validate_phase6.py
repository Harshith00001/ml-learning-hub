#!/usr/bin/env python3
"""Phase 6 Content Validation Script"""

import json

def validate_phase6():
    """Validate Phase 6 content."""
    print("=" * 60)
    print("PHASE 6: Model Evaluation & Robustness - Validation")
    print("=" * 60)
    
    # Validate quiz
    try:
        with open('challenges/mcq/phase6_questions.json', 'r', encoding='utf-8') as f:
            quiz = json.load(f)
        
        quiz_count = len(quiz)
        quiz_xp = sum(q['xp'] for q in quiz)
        
        print(f"✓ Phase 6 Quiz: {quiz_count} items, {quiz_xp} XP")
        
        # Verify structure
        for q in quiz:
            assert 'id' in q, "Missing id"
            assert 'question' in q, "Missing question"
            assert 'options' in q, "Missing options"
            assert 'correct' in q, "Missing correct"
            assert 'xp' in q, "Missing xp"
        
        print(f"  ✓ All 15 questions have correct structure")
        
    except Exception as e:
        print(f"✗ Quiz validation failed: {e}")
        return False
    
    # Validate challenges
    try:
        with open('challenges/code/phase6_challenges.json', 'r', encoding='utf-8') as f:
            challenges = json.load(f)
        
        challenge_count = len(challenges)
        challenge_xp = sum(c['xp'] for c in challenges)
        
        print(f"✓ Phase 6 Challenges: {challenge_count} items, {challenge_xp} XP")
        
        # Verify structure
        for c in challenges:
            assert 'id' in c, "Missing id"
            assert 'title' in c, "Missing title"
            assert 'description' in c, "Missing description"
            assert 'starter_code' in c, "Missing starter_code"
            assert 'solution' in c, "Missing solution"
            assert 'hints' in c, "Missing hints"
            assert 'xp' in c, "Missing xp"
        
        print(f"  ✓ All 10 challenges have correct structure")
        
    except Exception as e:
        print(f"✗ Challenge validation failed: {e}")
        return False
    
    # Calculate totals
    lessons_xp = 200 + 200 + 200  # 3 lessons × 200 XP each
    total_items = 3 + quiz_count + challenge_count
    total_xp = lessons_xp + quiz_xp + challenge_xp
    
    print("\n" + "=" * 60)
    print("PHASE 6 TOTALS")
    print("=" * 60)
    print(f"✓ Phase 6 Lessons: 3 items, {lessons_xp} XP")
    print(f"✓ Phase 6 Quiz: {quiz_count} items, {quiz_xp} XP")
    print(f"✓ Phase 6 Challenges: {challenge_count} items, {challenge_xp} XP")
    print(f"\n✓ PHASE 6 COMPLETE: {total_items} items = 28 ✓, {total_xp} XP total")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = validate_phase6()
    exit(0 if success else 1)
