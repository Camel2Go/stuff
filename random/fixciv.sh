#!/bin/sh
# the game needs several dynamic-loaded-librarys located in dll to run successfully
# as these are 32-bit, we need lib32-glibc to run them
# at the time of writing, the current glibc-version is 2.36
# however, the game and libs are compiled with glibc-2.0/2.1 from 1997 (https://en.wikipedia.org/wiki/Glibc#Version_history)

# when we run the game, it tries to load /lib/libc.so.6, which surprisingly is 64-bit on every system nowadays,
# producing "ELF file class not 32bit"

# we can change the hardcoded libc-path with "patchelf --replace-needed libc.so.6 /usr/lib32/libc.so.6 dll/map/geometric.so"
# that all leads us to "undefined symbol: memcpy" with glibc-2.0 and "ELF file OS ABI not 0" with glibc-2.1

# therefore it seems we actually need to provide an glibc-2.0 from 1997, so lets get one!
# https://snapshot.debian.org/package/glibc/

wget https://snapshot.debian.org/archive/debian-archive/20090802T004153Z/debian/pool/main/g/glibc/libc6_2.1.3-25_i386.deb
ar x libc6_2.1.3-25_i386.deb
tar xf data.tar.gz
rm -r debian-binary control.tar.gz data.tar.gz libc6_2.1.3-25_i386.deb usr/ etc/ var/


# now the last thing is to convince the game to use that

# when trying to patch the runpath with "patchelf --set-rpath $(pwd)/lib dll/map/geometric.so", 
# we get a nice crash with "dynamic-link.h:57: elf_get_dynamic_info: Assertion `! "bad dynamic tag"' failed."

# so the ugly solution is to override the ld-library-path when starting the game
mv civctp civctp-bin
echo "#!/bin/sh" > civctp
echo "LD_LIBRARY_PATH=$(pwd)/lib ./civctp-bin" >> civctp
chmod +x civctp

# now, everything should be working quite nicely :)
echo "done, please try to run the game with ./civctp :)"