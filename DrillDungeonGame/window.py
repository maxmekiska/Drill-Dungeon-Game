import time

from .drill_dungeon_game import DrillDungeonGame
from .in_game_menus import PauseMenu, GameOverMenu, ShopMenu
from .utility import MUSIC_VOLUME
from .views import MenuView, InstructionView, ObjectivesView
import arcade


class Window(arcade.Window):
    def __init__(self, width: int, height: int, title: str) -> None:
        super().__init__(width, height, title)
        self.game_view = DrillDungeonGame(self)
        self.menu_view = MenuView(self)
        self.instructions_view = InstructionView(self)
        self.objectives_view = ObjectivesView(self)

        self.pause_view = PauseMenu(self.game_view, self.game_view.view)
        self.game_over_view = GameOverMenu(self.game_view, self.game_view.view)
        self.shop_view = ShopMenu(self.game_view, self.game_view.view)

        self._music_list = (
            arcade.Sound("resources/sound/background_song.wav", streaming=True),
        )
        self.music = None
        self._song_index = 0
        self.play_music()

    def advance_song(self) -> None:
        """
        Advance our pointer to the next song. This does NOT start the song.
        """
        self._song_index = (self._song_index + 1) % len(self._music_list)

    def play_music(self) -> None:
        """
        Play the background music.
        """
        # Stop what is currently playing.
        if self.music:
            self.music.stop()

        # Play the next song
        self.music = self._music_list[self._song_index]
        self.music.play(MUSIC_VOLUME)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        # time.sleep(0.03)

    def on_update(self, delta_time: float):
        if self.music:
            position = self.music.get_stream_position()
            if position == 0.0:
                self.advance_song()
                self.play_music()
