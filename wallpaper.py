from subprocess import run
from typing import List, Tuple
from pathlib import Path
from xml.etree import ElementTree as Et
from PIL import Image, ImageDraw, ImageFont, ImageColor


class Label:
    def __init__(self, k: str, v: str):
        self.key: str = k
        self.value: str = v
        self.key_position: Tuple[int, int] = (0, 0)
        self.value_position: Tuple[int, int] = (0, 0)
        self.width: int = 0

    def set_position(self, x: int, y: int) -> int:
        self.key_position = (x, y)
        key_bbox = font_radon.getbbox(f'{self.key} ')
        self.value_position = (x + key_bbox[2], y)
        value_bbox = font_krypton.getbbox(self.value)
        self.width = x + key_bbox[2] + value_bbox[2]
        y += font_size
        return y


tiling = {'W-c': 'Maximize',
          'C-W-c': 'Unmaximize',
          'W-Left': 'Left half',
          'W-Right': 'Right half',
          'W-Up': 'Top-left',
          'W-Down': 'Bottom-left',
          'W-Prior': 'Top-right',
          'W-Next': 'Bottom-right'}
empty_line_at = ['Maximize', 'GoToDesktop', 'Execute', 'DirectionalCycleWindows', 'ShowMenu', 'ToggleShowDektop',
                 'NextWindow']
font_size = int(36)
fonts_directory = Path.home().joinpath('.fonts').resolve()
font_radon = ImageFont.truetype(fonts_directory.joinpath('MonaspaceRadon-Regular.otf').as_posix(), font_size)
font_krypton = ImageFont.truetype(fonts_directory.joinpath('MonaspaceKrypton-Regular.otf').as_posix(), font_size)
labels: List[Label] = list()
# The prefix of every child element. No idea why...
xml_prefix = '{http://openbox.org/3.4/rc}'
y = 0
# Get each key binding.
rc = Path.home().joinpath('.config/openbox/rc.xml').resolve().as_posix()
for keybind in Et.parse(rc).getroot().find(f'{xml_prefix}keyboard').findall(f'{xml_prefix}keybind'):
    keys = keybind.attrib['key']
    if keys in tiling:
        if tiling[keys] in empty_line_at:
            y += font_size
        action = tiling[keys]
    else:
        action_element = keybind.find(f'{xml_prefix}action')
        action_name = action_element.attrib['name']
        if action_name in empty_line_at:
            empty_line_at.remove(action_name)
            y += font_size
        if action_name == 'GoToDesktop':
            to_element = action_element.find(f'{xml_prefix}to')
            action = f'Go to {to_element.text} desktop'
        elif action_name == 'SendToDesktop':
            to_element = action_element.find(f'{xml_prefix}to')
            action = f'Send to {to_element.text} desktop'
        elif action_name == 'Execute':
            action = action_element.find(f'{xml_prefix}command').text
            if action == 'mousepad':
                y += font_size
            if 'scrot' in action:
                action = action.split('~')[0].strip()
            elif 'pactl' in action:
                if '+' in action:
                    action = 'Volume up'
                    y += font_size
                elif '-' in action:
                    action = 'Volume down'
                else:
                    action = 'Toggle mute'
            elif 'brightnessctl' in action:
                if '+' in action:
                    action = 'Lower brightness'
                else:
                    action = 'Increase brightness'
        elif action_name == 'DirectionalCycleWindows':
            action = f'Cycle window {keys.split("-")[-1].lower()}'
        elif 'Window' in action_name:
            action = action_name.split('Window')[0] + ' Window'
        elif action_name == 'ShowMenu':
            action = 'Openbox Menu'
        elif action_name == 'ToggleShowDesktop':
            action = 'Toggle show desktop'
        elif action_name == 'Close':
            action = 'Close'
        elif action_name == 'Lower':
            action = 'Lower'
        else:
            raise Exception(action_name)
            # Replace Openbox characters with better characters.
    keys = keys.replace('C-', 'Ctrl-').replace('A-', 'Alt-').replace('W-', 'Super-').replace('S-',
                                                                                             'Shift-').replace(
        '-Next', '-PgDn').replace('-Prior', '-PgUp')
    # Parse shell script paths.
    if '.sh' in action:
        action = action.split('/')[-1].split('.sh')[0]
    keys = keys.replace('XF86Audio', '').replace('XF86Mon', '')
    # Get the label.
    label = Label(keys, action)
    # Set the label's position.
    y = label.set_position(x=font_size, y=y)
    labels.append(label)
# Get the label positions.
max_width = max([label.width for label in labels]) + font_size
max_key_width = max([label.value_position[0] - label.key_position[0] for label in labels])
panel_width = max_width + font_size
panel_height = y + font_size
y = font_size
# Create a new image.
image = Image.open(Path.home().joinpath('Pictures/wallpaper_base.jpeg'))
x = image.size[0] - panel_width - font_size
draw = ImageDraw.Draw(image)
color = ImageColor.getcolor("#82b8c7", mode="RGB")
# Draw the border.
draw.rectangle(((x, y), (x + panel_width, y + panel_height)), fill=None, outline=color, width=4)
# Draw the labels.
for label in labels:
    draw.text((label.key_position[0] + x, label.key_position[1] + y), label.key, font=font_radon, fill=color)
    draw.text((x + panel_width - max_key_width - font_size * 3, label.value_position[1] + y), label.value,
              font=font_krypton, fill=color)
wallpaper_path = Path.home().joinpath('Pictures/wallpaper.png').resolve().as_posix()
image.save(wallpaper_path, format='png')
run(['feh', '--bg-scale', wallpaper_path])
