"""Contains a function for compacting a list."""


def compact[T](sequence: list[T]) -> list[T]:
    """Compact a list by adding all elements up that can be added together.

    Parameters
    ----------
    sequence : list[T]
        The sequence to compact.

    Returns
    -------
    list[T]
        The compacted list.
    """
    if not sequence:
        return []

    add_groups = [sequence[0]]
    for element in sequence[1:]:
        for i in range(len(add_groups)):
            try:
                add_groups[i] += element  # pyright: ignore[reportOperatorIssue]
            except TypeError:
                continue
            else:
                break
        else:
            add_groups.append(element)

    return add_groups
