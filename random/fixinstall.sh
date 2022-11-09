#!/bin/sh
# installation doesn't work out of the box for several reasons
# therefore we need to change some stuff to the install-scripts
# as the dvd is read-only, the first step is to copy content of the whole CD to a folder on disk
# afterwards, run this script or the particular commands in the copied folder


# install-scripts are executed with "sh", but actually need to be executed with bash (contain bashism)
# when "sh" points to a POSIX-compliant shell (e.g. "dash" on ubuntu), installation throws an error regarding "function"-keyword
# therefore, we need to replace "sh" with "bash"
sed -i "s/bin\/sh/bin\/bash/g" install
for file in setup/printarch setup/unpack_data setup/printlibc setup/unpack_videos setup/checkarch; do sed -i "s/sh/bash/g" $file; done

# now the install failes with thinking that "fgrep is obsolencet; using grep -F" is an error
sed -i "s/fgrep/grep -F/g" setup/printlibc

# next the installation can't detect 64-bit-systems, therefore we need to use the i386-entry for x64 as well
sed -i "s/i?86/*86*/g" setup/printarch

# after that, we can execute the install-script
echo "fix done, running installer..."
echo "recomended: "
echo "- install videos (checkbox \"Videos installieren\")"
echo "- install in home-dir (/home/$USER/<location to install>)"
sleep 1
sh install
