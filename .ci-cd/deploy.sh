# Пример вызова скрипта
# nohup ./ci-cd/deploy.sh dev "123456:ABCDEsaw" "-1001018" "docker.helloworld.com" &
# nohup sh .ci-cd/deploy.sh master "bot1227874132:AAHdTV7_1aKNdq0pC1jO0wXXWCEgKb-0zBk" "-1001333389227" "docker.inseo.pro"

# 1. Устанавливаем из входных параметров переменные окружения
export HW_ENV=$1              # Окружение (dev/prod)
export HW_TG_BOT_TOKEN=$2     # Токен бота Telegram (пример - bot110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw)
export HW_TG_CHAT_ID=$3       # ID чата/канала в Telegram, куда бот будет отправлять сообщения (пример -1001234567890)
export HW_DOCKER_REGISTRY=$4  # Хост репозитория Docker
HW_BRANCH=$([ "${HW_ENV?}" "==" "prod" ] && echo master || echo dev)

# 3. Деплой
sh ./.ci-cd/curl_tg.sh "#deploy_start"

/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:previous"
/usr/bin/docker tag "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:new" "${HW_DOCKER_REGISTRY}/hw_back_${HW_BRANCH}:latest"
/usr/local/bin/docker-compose -p "hw_back_${HW_ENV}" up -d  --remove-orphans

sh ./.ci-cd/curl_tg.sh "#deploy_success"

