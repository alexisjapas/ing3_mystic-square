import pygame


class Display:
    def __init__(self, bg_color=(255, 255, 255)):
        self.screen_size = (1400, 600)
        self.bg_color = bg_color
        pygame.display.set_caption("Mystic Square Solver")

    def init_game_display(self, solver):
        # initialize and prepare the solver
        self.solver = solver

        # compute cells and board size
        self.cell_size = (self.screen_size[0] - 200) // (solver.grid_dim * 2)
        self.board_size = solver.grid_dim * self.cell_size

        # change screen size if cells dont fill it
        mid_size = 200
        if (self.screen_size[0] - mid_size) % solver.grid_dim:
            mid_size -= (self.screen_size[0] - 200) % solver.grid_dim
            print(mid_size)

        # set screen size
        self.offset_col = self.board_size + mid_size
        self.screen = pygame.display.set_mode(
            (2 * self.board_size + mid_size, self.board_size)
        )

        # init boards
        self.board_agents = self.init_board()
        self.board_target = self.init_board(self.offset_col)

    def init_board(self, offset_col=0):
        # Draw the game board on the screen
        return [
            [
                pygame.Rect(
                    offset_col + col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for row in range(self.solver.grid_dim)
            ]
            for col in range(self.solver.grid_dim)
        ]

    def draw_board(self, board):
        for col in range(self.solver.grid_dim):
            for row in range(self.solver.grid_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), board[col][row], 1)

    def draw_agents(self, mode="current"):
        assert mode == "current" or mode == "target"
        board = self.board_agents if mode == "current" else self.board_target
        for agent in self.solver.agents:
            pos = agent.current_pos if mode == "current" else agent.target_pos
            pygame.draw.rect(self.screen, agent.color, board[pos[0]][pos[1]], 0)

    def draw_distances(self):
        board = self.board_target  # TODO create distance board
        for agent in self.solver.agents:
            pos = agent.current_pos
            print(agent.distance)
            pygame.draw.rect(
                self.screen,
                (
                    255 - agent.distance * 10,
                    255 - agent.distance * 10,
                    255 - agent.distance * 10,
                ),
                board[pos[0]][pos[1]],
                0,
            )

    def draw_text(self, font, text, center_col, center_row, color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (center_col, center_row)
        self.screen.blit(text_surface, text_rect)

    def draw_simulation_info(self, offset_col=700):
        font = pygame.font.Font(None, 24)

        # grid size
        self.draw_text(font, "GRID SIZE", offset_col, 10)
        self.draw_text(
            font, f"{self.solver.grid_dim} x {self.solver.grid_dim}", offset_col, 30
        )

        # number of agents
        self.draw_text(font, "NUMBER OF AGENTS", offset_col, 70)
        self.draw_text(font, f"{int(self.solver.nb_agents)}", offset_col, 90)

        # number of moves
        self.draw_text(font, "MOVES COUNT", offset_col, 130)
        self.draw_text(font, f"{self.solver.stats['moves_count']}", offset_col, 150)

    def update(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_agents("current")
        self.draw_distances()
        self.draw_board(self.board_agents)
        self.draw_board(self.board_target)
        self.draw_simulation_info()
        pygame.display.flip()
