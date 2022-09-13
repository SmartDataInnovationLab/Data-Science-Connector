#!/bin/bash
chmod +x ./graft-over-testbed/ssh-workaround/88-enable_forwarding
git clone https://github.com/International-Data-Spaces-Association/IDS-testbed.git testbed
cd testbed
git checkout 46a2a5dd044c8372e33c9a2937dd49581714d4f9
cd ..
cp -r graft-over-testbed/. testbed