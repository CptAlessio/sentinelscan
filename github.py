import requests
import os
import zipfile


def download_github_repository(access_token, owner, repo_name):
    # Define the URL for the repository's archive in zip format
    url = f"https://api.github.com/repos/{owner}/{repo_name}/zipball"

    # Set the authentication header with the personal access token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make the request to download the archive
    response = requests.get(url, headers=headers)

    # Create a folder with the repository name to extract the archive
    folder_name = f"{owner}-{repo_name}-master"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        # Write the downloaded archive to a file in the repository folder
        zip_file = f"{folder_name}.zip"
        with open(zip_file, "wb") as file:
            file.write(response.content)

        # Extract the contents of the archive to the repository folder
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(folder_name)

        # Remove the downloaded archive
        os.remove(zip_file)
    else:
        print("Found an existing folder for the specified repository. I ill use the existing code and will not "
              "download the repository again.")

    # Return the path where the code is
    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, folder_name)
    return full_path


def main(owner, repo_name):
    with open("access_token.txt", "r") as token_file:
        access_token = token_file.read().strip()

    return download_github_repository(access_token, owner, repo_name)
