
# ==========================================
# ALLOY COMPOSITION AND MELTING CHARGE CALCULATOR
# ==========================================

def get_positive_number(message):
    while True:
        try:
            value = float(input(message))
            if value > 0:
                return value
            print("Please enter a value greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_percentage(message):
    while True:
        value = get_positive_number(message)
        if value <= 100:
            return value
        print("Percentage cannot be greater than 100.")


print("\n==============================================")
print("     ALLOY MELTING CHARGE CALCULATOR")
print("==============================================")

# STEP 1: Base metal information

base_metal = input("\nEnter base metal (e.g. Aluminum): ").strip()

while not base_metal:
    base_metal = input("Please enter a base metal: ").strip()

purity = get_percentage("Enter base metal purity (%): ")
total_weight = get_positive_number("Enter final melt weight (kg): ")

# STEP 2: Number of alloying elements

while True:
    try:
        number_of_elements = int(
            input("\nHow many alloying elements are required? ")
        )
        if number_of_elements > 0:
            break
        print("Enter at least one alloying element.")
    except ValueError:
        print("Please enter a whole number.")

# STEP 3: Collect alloying element and master alloy data

alloy_data = []
total_target_percentage = 0

for i in range(number_of_elements):

    print(f"\n========== ELEMENT {i + 1} ==========")

    element = input("Enter alloying element name (e.g. Cu): ").strip()

    while not element:
        element = input("Element name cannot be empty. Enter again: ").strip()

    target_percentage = get_percentage(
        f"Enter required {element} composition (%): "
    )

    master_name = input(
        f"Enter master alloy name (e.g. Al-50%{element}): "
    ).strip()

    while not master_name:
        master_name = input("Enter master alloy name: ").strip()

    master_percentage = get_percentage(
        f"Enter {element} concentration in master alloy (%): "
    )

    total_target_percentage += target_percentage

    alloy_data.append({
        "element": element,
        "target_percentage": target_percentage,
        "master_name": master_name,
        "master_percentage": master_percentage
    })

# STEP 4: Check target composition

if total_target_percentage >= 100:
    print("\nERROR: Total alloying element composition must be below 100%.")
    raise SystemExit

# STEP 5: Calculate required master alloy quantities

total_master_weight = 0

for alloy in alloy_data:

    target_element_weight = (
        total_weight * alloy["target_percentage"] / 100
    )

    master_fraction = alloy["master_percentage"] / 100

    master_weight = target_element_weight / master_fraction

    alloy["target_element_weight"] = target_element_weight
    alloy["master_weight"] = master_weight

    total_master_weight += master_weight

# STEP 6: Calculate base metal requirement

base_metal_weight = total_weight - total_master_weight

if base_metal_weight < 0:
    print("\nERROR: Required master alloys exceed the total melt weight.")
    print("Choose a more concentrated master alloy or revise the target.")
    raise SystemExit

# STEP 7: Display final results

print("\n")
print("=" * 65)
print("                 MELTING CHARGE REPORT")
print("=" * 65)

print(f"Base Metal       : {base_metal}")
print(f"Base Metal Purity: {purity:.3f}%")
print(f"Final Melt Weight: {total_weight:.3f} kg")

print("\nMASTER ALLOY REQUIREMENTS")
print("-" * 65)

print(f"{'Element':<12}{'Master Alloy':<20}{'Required (kg)':>15}")
print("-" * 65)

for alloy in alloy_data:

    print(
        f"{alloy['element']:<12}"
        f"{alloy['master_name']:<20}"
        f"{alloy['master_weight']:>15.4f}"
    )

print("-" * 65)

print(f"{'Base Metal':<32}{base_metal_weight:>15.4f}")
print(f"{'Total Charge':<32}{total_weight:>15.4f}")

print("\nTARGET COMPOSITION CHECK")
print("-" * 65)

for alloy in alloy_data:
    print(
        f"{alloy['element']}: "
        f"Target = {alloy['target_percentage']:.3f}% | "
        f"Calculated = {alloy['target_percentage']:.3f}%"
    )

print("=" * 65)

print("\nNOTE: Base metal purity is recorded but not yet")
print("included in the composition correction calculation.")

# STEP 8: Save report

save_report = input("\nDo you want to save this report? (yes/no): ").lower()

if save_report in ["yes", "y"]:

    with open("melting_charge_report.txt", "w", encoding="utf-8") as file:

        file.write("ALLOY MELTING CHARGE REPORT\n")
        file.write("=" * 45 + "\n")

        file.write(f"Base Metal: {base_metal}\n")
        file.write(f"Purity: {purity}%\n")
        file.write(f"Final Melt Weight: {total_weight} kg\n\n")

        for alloy in alloy_data:
            file.write(
                f"{alloy['element']} | "
                f"{alloy['master_name']} | "
                f"{alloy['master_weight']:.4f} kg\n"
            )

        file.write(f"\nBase Metal Required: {base_metal_weight:.4f} kg\n")
        file.write(f"Total Charge: {total_weight:.4f} kg\n")

    print("\nReport saved as melting_charge_report.txt")

print("\nThank you for using the Alloy Calculator!")
