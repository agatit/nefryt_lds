import shutil, os, sys
import win32serviceutil
import site
import glob


uv_python = os.path.expandvars(r'%APPDATA%\uv\python')
dlls = glob.glob(os.path.join(uv_python, 'cpython-3.10*', 'python310.dll'))
if dlls:
    dll_src = dlls[0]
    dll_dst = os.path.join(os.path.dirname(sys.executable), 'python310.dll')
    shutil.copy2(dll_src, dll_dst)
    print(f'python310.dll copied ({dll_src} -> {dll_dst})')
else:
    print('WARNING: python310.dll not found in uv python directory')


venv_root = os.path.normpath(os.path.join(os.path.dirname(sys.executable), '..'))
search_roots = [
    venv_root,
    os.path.dirname(sys.executable),
] + site.getsitepackages()

print("Searching for pythonservice.exe...")
src = None
for search_root in search_roots:
    for root, dirs, files in os.walk(search_root):
        for f in files:
            if f == 'pythonservice.exe':
                src = os.path.join(root, f)
                print(f'Found: {src}')
                break
        if src:
            break
    if src:
        break

if not src:
    print("ERROR: pythonservice.exe not found")
    sys.exit(1)

dst = os.path.join(os.path.dirname(sys.executable), 'pythonservice.exe')
if os.path.abspath(src) != os.path.abspath(dst):
    shutil.copy2(src, dst)
    print(f'pythonservice.exe copied ({src} -> {dst})')
else:
    print('pythonservice.exe already in correct location')
