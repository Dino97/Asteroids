from multiprocessing import Process, Pipe


def _main(connection):
    scores = {}

    should_run = True

    while should_run:
        message = connection.recv()

        if message[0] == "add":
            player_id = message[1]
            score = message[2]

            if player_id not in scores:
                scores[player_id] = 0

            scores[player_id] += score
        elif message[0] == "get":
            player_id = message[1]

            if player_id in scores:
                connection.send(scores[player_id])
            else:
                connection.send(0)
        elif message[0] == "close":
            should_run = False
            print("Closing score manager process...")
        else:
            print("[ScoreManagerProcess]: Unknown command.")


class ScoreManager:
    def __init__(self):
        self._process_handle = None
        self._master_pipe = None

    def start(self):
        self._master_pipe, slave_pipe = Pipe()

        self._process_handle = Process(target=_main, args=(slave_pipe,), daemon=True)
        self._process_handle.start()

    def add_score(self, player_id, score):
        self._master_pipe.send(["add", player_id, score])

    def get_score(self, player_id):
        self._master_pipe.send(["get", player_id])
        return self._master_pipe.recv()

    def close(self):
        self._master_pipe.send(["close"])
