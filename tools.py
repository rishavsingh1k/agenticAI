from datetime import datetime

def datetime_tool(query: str) -> str:
    try:
        return f"Current date and time is: {datetime.now()}"
    except Exception as e:
        return f"Error: {str(e)}"