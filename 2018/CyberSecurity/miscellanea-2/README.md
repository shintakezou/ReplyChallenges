# Matrioska

The given file is an archive which contains an archive/compressed file
which contains/is another archive/compressed file, and so on.

So the first thing was to write a script to extract/uncompress all
these nested archives/compressed files.

- [unmatrioska.sh](unmatrioska.sh)

It uses 7z, among other tools, because 7z can extract *several kind of
archive*. When it finishes, you have the last matrioska in the folder
results. This file is a

> DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat",
> sectors/cluster 4, root entries 512, sectors 400 (volumes <=32 MB) ,
> Media descriptor 0xf8, sectors/FAT 1, sectors/track 32, heads 64,
> serial number 0xb4c0042a, unlabeled, FAT (12 bit)

If you mount it, you find a text file which mocks you saying you are
late, in fact he has already deleted the file you are looking for.

Has he shredded it properly?

Surely not, otherwise we wouldn't be here.

I've used [testdisk](https://www.cgsecurity.org/wiki/TestDisk) to
recover the “deleted” file, which contains the string

    e0ZMRzpEM2NyeXB0MW5nQzBkZX0K

I though this was the flag and wrote
`{FLG:e0ZMRzpEM2NyeXB0MW5nQzBkZX0K}`. But this is wrong. This made
me think it was all a deception: the name of the archives are of
this kind:

    matrioska.tmp.9nlPTQ

Not all, indeed (bzip2 doesn't store the original file name), but
many, many of them. So, maybe, altogether form an encoded string… I've
lost few attempts to follow this lead.

At last, I've tried to base64 decode the `e0ZM`… string, and that was
it.

