import json

# Validate phase4_questions.json
with open('challenges/mcq/phase4_questions.json', 'r', encoding='utf-8') as f:
    phase4_questions = json.load(f)

# Validate phase4_challenges.json  
with open('challenges/code/phase4_challenges.json', 'r', encoding='utf-8') as f:
    phase4_challenges = json.load(f)

quiz_xp = sum(q['xp'] for q in phase4_questions)
challenge_xp = sum(c['xp'] for c in phase4_challenges)
lesson_xp = 600

total_xp = lesson_xp + quiz_xp + challenge_xp

print("✓ Phase 4 Quiz Questions: " + str(len(phase4_questions)) + " items")
print("  Quiz XP: " + str(quiz_xp))
print("\n✓ Phase 4 Code Challenges: " + str(len(phase4_challenges)) + " items")
print("  Challenge XP: " + str(challenge_xp))
print("\n✓ PHASE 4 TOTALS:")
print("  - 3 Lessons: " + str(lesson_xp) + " XP")
print("  - 15 Quiz: " + str(quiz_xp) + " XP")
print("  - 10 Challenges: " + str(challenge_xp) + " XP")
print("  - TOTAL: " + str(total_xp) + " XP")
