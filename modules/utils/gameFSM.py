class GameState(object):
    def __init__(self, state='title'):
        self._state = state

    def manageState(self, action):
        if action == 'start' and self._state == 'title':
            self._state = 'begin'
        elif action == 'start' and self._state == 'begin':
            self._state = 'running'
        elif action == 'pause' and self._state != 'paused':
            self._state = 'paused'
        elif action == 'unpause' and self._state == 'paused':
            self._state = 'running'
        elif action == 'nextLevel' and self._state == 'running':
            self._state = 'startLoading'
        elif action == 'doneLoading' and self._state == 'startLoading':
            self._state = 'running'
        elif action == 'win' and self._state == 'running':
            self._state = 'end'

    def __eq__(self, other):
        return self._state == other
