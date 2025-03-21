def save_token():
    token = input("Please enter your Discord bot token: ")
    with open("nekot.txt", "w") as file:
        file.write(token)
    print("Token has been saved to nekot.txt.")

if __name__ == "__main__":
    save_token()
