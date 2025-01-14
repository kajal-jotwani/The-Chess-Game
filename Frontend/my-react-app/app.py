from bottle import run, app, request, response, route
import chess
import chess.engine
from bottle_cors_plugin import cors_plugin
import os

app = app()
app.install(cors_plugin('*'))

STOCKFISH_PATH = os.path.join(os.getcwd(), "stockfish", "16_x64_binary")

@route('/')
def hello():
    return {"message": "Hi"}

@route('/gen_move', method='POST')
def gen_move():
    data = request.json
    
    if data:
        fen = data.get('fen')
        board = chess.Board(fen)
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

        result = engine.play(board, chess.engine.Limit(time=1.0))
        board.push(result.move)

        engine.quit()

        return { 'fen': board.fen() }

    else:
        response.status = 400
        return {'status': 'error', 'message': 'Invalid data'}

if __name__ == '__main__':
    print('Hi')
    run(host='0.0.0.0', port=8000)
