def get_repos_from_file(path):
    try:
        with open(path, "r") as file:
            return [line.strip() for line in file]
    except Exception as e:
        return f"Error: {str(e)}"
