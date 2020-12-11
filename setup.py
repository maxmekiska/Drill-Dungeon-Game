from cx_Freeze import bdist_msi, Executable, setup


# https://docs.microsoft.com/en-us/windows/win32/msi/shortcut-table
shortcut_table = [
    ("DesktopShortcut",                                             # Shortcut
     "DesktopFolder",                                               # Directory_
     "DrillDungeonGame",                                            # Name
     "TARGETDIR",                                                   # Component_
     "[TARGETDIR]DrillDungeonGame.exe",                             # Target
     None,                                                          # Arguments
     None,                                                          # Description
     None,                                                          # Hotkey
     None,                                                          # Icon
     None,                                                          # IconIndex
     None,                                                          # ShowCmd
     "TARGETDIR",                                                   # WkDir
     )
]


executables = [Executable("main.py",
                          base="Win32GUI",
                          targetName="DrillDungeonGame.exe",
                          shortcutName="DrillDungeonGame",
                          shortcutDir="DesktopFolder",
                          icon="resources/images/favicon.ico",
                          )]


msi_data = {"Shortcut": shortcut_table}


bdist_msi_options = {
    "install_icon": "resources/images/favicon.ico",
    "summary_data": {"author": "Team Purple"},
    "data": msi_data,
}


build_exe_options = {
    "packages": [
        "arcade",
    ],
    "include_files": "resources",
}


setup(
    name="Drill Dungeon Game",
    version="1.0",
    description="A dungeon themed game centered around a drill!",

    options={
        "bdist_msi": bdist_msi_options,
        "build_exe": build_exe_options,
    },
    executables=executables,
)
