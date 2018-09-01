import rpc
import time

from PIL import Image, ImageGrab
import win32api
import win32con
import win32gui


DEBUG = 0

MY_WIDTH = 11.61

DISCORD_CLIENT_ID = '483214843734654987'

decoded = ''
wow_hwnd = None
rpc_obj = None


def callback(hwnd, extra):
    global wow_hwnd

    if (win32gui.GetWindowText(hwnd) == 'World of Warcraft' and
            win32gui.GetClassName(hwnd).startswith('GxWindowClass')):
        wow_hwnd = hwnd


def read_squares(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    height = (win32api.GetSystemMetrics(win32con.SM_CYCAPTION) +
              win32api.GetSystemMetrics(win32con.SM_CYBORDER) * 4 +
              win32api.GetSystemMetrics(win32con.SM_CYEDGE) * 2)

    new_rect = (rect[0] + 8, rect[1] + height,
                rect[2] - 8, rect[1] + height + MY_WIDTH)
    try:
        im = ImageGrab.grab(new_rect)
    except Image.DecompressionBombError:
        print('DecompressionBombError')
        return

    read = []
    for square_idx in range(int(im.width / MY_WIDTH)):
        x = int(square_idx * MY_WIDTH + MY_WIDTH / 2)
        y = int(MY_WIDTH / 2)
        r, g, b = im.getpixel((x, y))

        if DEBUG:
            im.putpixel((x, y), (255, 255, 255))

        if r == g == b == 0:
            break

        read.append(r)
        read.append(g)
        read.append(b)

    try:
        decoded = bytes(read).decode('utf-8').rstrip('\0')
    except Exception as exc:
        print('Error decoding the pixels: %s.' % exc)
        if not DEBUG:
            return

    parts = decoded.replace('$WorldOfWarcraftIPC$', '').split('|')
    print('Read: %s' % decoded)

    if DEBUG:
        im.show()
        return

    # sanity check
    if (len(parts) != 2 or
            not decoded.endswith('$WorldOfWarcraftIPC$') or
            not decoded.startswith('$WorldOfWarcraftIPC$')):
        print('Wrong data read.')
        return

    zone_name, type_ = parts

    activity = {
        'state': type_,
        'details': zone_name,
        'assets': {
            'large_image': 'wow-icon'
        }
    }

    print('Setting: %s' % activity)
    rpc_obj.set_activity(activity)


while True:
    wow_hwnd = None
    win32gui.EnumWindows(callback, None)

    if DEBUG:
        if wow_hwnd:
            print('Debug: reading squares. Is everything alright?')
            read_squares(wow_hwnd)
        else:
            print("Launching in debug mode but I couldn't find WoW.")
        break
    elif win32gui.GetForegroundWindow() == wow_hwnd:
        if not rpc_obj:
            print('Not connected, connecting')
            rpc_obj = rpc.DiscordIpcClient.for_platform(DISCORD_CLIENT_ID)
            print('Connected to RPC.')
        read_squares(wow_hwnd)
    elif not wow_hwnd and rpc_obj:
        print('WoW no longer exists, disconnecting')
        rpc_obj.close()
        rpc_obj = None
    time.sleep(5)
