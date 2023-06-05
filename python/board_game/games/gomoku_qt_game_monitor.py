from . import blackwhite_qt_game_monitor
from . import gomoku_qt_game_utils
from . import qt_game_monitor

class GomokuMonitorWidget(blackwhite_qt_game_monitor.BlackWhiteGameMonitorWidget):
    def create_state(self):
        return gomoku_qt_game_utils.create_state()

    def get_unit_size(self):
        return gomoku_qt_game_utils.get_unit_size()

    def get_transcript_save_path(self):
        return gomoku_qt_game_utils.get_transcript_save_path()

qt_game_monitor.main(GomokuMonitorWidget)
