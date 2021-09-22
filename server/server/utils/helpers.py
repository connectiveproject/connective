def get_nested_obj_attr_value(obj, lookup_str, seperator="__"):
    """
    return the value of an inner attribute of an object
    e.g. `user__organization__member__organization__slug` would return the organization slug related to the user

    :object obj: an object. could be model obj
    :string lookup_str: str to look for (e.g., organization__slug)
    :string seperator: seperator to identify the nesting in the lookup string
    """
    # recursion stop condition
    if seperator not in lookup_str:
        return getattr(obj, lookup_str)

    first_lookup_str, remaining_lookup_str = lookup_str.split(seperator, maxsplit=1)
    new_obj = getattr(obj, first_lookup_str)

    return get_nested_obj_attr_value(new_obj, remaining_lookup_str, seperator)
