#!/bin/bash

# Give myself sudo access.
su
/usr/sbin/usermod -aG sudo $USER
su $USER

# Install packages.
sudo apt update

# Remove Libreoffice.
if  [ "$*" != "-l" ] ; then
    sudo apt remove libreoffice-core -y
fi

# Remove atril.
sudo apt remove atril -y

# Install packages.
sudo apt install \
 alacritty \
 aptitude \
 arandr \
 curl \
 feh \
 firefox-esr \
 linux-headers-amd64 \
 lxappearance \
 lxsession-logout \
 lightdm \
 lightdm-gtk-greeter-settings \
 mousepad \
 network-manager-gnome \
 openbox \
 obconf \
 pavucontrol \
 picom \
 policykit-1-gnome \
 pulseaudio \
 ristretto \
 scrot \
 thunar \
 thunar-archive-plugin \
 thunar-volman \
 tint2 \
 unzip \
 volumeicon-alsa \
 wget \
 xarchiver \
 xfce4-taskmanager \
 -y

# Install NVIDIA drivers.
if [ "$*" == "-n" ]; then
    sudo echo "deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware" >> /etc/apt/sources.list
    sudo apt update
    sudo apt install nvidia-driver firmware-misc-nonfree -y
fi

# Remove unused packages.
sudo apt autoremove -y

# Install Rust.
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -- -y

# Install Starship.
curl -sS https://starship.rs/install.sh | sh
echo 'eval "$(starship init bash)"' >> ~/.bashrc

# Install VSCode.
curl -O -J -L 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
CODE_DEB=$(ls | grep code)
sudo dpkg -i $CODE_DEB
rm $CODE_DEB

# Install fonts.

# Download and unpack Monaspace.
mkdir -p ~/.fonts
wget 'https://github.com/githubnext/monaspace/releases/download/v1.101/monaspace-v1.101.zip'
MONASPACE=$(ls | grep monaspace)
unzip $MONASPACE
rm $MONASPACE
MONASPACE=$(ls | grep monaspace)
mv -v "$MONASPACE/fonts/otf/*" ~/.fonts
rm -r $MONASPACE
# Download and unpack the Monaspace Nerd Font.
wget 'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Monaspace.zip'
# Unzip only these fonts.
unzip Monaspace.zip 'MonaspiceArNerdFontMono*'
unzip Monaspace.zip 'MonaspiceRnNerdFontMono*'
rm Monaspace.zip
mv -v Monaspice* ~/.fonts

# Cache the fonts.
fc-cache -v

# Install icons.

# Clone the repo.
git clone https://github.com/rtlewis88/rtl88-Themes.git
# Copy the icons
mkdir -p ~/.icons
mv rt188-Themes/Crushed-Ice-Suru ~/.icons
# Remove the repo.
rm -r rt188-Themes

# Install the theme.

# Clone the repo.
git clone https://github.com/zoddDev/PinkNord.git
# Copy the theme, but only the files we actually need.
DST=~/.themes/PinkNord
mkdir -p $DST
SRC=PinkNord/.themes/pink-nord-theme
mv $SRC/gtk-2.0 $DST
mv $SRC/gtk-3.0 $DST
mv $SRC/gtk-assets $DST
mv $SRC/gtk-icons $DST
mv $SRC/openbox-3 $DST
mv $SRC/xfwm4 $DST
# Remove the repo.
rm -r PinkNord

# Copy config files.
cd .config
cp -r alacritty ~/.config
cp -r gtk-3.0 ~/.config
cp -r openbox ~/.config
cp -r tint2 ~/.config
cp -r volumeicon ~/.config
cp -r xfce4 ~/.config
cd ..

# Copy the wallpaper.
cp wallpaper.png ~/Pictures

# Set lightdm
# Copy the wallpaper.
sudo cp wallpaper_base.jpeg /usr/share/pixmaps/pink_base.jpg

chdir lightdm

# Copy the greeter settings.
sudo cp lightdm-gtk-greeter.conf /etc/lightdm

# Decide which lightdm config file to use.
if [ "$*" == "-s" ] ; then
    cp lightdm_screen_layout.config /etc/lightdm/lightdm.conf
else
    cp lightdm.config /etc/lightdm/lightdm.conf
fi