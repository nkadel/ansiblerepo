#! /bin/bash -ex

# You can set the version as an argument to the script,
# default is taken from the specfile
if [ "$1" = "" ]; then
    VERSION=$(
        rpm -q --qf "%{VERSION}\n" --specfile python-pygments.spec | head -n1
    )
else
    VERSION=$1
fi

SRCURL=https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-$VERSION.tar.gz
BADFILE=Pygments-$VERSION/tests/examplefiles/Intro.java
OUT=Pygments-$VERSION-clean.tar.xz

curl -L $SRCURL |
    gunzip |
    tar --delete $BADFILE --delete $BADFILE.output |
    xz > $OUT

if tar tJf $OUT | grep 'Intro.java'; then
    >&2 echo "Intro.java left in!"
    mv $OUT $OUT.bad
    exit 1
fi
