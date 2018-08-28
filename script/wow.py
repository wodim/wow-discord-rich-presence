import rpc
import time

from PIL import Image, ImageGrab
import win32api
import win32con
import win32gui


DEBUG = 0

MY_WIDTH = 11.61

if not DEBUG:
    client_id = '483214843734654987'
    rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
    print('RPC connection successful.')

decoded = ''
found = False


def callback(hwnd, extra):
    global found

    rect = win32gui.GetWindowRect(hwnd)
    height = (win32api.GetSystemMetrics(win32con.SM_CYCAPTION) +
              win32api.GetSystemMetrics(win32con.SM_CYBORDER) * 4 +
              win32api.GetSystemMetrics(win32con.SM_CYEDGE) * 2)

    if (win32gui.GetWindowText(hwnd) == 'World of Warcraft' and
            win32gui.GetClassName(hwnd) == 'GxWindowClassD3d9Ex'):
        found = True

        if not DEBUG and win32gui.GetForegroundWindow() != hwnd:
            return

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
        except:
            print('Error decoding the pixels.')
            if not DEBUG:
                return

        parts = decoded.split('|')
        print('Read: %s' % decoded)

        if DEBUG:
            im.show()
            return

        # sanity check
        if (len(parts) != 4 or
                not decoded.endswith('|') or
                not decoded.startswith('|')):
            print('Wrong data read.')
            return

        _, zone_name, type_, _ = parts

        activity = {
            'state': type_,
            'details': zone_name,
            'assets': {
                'large_image': 'wow-icon'
            }
        }
        print('Setting: %s' % activity)
        rpc_obj.set_activity(activity)


if DEBUG:
    win32gui.EnumWindows(callback, None)
else:
    while True:
        found = False
        win32gui.EnumWindows(callback, None)
        if not found:
            rpc_obj.set_activity({})
        time.sleep(5)
