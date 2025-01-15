#!/bin/bash

if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null
then
    echo "Docker и Docker Compose должны быть установлены."
    exit 1
fi

docker-compose up --build -d

echo "Flask-приложение запущено на http://localhost:5000"
