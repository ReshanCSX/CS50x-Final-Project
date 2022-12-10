def usd(value):
    """Format value as USD."""

    if value < 0:
        return f"${-(value):,.2f}"

    return f"${value:,.2f}"