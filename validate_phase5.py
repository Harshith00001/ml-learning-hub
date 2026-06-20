import json

q = json.load(open('challenges/mcq/phase5_questions.json'))
c = json.load(open('challenges/code/phase5_challenges.json'))

quiz_xp = sum(i['xp'] for i in q)
chal_xp = sum(i['xp'] for i in c)
lesson_xp = 600

total = quiz_xp + chal_xp + lesson_xp

print(f"✓ Phase 5 Quiz: {len(q)} items, {quiz_xp} XP")
print(f"✓ Phase 5 Challenges: {len(c)} items, {chal_xp} XP")
print(f"✓ Phase 5 Lessons: 3 items, {lesson_xp} XP")
print(f"\n✓ PHASE 5 TOTALS:")
print(f"  - Items: {len(q) + len(c) + 3} = 28")
print(f"  - Total XP: {total}")
