#!/bin/bash

# Clonar el repositorio
git clone https://github.com/HenryQuispeHuayta/interprete-pseudocodigo.git ~/interprete-pseudocodigo

# Verificar si se clonó correctamente
if [ $? -ne 0 ]; then
    echo "Error: No se pudo clonar el repositorio."
    exit 1
fi

# Definir el comando a utilizar
command="python ~/interprete-pseudocodigo/inFlex.py"

# Agregar alias a ~/.zshrc si se está utilizando Zsh
if [ -f ~/.zshrc ]; then
    if ! grep -q "alias inFlex='$command'" ~/.zshrc; then
        echo "alias inFlex='$command'" >> ~/.zshrc
        echo "Alias agregado a ~/.zshrc"
    else
        echo "El alias 'inFlex' ya está definido en ~/.zshrc."
    fi
# Agregar alias a ~/.bashrc si no se está utilizando Zsh
elif [ -f ~/.bashrc ]; then
    if ! grep -q "alias inFlex='$command'" ~/.bashrc; then
        echo "alias inFlex='$command'" >> ~/.bashrc
        echo "Alias agregado a ~/.bashrc"
    else
        echo "El alias 'inFlex' ya está definido en ~/.bashrc."
    fi
else
    echo "No se pudo encontrar ni ~/.zshrc ni ~/.bashrc"
    exit 1
fi

# Recargar el archivo de configuración actual
source ~/.zshrc || source ~/.bashrc
