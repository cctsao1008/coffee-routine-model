from protocol_adapter import CoffeeEvent, coffee_to_observation


print("☕ tiny happy path")
print(coffee_to_observation(["+1?", "+", "☕", "👍"]))

print("\n🌿 pass is a real choice")
print(coffee_to_observation(["+1?", "pass"]))

print("\n🙈 a lonely thumb may stay mysterious")
print(coffee_to_observation(["👍"]))

print("\n🏖️ pause, update, and resume can be explicit")
print(
    coffee_to_observation(
        [
            CoffeeEvent("proactive_update", "leave notice"),
            CoffeeEvent("pause", "leave"),
            CoffeeEvent("resume", "back tomorrow"),
        ]
    )
)
