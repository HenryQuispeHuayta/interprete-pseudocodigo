git clone https://github.com/HenryQuispeHuayta/interprete-pseudocodigo.git ~/interprete-pseudocodigo
cd ~/interprete-pseudocodigo
if [ -f ~/.bashrc ]; then
    echo "alias inFlex='python $(pwd)/inFlex.py'" >> ~/.bashrc
elif [ -f ~/.zshrc ]; then
    echo "alias inFlex='python $(pwd)/inFlex.py'" >> ~/.zshrc
else
    echo "No se pudo encontrar ni ~/.bashrc ni ~/.zshrc"
    exit 1
fi
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
else
    source ~/.zshrc
fi