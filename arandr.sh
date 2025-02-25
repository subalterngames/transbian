#!/bin/bash

# Run this script after running arandr and saving a screen layout to: 
# ~/.screenlayout/screen_layout.sh

SRC=~/.screenlayout/screen_layout.sh
chmod +x $SRC
# Copy so that lightdm can find it.
sudo cp $SRC /usr/local/bin