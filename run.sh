
URL="http://localhost:8000"

OS=$(uname)
if [[ "$OS" != "Linux" && "$OS" == "Darwin" ]]; then
	echo "Sistema operativo no soportado: $OS"
	exit 1
fi

if [[ "$OS" == "Linux" ]]; then
	bash xdg-open $URL > /dev/null 2>&1 
elif [[ "$OS" == "Darwin" ]]; then
	open "$URL" $to_trash
fi

cd environment/frontend_server
python3 manage.py runserver
