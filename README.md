pbw-tools
=========

Download, extract, validate, and repack Pebble PBW files.

Current Status
--------------

Very, very hacky pre-alpha. Quite a bit of copy/paste since I wanted to get something up and running ASAP.

Given that the watchface SDK is now promised for mid-April 2013 I'm focusing on other projects for now.

Overview
--------

download_watchfaces.py will download all available watchfaces in to your current directory.

extract_pbw.py will extract a given PBW in to a new directory. This is called an "app directory" below.

unpack_pbpack.py will extract the current app directory's resources in to separate files. Currently only supports "png" resources.

validate_pbpack.py will do some basic sanity checking of the app resources - that is to say format of headers and CRCs of data - inside an app directory.

view_pebble_image.py will render a given image file.

invert_pebble_image.py will invert-in-place a given image file or set of files. No type checks or other safeties - be careful. Running it a second time will perfectly undo the inversion.

repack_pbpack.py will attempt to rebuild-in-place a given pbpack - as a safety measure, it reads from "app-resources.pbpack.backup" and writes to "app-resources.pbpack" - again, no other safeties. Some of the necessary magic is missing here - changing any of the component images breaks the app.

rebuild_manifest.py will update the manifest and rebuild a PBW from the current app directory. It will successfully rebuild untouched apps.

rename_app.py is still WIP.