from labs.delay.delay_lab import load

lab = load()

print()

print(lab.title)

print()

print(lab.objective)

print()

print(lab.theory)

print()

print("Questions")

print("----------------")

for question in lab.questions:

    print("-", question)

print()

print("Scenario")

print("----------------")

print(lab.scenario.name)
