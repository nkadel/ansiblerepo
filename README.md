docker-ce-repo
==============

Wrapper for SRPM building tools for docker-ce.

These RPM builds are not safe
-----------------------------

The .spec files and build processes from the published SRPM's rely,
extensively, on unlabeled tarballs of unspecified provenance, with
names like "engine.tgz" and no note of how the tarball was generated.

*THIS IS NOT SAFE *

They also include build procedures that write to directly a new location not in
the Linux File System Hierarchy and outside the working build directory, namely "/go".

* THIS IS NOT SAFE *

They also run "git clone" to untagged "master" versions of git repos hosted outside the SRPM, violating the rules that SRPMs should contain all the source code.

* THIS IS NOT SAFE *

To build
--------

My tools normally use "mock" to build software safely in local
pods. These .spec files make that impossible. Only "make build" works, and the dependencies have to be installed individually and locally on the build host.
