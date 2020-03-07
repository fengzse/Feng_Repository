class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_setting):
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        self.filename = 'High_score.txt'
        with open(self.filename, 'w') as self.file_object:
            self.file_object.write('self.high_score')

    def reset_stats(self):  # 初始化在游戏运行期间可能变化的统计信息
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
