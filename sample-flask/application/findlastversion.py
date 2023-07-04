import docker

client = docker.from_env()
images = client.images.list()

existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("tomerkul/myflask:")]

if existing_versions:
    latest_version = max(existing_versions)
    next_version = latest_version + 0.1
else:
    next_version = 1.0

# Format the version number to one decimal place
next_version = f"{next_version:.1f}"

image_name = f"tomerkul/myflask:{next_version}"
client.images.build(path=".", tag=image_name, rm=True, pull=True)
print(f"Successfully built image: {image_name}")

# Push the image with the specified tag
client.images.push(repository="tomerkul/myflask", tag=next_version)
print(f"Successfully pushed image: {image_name}")

# Tag the image as 'latest' and push it
latest_tag = "latest"
latest_image_name = f"tomerkul/myflask:{latest_tag}"
client.images.tag(image_name, repository="tomerkul/myflask", tag=latest_tag)
client.images.push(repository="tomerkul/myflask", tag=latest_tag)
print(f"Successfully pushed image: {latest_image_name}")

