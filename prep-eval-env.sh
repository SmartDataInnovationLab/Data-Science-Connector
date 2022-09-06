#!/bin/bash
chmod +x ./graft-over-testbed/ssh-workaround/88-enable_forwarding
git clone https://github.com/International-Data-Spaces-Association/IDS-testbed.git testbed
cd testbed
git checkout 46a2a5dd044c8372e33c9a2937dd49581714d4f9
cd ..
cp -r graft-over-testbed/. testbed

echo "ssh: 172.23.0.22:2222, jupyter: 172.23.0.88:8888 after compose up"