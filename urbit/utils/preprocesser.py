def sort_by(
        data,
        by: str = 'score',
        reverse: bool = True,
) -> list:
    data.sort(
        key=lambda x: x[by],
        reverse=reverse,
    )

    return data
    