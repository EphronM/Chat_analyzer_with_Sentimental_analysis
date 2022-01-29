mkdir -p ~/.streamlit/

echo "
[server]
headless = true
port = $PORT
enableCORS = false
[theme]
primaryColor = ‘#84a3a7’
backgroundColor = ‘#EFEDE8’
secondaryBackgroundColor = ‘#fafafa’
textColor= ‘#424242’
font = ‘sans serif’
" > ~/.streamlit/config.toml

