import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. 계산기 화면 구성 (HTML/CSS/JS)
HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Calculator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .calculator {
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
            width: 350px;
        }
        .display {
            width: 100%;
            height: 60px;
            background: #222;
            color: #fff;
            font-size: 32px;
            text-align: right;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: none;
            outline: none;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        button {
            padding: 20px;
            font-size: 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            background: #f0f0f0;
        }
        button:hover { transform: scale(1.05); background: #e0e0e0; }
        button:active { transform: scale(0.95); }
        .operator { background: #ff9500; color: #fff; }
        .operator:hover { background: #e08900; }
        .clear { background: #ff3b30; color: #fff; }
        .clear:hover { background: #d63027; }
        .equals { background: #34c759; color: #fff; grid-column: span 2; }
        .equals:hover { background: #2db149; }
    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" class="display" id="display" readonly>
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button onclick="append('/')" class="operator">÷</button>
            <button onclick="append('*')" class="operator">×</button>
            <button onclick="backspace()">⌫</button>
            <button onclick="append('7')">7</button>
            <button onclick="append('8')">8</button>
            <button onclick="append('9')">9</button>
            <button onclick="append('-')" class="operator">−</button>
            <button onclick="append('4')">4</button>
            <button onclick="append('5')">5</button>
            <button onclick="append('6')">6</button>
            <button onclick="append('+')" class="operator">+</button>
            <button onclick="append('1')">1</button>
            <button onclick="append('2')">2</button>
            <button onclick="append('3')">3</button>
            <button onclick="append('.')">.</button>
            <button onclick="append('0')">0</button>
            <button onclick="calculate()" class="equals">=</button>
        </div>
    </div>
    <script>
        const display = document.getElementById('display');
        function append(value) {
            if (display.value === 'Error') display.value = '';
            display.value += value;
        }
        function clearDisplay() { display.value = ''; }
        function backspace() { display.value = display.value.slice(0, -1); }
        function calculate() {
            try {
                let expr = display.value
                    .replace(/×/g, '*')
                    .replace(/÷/g, '/')
                    .replace(/−/g, '-');
                display.value = eval(expr);
            } catch {
                display.value = 'Error';
            }
        }
        document.addEventListener('keydown', (e) => {
            if (e.key >= '0' && e.key <= '9' || e.key === '.') append(e.key);
            else if (['+', '-', '*', '/'].includes(e.key)) append(e.key);
            else if (e.key === 'Enter') calculate();
            else if (e.key === 'Backspace') backspace();
            else if (e.key === 'Escape') clearDisplay();
        });
    </script>
</body>
</html>"""

# 2. 서버 핸들러 설정
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))

    def log_message(self, format, *args):
        # 터미널에 접속 로그가 남지 않도록 무시
        pass

# 3. 서버 실행 함수
def run():
    port = 8000
    server_address = ('localhost', port)
    
    try:
        # HTTPServer 인스턴스 생성
        httpd = HTTPServer(server_address, Handler)
        
        # [핵심] 포트 재사용 허용 (에러 방지)
        httpd.allow_reuse_address = True
        
        print(f"계산기 서버가 실행되었습니다: http://localhost:{port}")
        print("종료하려면 터미널에서 Ctrl+C를 누르세요.")
        
        # [핵심] 브라우저 자동 열기
        webbrowser.open(f'http://localhost:{port}')
        
        # 서버 무한 대기
        httpd.serve_forever()
        
    except OSError as e:
        if e.errno == 48:
            print(f"\n오류: 포트 {port}번이 이미 사용 중입니다.")
            print("기존에 실행된 프로그램을 종료하거나 잠시 후 다시 시도하세요.")
        else:
            print(f"알 수 없는 오류 발생: {e}")

if __name__ == "__main__":
    run()