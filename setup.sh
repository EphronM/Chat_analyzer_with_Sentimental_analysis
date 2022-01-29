mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
[theme]\n\
primaryColor="#ECE5DD"\n\
backgroundColor="#FFFFFF"\n\
secondaryBackgroundColor="#128C7E"\n\
textColor="#262730"\n\
font = "sans serif"\n\

" > ~/.streamlit/config.toml
