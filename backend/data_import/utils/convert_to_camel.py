from pydantic.alias_generators import to_camel


def custom_camel(string: str) -> str:
    # First use the original to_camel function
    result = to_camel(string)

    # Then handle the special TERYT case
    if "Teryt" in result:
        result = result.replace("Teryt", "TERYT")

    return result
