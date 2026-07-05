import markdown

def render_markdown(text):
    """Utility to render markdown on backend if needed, though primarily handled by marked.js on frontend."""
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])