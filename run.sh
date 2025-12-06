set -e

PYTHON=python
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=py
fi

if [ ! -d ".venv" ]; then
  "$PYTHON" -m venv .venv
fi

source .venv/Scripts/activate


"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install -r requirements.txt

"$PYTHON" -m playwright install

cd frontend
npm install
npm run build
cd ..

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000