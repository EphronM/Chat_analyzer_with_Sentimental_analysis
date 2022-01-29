mkdir -p ~/.streamlit/

echo "[theme]
primaryColor = ‘#ECE5DD’
backgroundColor = ‘#FFFFFF’
secondaryBackgroundColor = ‘#128C7E’
textColor= ‘#262730’
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
