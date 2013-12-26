AlphaBeta(Depth, State, Action, Agent, Color, Alpha, Beta, Round):
    if Goal(State) or Depth == 0:
        return Heuristic(State, Agent), Action

    TurnAgent, TurnColor = Turn(State)
    Children = Successors(State)

    if TurnColor == Color:
        CurrentMax = -Infinity
        CurrentAction = None

        for child, action in Children:
            value, action = AlphaBeta(Depth - 1, child, action, Agent, Color, \
                    Alpha, Beta, Round + 1 % 4)
            if value > CurrentMax:
                CurrentMax = value
                CurrentAction = action

            Alpha = Max(CurrentMax, Alpha)
            if CurrentMax >= Beta:
                return Infinity, None

        return CurrentMax, CurrentAction
    else:
        CurrentMin = Infinity
        CurrentAction = None

        for child, action in Children:
            value, action = AlphaBeta(Depth - 1, child, action, Agent, Color, \
                    Alpha, Beta, Round + 1 % 4)
            if value < CurrentMin:
                CurrentMin = value
                CurrentAction = action

            Beta = Min(CurrentMin, Beta)
            if Round == 3 and CurrentMin <= Alpha:
                return -Infinity, None

        return CurrentMin, CurrentAction

# Initial call is AlphaBeta(Depth, State, Agent, Color, -Infinity, Infinity, 0)
