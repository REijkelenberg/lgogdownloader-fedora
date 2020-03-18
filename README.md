# LGOGDownloader-Fedora

This repository contains the files required for building an RPM package of [LGOGDownloader](https://github.com/Sude-/lgogdownloader). Pretty much everything in this repo has been forked from [scx's COPR repo](https://copr.fedorainfracloud.org/coprs/scx/lgogdownloader/). However, whereas scx's COPR repo only provides v3.4 of lgogdownloader, this repository enables you to build v3.6 as well.

To directly install LGOGDownloader (as opposed to compiling it yourself), you can use [my COPR repository](https://copr.fedorainfracloud.org/coprs/ruub/lgogdownloader/) instead.

_Note: Currently only Fedora 30 and 31 are supported._

## Branches:

| Branch               | Description   |
| :------------------- |:--------------| 
| master               | Always contains the latest version (currently v3.6, only supports Fedora 30 and 31, possibly supports Fedora 29 and older) |
| v3.4-fedora30-31     | LGOGDownloader v3.4, only supports Fedora 30 and 31 (possibly Fedora 29 and older)      |
| v3.6-fedora30-31     | LGOGDownloader v3.6, only supports Fedora 30 and 31 (possibly Fedora 29 and older)      |
