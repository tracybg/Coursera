    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = []

        # rows
        lines.extend(board)

        # cols
        cols = [[board[rowidx][colidx] for rowidx in dimrng]
                for colidx in dimrng]
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in dimrng]
        diag2 = [board[idx][dim - idx -1] 
                 for idx in dimrng]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None
