def log(tag="", message=""):
    with open("log.txt", "w+b") as log:
        log.write(f"{tag}: {message}\n".encode("utf-8"))
