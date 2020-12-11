import cx_Freeze


executables = [cx_Freeze.Executable("main.py",
                                    base="Win32GUI",
                                    targetName="DrillDungeonGame.exe",
                                    shortcutName="Drill Dungeon Game",
                                    shortcutDir="DesktopFolder",
                                    icon="resources/images/favicon.ico",
                                    )]


bdist_msi_options = {
    "install_icon": "resources/images/favicon.ico",
    "summary_data": {"author": "Team Purple"},
}


build_exe_options = {
    "packages": [
        "arcade",
    ],
    "include_files": "resources",
}


cx_Freeze.setup(
    name="Drill Dungeon Game",
    version="1.0",
    description="A dungeon themed game centered around a drill!",

    options={
        "bdist_msi": bdist_msi_options,
        "build_exe": build_exe_options,
    },
    executables=executables,
)
