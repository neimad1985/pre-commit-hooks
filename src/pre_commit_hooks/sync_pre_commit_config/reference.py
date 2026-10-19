REV_PLACEHOLDER = "{rev}"


def render_reference(template: str, rev: str) -> str:
    if REV_PLACEHOLDER not in template:
        message = f"Reference template has no {REV_PLACEHOLDER} placeholder"
        raise ValueError(message)
    return template.replace(REV_PLACEHOLDER, rev)
