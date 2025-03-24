user_id = input("Enter your Discord User ID: ")

with open("sdi1.txt", "w") as file:
    file.write(user_id)

print("Saved successfully to sdi1.txt.")
