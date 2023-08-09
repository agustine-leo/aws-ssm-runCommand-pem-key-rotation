"#!/bin/bash",
"echo \"Running command in `pwd`\"",
"echo Untar key_rotate.tar"
"tar xvf key_rotate.tar"
"echo \"Run key-rotate.py script.\"",
"python3 key-rotate.py \"{{Version}}\""
"echo \"Done\"",
