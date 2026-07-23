def clean_feature_name(feature):
    if feature.startswith("remainder__"):
        feature = feature.replace("remainder__", "")

    elif feature.startswith("cat__MAKE_"):
        feature = feature.replace("cat__MAKE_", "Make: ")

    elif feature.startswith("cat__FUEL TYPE_"):
        fuel_map = {
            "D": "Diesel",
            "E": "Ethanol",
            "N": "Natural Gas",
            "X": "Regular Gasoline",
            "Z": "Premium Gasoline"
        }

        code = feature.replace("cat__FUEL TYPE_", "")
        feature = f"Fuel Type: {fuel_map.get(code, code)}"

    elif feature.startswith("cat__TRANSMISSION_"):
        feature = feature.replace(
            "cat__TRANSMISSION_",
            "Transmission: "
        )

    elif feature.startswith("cat__VEHICLE CLASS_"):
        feature = feature.replace(
            "cat__VEHICLE CLASS_",
            "Vehicle Class: "
        )

    return feature