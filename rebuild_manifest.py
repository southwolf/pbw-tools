from libpebble.stm32_crc import crc32
import json, os, os.path
from zipfile import ZipFile

if __name__ == "__main__":
    manifest = json.load(open("manifest.json"))
    
    manifest["resources"]["crc"] = crc32(open("app_resources.pbpack", 'rb').read())
    s = os.stat("app_resources.pbpack")
    manifest["resources"]["size"] = s.st_size
    manifest["resources"]["timestamp"] = int(s.st_ctime)
    
    manifest["application"]["crc"] = crc32(open("pebble-app.bin", 'rb').read())
    s = os.stat("pebble-app.bin")
    manifest["application"]["size"] = s.st_size
    manifest["application"]["timestamp"] = int(s.st_ctime)
    
    with open("manifest.json", "wb") as f:
        json.dump(manifest, f)
    
    with ZipFile("%s.pbw" % os.path.basename(os.getcwd()), 'w') as app:
        app.write("manifest.json")
        app.write("app_resources.pbpack")
        app.write("pebble-app.bin")