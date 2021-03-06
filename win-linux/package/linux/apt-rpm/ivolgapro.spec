Summary: Desktop editors for text, spreadsheet and presentation files
Name: {{PACKAGE_NAME}}
Version: {{PRODUCT_VERSION}}
Release: {{BUILD_NUMBER}}
License: Commercial
Group: Applications/Office
URL: http://ivolgapro.com/
Vendor: Novie kommunikacionnie tehnologii, CJSC
Packager: Novie kommunikacionnie tehnologii, CJSC <support@ivolgapro.ru>
Requires: libX11, libXScrnSaver, libcurl, libgtkglext, libcairo, fonts-ttf-dejavu
#Suggests: fonts-ttf-liberation, fonts-ttf-ms, fonts-ttf-crosextra-carlito
BuildArch: x86_64
AutoReq: no
AutoProv: no

%description
IvolgaPro installation package
 IvolgaPro is an application for editing office documents (text documents, spreadsheets and presentations) from ivolgapro cloud portal on local computer without browser using.

%prep
rm -rf "$RPM_BUILD_ROOT"

%build

%install

#install desktopeditor files
mkdir -p "$RPM_BUILD_ROOT"
cp -r ../../../common/ivolgapro/* "$RPM_BUILD_ROOT/"

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%attr(777, root, root) /opt/ivolgapro/desktopeditors/*
%attr(777, root, root) /usr/bin/ivolgapro
%attr(-, root, root) /usr/share/applications/*.desktop
%attr(-, root, root) /usr/share/fonts/truetype/ivolgapro/*
%attr(-, root, root) /var/lib/ivolgapro/desktopeditors/*

%pre

%post

set -e 		# fail on any error
set -u 		# treat unset variable as errors

# Add icons to the system icons
XDG_ICON_RESOURCE="`which xdg-icon-resource 2> /dev/null || true`"
if [ ! -x "$XDG_ICON_RESOURCE" ]; then
  echo "Error: Could not find xdg-icon-resource" >&2
  exit 1
fi
for icon in "/opt/ivolgapro/desktopeditors/asc-de-"*.png; do
  size="${icon##*/asc-de-}"
  "$XDG_ICON_RESOURCE" install --size "${size%.png}" "$icon" "asc-de"
done

UPDATE_MENUS="`which update-menus 2> /dev/null || true`"
if [ -x "$UPDATE_MENUS" ]; then
  update-menus
fi

# Update cache of .desktop file MIME types. Non-fatal since it's just a cache.
#update-desktop-database > /dev/null 2>&1 || true

mkdir -p /var/lib/ivolgapro
chmod -R 777 /var/lib/ivolgapro

ln -sf /usr/lib64/libcurl.so.4 /usr/lib64/libcurl-gnutls.so.4

%preun

set -e

action="$1"
if [ "$2" = "in-favour" ]; then
  # Treat conflict remove as an upgrade.
  action="upgrade"
fi
# Don't clean-up just for an upgrade.`
if [ "$action" = "upgrade" ] ; then
  exit 0
fi

# Remove icons from the system icons
XDG_ICON_RESOURCE="`which xdg-icon-resource 2> /dev/null || true`"
if [ ! -x "$XDG_ICON_RESOURCE" ]; then
  echo "Error: Could not find xdg-icon-resource" >&2
  exit 1
fi
for icon in "/opt/ivolgapro/desktopeditors/asc-de-"*.png; do
  size="${icon##*/asc-de-}"
  "$XDG_ICON_RESOURCE" uninstall --size "${size%.png}" "asc-de"
done

UPDATE_MENUS="`which update-menus 2> /dev/null || true`"
if [ -x "$UPDATE_MENUS" ]; then
  update-menus
fi

# Update cache of .desktop file MIME types. Non-fatal since it's just a cache.
#update-desktop-database > /dev/null 2>&1 || true

%postun

set -e 		# fail on any error

rm -rf /var/lib/ivolgapro/desktopeditors
